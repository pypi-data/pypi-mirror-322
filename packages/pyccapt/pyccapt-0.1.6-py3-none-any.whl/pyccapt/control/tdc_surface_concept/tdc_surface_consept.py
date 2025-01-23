import asyncio
import concurrent.futures
import multiprocessing as mp
import os
import time
import atexit
from queue import Queue

import numpy as np

# local imports
from pyccapt.control.devices import initialize_devices
from pyccapt.control.tdc_surface_concept import scTDC

QUEUE_DATA = 0
QUEUE_ENDOFMEAS = 1
CHUNK_SIZE = 200_000  # Adjust the chunk size as needed

class BufDataCB4(scTDC.buffered_data_callbacks_pipe):
    """
    The class inherits from python wrapper module scTDC and class: buffered_data_callbacks_pipe
    """

    def __init__(self, lib, dev_desc, data_field_selection, dld_events,
                 max_buffered_data_len=500_000):
        """
		Initialize the base class: scTDC.buffered_data_callbacks_pipe

		Args:
			lib (scTDClib): A scTDClib object.
			dev_desc (int): Device descriptor as returned by sc_tdc_init_inifile(...).
			data_field_selection (int): A 'bitwise or' combination of SC_DATA_FIELD_xyz constants.
			dld_events (bool): True to receive DLD events, False to receive TDC events.
			max_buffered_data_len (int): Number of events buffered before invoking callbacks.
		"""
        super().__init__(lib, dev_desc, data_field_selection, max_buffered_data_len, dld_events)

        self.queue = Queue()
        self.end_of_meas = False

    def on_data(self, d):
        """
        This class method function:
            1. Makes a deep copy of numpy arrays in d
            2. Inserts basic values by simple assignment
            3. Inserts numpy arrays using the copy method of the source array

        Args:
            d (dict): Data dictionary.

        Returns:
            None
        """
        dcopy = {}
        for k in d.keys():
            if isinstance(d[k], np.ndarray):
                dcopy[k] = d[k].copy()
            else:
                dcopy[k] = d[k]
        self.queue.put((QUEUE_DATA, dcopy))
        if self.end_of_meas:
            self.end_of_meas = False
            self.queue.put((QUEUE_ENDOFMEAS, None))

    def on_end_of_meas(self):
        """
        This class method sets end_of_meas to True.

        Returns:
            True (bool)
        """
        self.end_of_meas = True
        return True


def errorcheck(device, bufdatacb, bufdatacb_raw, retcode):
    """
    This function checks return codes for errors and does cleanup.

    Args:
        retcode (int): Return code.
        bufdatacb (BufDataCB4): A BufDataCB4 object.
        bufdatacb_raw (BufDataCB4): A BufDataCB4 object.
        device (scTDC.Device): A scTDC.Device object.

    Returns:
        int: 0 if success return code or return code > 0, -1 if return code is error code or less than 0.
    """
    if retcode < 0:
        print(device.lib.sc_get_err_msg(retcode))
        bufdatacb.close()
        bufdatacb_raw.close()
        device.deinitialize()
        return -1
    else:
        return 0


def atexit_handler(executor):
    executor.shutdown()


async def async_save_chunk(chunk_id, path, data_dict, executor):
    """Asynchronously saves a chunk of data to disk using memory mapping."""
    loop = asyncio.get_running_loop()
    def blocking_io():
        for key, data in data_dict.items():
             # Create a memory-mapped file
            filename = os.path.join(path, f"chunks/{key}_chunk_{chunk_id}.npy")
            with open(filename, 'wb') as f:
                np.save(f, data)

    await loop.run_in_executor(executor, blocking_io)
    print(f"Chunk {chunk_id} saved.")

def save_chunk_worker(save_queue, executor):
    async def process_queue():
        while True:
            item = save_queue.get()
            if item is None:
                break
            chunk_id, path, data_dict = item

            await async_save_chunk(chunk_id, path, data_dict, executor)
    asyncio.run(process_queue())


