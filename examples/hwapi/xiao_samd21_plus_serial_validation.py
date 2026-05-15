import gc,sys,time,machine
from machine import Pin,ADC,I2C,SPI,UART,PWM

A=("A0","A1","A2","A3","A4","A5","A6","A7","A8","A9","A10")
G=("D0","D1","D2","D3")

def z(ns):
    for n in ns:
        try: Pin(n,Pin.IN)
        except: pass

def h():
    print("h help")
    print("i id")
    print("l led")
    print("t rgb+rxled")
    print("n rgb")
    print("g gpio")
    print("a adc")
    print("c i2c")
    print("v i2c1")
    print("s spi D10->D9")
    print("u uart D6->D7")
    print("p pwm")
    print("b button")
    print("r reset")

def i():
    print("Board: SEEED_XIAO_SAMD21_PLUS")
    print("Impl:",sys.implementation.name)
    print("Machine:",machine.freq())

def l():
    p=Pin("LED",Pin.OUT,value=0)
    try:
        for _ in range(3):
            p.value(1);time.sleep_ms(120)
            p.value(0);time.sleep_ms(120)
    finally:
        z(("LED",))

def t():
    a=Pin("RGB_LED",Pin.OUT,value=0);b=Pin("RX_LED",Pin.OUT,value=0)
    try:
        for _ in range(3):
            a.value(1);b.value(1);time.sleep_ms(100)
            a.value(0);b.value(0);time.sleep_ms(100)
    finally:
        z(("RGB_LED","RX_LED"))

def n():
    p=Pin("RGB_LED",Pin.OUT,value=0)
    t=(400,850,800,450)
    try:
        for buf in (b"\x10\x00\x00",b"\x00\x10\x00",b"\x00\x00\x10",b"\x00\x00\x00"):
            machine.bitstream(p,0,t,buf)
            time.sleep_ms(150)
        print("rgb ok")
    finally:
        z(("RGB_LED",))

def g():
    for n in G:
        p=Pin(n,Pin.OUT,value=0);p.value(1);print(n,p.value());p.value(0)
    z(G)

def a():
    for n in A: print(n,ADC(Pin(n)).read_u16())

def c():
    x=I2C(2,scl=Pin("D5"),sda=Pin("D4"),freq=100000)
    try: print("i2c",x.scan())
    finally:
        try: x.deinit()
        except: pass
        z(("D4","D5"))

def v():
    x=I2C(1,scl=Pin("SCL1"),sda=Pin("SDA1"),freq=100000)
    try: print("i2c1",x.scan())
    finally:
        try: x.deinit()
        except: pass
        z(("SCL1","SDA1"))

def s():
    x=SPI(0,baudrate=500000,polarity=0,phase=0,sck=Pin("D8"),mosi=Pin("D10"),miso=Pin("D9"))
    try:
        t=b"SPI";r=bytearray(3);x.write_readinto(t,r);print("spi",bytes(r))
    finally:
        try: x.deinit()
        except: pass
        z(("D8","D9","D10"))

def u():
    x=UART(4,baudrate=115200,tx=Pin("D6"),rx=Pin("D7"))
    try:
        t=b"UART\r\n";x.write(t);st=time.ticks_ms();r=b""
        while time.ticks_diff(time.ticks_ms(),st)<400:
            if x.any():
                r=x.read() or b"";break
            time.sleep_ms(10)
        print("uart",r)
    finally:
        try: x.deinit()
        except: pass
        z(("D6","D7"))

def p():
    x=PWM(Pin("D1"),freq=1000,duty_u16=32768)
    try:
        time.sleep_ms(200);print("pwm ok")
    finally:
        try: x.deinit()
        except: pass
        z(("D1",))

def b():
    x=Pin("BUTTON",Pin.IN)
    print("button",x.value())

def r():
    z(G+("LED","RX_LED","RGB_LED","BUTTON","SCL1","SDA1","D1","D4","D5","D6","D7","D8","D9","D10"))
    gc.collect()
    print("reset ok")

def run(cmd):
    try:
        if cmd=="h": h()
        elif cmd=="i": i()
        elif cmd=="l": l()
        elif cmd=="t": t()
        elif cmd=="n": n()
        elif cmd=="g": g()
        elif cmd=="a": a()
        elif cmd=="c": c()
        elif cmd=="v": v()
        elif cmd=="s": s()
        elif cmd=="u": u()
        elif cmd=="p": p()
        elif cmd=="b": b()
        elif cmd=="r": r()
        else: print("bad cmd")
    except Exception as e:
        print("ERR",type(e).__name__,e)
    gc.collect()
    print("idle")

gc.collect()
print("XIAO SAMD21 PLUS test")
h()
print("idle")
while 1:
    try: x=input("> ").strip()
    except:
        print("");r();print("idle");continue
    if x: run(x)
