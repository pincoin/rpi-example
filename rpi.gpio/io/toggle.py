#!/usr/bin/env python
#-*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

led=14
pullup=15
blink=False


def toggle(pin):
    global blink

    if blink:
        GPIO.output(pin, GPIO.LOW)
        blink=False
        print('LED 끄기') 
    else:
        GPIO.output(pin, GPIO.HIGH)
        blink=True
        print('LED 켜기') 

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(pullup, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    while True:
        if GPIO.input(pullup) == GPIO.LOW:
            toggle(led)

        time.sleep(0.1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception, e:
        print str(e)
    finally:
        GPIO.cleanup()
