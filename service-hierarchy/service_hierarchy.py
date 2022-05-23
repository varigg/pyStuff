"""magpie.magpie: provides entry point main()."""


__version__ = "0.1.0"

import argparse
import logging
import sys

LOGGER = logging.getLogger(__name__)
# Takes a csv file of the following format:
# 
# division, group, team, service_name
# windows, networking, ui, networking-ui-service
# windows, files, search, search-service
# office,....
#
# Output it as a tree, eg
#
# windows
#.   networking
#          ui
#             networking-ui-service
#   files
# office

groups = {}
teams = {}
services = {}

def read_file(path_to_file):
    with open(path_to_file) as f:
        line=f.readline()
        line_number=1
        while line!='':
            service_def=line.split(',')
            if len(service_def) != 4:
                raise Exception(f"data format error on line {line_number}")
            division, group, team, service_name=service_def[0], service_def[1], service_def[2], service_def[3]
            if division in groups:
                groups[division].add(group)
            else:
                groups[division]=set([group])
            if group in teams:
                teams[group].add(team)
            else:
                teams[group]=set([team])
            if team in services:
                services[team].add(service_name)
            else:
                services[team]=set([service_name])
            line=f.readline()
            line_number+=1

def print_tree():
    for division in groups:
        print(division)
        for group in groups[division]:
            print("\t"+group)
            for team in teams[group]:
                print("\t\t"+team)
                for service in services[team]:
                    print("\t\t\t"+service)
 

def main():
    parser = argparse.ArgumentParser(
        description='A tool for building a service hierarchy from a csv file')

    parser.add_argument('-s',  '--source', type=str,
                        help="path to the source file")

    parser.add_argument(
        '-v', '--verbose',
        help="Be verbose",
        action="store_const", dest="loglevel", const=logging.INFO,
        default=logging.WARNING,
    )
    parser.add_argument(
        '-q', '--quiet',
        help="Only print critical errors",
        action="store_const", dest="loglevel", const=logging.ERROR,
    )
    parser.add_argument(
        '-x', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
    )
    args = parser.parse_args()
    logging.basicConfig(level=args.loglevel)
    if args.source is None:
        parser.print_help()
        exit(1)
    read_file(args.source)
    print_tree()

if __name__ == '__main__':
    main()