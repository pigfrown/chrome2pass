#!/usr/bin/env python3

# Author: Pig Frown <pigfrown@protonmail.com>
# Copyright 2022 Pig Frown
# This file is licensed under the MIT License. See LICENSE in repository

import subprocess
import argparse
import sys
import csv


class ArgParser(argparse.ArgumentParser):
    def error(self, msg):
        print(msg, file=sys.stderr)
        self.print_help()
        sys.exit(1)


def confirmed(site, username=None):
    if username is None:
        prompt = f"Import {site} for no user password? (Y/n)"
    else:
        prompt = f"Import {site} for user {username}? (Y/n)"

    while True:
        user_input = input(prompt)

        # Default to yes
        if len(user_input) > 0:
            first_char = user_input.lower()[0]
        else:
            first_char = 'y'

        if first_char == 'y':
            return True
        elif first_char == 'n':
            return False

        print("Please enter y or n")


def import_password(site, user, password):
    path = f"{site}/{user}"
    pass_input = f"{password}\n".encode()

    cmd = ["pass", "insert", "-m", path]
    proc = subprocess.Popen(cmd,
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            )

    stdout, stderr = proc.communicate(pass_input)
    returned = proc.wait()

    if returned != 0:
        print(f"ERROR: could not import {site}.. pass returned {returned}")


def main():
    description = "Import pass entries from Chrome based browser export CSV"
    parser = ArgParser(description=description)

    parser.add_argument("csv_file", help="The exported Chrome CSV file")
    parser.add_argument("--confirm",
                        action="store_true",
                        help="Ask for confirmation before importing each password")

    args = parser.parse_args()

    for row in csv.DictReader(open(args.csv_file, 'r')):
        # CSV format is name,url,username,password.
        # don't care about url, just use name
        if args.confirm:
            if not confirmed(row["name"], row["username"]):
                continue

        import_password(row["name"], row["username"], row["password"])


if __name__ == "__main__":
    main()
