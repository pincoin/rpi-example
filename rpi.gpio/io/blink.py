#!/usr/bin/env python
#-*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

led=14

def blink(pin):
    GPIO.output(pin, GPIO.HIGH)
    if GPIO.input(pin):
        print('LED 켜짐') 
        time.sleep(1);

    GPIO.output(pin, GPIO.LOW)
    if not GPIO.input(pin):
        print('LED 꺼짐') 
        time.sleep(1);

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)

    for i in range(0, 5):
        blink(led)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception, e:
        print str(e)
    finally:
        GPIO.cleanup()
