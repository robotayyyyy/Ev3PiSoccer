import serial,time,os, inspect

current_dir = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ) )[0]))
os.chdir(current_dir)
import EV3BT

#EV3 = serial.Serial('/dev/rfcomm0')



try:
    ev3 = serial.Serial('COM6')
except Exception as e:
    print(str(e))



s = EV3BT.encodeMessage(EV3BT.MessageType.Text, 'abc', 'Eat responsibly')
print(EV3BT.printMessage(s))
ev3.write(s)



while True:
    try:
        message = input("Enter a message: ")
        if message=='exit':
            break
        #print(message)
        #ev3.write(bytes([1,2,3,4,5,6]))
        time.sleep(0.1)
    except Exception as e:
        print(str(e))

ev3.close()