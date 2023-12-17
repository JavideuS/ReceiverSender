from ustruct import pack,unpack,unpack_from,pack_into
from micropython import const
from microbit import pin8,pin13,pin14,i2c,sleep
LEFT=0
RIGHT=1
BOTH=2
FORWARD=1
BACKWARD=-1
motor_power_left=50
motor_power_right=50
neopixelstrip=None
LINE_SENSOR=5
LIGHT_SENSOR=6
_BUFFER=bytearray(10)
_GIGGLEBOT_ADDRESS=const(0x04)
_DS=None
_THP=None
_LCS=None
def init():
 from neopixel import NeoPixel
 global neopixelstrip
 neopixelstrip=NeoPixel(pin8,9)
 pixels_off()
 set_eye_color_on_start()
 stop()
 return neopixelstrip
def set_smile(R=25,G=0,B=0):
 for i in b'\x02\x03\x04\x05\x06\x07\x08':
  neopixelstrip[i]=(R,G,B)
 neopixelstrip.show()
def set_eyes(which=BOTH,R=0,G=0,B=10):
 if which!=LEFT:neopixelstrip[0]=(R,G,B)
 if which!=RIGHT:neopixelstrip[1]=(R,G,B)
 neopixelstrip.show()
def set_eye_color_on_start():
 i2c.write(0x04,b'\x04')
 if unpack('>H',i2c.read(0x04,2))[0]<3400:
  neopixelstrip[0]=(10,0,0)
  neopixelstrip[1]=(10,0,0)
 else:
  neopixelstrip[0]=(0,0,10)
  neopixelstrip[1]=(0,0,10)
 neopixelstrip.show()
def pixels_off():
 for i in b'\x00\x01\x02\x03\x04\x05\x06\x07\x08':
  neopixelstrip[i]=(0,0,0)
 neopixelstrip.show()
def drive(dir=FORWARD,milliseconds=-1):
 i2c.write(0x04,b'\x0a'+pack('BB',int(motor_power_left*dir)&0xFF,int(motor_power_right*dir)&0xFF))
 if milliseconds>=0:
  sleep(milliseconds)
  stop()
def turn(dir=LEFT,milliseconds=-1):
 if dir==LEFT:
  i2c.write(0x04,b'\x0a'+pack('BB',int(motor_power_left)&0xFF,0))
 if dir==RIGHT:
  i2c.write(0x04,b'\x0a'+pack('BB',0,int(motor_power_right)&0xFF))
 if milliseconds>=0:
  sleep(milliseconds)
  stop()
def stop():
 i2c.write(0x04,b'\x0a'+b'\x00\x00')
def set_speed(power_left,power_right):
 global motor_power_left,motor_power_right
 motor_power_left=power_left
 motor_power_right=power_right
def set_servo(which=LEFT,degrees=90):
 us=min(2400,max(600,600+(1800*degrees//180)))
 duty=round(us*1024*50//1000000)
 if which==LEFT or which==BOTH:
  pin14.set_analog_period(20)
  pin14.write_analog(duty)
 if which==RIGHT or which==BOTH:
  pin13.set_analog_period(20)
  pin13.write_analog(duty)
def servo_off(which):
 if which==LEFT or which==BOTH:
  pin14.write_digital(0)
 if which==RIGHT or which==BOTH:
  pin13.write_digital(0)
def read_sensor(which_sensor,which_side):
 i2c.write(0x04,pack('B',which_sensor))
 buf=i2c.read(0x04,3)
 pack_into('>HH',_BUFFER,0,1023-(buf[0]<<2|((buf[2]&0xC0)>>6)),1023-(buf[1]<<2|((buf[2]&0x30)>>4)))
 if which_side==LEFT:
  return unpack_from('>H',_BUFFER,2)[0]
 elif which_side==RIGHT:
  return unpack_from('>H',_BUFFER,0)[0]
 else:
  return unpack_from('>HH',_BUFFER)
def read_distance_sensor():
 global _DS
 if _DS is None:
  from distance_sensor import DistanceSensor
  _DS=DistanceSensor()
 return _DS.read_range_single()
def read_thp_sensor():
 global _THP
 if _THP is None:
  from thp import TempHumPress
  _THP=TempHumPress()
 return(_THP.get_temperature_celsius(),_THP.get_temperature_fahrenheit(),_THP.get_pressure(),_THP.get_humidity(),_THP.get_dewpoint_celsius(),_THP.get_dewpoint_fahrenheit())
def read_light_color_sensor():
 global _LCS
 if _LCS is None:
  from lightcolor import LightColorSensor
  _LCS=LightColorSensor()
  _LCS.set_led(True)
 return _LCS.get_color()
def volt():
 i2c.write(0x04,b'\x04')
 return unpack('>H',i2c.read(0x04,2))[0]/1000.0
# Created by pyminifier (https://github.com/liftoff/pyminifier)

