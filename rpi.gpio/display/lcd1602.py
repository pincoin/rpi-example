#!/usr/bin/env python
#-*- coding: utf-8 -*-

# 문자 LCD 모듈과 라즈베리 파이 결선
# 1 : GND
# 2 : 5V
# 3 : 명암 (0-5V) - 0~20Kohm 가변저항 연결
# 4 : RS (Register Select) - GPIO7
# 5 : R/W (Read Write) - GND
# 6 : E (Enable) - GPIO8
# 7 : DB0 (Data Bit 0) - 연결안함
# 8 : DB1 (Data Bit 1) - 연결안함
# 9 : DB2 (Data Bit 2) - 연결안함
# 10: DB3 (Data Bit 3) - 연결안함
# 11: DB4 (Data Bit 4) - GPIO25
# 12: DB5 (Data Bit 5) - GPIO24
# 13: DB6 (Data Bit 6) - GPIO23
# 14: DB7 (Data Bit 7) - GPIO18
# 15: LCD 백라이트 +5V - 220ohm 저항 연결
# 16: LCD 백라이트 GND

import RPi.GPIO as GPIO
import time

class Pincoin_CharLCD(object):
    # Define some device constants
    LCD_WIDTH=16 # 한 줄에 최대문자수
    LCD_CHR=True
    LCD_CMD=False

    LCD_LINE_1=0x80 # 첫 번째 줄 LCD RAM 주소
    LCD_LINE_2=0xC0 # 두 번째 줄 LCD RAM 주소

    # 타이밍 상수
    E_PULSE=0.0005 # 지연 시간
    E_DELAY=0.0005 # E핀 펄스 유지 시간

    # 명령어
    CMD_CLEARDISPLAY=0x01
    CMD_RETURNHOME=0x02
    CMD_ENTRYMODESET=0x04
    CMD_DISPLAYCONTROL=0x08
    CMD_CURSORSHIFT=0x10
    CMD_FUNCTIONSET=0x20
    CMD_SETCGRAMADDR=0x40
    CMD_SETDDRAMADDR=0x80

    # ENTRYMODESET 플래그
    FLAG_ENTRYRIGHT=0x00
    FLAG_ENTRYLEFT=0x02
    FLAG_ENTRYSHIFTINCREMENT=0x01
    FLAG_ENTRYSHIFTDECREMENT=0x00

    # DISPLAYCONTROL 플래그
    FLAG_DISPLAYON=0x04
    FLAG_DISPLAYOFF=0x00
    FLAG_CURSORON=0x02
    FLAG_CURSOROFF=0x00
    FLAG_BLINKON=0x01
    FLAG_BLINKOFF=0x00

    # CURSORSHIFT 플래그
    FLAG_DISPLAYMOVE=0x08
    FLAG_CURSORMOVE=0x00
    FLAG_MOVERIGHT=0x04
    FLAG_MOVELEFT=0x00

    # FUNCTIONSET 플래그
    FLAG_8BITMODE=0x10
    FLAG_4BITMODE=0x00
    FLAG_2LINE=0x08
    FLAG_1LINE=0x00
    FLAG_5x10DOTS=0x04
    FLAG_5x8DOTS=0x00

    def __init__(self, pin_rs=7, pin_e=8, pins_db=[25, 24, 23, 18]):
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin_e, GPIO.OUT)  # E
        GPIO.setup(self.pin_rs, GPIO.OUT) # RS
        for pin in self.pins_db: # Data Bits
            GPIO.setup(pin, GPIO.OUT)

        # 4비트 모드로 변환
        # 연결되지 않은 하위4비트는 무시되어
        # 0x30 0x30 0x30 0x20 4바이트 전송으로 인식
        self.write_byte(0x33, self.LCD_CMD)
        self.write_byte(0x32, self.LCD_CMD)

    def begin(self):
        # 2줄 5x8크기
        self.write_byte(self.CMD_FUNCTIONSET | self.FLAG_2LINE | self.FLAG_5x8DOTS, self.LCD_CMD)
        # 화면 on, 커서 off, 커서 깜빡임 off
        self.write_byte(self.CMD_DISPLAYCONTROL | self.FLAG_DISPLAYON, self.LCD_CMD)
        # 화면 지우기
        self.write_byte(self.CMD_CLEARDISPLAY, self.LCD_CMD)
        # 출력 후 커서를 오른쪽으로 옮김 (DDRAM의 주소 증가, 화면이동은 없음)
        self.write_byte(self.CMD_ENTRYMODESET | self.FLAG_ENTRYLEFT, self.LCD_CMD)
        time.sleep(self.E_DELAY)

    def write(self):
        print('쓰기')

    def write_byte(self, bits, mode):
        # 4비트 2회로 바이트 쓰기
        # bits = data
        # mode = True(데이터) / False(명령어)

        GPIO.output(self.pin_rs, mode) # RS

        # 상위비트 전송
        for pin in self.pins_db: # Data Bits
            GPIO.output(pin, False)

        GPIO.output(self.pins_db[0], bool(bits&0x10))
        GPIO.output(self.pins_db[1], bool(bits&0x20))
        GPIO.output(self.pins_db[2], bool(bits&0x40))
        GPIO.output(self.pins_db[3], bool(bits&0x80))

        # E핀 펄스
        self.pulse_enable()

        # 하위비트 전송
        for pin in self.pins_db: # Data Bits
            GPIO.output(pin, False)

        GPIO.output(self.pins_db[0], bool(bits&0x01))
        GPIO.output(self.pins_db[1], bool(bits&0x02))
        GPIO.output(self.pins_db[2], bool(bits&0x04))
        GPIO.output(self.pins_db[3], bool(bits&0x08))

        # E핀 펄스
        self.pulse_enable()

    def pulse_enable(self):
        # E핀 펄스 = 토글
        time.sleep(self.E_DELAY)
        GPIO.output(self.pin_e, True)
        time.sleep(self.E_PULSE)
        GPIO.output(self.pin_e, False)
        time.sleep(self.E_DELAY)

    def message(self, message, line):
        # 출력 라인 선택
        self.write_byte(line, self.LCD_CMD)

        message = message.ljust(self.LCD_WIDTH, " ")

        for i in range(self.LCD_WIDTH):
            self.write_byte(ord(message[i]), self.LCD_CHR)

    def home(self):
        self.write_byte(self.CMD_RETURNHOME, self.LCD_CMD)
        time.sleep(self.E_DELAY)

    def clear(self):
        self.write_byte(self.CMD_CLEARDISPLAY, self.LCD_CMD)
        time.sleep(self.E_DELAY)

if __name__ == '__main__':
    try:
        lcd = Pincoin_CharLCD()
        lcd.begin()

        while True:
            lcd.message("PINCOIN.INFO", lcd.LCD_LINE_1)
            lcd.message("16x2 LCD Test", lcd.LCD_LINE_2)
            time.sleep(2)

            lcd.clear()
            time.sleep(1)

            lcd.message("1234567890123456", lcd.LCD_LINE_1)
            lcd.message("abcdefghijklmnop", lcd.LCD_LINE_2)
            time.sleep(2)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()