def load_and_concatenate_chunks(path, chunk_id):
    all_data = {
        "x_bin": [], "x_data": [], "y_bin": [], "y_data": [], "t_bin": [], "t_data": [],
        "voltage_data": [], "voltage_pulse_data": [], "laser_pulse_data": [], "start_counter": [],
        "channel_data": [], "time_data": [], "tdc_start_counter": [], "voltage_data_tdc": [],
        "voltage_pulse_data_tdc": [], "laser_pulse_data_tdc": []
    }

    total_sizes = {key: 0 for key in all_data}  # Store total sizes for memmap creation

    for i in range(1, chunk_id + 1):
        for attr_name in all_data:
            chunk_file = os.path.join(path, f"chunks/{attr_name}_chunk_{i}.npy")
            if os.path.exists(chunk_file):
                try:
                    with open(chunk_file, 'rb') as f:
                        arr = np.load(f, allow_pickle=False) # Important for memmap
                        total_sizes[attr_name] += arr.shape[0]
                        all_data[attr_name].append(arr)
                except Exception as e:
                    print(f"Error loading {chunk_file}: {e}")
            else:
                print(f"File '{chunk_file}' not found.")

    memmaped_data = {}

    for attr_name in all_data:
        if total_sizes[attr_name] > 0:
            dtype = all_data[attr_name][0].dtype
            shape = (total_sizes[attr_name],) + all_data[attr_name][0].shape[1:]  # Calculate correct shape
            memmap_filename = os.path.join(path, f"{attr_name}_memmap.npy")

            try:
                memmaped_data[attr_name] = np.memmap(memmap_filename, dtype=dtype, mode='w+', shape=shape)
                current_index = 0
                for arr in all_data[attr_name]:
                    memmaped_data[attr_name][current_index:current_index + len(arr)] = arr
                    current_index += len(arr)
                memmaped_data[attr_name].flush() #flush to disk
            except Exception as e:
                print(f"Error creating memmap for {attr_name}: {e}")
                return None
        else:
            memmaped_data[attr_name] = np.array([])
    return tuple(memmaped_data.values())

