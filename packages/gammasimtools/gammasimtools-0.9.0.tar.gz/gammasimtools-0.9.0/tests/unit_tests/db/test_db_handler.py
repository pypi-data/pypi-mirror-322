#!/usr/bin/python3

import copy
import logging
import re
import uuid

import pytest

from simtools.db import db_handler

logger = logging.getLogger()


@pytest.fixture
def random_id():
    return uuid.uuid4().hex


@pytest.fixture
def db_no_config_file():
    """Database object (without configuration)."""
    return db_handler.DatabaseHandler(mongo_db_config=None)


@pytest.fixture
def _db_cleanup(db, random_id):
    yield
    # Cleanup
    logger.info(f"dropping sandbox_{random_id} collections")
    db.db_client[f"sandbox_{random_id}"]["telescopes"].drop()
    db.db_client[f"sandbox_{random_id}"]["calibration_devices"].drop()
    db.db_client[f"sandbox_{random_id}"]["sites"].drop()


@pytest.fixture
def fs_files():
    return "fs.files"


@pytest.fixture
def _db_cleanup_file_sandbox(db_no_config_file, random_id, fs_files):
    yield
    # Cleanup
    logger.info("Dropping the temporary files in the sandbox")
    db_no_config_file.db_client[f"sandbox_{random_id}"]["fs.chunks"].drop()
    db_no_config_file.db_client[f"sandbox_{random_id}"][fs_files].drop()


def test_valid_db_config(db, db_config):
    assert db.mongo_db_config == db._validate_mongo_db_config(db_config)
    assert db._validate_mongo_db_config(None) is None
    none_db_dict = copy.deepcopy(db_config)
    for key in none_db_dict.keys():
        none_db_dict[key] = None
    assert db._validate_mongo_db_config(none_db_dict) is None
    assert db._validate_mongo_db_config({}) is None
    with pytest.raises(ValueError, match=r"Invalid MongoDB configuration"):
        db._validate_mongo_db_config({"wrong_config": "wrong"})


def test_find_latest_simulation_model_db(db, db_no_config_file, mocker):

    db_no_config_file._find_latest_simulation_model_db()
    assert db_no_config_file.mongo_db_config is None

    db_name = db.mongo_db_config["db_simulation_model"]
    db._find_latest_simulation_model_db()
    assert db_name == db.mongo_db_config["db_simulation_model"]

    db_copy = copy.deepcopy(db)
    db_copy.mongo_db_config["db_simulation_model"] = "DB_NAME-LATEST"
    with pytest.raises(
        ValueError, match=r"Found LATEST in the DB name but no matching versions found in DB."
    ):
        db_copy._find_latest_simulation_model_db()

    db_names = [
        "CTAO-Simulation-Model-v0-3-0",
        "CTAO-Simulation-Model-v0-2-0",
        "CTAO-Simulation-Model-v0-1-19",
        "CTAO-Simulation-Model-v0-3-9",
        "CTAO-Simulation-Model-v0-3-19",
        "CTAO-Simulation-Model-v0-3-0",
        "CTAO-Simulation-Model-v0-3-0-alpha-2",
        "CTAO-Simulation-Model-v0-4-19-alpha-1",
        "CTAO-Simulation-Model-v0-4-19-dev1",
    ]
    mocker.patch.object(db_copy.db_client, "list_database_names", return_value=db_names)
    db_copy.mongo_db_config["db_simulation_model"] = "CTAO-Simulation-Model-LATEST"
    db_copy._find_latest_simulation_model_db()
    assert db_copy.mongo_db_config["db_simulation_model"] == "CTAO-Simulation-Model-v0-3-19"


def test_reading_db_lst_without_simulation_repo(db, model_version):

    db_copy = copy.deepcopy(db)
    db_copy.mongo_db_config["db_simulation_model_url"] = None
    pars = db.get_model_parameters("North", "LSTN-01", model_version, collection="telescopes")
    assert pars["parabolic_dish"]["value"] == 1
    assert pars["camera_pixels"]["value"] == 1855


def test_reading_db_lst(db, model_version):
    logger.info("----Testing reading LST-North-----")
    pars = db.get_model_parameters("North", "LSTN-01", model_version, collection="telescopes")
    if db.mongo_db_config:
        assert pars["parabolic_dish"]["value"] == 1
        assert pars["camera_pixels"]["value"] == 1855
    else:
        assert pars["parabolic_dish"] == 1
        assert pars["camera_pixels"] == 1855


