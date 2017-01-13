import datetime
import re
import shlex
import simplejson as json
from six import string_types
from subprocess import CalledProcessError, Popen, check_output, PIPE, STDOUT
from urllib import urlencode

from .exceptions import InvisibleRoadsError


def run_command(command, exception_by_error=None):
    if not isinstance(command, string_types):
        command = ' '.join(command)
    command = command.split(';', 1)[0]
    return run_raw_command(command, exception_by_error)


def run_raw_command(command, exception_by_error=None):
    if isinstance(command, string_types):
        command = shlex.split(command)
    try:
        output = check_output(command, stderr=STDOUT)
    except CalledProcessError as e:
        o = e.output
        for error_text, exception in (exception_by_error or {}).items():
            if error_text in o:
                raise exception
        else:
            raise InvisibleRoadsError(o)
    except OSError as e:
        raise InvisibleRoadsError(e.strerror)
    return output.strip()


def schedule_curl_callback(
        minute_count, base_url, value_by_key=None, headers=None, method='GET'):
    # Prepare more_lines
    full_url = base_url
    more_lines = []
    if value_by_key:
        if method == 'POST':
            headers['Content-Type'] = 'application/json'
            more_lines.append('-d \'%s\'' % json.dumps(value_by_key))
        else:
            full_url += urlencode(value_by_key)
    more_lines.extend(['-X %s' % method, full_url])
    # Prepare header_lines
    header_lines = []
    for k, v in (headers or {}).items():
        header_lines.append('-H "%s: %s"' % (k, v))
    # Schedule callback
    shell_parts = ['curl'] + header_lines + more_lines
    shell_text = ' '.join(shell_parts)
    return schedule_shell_callback(minute_count, shell_text)


def schedule_shell_callback(minute_count, shell_text):
    stdout, stderr = Popen([
        'at', 'now + %s minutes' % minute_count,
    ], stdin=PIPE, stdout=PIPE, stderr=PIPE).communicate(shell_text + '\n')
    job_id, when_string = re.search('job (\d+) at (.+)', stderr).groups()
    when = datetime.datetime.strptime(when_string, '%a %b %d %H:%M:%S %Y')
    return job_id, when
