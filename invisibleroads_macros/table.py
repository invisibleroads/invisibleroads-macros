from functools import partial


def duplicate_selected_column_names(selected_column_names, column_names):
    suffix = '*'
    while set(column_names).intersection(
            x + suffix for x in selected_column_names):
        suffix += '*'
    return list(column_names) + [x + suffix for x in selected_column_names]


def load_csv_safely(path, **kw):
    try:
        from pandas import read_csv
    except ImportError:
        import pip
        pip.main('install pandas'.split())
        from pandas import read_csv
    if 'skipinitialspace' not in kw:
        kw['skipinitialspace'] = True
    f = partial(read_csv, **kw)
    try:
        return f(path, encoding='utf-8')
    except UnicodeDecodeError:
        pass
    try:
        return f(path, encoding='latin-1')
    except UnicodeDecodeError:
        pass
    return f(open(path, errors='replace'))
