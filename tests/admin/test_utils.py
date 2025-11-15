import pytest

from admin.utils import multiple_parameters


class TestMultipleParameters:
    @pytest.mark.parametrize(
        'parameter, options, expected',
        [
            ('--foo', ['a', 'b'], ['--foo', 'a', '--foo', 'b']),
            ('--foo', ['a'], ['--foo', 'a']),
            ('--foo', [], []),
            ('--foo', ['a', 2], ['--foo', 'a', '--foo', '2']),
        ],
    )
    def test_multiple_parameters(self, parameter, options, expected):
        assert multiple_parameters(parameter, *options) == expected
