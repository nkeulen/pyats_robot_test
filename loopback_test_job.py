#!/usr/bin/env python3

# Easypy example.
# How to run from commandline: pyats run job loopback_test_job.py

from pyats.easypy import run

def main():
    run('loopback_test.py', testbed='yaml/testbed.yml', loopback='Loopback100', loopback_ip='10.20.30.40/32')

