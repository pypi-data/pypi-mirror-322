"""Retrieval of array elements from the database."""

from functools import lru_cache

from pymongo import ASCENDING

from simtools.utils import names


@lru_cache
def get_array_elements(db_collection, model_version):
    """
    Get all array element names and their design model for a given DB collection.

    Uses the 'design_model' parameter to determine the design model of the array element.
    Assumes that a design model is defined for every array element.

    Parameters
    ----------
    db_collection:
        pymongo.collection.Collection
    model_version: str
       Model version.

    Returns
    -------
    dict
        Dict with array element names found and their design model

    Raises
    ------
    ValueError
        If query for collection name not implemented.
    KeyError
        If array element entry in the database is incomplete.

    """
    query = {"version": model_version}
    results = db_collection.find(query, {"instrument": 1, "value": 1, "parameter": 1}).sort(
        "instrument", ASCENDING
    )

    _all_available_array_elements = {}
    for doc in results:
        try:
            if doc["parameter"] == "design_model":
                _all_available_array_elements[doc["instrument"]] = doc["value"]
        except KeyError as exc:
            raise KeyError(f"Incomplete array element entry in the database: {doc}.") from exc

    if len(_all_available_array_elements) == 0:
        raise ValueError(f"No array elements found in DB collection {db_collection}.")

    return _all_available_array_elements


def get_array_element_list_for_db_query(array_element_name, db, model_version, collection):
    """
    Get array element name and design model for querying the database.

    Return a list of array element names to be used for querying the database for a given array
    element. This is in most cases the array element itself and its design model.
    In cases of no design model available, the design model of the array element is returned.

    Parameters
    ----------
    array_element_name: str
        Name of the array element model (e.g. MSTN-01).
    db: DBHandler
        Instance of the database handler
    model_version: str
        Model version.
    collection: str
        DB collection to get the array elements from (e.g., telescopes, calibration_devices)

    Returns
    -------
    list
        List of array element model names as used in the DB.

    """
    try:
        _available_array_elements = get_array_elements(
            db.get_collection(db_name=None, collection_name=collection),
            db.model_version(model_version),
        )
    except ValueError:
        return [names.get_array_element_type_from_name(array_element_name) + "-design"]
    try:
        return [_available_array_elements[array_element_name], array_element_name]
    except KeyError:
        pass

    if array_element_name in _available_array_elements.values():
        return [array_element_name]

    raise ValueError(f"Array element {array_element_name} not found in DB.")


def get_array_elements_of_type(array_element_type, db, model_version, collection):
    """
    Get all array elements of a certain type in the specified collection in the DB.

    Return e.g. for array_element_type='MSTS' all MSTS array elements found in the collection.

    Parameters
    ----------
    array_element_type : str
        Type of the array element (e.g. LSTN, MSTS)
    model_version : str
        Which version to get the array elements of
    collection : str
        Which collection to get the array elements from:
        i.e. telescopes, calibration_devices
    db_name : str
        Database name

    Returns
    -------
    list
        Sorted list of all array element names found in collection

    """
    _available_array_elements = get_array_elements(
        db.get_collection(db_name=None, collection_name=collection),
        db.model_version(model_version),
    )
    return sorted(
        [entry for entry in _available_array_elements if entry.startswith(array_element_type)]
    )
