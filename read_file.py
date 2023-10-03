# This module will look at the file given as input, either returning FILE NOT FOUND if the
# file cannot be found, or reading through the file to obtain the characteristics for the
# program.

from devices import *


def read_input_file(file_path):
    """
    Reads the input file then checks if it exists. If it does not exist, the program ends.
    Returns a list of the file's contents.
    """

    if file_path.is_file():
        with open(file_path, 'r') as opened_file:
            file_contents = opened_file.readlines()  # the file contents are in a list
        return file_contents

    else:
        print("FILE NOT FOUND")


def append_contents(contents_in_file):
    """
    Appends the list of characteristics to their respective keys in the dictionary.
    Returns the dictionary of lists of the characteristics in the file.
    """

    # dictionary of characteristics
    contents_dict = {"devices": {}, "propagation": [], "events": []}

    for line in contents_in_file:
        line.strip()  # remove the newlines from each line of the file

        # add the different characteristics to their respective keys in the dictionary
        if "LENGTH" in line:
            length_time = int(line.split()[1])
            contents_dict["length"] = length_time
        elif "DEVICE" in line:
            device_number = int(line.split()[1])
            contents_dict["devices"][device_number] = Device(device_number)
        elif "PROPAGATE" in line:
            initial_device = int(line.split()[1])
            device_to_propagate_to = int(line.split()[2])
            time_delay = int(line.split()[3])
            contents_dict["propagation"].append([initial_device, device_to_propagate_to, time_delay])
        elif "ALERT" in line:
            device_alert_start = int(line.split()[1])
            alert_name = line.split()[2]
            alert_time = int(line.split()[3])
            contents_dict["events"].append(AlertEvent(alert_time, -1, device_alert_start, alert_name))
        elif "CANCEL" in line:
            device_cancel_start = int(line.split()[1])
            cancel_name = line.split()[2]
            cancel_time = int(line.split()[3])
            contents_dict["events"].append(CancelEvent(cancel_time, -1, device_cancel_start, cancel_name))
    contents_dict['events'].sort()

    for initial_device, device_to_propagate_to, time_delay in contents_dict['propagation']:
        contents_dict["devices"][initial_device].add_propagation(device_to_propagate_to, time_delay)

    return contents_dict

