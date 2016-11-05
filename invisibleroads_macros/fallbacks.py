import os


if os.name == 'nt':
    COMMAND_LINE_HOME = '%UserProfile%'
else:
    COMMAND_LINE_HOME = '~'
