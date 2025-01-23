import json
import logging
from pprint import pprint
from typing import Union

import xmltodict

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s@%(name)s:%(lineno)d - %(message)s",
)
log = logging.getLogger(__name__)


def read_voevent(xml_content, is_file=False):
    """
    Converts a VOEvent XML string to a Python dictionary.

    Parameters:
        xml_content (str): The VOEvent XML data as a string.
        is_file (bool): If True, xml_content is a file path.

    Returns:
        dict: A Python dictionary representation of the VOEvent.
    """
    if is_file:
        log.debug(f"Reading VOEvent from file: {xml_content}")
        with open(xml_content, "r") as f:
            xml_content = f.read()
    # Parse the XML content using xmltodict
    log.debug("Parsing VOEvent XML")
    voevent_dict = xmltodict.parse(xml_content)
    log.debug("Cleaning VOEvent dictionary")
    d = clean_voevent(voevent_dict)
    if not hasattr(d, "RA") or not hasattr(d, "Dec"):
        try:
            d["RA"] = d["WhereWhen"]["ObsDataLocation"]["ObservationLocation"][
                "AstroCoords"
            ]["Position2D"]["Value2"]["C1"]
            d["Dec"] = d["WhereWhen"]["ObsDataLocation"]["ObservationLocation"][
                "AstroCoords"
            ]["Position2D"]["Value2"]["C2"]
        except KeyError:
            log.debug("RA and Dec not found in event")
            d["RA"] = None
            d["Dec"] = None
    return d


def coerce(val):
    """
    Turn our string representation of a value into a Python object.
    Priority is given to int, then float, then bool, then str.
    If an object is not a string, it is returned as is.

    Parameters:
    val (str): The string representation of a value.

    Returns:
    val (int, float, bool, str, obj): The Python object representation of a value.
    """
    # If the value is not a string, return it as is
    if not isinstance(val, str):
        return val

    # Try to convert the value to an int, then a float, then a bool
    try:
        return int(val)
    except ValueError:
        try:
            return float(val)
        except ValueError:
            if val.strip().lower() == "true":
                return True
            elif val.strip().lower() == "false":
                return False
            else:
                return val


def noat(val):
    """
    Remove the '@' symbol from a string if it exists.
    """
    if val.startswith("@"):
        return val[1:]
    return val


def clean_voevent(voevent: dict) -> dict:
    """
    Clean up the structure of the voevent dict so that it's much easier
    to work with.

    Parameters:
        voevent (dict): The VOEvent dictionary.

    Returns:
        dict: The cleaned VOEvent dictionary
    """

    # Check if the VOEvent is in the "voe:VOEvent" or "VOEvent" key
    # because the key changes depending on the VOEvent version
    if "voe:VOEvent" in voevent:
        k = "voe:VOEvent"
    else:
        k = "VOEvent"
    log.debug("Cleaning VOEvent:")
    if log.isEnabledFor(logging.DEBUG):
        pprint(voevent[k])
    return clean_dict(voevent[k])


def clean_dict(dirty: dict) -> dict:
    """
    Unpack a dict made by xlmtodict into a more readable format. This will
    remove all the @name and @value keys and replace them with the actual names
    and values.
    """
    new = dict()
    for k, v in dirty.items():
        name = noat(k)
        log.debug(f"Cleaning {name}")
        if name == "Param":
            new.update(group_params(v))
        elif name == "Group":
            new.update(group_groups(v))
        elif isinstance(v, dict):
            new[name] = clean_dict(v)
        elif isinstance(v, list):
            new[name] = clean_list(v)
        else:
            new[name] = coerce(v)
    return new


def clean_list(dirty: Union[list, dict]) -> list:
    new = []
    for item in dirty:
        if isinstance(item, dict):
            new.append(clean_dict(item))
        elif isinstance(item, list):
            new.append(clean_list(item))
        else:
            new.append(coerce(item))
    return new


def group_params(params: list) -> dict:
    new = dict()
    if not isinstance(params, list):
        params = [params]
    for p in params:
        name = p["@name"]
        log.debug(f"\tParam: {name}")
        new[name] = coerce(p["@value"])
        for k, v in p.items():
            if k not in ["@name", "@value"]:
                new[name + f"_{noat(k)}"] = coerce(v)
    return new


def group_groups(groups: Union[list, dict]) -> dict:
    new = dict()
    log.debug(f"Group: {groups}")
    if isinstance(groups, list):
        for p in groups:
            new.update(clean_dict(p))
            # name = p["@name"]
            # new[name] = group_params(p["Param"])
    elif isinstance(groups, dict):
        new.update(clean_dict(groups))
    return new


def test_all():
    from glob import glob

    print("| file | result | note |")
    print("| --- | --- | --- |")
    passed = 0
    failed = 0
    for fname in sorted(glob("output/*.xml")):
        try:
            if "classic" in fname:
                event = read_voevent(fname, is_file=True)
            else:
                with open(fname, "r") as f:
                    event = json.loads(f.read())
            new_fname = fname.replace(".xml", ".json")
            with open(new_fname, "w") as f:
                f.write(json.dumps(event))
        except Exception as e:
            print(f"| {fname} | fail | {e} |")
            failed += 1
        else:
            print(f"| {fname} | pass | |")
            passed += 1
    print(f"{passed} passed, {failed} failed")


def test_one(fname):
    log.setLevel(logging.DEBUG)
    if "classic" in fname:
        read_voevent(fname, is_file=True)
    else:
        with open(fname, "r") as f:
            json.loads(f.read())
    log.info(f"Successfully read {fname}")


if __name__ == "__main__":
    test_all()
    # test_one("output/20250123_063239_290_gcn.classic.voevent.LVC_PRELIMINARY.xml")
