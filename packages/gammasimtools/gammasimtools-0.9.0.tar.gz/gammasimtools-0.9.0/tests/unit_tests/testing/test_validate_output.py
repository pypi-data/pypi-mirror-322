#!/usr/bin/python3

import json
import logging
from pathlib import Path

import pytest
import yaml
from astropy.table import Table

from simtools.testing import validate_output

logging.getLogger().setLevel(logging.DEBUG)


@pytest.fixture
def create_json_file(tmp_test_directory):
    def _create_json_file(file_name, content):
        file = tmp_test_directory / file_name
        file.write_text(json.dumps(content), encoding="utf-8")
        return file

    return _create_json_file


@pytest.fixture
def create_yaml_file(tmp_path):
    def _create_yaml_file(file_name, content):
        file = tmp_path / file_name
        with open(file, "w", encoding="utf-8") as f:
            yaml.dump(content, f)
        return file

    return _create_yaml_file


@pytest.fixture
def create_ecsv_file(tmp_path):
    def _create_ecsv_file(file_name, content):
        table = Table(content)
        file_path = tmp_path / file_name
        table.write(file_path, format="ascii.ecsv")
        return file_path

    return _create_ecsv_file


@pytest.fixture
def file_name():
    def _file_name(counter, suffix):
        return f"file{counter}.{suffix}"

    return _file_name


@pytest.fixture
def output_path():
    return "/path/to/output"


@pytest.fixture
def mock_validate_application_output(mocker):
    return mocker.patch("simtools.testing.validate_output.validate_application_output")


@pytest.fixture
def mock_path_exists(mocker):
    return mocker.patch("simtools.testing.validate_output.Path.exists", return_value=True)


@pytest.fixture
def mock_check_output(mocker):
    return mocker.patch("simtools.testing.assertions.check_output_from_sim_telarray")


@pytest.fixture
def mock_validate_reference_output_file(mocker):
    return mocker.patch("simtools.testing.validate_output._validate_reference_output_file")


@pytest.fixture
def mock_validate_output_path_and_file(mocker):
    return mocker.patch("simtools.testing.validate_output._validate_output_path_and_file")


@pytest.fixture
def mock_assert_file_type(mocker):
    return mocker.patch("simtools.testing.assertions.assert_file_type")


def test_compare_json_files_float_strings(create_json_file, file_name):
    content = {"key": 1, "value": "1.23 4.56 7.89"}
    file1 = create_json_file(file_name(1, "json"), content)
    file2 = create_json_file(file_name(2, "json"), content)

    assert validate_output.compare_json_or_yaml_files(file1, file2)

    content3 = {"key": 2, "value": "1.23 4.56 7.80"}
    file3 = create_json_file(file_name(3, "json"), content3)
    assert not validate_output.compare_json_or_yaml_files(file1, file3)


def test_compare_json_files_equal_integers(create_json_file, file_name):
    content = {"key": 1, "value": 5}
    file1 = create_json_file(file_name(1, "json"), content)
    file2 = create_json_file(file_name(2, "json"), content)

    assert validate_output.compare_json_or_yaml_files(file1, file2)

    content3 = {"key": 2, "value": 7}
    file3 = create_json_file(file_name(3, "json"), content3)
    assert not validate_output.compare_json_or_yaml_files(file1, file3)


def test_compare_yaml_files_float_strings(create_yaml_file, file_name):
    content = {"key": 1, "value": "1.23 4.56 7.89"}
    file1 = create_yaml_file(file_name(1, "yaml"), content)
    file2 = create_yaml_file(file_name(2, "yaml"), content)

    assert validate_output.compare_json_or_yaml_files(file1, file2)

    content3 = {"key": 2, "value": "1.23 4.56 7.80"}
    file3 = create_yaml_file(file_name(3, "yaml"), content3)
    assert not validate_output.compare_json_or_yaml_files(file1, file3)


def test_compare_yaml_files_equal_integers(create_yaml_file, file_name):
    content = {"key": 1, "value": 5}
    file1 = create_yaml_file(file_name(1, "yaml"), content)
    file2 = create_yaml_file(file_name(2, "yaml"), content)

    assert validate_output.compare_json_or_yaml_files(file1, file2)

    content3 = {"key": 2, "value": 7}
    file3 = create_yaml_file(file_name(3, "yaml"), content3)
    assert not validate_output.compare_json_or_yaml_files(file1, file3)


def test_compare_ecsv_files_equal(create_ecsv_file, file_name):
    content = {"col1": [1.1, 2.2, 3.3], "col2": [4.4, 5.5, 6.6]}
    file1 = create_ecsv_file(file_name(1, "ecsv"), content)
    file2 = create_ecsv_file(file_name(2, "ecsv"), content)

    assert validate_output.compare_ecsv_files(file1, file2)


