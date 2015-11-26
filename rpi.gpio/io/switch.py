#!/usr/bin/env python
#-*- coding: utf-8 -*-

import RPi.GPIO as GPIO
import time

pullup_pin=15
pulldown_pin=18

def main():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pullup_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(pulldown_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    while True:
        # 버튼이 눌렸을 때 처리사항이 길어지면
        # 다른 버튼을 눌러도 무응답
        if GPIO.input(pullup_pin) == GPIO.LOW:
            print('내부풀업저항 연결 스위치 눌림')

        if GPIO.input(pulldown_pin) == GPIO.HIGH:
            print('내부풀다운저항 연결 스위치 눌림')

        # sleep 시간이 너무 길면 버튼을 눌러도 무응답
        # sleep 시간이 너무 짧으면 불필요하게 비효율적인 입력 검사
        # 이 값이 일종의 bounce 시간 지정 효과
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
