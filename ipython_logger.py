# coding: utf-8
import IPython
from pathlib import Path
import re
ih_len = 20 # ipython history max length
# log_filepath = Path('/data/DSST/scripts/ipython.log')
log_filepath = Path.cwd().joinpath('test.log')
if not log_filepath.exists():
    log_filepath.write_text('# IPython log\n')

# --------------------------
def tail(filepath, count=1, offset=1024):
    """
    A more efficent way of getting the last few lines of a file.
    The function is taken (with some edits) from :http://drewfradette.ca
    /python-native-head- and-tail-functions
    """
    f_size = filepath.stat().st_size
    if f_size == 0 or count ==0:
        return []
    with filepath.open('r') as f:
        if f_size <= offset:
            offset = int(f_size / 2)
        while True:
            seek_to = min(f_size - offset, 0)
            f.seek(seek_to)
            lines = f.readlines()
            # Empty file
            if seek_to <= 0 and len(lines) == 0:
                return []
                # count is larger than or equal to lines in file
            if seek_to == 0 and len(lines) <= count:
                return lines
                # Standard case
            return lines[count * -1:]


def get_log(fname = None):
    """
    Read commands from my local ipython logfile into a dictionary
    Because of multiline commands the count just refers to number
    of lines and not commands
    """
    count = 100
    current_log_tail = ''.join(tail(fname, count))
    return current_log_tail


def get_cmd_str(tup):
    return str(tup[0]) + ' ' + str(tup[1]) + ' ' + tup[2] + '\n\n'
# --------------------------


# get the current tail of the log file and the ipython history accessor
hist_accessor = IPython.core.history.HistoryAccessor()
log_hist = get_log(log_filepath)

# write any additions if they exist
with log_filepath.open('a') as f:
    [f.write(get_cmd_str(tup)) \
    for tup in hist_accessor.get_tail(ih_len) \
    if ('\n'+str(tup[0])+ ' '+str(tup[1])) not in log_hist]