def test_compare_ecsv_files_different_lengths(create_ecsv_file, file_name):
    content1 = {"col1": [1.1, 2.2, 3.3], "col2": [4.4, 5.5, 6.6]}
    content2 = {"col1": [1.1, 2.2], "col2": [4.4, 5.5]}
    file1 = create_ecsv_file(file_name(1, "yaml"), content1)
    file2 = create_ecsv_file(file_name(2, "ecsv"), content2)

    assert not validate_output.compare_ecsv_files(file1, file2)


def test_compare_ecsv_files_close_values(create_ecsv_file, file_name):
    content1 = {"col1": [1.1001, 2.2001, 3.3001], "col2": [4.4001, 5.5001, 6.6001]}
    content2 = {"col1": [1.1, 2.2, 3.3], "col2": [4.4, 5.5, 6.6]}
    file1 = create_ecsv_file(file_name(1, "ecsv"), content1)
    file2 = create_ecsv_file(file_name(2, "ecsv"), content2)

    assert validate_output.compare_ecsv_files(file1, file2, tolerance=1.0e-3)


def test_compare_ecsv_files_large_difference(create_ecsv_file, file_name):
    content1 = {"col1": [1.1, 2.2, 3.3], "col2": [4.4, 5.5, 6.6]}
    content2 = {"col1": [10.1, 20.2, 30.3], "col2": [40.4, 50.5, 60.6]}
    file1 = create_ecsv_file(file_name(1, "ecsv"), content1)
    file2 = create_ecsv_file(file_name(2, "ecsv"), content2)

    assert not validate_output.compare_ecsv_files(file1, file2)


def test_compare_files_ecsv(create_ecsv_file, file_name):
    content = {"col1": [1.1, 2.2, 3.3], "col2": [4.4, 5.5, 6.6]}
    file1 = create_ecsv_file(file_name(1, "ecsv"), content)
    file2 = create_ecsv_file(file_name(2, "ecsv"), content)

    assert validate_output.compare_files(file1, file2)


def test_compare_files_ecsv_columns(create_ecsv_file, file_name):
    content1 = {"col1": [1.1, 2.2, 3.3], "col2": [4.4, 5.5, 6.6]}
    content2 = {"col1": [1.1, 2.21, 3.31], "col2": [4.47, 5.5, 6.6], "col3": [7.7, 8.8, 9.9]}
    file1 = create_ecsv_file(file_name(1, "ecsv"), content1)
    file2 = create_ecsv_file(file_name(2, "ecsv"), content2)

    assert validate_output.compare_files(file1, file2, 0.5)
    assert validate_output.compare_files(file1, file2, 0.005, [{"TEST_COLUMN_NAME": "col1"}])
    assert not validate_output.compare_files(file1, file2, 0.005, None)
    assert not validate_output.compare_files(file1, file2, 0.005, [{"TEST_COLUMN_NAME": "col2"}])
    assert validate_output.compare_files(
        file1,
        file2,
        0.005,
        [{"TEST_COLUMN_NAME": "col1", "CUT_COLUMN_NAME": "col2", "CUT_CONDITION": "> 4.5"}],
    )
    # select first column only (same values)
    assert validate_output.compare_files(
        file1,
        file2,
        1.0e-3,
        [{"TEST_COLUMN_NAME": "col1", "CUT_COLUMN_NAME": "col2", "CUT_CONDITION": "<5."}],
    )
    # select 2nd/3rd column with larger difference between values
    assert not validate_output.compare_files(
        file1,
        file2,
        1.0e-3,
        [{"TEST_COLUMN_NAME": "col1", "CUT_COLUMN_NAME": "col2", "CUT_CONDITION": ">5."}],
    )


def test_compare_files_json(create_json_file, file_name):
    content = {"key": 1, "value": "1.23 4.56 7.89"}
    file1 = create_json_file(file_name(1, "json"), content)
    file2 = create_json_file(file_name(2, "json"), content)

    assert validate_output.compare_files(file1, file2)


def test_compare_files_yaml(create_yaml_file, file_name):
    content = {"key": 1, "value": "1.23 4.56 7.89"}
    file1 = create_yaml_file(file_name(1, "yaml"), content)
    file2 = create_yaml_file(file_name(2, "yaml"), content)

    assert validate_output.compare_files(file1, file2)


def test_compare_files_different_suffixes(create_json_file, create_yaml_file, file_name):
    content = {"key": 1, "value": "1.23 4.56 7.89"}
    file1 = create_json_file(file_name(1, "json"), content)
    file2 = create_yaml_file(file_name(2, "yaml"), content)

    with pytest.raises(ValueError, match="File suffixes do not match"):
        validate_output.compare_files(file1, file2)


def test_compare_files_unknown_type(tmp_test_directory, file_name):
    file1 = tmp_test_directory / file_name(1, "txt")
    file2 = tmp_test_directory / file_name(2, "txt")
    file1.write_text("dummy content", encoding="utf-8")
    file2.write_text("dummy content", encoding="utf-8")

    assert not validate_output.compare_files(file1, file2)


