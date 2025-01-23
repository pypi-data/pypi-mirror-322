import json
from glob import glob

import pytest

from vo2dict import read_voevent


@pytest.mark.parametrize("xml_file", glob("tests/test_events/*.xml"))
def test_read_voevent(xml_file):
    event = read_voevent(xml_file, is_file=True)
    if not isinstance(event, dict):
        raise TypeError(f"Expected dict, got {type(event)}")


@pytest.mark.parametrize("json_file", glob("tests/test_events/*.json"))
def test_read_json(json_file):
    with open(json_file, "r") as f:
        event = json.loads(f.read())
    if not isinstance(event, dict):
        raise TypeError(f"Expected dict, got {type(event)}")
