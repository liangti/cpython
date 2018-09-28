"""
Provide test cases to test multiprocessing behaviors on different operating systems such as Solaris and AIX.
"""


import unittest
import time
import sys
import os
from test import support
import multiprocessing
from multiprocessing import Process
import multiprocessing.pool as pool

TIMEOUT1, TIMEOUT2, TIMEOUT3 = 0.1, 0.5, 1.0



def func(wait=0.0):
    time.sleep(wait)
    x = sum([x for x in range(100)])

def job_wrapper(pool):
    jobs = []
    for i in range(100):
        jobs.append(pool.apply_async(func))

    for job in jobs:
        try:
            job.wait(timeout=TIMEOUT3)
        except :
            print("Aborting due to timeout")
            pool.terminate()
            raise

# Practice class, should delete before submit
class TestProcess(unittest.TestCase):
    def test_start(self):
        name = "BasicProcess"
        p = Process(target=func,  name=name)
        self.assertFalse(p.is_alive())
        p.start()
        self.assertTrue(p.is_alive())
        time.sleep(TIMEOUT1)
        self.assertFalse(p.is_alive())
        self.assertEqual(p.exitcode, 0)

# Test pool hang issue
# Try to reproduce the issues on Solaris/AIX machine
class TestPoolTimeout(unittest.TestCase):
    def test_thread_pool_initialize(self):
        pool = multiprocessing.pool.ThreadPool(processes=multiprocessing.cpu_count()-1)
        job_wrapper(pool)
        for p in pool._pool:
            self.assertFalse(p.is_alive())
            self.assertEqual(p.exitcode, 0)
