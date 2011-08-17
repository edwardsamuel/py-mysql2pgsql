from __future__ import absolute_import

import os
import sys
from functools import wraps

from .mysql_reader import MysqlReader

from termcolor import colored, cprint


def print_row_progress(val):
    if os.name == 'posix':
        cprint('  %s' % val, 'cyan', end=' ')
    else:
        print('  %s' % val),
    sys.stdout.flush()


def print_start_table(val):
    if os.name == 'posix':
        cprint(val, 'magenta')
    else:
        print(val)


def print_table_actions(val):
    if os.name == 'posix':
        cprint('  %s' % val, 'green')
    else:
        print('  %s' % val)


def find_first(items, func):
    return next((item for item in items if func(item)), None)


def print_red(val):
    if os.name == 'posix':
        cprint(val, 'red')
    else:
        print(val)


def status_logger(f):
    start_template = 'START  - %s'
    finish_template = 'FINISH - %s'
    truncate_template = 'TRUNCATING TABLE %s'
    create_template = 'CREATING TABLE %s'
    constraints_template = 'ADDING CONSTRAINTS ON %s'
    write_contents_template = 'WRITING DATA TO %s'
    index_template = 'ADDING INDEXES TO %s'
    statuses = {
        'truncate': {
            'start': start_template % truncate_template,
            'finish': finish_template % truncate_template
            },
        'write_table': {
            'start': start_template % create_template,
            'finish': finish_template % create_template,
            },
        'write_constraints': {
            'start': start_template % constraints_template,
            'finish': finish_template % constraints_template,
            },
        'write_contents': {
            'start': start_template % write_contents_template,
            'finish': finish_template % write_contents_template,
            },
        'write_indexes': {
            'start': start_template % index_template,
            'finish': finish_template % index_template,
            },
    }

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if getattr(args[0], 'verbose', False):
            if 'table' in kwargs:
                table = kwargs['table']
            else:
                table = find_first(list(args) + kwargs.values(), lambda c: c.__class__ is MysqlReader.Table)
            assert table
            print_table_actions(statuses[f.func_name]['start'] % table.name)
            ret = f(*args, **kwargs)
            print_table_actions(statuses[f.func_name]['finish'] % table.name)
            return ret
        else:
            return f(*args, **kwargs)
    return decorated_function
