# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from datetime import datetime
import threading
def factorial(number):
    fact = 1
    for n in range(1, number+1):
        fact *= n
    return fact
number = 100000
thread1 = threading.Thread(target=factorial, args=(number,))
thread2 = threading.Thread(target=factorial, args=(number,))
startTime = datetime.now()
thread1.start()
thread2.start()
thread1.join()
thread2.join()
endTime = datetime.now()
print "Time for execution: ", endTime - startTime