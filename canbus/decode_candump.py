""" decode_candump.py is a program for reading CAN-based Frames of a candump dumpfile created using
the SocketCAN Utility toolbox.
There are currently two vehicle data identifier frames identified:
"Revolutions per minute (RPM)" and "Fuel consumption", these are processed in this program.
Using low byte, high byte information and scaling factors, we can decode the hexadecimal-based message format.
Additional CAN metadata can be identified, and implemented using this approach.

Author: Dezhi Fu

"""


# Exemplatory identifiers
revolutions_per_minute_identifier = '0CF004F0'
fuel_consumption_identifier = '0CFEF2F0'
# Low Byte High Byte
rpm_low_byte = 3
rpm_high_byte = 4
consumption_low_byte = 0
consumption_high_byte = 1
# Scaling factor
rpm_scaling_factor = 8
consumption_scaling_factor = 20
# functions


def decode_can_message(data_field, low_byte, high_byte, scaling_factor):
    """ decode_can_message accepts 4 parameters in order to decode a hexadecimal CAN frame data field string into a number.
    It returns the decoded data value.
    data_field: The hexadecimal string to decode. It is converted using int(argument, 16) to an integer.
    low_byte: The position of the hexadecimal string of low data field byte.
    high_byte: The position of the hexadecimal string of high data field byte.
    scaling_factor: The reciprocal conversion factor we need to apply on the measured value.
    """
    data_value_low = (int("".join(data_field[low_byte]), 16))
    data_value_high = (int("".join(data_field[high_byte])+'00', 16))
    data_value = (data_value_low+data_value_high)/scaling_factor
    return data_value


def build_sentence(identifier, local_time_stamp, data_value):
    """ build_sentence accepts 3 parameters in order to construct a telemetry data sentence.
    Those are the hexadecimal identifier of the CAN frame, the local time timestamp, and the measured value.
    It returns a data sentence, which contains a unique identifier, the data value, the observed property and unit.
    identifier: Hexadecimal identifier of CAN frame.
    local_time_stamp: The number of seconds, including after dot values, counted from a reference time.
    data_value: The converted data value from the CAN frame.
    """
    if (revolutions_per_minute_identifier == identifier):
        return local_time_stamp+",RPM," + str(data_value) + ",r/min"
    elif (fuel_consumption_identifier == identifier):
        return local_time_stamp+",Consumption," + str(data_value) + ",l/h"


def file_len(fname):
    """ file_len accepts 1 parameter, which represents the path of a file.
    It calculates the number of lines in the file and returns it.
    fname: The path to the file.  
    """
    with open(fname) as f:
        return len(f.readlines())


def get_file(fname):
    """ get_file accepts 1 parameter, which represents the path of a file.
    It returns the content of a textfile as a list.
    fname: The path to the file.  
    """
    with open(fname, "r") as f:
        return f.readlines()


def skip_and_pad(string, length):
    """ skip_and_pad accepts 2 parameters, which represent the to be processed string
    and the number of characters we want to skip over.
    It returns the string with whitespaces, which are inserted after "length" characters.
    string: The to be processed string.
    length: The number of characters to skip over.
    """
    return ' '.join(string[i:i+length] for i in range(0, len(string), length))


def compute_data_field(single_can_frame):
    """ compute_data_field accepts 1 parameter and computes a data field suitable for sentence construction.
    single_can_frame: A single can frame.
    """
    # get data field of CAN frame
    data_field = single_can_frame[2][9::]
    # pad it
    data_field = skip_and_pad(data_field, 2)
    # split the result to get twin digits
    data_field = data_field.split(" ")
    return data_field


def compute_data_sentence(data_field, local_time_stamp, low_byte, high_byte, scaling_factor):
    """ compute_data_sentence accepts 5 parameters and compute the final data result set (the data sentence).
    data_field: The data field.
    local_time_stamp: A timestamp.
    low_byte: Low byte of the can data.
    high_byte: High byte of the can data.
    scaling_factor: Scaling factor of the can data.
    """
    data_value = decode_can_message(
        data_field, low_byte, high_byte, scaling_factor)
    data_sentence = build_sentence(identifier, local_time_stamp, data_value)
    return data_sentence


# Get all lines from file
candump_file = get_file("./resources/candump-2016-07-14_184358.log")

identifier_frame_index = 2
identifier_start_index = 0
identifier_end_index = 8
# for each line
for line in candump_file:
    # get one CAN Frame and save to list
    single_can_frame = [x for x in line.split(' ') if x]
    # extract identifier
    identifier = single_can_frame[identifier_frame_index][identifier_start_index:identifier_end_index]
    # extract localtime timestamp
    local_time_stamp = single_can_frame[0][1:len(single_can_frame[0])-1]
    data_field = compute_data_field(single_can_frame)
    # decode message according to identifier
    data_sentence = None
    if (revolutions_per_minute_identifier == identifier):
        data_sentence = compute_data_sentence(
            data_field, local_time_stamp, rpm_low_byte, rpm_high_byte, rpm_scaling_factor)
    elif (fuel_consumption_identifier == identifier):
        data_sentence = compute_data_sentence(
            data_field, local_time_stamp, consumption_low_byte, consumption_high_byte, consumption_scaling_factor)
    if (data_sentence is not None):
        with open('./resources/CANData.txt', 'a') as file:
            file.write(data_sentence + '\n')
