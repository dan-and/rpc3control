#!/usr/bin/env python
import pexpect
import unittest
import sys, os, time
import PexpectTestCase

class Exp_TimeoutTestCase(PexpectTestCase.PexpectTestCase):
    def test_matches_exp_timeout (self):
        """This tests that we can raise and catch TIMEOUT.
        """
        try:
            raise pexpect.TIMEOUT("TIMEOUT match test")
        except pexpect.TIMEOUT:
            pass
            #print "Correctly caught TIMEOUT when raising TIMEOUT."
        else:
            self.fail('TIMEOUT not caught by an except TIMEOUT clause.')

    def test_pattern_printout (self):
        """Verify that a TIMEOUT returns the proper patterns it is trying to match against.
        Make sure it is returning the pattern from the correct call."""
        try:
            p = pexpect.spawn('cat')
            p.sendline('Hello')
            p.expect('Hello')
            p.expect('Goodbye',timeout=5)
        except pexpect.TIMEOUT, expTimeoutInst:
            assert p.match_index == None
        else:
            self.fail("Did not generate a TIMEOUT exception.")

    def test_exp_timeout_notThrown (self):
        """Verify that a TIMEOUT is not thrown when we match what we expect."""
        try:
            p = pexpect.spawn('cat')
            p.sendline('Hello')
            p.expect('Hello')
        except pexpect.TIMEOUT:
            self.fail("TIMEOUT caught when it shouldn't be raised because we match the proper pattern.")
        
    def test_stacktraceMunging (self):
        """Verify that the stack trace returned with a TIMEOUT instance does not contain references to pexpect."""
        try:
            p = pexpect.spawn('cat')
            p.sendline('Hello')
            p.expect('Goodbye',timeout=5)
        except pexpect.TIMEOUT, e:
            if e.get_trace().count("pexpect.py") != 0:
                self.fail("The TIMEOUT get_trace() referenced pexpect.py. It should only reference the caller.\n"+e.get_trace())

    def test_correctStackTrace (self):
        """Verify that the stack trace returned with a TIMEOUT instance correctly handles function calls."""
        def nestedFunction (spawnInstance):
            spawnInstance.expect("junk", timeout=3)

        try:
            p = pexpect.spawn('cat')
            p.sendline('Hello')
            nestedFunction(p)
        except pexpect.TIMEOUT, e:
            if e.get_trace().count("nestedFunction") == 0:
                self.fail("The TIMEOUT get_trace() did not show the call to the nestedFunction function.\n" + str(e) + "\n" + e.get_trace())

if __name__ == '__main__':
    unittest.main()

suite = unittest.makeSuite(Exp_TimeoutTestCase,'test')