def run_experiment_measure(variables, x_plot, y_plot, t_plot, main_v_dc_plot, stop_event):
    """
    Measurement function: This function is called in a process to read data from the queue.

    Args:
        variables (share_variables.Variables): A share_variables.Variables object.
        x_plot (multiprocessing.Array): A multiprocessing.Array object.
        y_plot (multiprocessing.Array): A multiprocessing.Array object.
        t_plot (multiprocessing.Array): A multiprocessing.Array object.
        main_v_dc_plot (multiprocessing.Array): A multiprocessing.Array object.
        stop_event (multiprocessing.Event): A multiprocessing.Event object.

    Returns:
        int: Return code.
    """

    exposure_time = 100
    # surface concept tdc specific binning and factors
    TOFFACTOR = 27.432 / (1000 * 4)  # 27.432 ps/bin, tof in ns, data is TDC time sum
    DETBINS = 4900
    BINNINGFAC = 2
    XYFACTOR = 80 / DETBINS * BINNINGFAC  # XXX mm/bin
    XYBINSHIFT = DETBINS / BINNINGFAC / 2  # to center detector

    device = scTDC.Device(autoinit=False)
    retcode, errmsg = device.initialize()

    if retcode < 0:
        print("Error during init:", retcode, errmsg)
        print(f"{initialize_devices.bcolors.FAIL}Error: Restart the TDC manually "
              f"(Turn it On and Off){initialize_devices.bcolors.ENDC}")
        # variables.flag_tdc_failure = True
        return -1

    else:
        print("TDC is successfully initialized")
        variables.flag_tdc_failure = False

    DATA_FIELD_SEL = (scTDC.SC_DATA_FIELD_DIF1 |
                      scTDC.SC_DATA_FIELD_DIF2 |
                      scTDC.SC_DATA_FIELD_TIME |
                      scTDC.SC_DATA_FIELD_START_COUNTER)
    DATA_FIELD_SEL_raw = (scTDC.SC_DATA_FIELD_TIME |
                          scTDC.SC_DATA_FIELD_CHANNEL |
                          scTDC.SC_DATA_FIELD_START_COUNTER)

    bufdatacb = BufDataCB4(device.lib, device.dev_desc, DATA_FIELD_SEL, dld_events=True)
    bufdatacb_raw = BufDataCB4(device.lib, device.dev_desc, DATA_FIELD_SEL_raw, dld_events=False)

    # DLD data
    xx = []
    yy = []
    tt = []
    voltage_data = []
    voltage_pulse_data = []
    laser_pulse_data = []
    start_counter = []

    # The binning of DLD events
    xx_list_bin = []
    yy_list_bin = []
    tt_list_bin = []

    # TDC data (Raw data)
    channel_data = []
    time_data = []
    tdc_start_counter = []
    voltage_data_tdc = []
    voltage_pulse_data_tdc = []
    laser_pulse_data_tdc = []

    retcode = bufdatacb.start_measurement(exposure_time)
    if errorcheck(device, bufdatacb, bufdatacb_raw, retcode) < 0:
        print("Error during read:", retcode, device.lib.sc_get_err_msg(retcode))
        print(f"{initialize_devices.bcolors.FAIL}Error: Restart the TDC manually "
              f"(Turn it On and Off){initialize_devices.bcolors.ENDC}")
        return -1

    loop_time = 1 / variables.ex_freq
    events_detected = 0
    events_detected_tmp = 0
    raw_signal_detected = 0
    start_time = time.time()
    pulse_frequency = variables.pulse_frequency * 1000
    loop_counter = 0
    loop_delay_counter = 0

    with concurrent.futures.ThreadPoolExecutor() as executor:
        chunk_id = 0
        save_queue = mp.Queue()
        save_process = mp.Process(target=save_chunk_worker, args=(save_queue, executor))
        save_process.start()
        path = variables.path + "/temp_data/"
        # Create folder to save the data
        if not os.path.isdir(path):
            os.makedirs(path, mode=0o777, exist_ok=True)
        if not os.path.isdir(path + "chunks/"):
            os.makedirs(path + "chunks/", mode=0o777, exist_ok=True)

        while not stop_event.is_set():
            start_time_loop = time.time()
            eventtype, data = bufdatacb.queue.get()
            eventtype_raw, data_raw = bufdatacb_raw.queue.get()  # waits until element available
            specimen_voltage = variables.specimen_voltage
            voltage_pulse = variables.pulse_voltage
            laser_pulse = variables.laser_pulse_energy
            if eventtype == QUEUE_DATA:
                # correct for binning of surface concept
                xx_dif = data["dif1"]
                length = len(xx_dif)
                if length > 0:
                    events_detected_tmp += length
                    events_detected += length
                    yy_dif = data["dif2"]
                    tt_dif = data["time"]
                    start_counter.extend(data["start_counter"].tolist())
                    xx_tmp = ((xx_dif - XYBINSHIFT) * XYFACTOR) * 0.1  # from mm to in cm by dividing by 10
                    yy_tmp = ((yy_dif - XYBINSHIFT) * XYFACTOR) * 0.1  # from mm to in cm by dividing by 10
                    tt_tmp = tt_dif * TOFFACTOR  # in ns
                    dc_voltage_tmp = np.tile(specimen_voltage, len(xx_tmp))

                    # put data in shared memory for visualization
                    x_plot.put(xx_tmp)
                    y_plot.put(yy_tmp)
                    t_plot.put(tt_tmp)
                    main_v_dc_plot.put(dc_voltage_tmp)

                    # change to list
                    xx_tmp = xx_tmp.tolist()
                    yy_tmp = yy_tmp.tolist()
                    tt_tmp = tt_tmp.tolist()

                    # extend the main list with the new data
                    xx.extend(xx_tmp)
                    yy.extend(yy_tmp)
                    tt.extend(tt_tmp)
                    dc_voltage_tmp = dc_voltage_tmp.tolist()
                    p_voltage_tmp = np.tile(voltage_pulse, len(xx_tmp)).tolist()
                    p_laser_tmp = np.tile(laser_pulse, len(xx_tmp)).tolist()
                    voltage_data.extend(dc_voltage_tmp)
                    voltage_pulse_data.extend(p_voltage_tmp)
                    laser_pulse_data.extend(p_laser_tmp)

                    # The binning of DLD events
                    xx_list_bin.extend(xx_dif.tolist())
                    yy_list_bin.extend(yy_dif.tolist())
                    tt_list_bin.extend(tt_dif.tolist())

            if eventtype_raw == QUEUE_DATA:
                channel_data_tmp = data_raw["channel"].tolist()
                if len(channel_data_tmp) > 0:
                    raw_signal_detected += len(channel_data_tmp)
                    tdc_start_counter.extend(data_raw["start_counter"].tolist())
                    time_data.extend(data_raw["time"].tolist())
                    # raw data
                    channel_data.extend(channel_data_tmp)
                    voltage_data_tdc.extend((np.tile(specimen_voltage, len(channel_data_tmp))).tolist())
                    voltage_pulse_data_tdc.extend((np.tile(voltage_pulse, len(channel_data_tmp))).tolist())
                    laser_pulse_data_tdc.extend((np.tile(laser_pulse, len(channel_data_tmp))).tolist())

            if eventtype == QUEUE_ENDOFMEAS:
                retcode = bufdatacb.start_measurement(exposure_time, retries=10)  # retries is the number of times to retry
                if retcode < 0:
                    print("Error during read (error code: %s - error msg: %s):" % (retcode,
                                                                                   device.lib.sc_get_err_msg(retcode)))
                    # variables.flag_tdc_failure = True
                    break

            # Calculate the detection rate
            # Check if the detection rate interval has passed
            current_time = time.time()
            if current_time - start_time >= 0.5:
                detection_rate = events_detected_tmp * 100 / pulse_frequency
                variables.detection_rate_current = detection_rate * 2  # to get the rate per second
                variables.detection_rate_current_plot = detection_rate * 2  # to get the rate per second
                variables.total_ions = events_detected
                variables.total_raw_signals = raw_signal_detected
                # Reset the counter and timer
                events_detected_tmp = 0
                start_time = current_time

            if len(xx_list_bin) >= CHUNK_SIZE:
                if len(xx_list_bin) >= CHUNK_SIZE:
                    chunk_id += 1
                    data_to_save = {
                        "x_bin": np.array(xx_list_bin),
                        "x_data": np.array(xx),
                        "y_bin": np.array(yy_list_bin),
                        "y_data": np.array(yy),
                        "t_bin": np.array(tt_list_bin),
                        "t_data": np.array(tt),
                        "voltage_data": np.array(voltage_data),
                        "voltage_pulse_data": np.array(voltage_pulse_data),
                        "laser_pulse_data": np.array(laser_pulse_data),
                        "start_counter": np.array(start_counter),
                        "channel_data": np.array(channel_data),
                        "time_data": np.array(time_data),
                        "tdc_start_counter": np.array(tdc_start_counter),
                        "voltage_data_tdc": np.array(voltage_data_tdc),
                        "voltage_pulse_data_tdc": np.array(voltage_pulse_data_tdc),
                        "laser_pulse_data_tdc": np.array(laser_pulse_data_tdc),
                    }
                    save_queue.put((chunk_id, path, data_to_save))
                xx_list_bin.clear()
                xx.clear()
                yy_list_bin.clear()
                yy.clear()
                tt_list_bin.clear()
                tt.clear()
                voltage_data.clear()
                voltage_pulse_data.clear()
                laser_pulse_data.clear()
                start_counter.clear()
                channel_data.clear()
                time_data.clear()
                tdc_start_counter.clear()
                voltage_data_tdc.clear()
                voltage_pulse_data_tdc.clear()
                laser_pulse_data_tdc.clear()

            if time.time() - start_time_loop > loop_time:
                loop_delay_counter += 1
            loop_counter += 1

        print("TDC process: for %s times loop time took longer than %s second" % (loop_delay_counter, loop_time),
              'out of %s iteration' % loop_counter)
        variables.total_ions = events_detected
        variables.total_raw_signals = raw_signal_detected
        print("TDC Measurement stopped")

        if chunk_id > 0:
            chunk_id += 1
            data_to_save = {
                "x_bin": np.array(xx_list_bin),
                "x_data": np.array(xx),
                "y_bin": np.array(yy_list_bin),
                "y_data": np.array(yy),
                "t_bin": np.array(tt_list_bin),
                "t_data": np.array(tt),
                "voltage_data": np.array(voltage_data),
                "voltage_pulse_data": np.array(voltage_pulse_data),
                "laser_pulse_data": np.array(laser_pulse_data),
                "start_counter": np.array(start_counter),
                "channel_data": np.array(channel_data),
                "time_data": np.array(time_data),
                "tdc_start_counter": np.array(tdc_start_counter),
                "voltage_data_tdc": np.array(voltage_data_tdc),
                "voltage_pulse_data_tdc": np.array(voltage_pulse_data_tdc),
                "laser_pulse_data_tdc": np.array(laser_pulse_data_tdc),
            }
            save_queue.put((chunk_id, path, data_to_save))
            # Load all chunks and extend variables
            (xx_list_bin, xx, yy_list_bin, yy, tt_list_bin, tt, voltage_data, voltage_pulse_data,
             laser_pulse_data, start_counter, channel_data,
             time_data, tdc_start_counter, voltage_data_tdc, voltage_pulse_data_tdc,
             laser_pulse_data_tdc) = load_and_concatenate_chunks(path, chunk_id)

        save_queue.put(None)  # Signal the save process to end
        save_process.join()  # Wait for the save process to finish

        # save DLD data
        np.save(variables.path + "/temp_data/x_data.npy", np.array(xx))
        np.save(variables.path + "/temp_data/y_data.npy", np.array(yy))
        np.save(variables.path + "/temp_data/t_data.npy", np.array(tt))
        np.save(variables.path + "/temp_data/voltage_data.npy", np.array(voltage_data))
        np.save(variables.path + "/temp_data/voltage_pulse_data.npy", np.array(voltage_pulse_data))
        np.save(variables.path + "/temp_data/laser_pulse_data.npy", np.array(laser_pulse_data))
        np.save(variables.path + "/temp_data/start_counter.npy", np.array(start_counter))

        # save DLD data binning
        np.save(variables.path + "/temp_data/x_bin.npy", np.array(xx_list_bin))
        np.save(variables.path + "/temp_data/y_bin.npy", np.array(yy_list_bin))
        np.save(variables.path + "/temp_data/t_bin.npy", np.array(tt_list_bin))

        # save TDC data
        np.save(variables.path + "/temp_data/channel_data.npy", np.array(channel_data))
        np.save(variables.path + "/temp_data/time_data.npy", np.array(time_data))
        np.save(variables.path + "/temp_data/main_raw_counter.npy", np.array(tdc_start_counter))
        np.save(variables.path + "/temp_data/voltage_data_tdc.npy", np.array(voltage_data_tdc))
        np.save(variables.path + "/temp_data/voltage_pulse_data_tdc.npy", np.array(voltage_pulse_data_tdc))
        np.save(variables.path + "/temp_data/laser_pulse_data_tdc.npy", np.array(laser_pulse_data_tdc))

        variables.extend_to('x', xx)
        variables.extend_to('y', yy)
        variables.extend_to('t', tt)
        variables.extend_to('dld_start_counter', start_counter)
        variables.extend_to('main_v_dc_dld', voltage_data)
        variables.extend_to('main_v_p_dld', voltage_pulse_data)
        variables.extend_to('main_l_p_dld', laser_pulse_data)

        variables.extend_to('channel', channel_data)
        variables.extend_to('time_data', time_data)
        variables.extend_to('tdc_start_counter', tdc_start_counter)
        variables.extend_to('main_v_dc_tdc', voltage_data_tdc)
        variables.extend_to('main_v_p_tdc', voltage_pulse_data_tdc)
        variables.extend_to('main_l_p_tdc', laser_pulse_data_tdc)
        print("data save in share variables")
        time.sleep(0.1)
        bufdatacb.close()
        bufdatacb_raw.close()
        device.deinitialize()

        variables.flag_finished_tdc = True

        return 0


def experiment_measure(variables, x_plot, y_plot, t_plot, main_v_dc_plot, stop_event):

    run_experiment_measure(variables, x_plot, y_plot, t_plot, main_v_dc_plot, stop_event)
