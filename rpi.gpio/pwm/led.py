#!/usr/bin/env python
#-*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

led=14

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led, GPIO.OUT, initial=GPIO.LOW)

    pwm_led = GPIO.PWM(led, 500)
    pwm_led.start(100)

    while True:
        # 0, 20, 40, 60, 80 (100 출력 안 함)
        for duty in range(0, 100, 20):
            pwm_led.ChangeDutyCycle(duty)
            time.sleep(0.2)
        # 100, 80, 60, 40, 20 (0 출력 안 함)
        for duty in range(100, 0, -20):
            pwm_led.ChangeDutyCycle(duty)
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
