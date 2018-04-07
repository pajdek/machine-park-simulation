import simulator.simulator_input_data as simulator_input_data
from datetime import datetime
import pytest
from argparse import ArgumentTypeError
from unittest import mock


def test_valid_date_time_format_returns_datetime_object():
    mock_input_string = '2017-11-23 10:10'
    assert True is isinstance(simulator_input_data.valid_date_time_format(mock_input_string), datetime)


def test_valid_date_time_format_raise_exception_when_input_datetime_is_in_wrong_format():
    with pytest.raises(ArgumentTypeError):
        simulator_input_data.valid_date_time_format('wrong_format')


@pytest.fixture()
def raw_mock_data_from_db():
    raw_mock_avaliable_machines = [('machine_1', 0), ('machine_2', 0), ('machine_3', 0)]
    return raw_mock_avaliable_machines


@mock.patch('simulator.simulator_input_data.execute_select_method_and_return_fatchedall_data')
def test_get_avaliable_machines(mock_data, raw_mock_data_from_db):
    mock_data.return_value = raw_mock_data_from_db
    avaliable_machines = simulator_input_data.get_available_machines_from_data_base()
    assert avaliable_machines == ['machine_1', 'machine_2', 'machine_3']


@mock.patch('simulator.simulator_input_data.execute_select_method_and_return_fatchedall_data')
def test_input_machine_which_is_available_is_properly_returned(mock_data, raw_mock_data_from_db):
    mock_data.return_value = raw_mock_data_from_db
    assert 'machine_1' == simulator_input_data.valid_machine_id_and_check_machine_is_not_working('machine_1')


@mock.patch('simulator.simulator_input_data.execute_select_method_and_return_fatchedall_data')
def test_valid_machine_id_allows_only_defined_machine_id(mock_data, raw_mock_data_from_db):
    mock_proper_machine_id = 'machine_2'
    mock_wrong_machine_id = 'mm22'
    mock_data.return_value = raw_mock_data_from_db
    assert 'machine_2' == simulator_input_data.valid_machine_id_and_check_machine_is_not_working(mock_proper_machine_id)
    with pytest.raises(ArgumentTypeError):
        simulator_input_data.valid_machine_id_and_check_machine_is_not_working(mock_wrong_machine_id)