def test_validate_all_tests_no_model_version(mocker, mock_validate_application_output):
    config = {"key": "value"}
    request = mocker.Mock()
    request.config.getoption.return_value = None
    config_file_model_version = None

    validate_output.validate_all_tests(config, request, config_file_model_version)

    mock_validate_application_output.assert_called_once_with(config)


def test_validate_all_tests_matching_model_version(mocker, mock_validate_application_output):
    config = {"key": "value"}
    request = mocker.Mock()
    request.config.getoption.return_value = "1.0"
    config_file_model_version = "1.0"

    validate_output.validate_all_tests(config, request, config_file_model_version)

    mock_validate_application_output.assert_called_once_with(config)


def test_validate_all_tests_non_matching_model_version(mocker, mock_validate_application_output):
    config = {"key": "value"}
    request = mocker.Mock()
    request.config.getoption.return_value = "1.0"
    config_file_model_version = "2.0"

    validate_output.validate_all_tests(config, request, config_file_model_version)

    mock_validate_application_output.assert_not_called()


def test_validate_reference_output_file(mocker, output_path):
    config = {"CONFIGURATION": {"OUTPUT_PATH": output_path, "OUTPUT_FILE": "output_file"}}
    integration_test = {
        "REFERENCE_OUTPUT_FILE": "/path/to/reference/file",
        "TOLERANCE": 1.0e-5,
        "TEST_COLUMNS": None,
    }

    mock_compare_files = mocker.patch(
        "simtools.testing.validate_output.compare_files", return_value=True
    )

    validate_output._validate_reference_output_file(config, integration_test)

    mock_compare_files.assert_called_once_with(
        integration_test["REFERENCE_OUTPUT_FILE"],
        Path(config["CONFIGURATION"]["OUTPUT_PATH"]).joinpath(
            config["CONFIGURATION"]["OUTPUT_FILE"]
        ),
        integration_test.get("TOLERANCE", 1.0e-5),
        integration_test.get("TEST_COLUMNS", None),
    )


def test_validate_output_path_and_file(output_path, mock_path_exists, mock_check_output):
    config = {
        "CONFIGURATION": {"OUTPUT_PATH": output_path, "DATA_DIRECTORY": "/path/to/data"},
        "INTEGRATION_TESTS": [{"EXPECTED_OUTPUT": "expected_output"}],
    }
    integration_test = [
        {"PATH_DESCRIPTOR": "DATA_DIRECTORY", "FILE": "output_file", "EXPECTED_OUTPUT": {}}
    ]

    validate_output._validate_output_path_and_file(config, integration_test)

    mock_path_exists.assert_called()
    mock_check_output.assert_called_once_with(
        Path(config["CONFIGURATION"]["DATA_DIRECTORY"]).joinpath(integration_test[0]["FILE"]),
        {},
    )

    wrong_integration_test = [
        {"PATH_DESCRIPTOR": "WRONG_PATH", "FILE": "output_file", "EXPECTED_OUTPUT": {}}
    ]
    with pytest.raises(
        KeyError, match="Path WRONG_PATH not found in integration test configuration."
    ):
        validate_output._validate_output_path_and_file(config, wrong_integration_test)


def test_validate_application_output_no_integration_tests(mocker, output_path):
    config = {"CONFIGURATION": {"OUTPUT_PATH": output_path}}
    mock_logger_info = mocker.patch("simtools.testing.validate_output._logger.info")

    validate_output.validate_application_output(config)

    mock_logger_info.assert_not_called()


def test_validate_application_output_with_reference_output_file(
    output_path,
    mock_assert_file_type,
    mock_validate_output_path_and_file,
    mock_validate_reference_output_file,
):
    config = {
        "CONFIGURATION": {"OUTPUT_PATH": output_path},
        "INTEGRATION_TESTS": [{"REFERENCE_OUTPUT_FILE": "/path/to/reference/file"}],
    }

    validate_output.validate_application_output(config)

    mock_validate_reference_output_file.assert_called_once_with(
        config, config["INTEGRATION_TESTS"][0]
    )
    mock_validate_output_path_and_file.assert_not_called()
    mock_assert_file_type.assert_not_called()


def test_validate_application_output_with_file_type(
    output_path,
    mock_assert_file_type,
    mock_validate_output_path_and_file,
    mock_validate_reference_output_file,
):
    config = {
        "CONFIGURATION": {"OUTPUT_PATH": output_path, "OUTPUT_FILE": "output_file"},
        "INTEGRATION_TESTS": [
            {"FILE_TYPE": "ecsv", "TEST_OUTPUT_FILES": [], "OUTPUT_FILE": "output_file"}
        ],
    }

    validate_output.validate_application_output(config)

    mock_validate_reference_output_file.assert_not_called()
    mock_validate_output_path_and_file.assert_called()
    assert mock_validate_output_path_and_file.call_count == 2
    mock_assert_file_type.assert_called_once_with(
        "ecsv",
        Path(config["CONFIGURATION"]["OUTPUT_PATH"]).joinpath(
            config["CONFIGURATION"]["OUTPUT_FILE"]
        ),
    )
