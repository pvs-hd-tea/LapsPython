"""Unit tests for module lapspython.types."""

import pytest

from lapspython.types import ParsedPrimitive


class TestParsedPrimitive:
    """Run tests for lapspython.types.ParsedPrimitive."""

    def test_init_valid(self):
        """Construction using valid parameters."""
        name = 'name'
        source = 'source'
        args = ['arg0', 'arg1']
        pp = ParsedPrimitive(name, source, args)

        members = ('name', 'source', 'args')
        assert all(member in dir(pp) for member in members)
        assert type(pp.name) == str
        assert pp.name == name
        assert type(pp.source) == str
        assert pp.source == source
        assert type(pp.args) == list
        assert len(pp.args) == 2
        assert all(pp.args[i] == args[i] for i in range(len(args)))
        assert pp.args == args

    def test_init_args_tuple(self):
        """Construction using arguments tuple."""
        args = ('arg0', 'arg1', 'arg2')
        pp = ParsedPrimitive('name', 'source', args)
        assert type(pp.args) == tuple
        assert len(pp.args) == 3
        assert pp.args == args
        assert all(pp.args[i] == args[i] for i in range(len(args)))

    def test_init_args_empty(self):
        """Construction using empty arguments."""
        pp = ParsedPrimitive('name', 'source', [])
        assert type(pp.args) == list
        assert len(pp.args) == 0
        assert pp.args == []

    def test_init_invalid_name(self):
        """Construction using invalid name parameters."""
        expected_message = 'name must be a non-empty string.'
        with pytest.raises(TypeError, match=expected_message):
            ParsedPrimitive(42, 'source', [])
        with pytest.raises(ValueError, match=expected_message):
            ParsedPrimitive('', 'source', [])

    def test_init_invalid_source(self):
        """Construction using invalid source parameters."""
        expected_message = 'source must be a non-empty string.'
        with pytest.raises(TypeError, match=expected_message):
            ParsedPrimitive('name', 42, [])
        with pytest.raises(ValueError, match=expected_message):
            ParsedPrimitive('name', '', [])

    def test_init_invalid_args(self):
        """Construction using invalid args parameters."""
        expected_message = 'args must be a list or tuple of strings.'
        with pytest.raises(TypeError, match=expected_message):
            ParsedPrimitive('string', 'source', 'arg')
        with pytest.raises(TypeError, match=expected_message):
            ParsedPrimitive('name', 'source', 42)
        with pytest.raises(TypeError, match=expected_message):
            ParsedPrimitive('name', 'source', [42])

    def test_resolve_valid(self):
        """Resolution using valid parameters."""
        source = 'token0 token1 token2 token3'
        pp = ParsedPrimitive('name', source, ['token1', 'token2'])
        new_args = ['mask0', 'mask1']
        new_source = 'token0 mask0 mask1 token3'
        assert pp.resolve(new_args) == new_source

    def test_resolve_identity(self):
        """Resolution using identical arguments."""
        source = 'token0 token1 token2 token3'
        args = ['token1', 'token2']
        pp = ParsedPrimitive('name', source, args)
        assert pp.resolve(args) == source

    def test_resolve_empty(self):
        """Resolution using empty arguments."""
        pp = ParsedPrimitive('name', 'source', [])
        assert pp.resolve([]) == 'source'

    def test_resolve_invalid_args(self):
        """Resolution using invalid arguments."""
        pp = ParsedPrimitive('name', 'source', [])
        expected_message = 'args must be a list or tuple of strings.'
        with pytest.raises(TypeError, match=expected_message):
            pp.resolve('mask')
        with pytest.raises(TypeError, match=expected_message):
            pp.resolve(42)
        with pytest.raises(TypeError, match=expected_message):
            pp.resolve([42])

    def test_resolve_invalid_length(self):
        """Resolution using incomplete arguments."""
        pp = ParsedPrimitive('name', 'source', ['arg'])
        expected_message = 'args length 2 != 1.'
        with pytest.raises(ValueError, match=expected_message):
            pp.resolve(['arg0', 'arg1'])

