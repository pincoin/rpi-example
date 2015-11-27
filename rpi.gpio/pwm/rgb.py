#!/usr/bin/env python
#-*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time
import random

red_pin=18
green_pin=15
blue_pin=14

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(red_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(green_pin, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(blue_pin, GPIO.OUT, initial=GPIO.LOW)

    pwm_red_led = GPIO.PWM(red_pin, 500)
    pwm_red_led.start(0)

    pwm_green_led = GPIO.PWM(green_pin, 500)
    pwm_green_led.start(0)

    pwm_blue_led = GPIO.PWM(blue_pin, 500)
    pwm_blue_led.start(0)

    while True:
        red_duty = random.randint(0, 10) * 10
        green_duty = random.randint(0, 10) * 10
        blue_duty = random.randint(0, 10) * 10

        pwm_red_led.ChangeDutyCycle(red_duty)
        pwm_green_led.ChangeDutyCycle(green_duty)
        pwm_blue_led.ChangeDutyCycle(blue_duty)

        print('R: %3d / G: %3d / B: %3d' % (red_duty, green_duty, blue_duty))
        time.sleep(0.5)
        
if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception, e:
        print str(e)
    finally:
        GPIO.cleanup()
