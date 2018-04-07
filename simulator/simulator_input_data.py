import argparse
import datetime
import sqlite3


DATE_TIME_FORMAT = '%Y-%m-%d %H:%M'


def get_input_from_user_by_argparse():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-m', '-machine_id', help='Machine name from simulation environment', required=True,
                            type=valid_machine_id_and_check_machine_is_not_working)
    arg_parser.add_argument('-sd', '-start_date', help="Start simulation date, should be earlier than stop_date, "
                                                       "format Y-m-d H:M", required=True, type=valid_date_time_format)
    arg_parser.add_argument('-ed', '-end_date', help="End simulation date, should be later than stop_date, "
                                                     "format Y-m-d H:M", required=True, type=valid_date_time_format)
    args = arg_parser.parse_args()
    input_data = {'start_simulation_date': args.sd, 'end_simulation_date': args.ed, 'machine': args.m}
    print(input_data)
    return input_data


def valid_date_time_format(input_value):
    try:
        return datetime.datetime.strptime(input_value, DATE_TIME_FORMAT)
    except ValueError:
        msg = "Not valid data time format, accepted format: {proper_format} " \
              "or date isn't exist".format(proper_format=DATE_TIME_FORMAT)
        raise argparse.ArgumentTypeError(msg)


def valid_machine_id_and_check_machine_is_not_working(machine_id):
    return check_machine_id_exist_in_database_and_its_simulation_is_not_running(machine_id)


def check_machine_id_exist_in_database_and_its_simulation_is_not_running(machine_id):
    avaliable_machines = get_available_machines_from_data_base()
    if machine_id in avaliable_machines:
        return machine_id
    else:
        msg = "Machine: {} is unavailable, available not working machines: {}".format(
            machine_id, avaliable_machines)
        raise argparse.ArgumentTypeError(msg)


def get_available_machines_from_data_base():
    query = "SELECT machine_name FROM machines WHERE is_working=0;"
    avaliable_machines = execute_select_method_and_return_fatchedall_data(query)
    avaliable_machines = [machine[0] for machine in avaliable_machines]
    return avaliable_machines


def execute_select_method_and_return_fatchedall_data(query):
    with sqlite3.connect('machines.db') as db:
        avaliable_machines = db.execute(query).fetchall()
    return avaliable_machines


get_input_from_user_by_argparse()
