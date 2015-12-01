#!/usr/bin/env python
#-*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import sys

# 입력 파라미터로 GPIO 핀 번호 읽음
led_pin = (14, 15, 18, 23, 24, 25, 8, 7)

def turn_on(pin):
    GPIO.output(pin, GPIO.HIGH)
    if GPIO.input(pin):
        print('LED %2d 켜짐' % pin)

def turn_off(pin):
    GPIO.output(pin, GPIO.LOW)
    if not GPIO.input(pin):
        print('LED %2d 꺼짐' % pin)

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    for pin in led_pin:
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

        print('LED %2d 핀' % pin)

    while True:
        for pin in led_pin:
            turn_on(pin)
            time.sleep(0.2)

        for pin in led_pin:
            turn_off(pin)
            time.sleep(0.2)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception, e:
        print str(e)
    finally:
        GPIO.cleanup()
