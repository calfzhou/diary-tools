# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import subprocess


def git(command, *args, **kwargs):
    ignore_error = kwargs.pop('ignore_error', False)
    is_preview = kwargs.pop('is_preview', False)

    cmd = ['git', command]

    for key, value in kwargs.iteritems():
        if len(key) == 1:
            cmd.append('-{}'.format(key))
        else:
            cmd.append('--{}'.format(key))
        cmd.append(value)

    cmd.extend(args)

    print(' '.join(cmd))
    if is_preview:
        return 0
    else:
        return_code = subprocess.call(cmd)
        if return_code != 0 and not ignore_error:
            raise Exception('git command {} failed with error code {}'.format(command, return_code))
        return return_code


class DateFormatter(object):
    @staticmethod
    def format_year(year):
        """
        :type year: int
        """
        return '{}'.format(year)

    @classmethod
    def format_year_branch(cls, year):
        """
        :type year: int
        """
        return cls.format_year(year)

    @staticmethod
    def format_month(month):
        """
        :type month: int
        """
        return '{:02d}'.format(month)

    @classmethod
    def format_month_branch(cls, year, month):
        """
        :type year: int
        :type month: int
        """
        return '{}-{}'.format(cls.format_year(year), cls.format_month(month))

    @staticmethod
    def format_day(day):
        """
        :type day: int
        """
        return '{:02d}'.format(day)