def test_reading_db_mst_nc(db, model_version):
    logger.info("----Testing reading MST-North-----")
    pars = db.get_model_parameters("North", "MSTN-design", model_version, collection="telescopes")
    if db.mongo_db_config:
        assert pars["camera_pixels"]["value"] == 1855
    else:
        assert pars["camera_pixels"] == 1855


def test_reading_db_mst_fc(db, model_version):
    logger.info("----Testing reading MST-South-----")
    pars = db.get_model_parameters("South", "MSTS-design", model_version, collection="telescopes")
    if db.mongo_db_config:
        assert pars["camera_pixels"]["value"] == 1764
    else:
        assert pars["camera_pixels"] == 1764


def test_reading_db_sst(db, model_version):
    logger.info("----Testing reading SST-----")
    pars = db.get_model_parameters("South", "SSTS-design", model_version, collection="telescopes")
    if db.mongo_db_config:
        assert pars["camera_pixels"]["value"] == 2048
    else:
        assert pars["camera_pixels"] == 2048


@pytest.mark.xfail(reason="Test requires Derived-Values Database")
def test_get_derived_values(db, model_version_prod5):
    logger.info("----Testing reading derived values-----")
    try:
        pars = db.get_derived_values("North", "LSTN-01", model_version_prod5)
        assert (
            pars["ray_tracing"]["value"]
            == "ray-tracing-North-LST-1-d10.0-za20.0_validate_optics.ecsv"
        )
    except ValueError:
        logger.error("Derived DB not updated for new telescope names. Expect failure")
        raise AssertionError

    with pytest.raises(ValueError, match=r"^abc"):
        pars = db.get_derived_values("North", None, model_version_prod5)


def test_get_sim_telarray_configuration_parameters(db, model_version):

    _pars = db.get_model_parameters(
        "North", "LSTN-01", model_version, collection="configuration_sim_telarray"
    )
    assert "min_photoelectrons" in _pars

    _pars = db.get_model_parameters(
        "North", "LSTN-design", model_version, collection="configuration_sim_telarray"
    )
    assert "min_photoelectrons" in _pars


@pytest.mark.usefixtures("_db_cleanup")
def test_copy_array_element_db(db, random_id, io_handler, model_version):
    logger.info("----Testing copying a whole telescope-----")
    db.copy_array_element(
        db_name=None,
        element_to_copy="LSTN-01",
        version_to_copy=model_version,
        new_array_element_name="LSTN-test",
        collection_name="telescopes",
        db_to_copy_to=f"sandbox_{random_id}",
        collection_to_copy_to="telescopes",
    )
    pars = db.read_mongo_db(
        db_name=f"sandbox_{random_id}",
        array_element_name="LSTN-test",
        model_version=model_version,
        run_location=io_handler.get_output_directory(sub_dir="model"),
        collection_name="telescopes",
        write_files=False,
    )
    assert pars["camera_pixels"]["value"] == 1855


