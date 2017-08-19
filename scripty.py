import  RPi.GPIO as GPIO
import time
import signal
import multiprocessing
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

MSG = "Welcome! You can use the script."
START_BUTTON = 18
STOP_BUTTON = 15
ON_LED = 14
FAN_1 = 20
FAN_2 = 21

GPIO.setup(START_BUTTON, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(STOP_BUTTON, GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(ON_LED,GPIO.OUT)
GPIO.setup(FAN_1,GPIO.OUT)
GPIO.setup(FAN_2,GPIO.OUT)

def handler(signum, frame):
    print('\tCtrl+Z pressed, but ignored.Press Ctrl+C to stop it')

def fans():
        print("Fans are ON!")
        time.sleep(0.3)
        GPIO.output(FAN_1,GPIO.HIGH)
        time.sleep(0.8)
        GPIO.output(FAN_2,GPIO.HIGH)


def blink():
        print("Led is ON!")
        while True:
                GPIO.output(ON_LED,GPIO.HIGH)
                time.sleep(1)
                GPIO.output(ON_LED,GPIO.LOW)
                time.sleep(1)

def terminate_process(led,fans):

        led.terminate()
        fans.terminate()
        GPIO.output(FAN_1,GPIO.LOW)
        GPIO.output(FAN_2,GPIO.LOW)
        GPIO.output(ON_LED,GPIO.LOW)
        print("Led is OFF!")
        print("Fans are OFF!")
def exit_gracefully(signum, frame):
        # restore the original signal handler as otherwise evil things will happen
        # in raw_input when CTRL+C is pressed, and our signal handler is not re-entrant
        signal.signal(signal.SIGINT, original_sigint)

        if v == 1:
                print("Stop the fans first!")
        else:
                signal.signal(signal.SIGINT, original_sigint)

                try:
                        if input("\nReally quit? (y/n)> ").lower().startswith('y'):
                                GPIO.output(FAN_1,GPIO.LOW)
                                GPIO.output(FAN_2,GPIO.LOW)
                                GPIO.output(ON_LED,GPIO.LOW)
                                sys.exit(1)
		 except KeyboardInterrupt:
                        print("\nOk ok, quitting")
                        GPIO.output(FAN_1,GPIO.LOW)
                        GPIO.output(FAN_2,GPIO.LOW)
                        GPIO.output(ON_LED,GPIO.LOW)
                        sys.exit(1)

                # restore the exit gracefully handler here
                signal.signal(signal.SIGINT, exit_gracefully)

def border_msg(msg):
        row = len(msg)
        h = ''.join(['\t\t\t\t\t'] + ['+'] + ['-' *row] + ['+'])
        result= h + '\n\t\t\t\t\t'"|"+msg+"|"'\n' + h
        print("\n")
        print(result)

def main():
        border_msg(MSG)
        led_value = 0  # Check if led is already on
        global v
        while True:
                inputValue = GPIO.input(START_BUTTON)
                inputValue2= GPIO.input(STOP_BUTTON)
                if (inputValue == False):
                        print("Button 1 pressed!")
                        if led_value == 1:
                                print("Led is alerady blinking")
                        elif led_value == 0:
                                led_process = multiprocessing.Process(target = blink)
                                fan_process = multiprocessing.Process(target = fans)
                                fan_process.start()
                                led_process.start()

                        led_value = 1

		elif (inputValue2 == False):
                        print("Button 2 pressed!")
                        if led_value == 1:
                                terminate_process(led_process,fan_process)
                                led_value = 0
                v = led_value
                time.sleep(0.3)

        GPIO.cleanup()

if __name__ == '__main__':
        # store the original SIGINT handler
        signal.signal(signal.SIGTSTP, handler)
        original_sigint = signal.getsignal(signal.SIGINT)
        signal.signal(signal.SIGINT, exit_gracefully)
        main()




