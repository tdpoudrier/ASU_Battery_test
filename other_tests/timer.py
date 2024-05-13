"""
Learning how to use timer
"""

from threading import Timer

#define function called by timer
def hello():
    print("Hello, world")

#define timer interval and callback function
t = Timer(3.0, hello)

#start timer
t.start()
print("Timer started")