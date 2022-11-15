import machine, time
from machine import Pin
rs232=machine.UART(2,115200)
trig=Pin(23, Pin.OUT)
eco=Pin(34, Pin.IN)
horario=Pin(33, Pin.OUT)
antih=Pin(32, Pin.OUT)
s1=Pin(26, Pin.IN)
s2=Pin(25, Pin.IN)
s3=Pin(0, Pin.IN)
i=0
stdOpen=0
stdClose=0
autoOn=0
ok232=0
if s1.value()==1:
    stdClose=1
if s2.value()==1:
    stdOpen=1
#print(stdOpen,stdClose)
pulse_time=0
while True:
    time.sleep_ms(100)
    rs232.write(b'\x0A\xFF\x09\x88\x00\x00\x00\x00\x01\x02\x06\x5d')
    read232=rs232.readline()
    #print(read232)
    if read232==b'\x0b\xc8\x0f\x00\x00\xe2\x00G\x17\xaa\xbbh!&\x0f\x01\x0c\xae':
        ok232=1
    else:
        ok232=0
        
    trig.value(0)
    time.sleep_us(5)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    pulse_time = machine.time_pulse_us(eco, 1)
    #print(pulse_time)
    time.sleep_ms(100)
    if pulse_time > 500 and pulse_time<1500:
        autoOn=1
    else:
        autoOn=0
    
    if ok232==1 and stdClose==1 and autoOn==1:
        antih.value(1)
        time.sleep_ms(150)
    #elif s1.value()==0 and s2.value()==1:
        antih.value(0)
        stdClose=0
        stdOpen=1
        time.sleep(2)
        
    if ok232==0 and stdOpen==1 and autoOn==0:
        time.sleep(5)
        horario.value(1)
        time.sleep_ms(150)
    #elif s1.value()==1 and s2.value()==0:
        horario.value(0)
        stdClose=1
        stdOpen=0
   
    print("ok232",ok232)
    print("stdOpen",stdOpen)
    print("autoOn", autoOn)
    print("Sensor puerta cerrada",s1.value())