@pytest.mark.usefixtures("_db_cleanup")
def test_adding_new_parameter_db(db, random_id, io_handler, model_version):
    logger.info("----Testing adding a new parameter-----")
    test_model_version = "0.0.9876"
    tmp_par_dict = {
        "parameter": None,
        "instrument": "LSTN-test",
        "site": "North",
        "version": test_model_version,
        "value": None,
        "unit": None,
        "type": None,
        "applicable": True,
        "file": False,
    }

    par_dict_int = copy.deepcopy(tmp_par_dict)
    par_dict_int["parameter"] = "num_gains"
    par_dict_int["value"] = 3
    par_dict_int["type"] = "int64"
    with pytest.raises(
        ValueError,
        match=re.escape("Value for column '0' out of range. ([3, 3], allowed_range: [1, 2])"),
    ):
        db.add_new_parameter(
            db_name=f"sandbox_{random_id}",
            par_dict=par_dict_int,
            collection_name="telescopes",
        )
    par_dict_int["value"] = 2
    db.add_new_parameter(
        db_name=f"sandbox_{random_id}",
        par_dict=par_dict_int,
        collection_name="telescopes",
    )

    par_dict_list = copy.deepcopy(tmp_par_dict)
    par_dict_list["parameter"] = "telescope_transmission"
    par_dict_list["value"] = [0.969, 0.01, 0.0, 0.0, 0.0, 0.0]
    par_dict_list["type"] = "float64"
    db.add_new_parameter(
        db_name=f"sandbox_{random_id}",
        par_dict=par_dict_list,
        collection_name="telescopes",
    )
    par_dict_quantity = copy.deepcopy(tmp_par_dict)
    par_dict_quantity["parameter"] = "focal_length"
    par_dict_quantity["value"] = 12.5  # test that value is converted to cm
    par_dict_quantity["type"] = "float64"
    par_dict_quantity["unit"] = "m"
    db.add_new_parameter(
        db_name=f"sandbox_{random_id}",
        par_dict=par_dict_quantity,
        collection_name="telescopes",
    )

    par_dict_file = copy.deepcopy(tmp_par_dict)
    par_dict_file["parameter"] = "mirror_list"
    par_dict_file["value"] = "mirror_list_CTA-N-LST1_v2019-03-31_rotated_simtel.dat"
    par_dict_file["type"] = "file"
    par_dict_file["file"] = True
    with pytest.raises(FileNotFoundError, match=r"^The location of the file to upload"):
        db.add_new_parameter(
            db_name=f"sandbox_{random_id}",
            par_dict=par_dict_file,
            collection_name="telescopes",
        )
    db.add_new_parameter(
        db_name=f"sandbox_{random_id}",
        par_dict=par_dict_file,
        collection_name="telescopes",
        file_prefix="tests/resources",
    )

    pars = db.read_mongo_db(
        db_name=f"sandbox_{random_id}",
        array_element_name="LSTN-test",
        model_version=test_model_version,
        run_location=io_handler.get_output_directory(sub_dir="model"),
        collection_name="telescopes",
        write_files=False,
    )
    assert pars["num_gains"]["value"] == 2
    assert pars["num_gains"]["type"] == "int64"
    assert isinstance(pars["telescope_transmission"]["value"], list)
    assert pars["focal_length"]["value"] == pytest.approx(1250.0)
    assert pars["focal_length"]["unit"] == "cm"
    assert pars["mirror_list"]["file"] is True

    # make sure that cache has been emptied after updating
    assert (
        db._parameter_cache_key("North", "LSTN-test", test_model_version)
        not in db.model_parameters_cached
    )


def test_reading_db_sites(db, db_config, simulation_model_url, model_version):
    logger.info("----Testing reading La Palma parameters-----")
    db.mongo_db_config["db_simulation_model_url"] = None
    pars = db.get_site_parameters("North", model_version)
    if db.mongo_db_config:
        _obs_level = pars["corsika_observation_level"].get("value")
        assert _obs_level == pytest.approx(2156.0)
    else:
        assert pars["altitude"] == 2156

    logger.info("----Testing reading Paranal parameters-----")
    pars = db.get_site_parameters("South", model_version)
    if db.mongo_db_config:
        _obs_level = pars["corsika_observation_level"].get("value")
        assert _obs_level == pytest.approx(2147.0)
    else:
        assert pars["altitude"] == 2147

    db._reset_parameter_cache("South", None, model_version)
    if db.mongo_db_config.get("db_simulation_model_url", None) is None:
        db.mongo_db_config["db_simulation_model_url"] = simulation_model_url
    pars = db.get_site_parameters("South", model_version)
    assert pars["corsika_observation_level"]["value"] == 2147.0
    db.mongo_db_config["db_simulation_model_url"] = None  # make sure that this is reset


def test_separating_get_and_write(db, io_handler, model_version):
    logger.info("----Testing getting parameters and exporting model files-----")
    pars = db.get_model_parameters("North", "LSTN-01", model_version, collection="telescopes")

    file_list = []
    for par_now in pars.values():
        if par_now["file"] and par_now["value"] is not None:
            file_list.append(par_now["value"])
    db.export_model_files(
        pars,
        io_handler.get_output_directory(sub_dir="model"),
    )
    logger.debug(
        "Checking files were written to " f"{io_handler.get_output_directory(sub_dir='model')}"
    )
    for file_now in file_list:
        assert io_handler.get_output_file(file_now, sub_dir="model").exists()


