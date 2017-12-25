from invisibleroads_macros.shell import format_variables_as_shell_script


def test_format_variables_as_shell_script():
    f = format_variables_as_shell_script
    assert f({'x': 1}) == 'X="1"'
    assert f({'x': None}) == 'X=""'
