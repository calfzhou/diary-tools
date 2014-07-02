#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import argparse
import sys
from diary.utils import DateFormatter, git


def finalize_year(year, auto_push=False, first_month=1, last_month=12):
    """
    :type year: int
    :type auto_push: bool
    :type first_month: int
    :type last_month: int
    """
    git('checkout', DateFormatter.format_month_branch(year, first_month))
    for month in xrange(first_month + 1, last_month + 1):
        git('checkout', DateFormatter.format_month_branch(year, month))
        git('rebase', DateFormatter.format_month_branch(year, month - 1))

    git('checkout', '-b', DateFormatter.format_year_branch(year))

    for month in xrange(first_month, last_month + 1):
        git('branch', '-D', DateFormatter.format_month_branch(year, month))

    need_push = auto_push or (raw_input('Do you want to push changes to remote repo? [y|N]') == 'y')
    is_preview = not need_push
    if is_preview:
        print('You can run the following commands later to push changes to remote repo')

    for month in xrange(first_month, last_month + 1):
        git('push', 'origin', '--delete', DateFormatter.format_month_branch(year, month), is_preview=is_preview)

    git('push', is_preview=is_preview)


def main():
    parser = argparse.ArgumentParser(description="Finalizes one year's whole diary - run in git repository root")
    parser.add_argument('year', type=int, help='which year to finalize')
    parser.add_argument('--push', action='store_true',
                        help='automatically push changes to remote repo')
    parser.add_argument('--first-month', type=int, default=1,
                        help='the first month to finalize (default is Jan)')
    parser.add_argument('--last-month', type=int, default=12,
                        help='the last month to finalize (default is Dec)')

    unicode_args = map(lambda s: unicode(s, sys.getfilesystemencoding()), sys.argv)
    args = parser.parse_args(unicode_args[1:])

    finalize_year(args.year, args.push, args.first_month, args.last_month)


if __name__ == '__main__':
    main()