def test_export_file_db(db, io_handler):
    logger.info("----Testing exporting files from the DB-----")
    output_dir = io_handler.get_output_directory(sub_dir="model")
    file_name = "mirror_CTA-S-LST_v2020-04-07.dat"
    file_to_export = output_dir / file_name
    db.export_file_db(None, output_dir, file_name)
    assert file_to_export.exists()


@pytest.mark.usefixtures("_db_cleanup_file_sandbox")
def test_insert_files_db(db, io_handler, random_id, caplog):
    logger.info("----Testing inserting files to the DB-----")
    logger.info(
        "Creating a temporary file in " f"{io_handler.get_output_directory(sub_dir='model')}"
    )
    file_name = io_handler.get_output_directory(sub_dir="model") / f"test_file_{random_id}.dat"
    with open(file_name, "w") as f:
        f.write("# This is a test file")

    file_id = db.insert_file_to_db(file_name, f"sandbox_{random_id}")
    assert (
        file_id == db._get_file_mongo_db(f"sandbox_{random_id}", f"test_file_{random_id}.dat")._id
    )
    logger.info("Now test inserting the same file again, this time expect a warning")
    with caplog.at_level(logging.WARNING):
        file_id = db.insert_file_to_db(file_name, f"sandbox_{random_id}")
    assert "exists in the DB. Returning its ID" in caplog.text
    assert (
        file_id == db._get_file_mongo_db(f"sandbox_{random_id}", f"test_file_{random_id}.dat")._id
    )


def test_get_all_versions(db, mocker, caplog):

    # not specifying any database names, collections, or parameters
    all_versions = db.get_all_versions()
    assert all(_v in all_versions for _v in ["5.0.0", "6.0.0"])
    assert any(key.endswith("None") for key in db.model_versions_cached)

    # not specifying a telescope model name and parameter
    all_versions = db.get_all_versions(
        array_element_name=None,
        site="North",
        parameter=None,
        collection="telescopes",
    )
    assert all(_v in all_versions for _v in ["5.0.0", "6.0.0"])
    assert any("telescopes" in key for key in db.model_versions_cached)

    # using a specific parameter
    all_versions = db.get_all_versions(
        array_element_name="LSTN-01",
        site="North",
        parameter="camera_config_file",
        collection="telescopes",
    )
    assert all(_v in all_versions for _v in ["5.0.0", "6.0.0"])
    assert any(
        key.endswith("telescopes-camera_config_file-LSTN-01") for key in db.model_versions_cached
    )

    all_versions = db.get_all_versions(
        site="North",
        parameter="corsika_observation_level",
        collection="sites",
    )
    assert all(_v in all_versions for _v in ["5.0.0", "6.0.0"])
    assert any(
        key.endswith("sites-corsika_observation_level-North") for key in db.model_versions_cached
    )

    # no db_name defined
    mocker.patch.object(db, "_get_db_name", return_value=None)
    with caplog.at_level(logging.WARNING):
        assert db.get_all_versions() == []
    assert "No database name defined to determine" in caplog.text


def test_parameter_cache_key(db, model_version_prod5):

    assert db._parameter_cache_key("North", "LSTN-01", model_version_prod5) == "North-LSTN-01-5.0.0"
    assert db._parameter_cache_key("North", None, model_version_prod5) == "North-5.0.0"
    assert db._parameter_cache_key(None, None, model_version_prod5) == "5.0.0"


def test_model_version(db):

    assert db.model_version(version="6.0.0") == "6.0.0"

    with pytest.raises(ValueError, match=r"Invalid model version test"):
        db.model_version(version="test")
    with pytest.raises(ValueError, match=r"Invalid model version 0.0.9876"):
        db.model_version(version="0.0.9876")


def test_get_collections(db, db_config, fs_files):

    collections = db.get_collections()
    assert isinstance(collections, list)
    assert "telescopes" in collections

    collections_from_name = db.get_collections(db_config["db_simulation_model"])
    assert isinstance(collections_from_name, list)
    assert "telescopes" in collections_from_name
    assert fs_files in collections_from_name

    collections_no_model = db.get_collections(db_config["db_simulation_model"], True)
    assert isinstance(collections_no_model, list)
    assert "telescopes" in collections_no_model
    assert fs_files not in collections_no_model
    assert "metadata" not in collections_no_model


def test_model_version_empty(db, mocker):

    mocker.patch.object(db, "get_all_versions", return_value=[])
    assert db.model_version("6.0.0") is None
