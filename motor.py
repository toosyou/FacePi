import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

MOTOR_PIN1 = 11
MOTOR_PIN2 = 12

GPIO.setup(MOTOR_PIN1, GPIO.OUT)
GPIO.setup(MOTOR_PIN2, GPIO.OUT)

def move():
    GPIO.setup(MOTOR_PIN1, GPIO.IN)
    GPIO.output(MOTOR_PIN2, GPIO.HIGH)
    time.sleep(5)
    GPIO.output(MOTOR_PIN1, GPIO.HIGH)
    GPIO.output(MOTOR_PIN2, GPIO.LOW)
    GPIO.setup(MOTOR_PIN1, GPIO.IN)
    GPIO.setup(MOTOR_PIN2, GPIO.IN)


move()

