#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import argparse
import glob
from os import path
import os
import sys
import subprocess
import operator
import time


def git(command, *args, **kwargs):
    ignore_error = kwargs.pop('ignore_error', False)

    cmd = ['git', command]

    for key, value in kwargs.iteritems():
        if len(key) == 1:
            cmd.append('-{}'.format(key))
        else:
            cmd.append('--{}'.format(key))
        cmd.append(value)

    cmd.extend(args)

    print(' '.join(cmd))
    return_code = 0
    return_code = subprocess.call(cmd)
    if return_code != 0 and not ignore_error:
        raise Exception('git command {} failed with error code {}'.format(command, return_code))
    return return_code


def _get_year_text(year):
    """
    :type year: int
    """
    return '{}'.format(year)


def _get_month_text(month):
    """
    :type month: int
    """
    return '{:02d}'.format(month)


def _get_day_text(day):
    """
    :type day: int
    """
    return '{:02d}'.format(day)


def _get_all_months(forgetting_root_path, year_folder_name):
    """
    :type forgetting_root_path: string
    :type year_folder_name: string
    """
    all_months_names = map(path.basename, glob.glob(path.join(forgetting_root_path, year_folder_name, '??')))
    return map(int, sorted(all_months_names))


def _get_month_days_with_date(forgetting_root_path, month_folder_name):
    """
    :type forgetting_root_path: string
    :type month_folder_name: string
    """
    all_days_paths = glob.glob(path.join(forgetting_root_path, month_folder_name, '??.dia'))
    days_with_date = [
        (int(path.splitext(path.basename(p))[0]), path.getmtime(p))
        for p in all_days_paths
    ]
    return sorted(days_with_date, key=operator.itemgetter(1))


def _get_year_days_with_date(forgetting_root_path, year_folder_name):
    """
    :type forgetting_root_path: string
    :type year_folder_name: string
    :rtype: list[(int, int, int)]
    """
    all_months = _get_all_months(forgetting_root_path, year_folder_name)

    days_with_date = []
    for month in all_months:
        month_text = _get_month_text(month)
        month_folder_name = path.join(year_folder_name, month_text)
        month_days = _get_month_days_with_date(forgetting_root_path, month_folder_name)
        days_with_date.extend([(month, day, modify_date) for day, modify_date in month_days])

    return sorted(days_with_date, key=operator.itemgetter(2))


def convert_day_file(from_path, to_path):
    """
    :type from_path: string
    :type to_path: string
    """
    with open(from_path) as from_file:
        with open(to_path, 'w') as to_file:
            for line in from_file:
                line = line.decode('gbk')
                line = line.rstrip('\r\n')
                to_file.write(line.encode('utf-8'))
                to_file.write('\n')


def remember_something(forgetting_root_path, year, month):
    """
    :type forgetting_root_path: string
    :type year: int
    :type month: int
    """
    year_text = _get_year_text(year)
    year_folder_name = year_text
    month_text = _get_month_text(month)
    master_branch = 'master'
    # year_branch = year_text
    month_branch = '{}-{}'.format(year_text, month_text)
    month_folder_name = path.join(year_folder_name, month_text)
    format_date = lambda t: time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(t))

    month_days_with_date = _get_month_days_with_date(forgetting_root_path, month_folder_name)
    if not month_days_with_date:
        print('there is nothing in {}/{}'.format(forgetting_root_path, month_folder_name))
        return

    print('remembering', month_folder_name, '...')
    git('checkout', master_branch)
    git('checkout', b=month_branch)

    if not path.exists(month_folder_name):
        os.makedirs(month_folder_name)

    for day, modify_date in month_days_with_date:
        day_text = _get_day_text(day)
        day_file_name = '{}.dia'.format(day_text)
        day_file_path = path.join(month_folder_name, day_file_name)
        forgetting_day_file_path = path.join(forgetting_root_path, month_folder_name, day_file_name)
        convert_day_file(forgetting_day_file_path, day_file_path)

        git('add', day_file_path)
        git('commit', m='add diary {}.{}.{}'.format(year_text, month_text, day_text), date=format_date(modify_date))

    git('checkout', master_branch)
    # git('checkout', b=year_branch, ignore_error=True)
    # git('checkout', year_branch)
    # git('merge', '--no-commit', month_branch)
    # merge_time = month_days_with_date[-1][1] + 60  # add one minute delay
    # git('commit', m="Merge branch '{}'".format(month_branch), date=format_date(merge_time),
    #     ignore_error=True)
    # git('checkout', master_branch)
    # git('branch', '-D', month_branch)

    print('done!\n')


def main():
    parser = argparse.ArgumentParser(usage='remembering something - run in git repository root')
    parser.add_argument('forgetting_root', help='the root directory path for what you are going to forget')
    parser.add_argument('year', type=int, help='which year you want to remember')
    parser.add_argument('month', type=int, nargs='?',
                        help='which month do you want to remember, default to the whole year')

    unicode_args = map(lambda s: unicode(s, sys.getfilesystemencoding()), sys.argv)
    args = parser.parse_args(unicode_args[1:])

    forgetting_root_path = args.forgetting_root
    """:type: string"""
    year = args.year
    """:type: int"""
    month = args.month
    """:type: None|int"""

    if month is None:
        year_folder_name = _get_year_text(year)
        for month_in_place in _get_all_months(forgetting_root_path, year_folder_name):
            remember_something(forgetting_root_path, year, month_in_place)
    else:
        remember_something(forgetting_root_path, year, month)


if __name__ == '__main__':
    main()
