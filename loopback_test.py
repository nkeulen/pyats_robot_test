#!/usr/bin/env python3

'''

setup:
    - connect to testbed devices
test:
    - configure provided loopback interface + ip
    - learn the interfaces and check if ip and loopback were configured
cleanup: 
    - remove created loopbacks

How to run (as standalone): ./loopback_test.py --testbed yaml/testbed.yml --loopback Loopback100 --loopback_ip "10.10.10.10/32"

'''

import logging
import genie.testbed
from pyats import aetest


logger = logging.getLogger(__name__)


class CommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def load_testbed(self, testbed):
        # Convert pyATS testbed to Genie Testbed
        logger.info("Converting pyATS testbed to Genie Testbed")
        testbed = genie.testbed.load(testbed)
        self.parent.parameters.update(testbed=testbed)

    @aetest.subsection
    def connect(self, testbed):
        ''' connect to all devices'''
        logger.info('connecting to devices in testbed')
        testbed.connect()


class CreateLoopbackTest(aetest.Testcase):

    @aetest.test
    def configure_loopback(self, testbed, loopback='Loopback100', loopback_ip='10.20.30.40/32'):
        logger.info('testbed = %s' % testbed)
        logger.info('loopback =  %s' % loopback)
        logger.info('loopback_ip =  %s' % loopback_ip)
        for host in testbed.devices:
            if testbed.devices[host].type == 'iosxr':
                testbed.devices[host].configure(f"interface {loopback}\n ipv4 address {loopback_ip}\n")

    @aetest.test
    def check_loopback(self, testbed, loopback='Loopback100', loopback_ip='10.20.30.40/32'):
        for host in testbed.devices:
            if testbed.devices[host].type == 'iosxr':
                try:
                    interfaces = testbed.devices[host].learn('interface')
                except Exception as e:                    
                    logging.error(f"Failed to learn interfaces on {host} ({e})")
                if loopback_ip not in interfaces.info[loopback]['ipv4'].keys():
                    self.failed(f'Loopback interface {loopback} with ip {loopback_ip} not found on {host}')

class FailingTest(aetest.Testcase):

    @aetest.test
    def fail(self, testbed):
        for host in testbed.devices:
            if testbed.devices[host].type == 'iosxr':
                testbed.devices[host].configure(f"interface thisinterfacedoesnotexist0/0/0\n ipv4 address 999.999.999.999/32\n")


class CommonCleanup(aetest.CommonCleanup):

    @aetest.subsection
    def clean_up_created_loopbacks(self, testbed, loopback='Loopback100'):
        for host in testbed.devices:
            if testbed.devices[host].type == 'iosxr':
                testbed.devices[host].configure(f"no interface {loopback}")

# main()
if __name__ == '__main__':

    # set logger level
    logger.setLevel(logging.INFO)

    # local imports
    import sys
    import argparse
    from pyats.topology import loader

    parser = argparse.ArgumentParser(description = "standalone parser")
    parser.add_argument('--testbed', dest = 'testbed')
    parser.add_argument('--loopback', dest = 'loopback')
    parser.add_argument('--loopback_ip', dest = 'loopback_ip')

    # parse args
    args, sys.argv[1:] = parser.parse_known_args(sys.argv[1:])

    # post-parsing processing
    testbed = loader.load(args.testbed)
    loopback = args.loopback.strip()
    loopback_ip = args.loopback_ip.strip()


    # and pass all arguments to aetest.main() as kwargs
    aetest.main(testbed=testbed, loopback=loopback, loopback_ip=loopback_ip)
