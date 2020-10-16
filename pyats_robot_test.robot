*** Settings ***
# Robotframework libraries:
#Library		Collections

# pyATS library:
Library		ats.robot.pyATSRobot

# Python files containing pyATS tests:
Library		loopback_test.py   


*** Variables ***
${testbed}      yaml/testbed.yml


*** Test Cases ***
Initialize
    use testbed "${testbed}"

Common Setup
    run testcase "loopback_test.CommonSetup"

Run create loopback test
    run testcase "loopback_test.CreateLoopbackTest"

Run test that will fail
    run testcase "loopback_test.FailingTest"    

Common Cleanup
    run testcase "loopback_test.CommonCleanup"

