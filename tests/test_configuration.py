from invisibleroads_macros.configuration import split_arguments


def test_split_arguments():
    assert ['one', 'two'] == split_arguments('one \\\ntwo')
    assert ['one', 'two'] == split_arguments('one ^\ntwo')
