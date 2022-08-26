"""Unit tests for lapspython.utils."""

import pytest

from dreamcoder.dreamcoder import ECResult
from lapspython.types import ParsedGrammar
from lapspython.utils import json_read, load_checkpoint


def test_load_checkpoint_valid():
    """Load valid checkpoint."""
    result = load_checkpoint('re2_test')
    assert isinstance(result, ECResult)


def test_load_checkpoint_invalid():
    """Try to load non-existent checkpoint."""
    msg = r".+ No such file or directory: 'checkpoints/invalid.pickle'"
    with pytest.raises(FileNotFoundError, match=msg):
        load_checkpoint('invalid')


def test_json_read_valid():
    """Load valid JSON."""
    json_dict = json_read('re2_test_python')
    assert list(json_dict.keys()) == ['grammar', 'result']
    assert isinstance(json_dict['grammar'], ParsedGrammar)
    assert isinstance(json_dict['result'], list)


def test_json_read_invalid():
    """Load non-existent JSON."""
    assert json_read('invalid') == {}
