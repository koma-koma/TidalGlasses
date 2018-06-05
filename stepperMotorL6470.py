import wiringpi as wp
import time
import struct

L6470_SPI_CHANNEL = 0
L6470_SPI_SPEED   = 1000000

BUSY_PIN= 21
SS_PIN = 20

io = wp.GPIO(wp.GPIO.WPI_MODE_GPIO)
io.pinMode(BUSY_PIN, io.INPUT)
io.pinMode(SS_PIN, io.OUTPUT)

# set parameter
def L6470_setparam_abspos(val):L6470_transfer(0x01,3,val)
def L6470_setparam_elpos(val):L6470_transfer(0x02,2,val)
def L6470_setparam_mark(val):L6470_transfer(0x03,3,val)
def L6470_setparam_acc(val):L6470_transfer(0x05,2,val)
def L6470_setparam_dec(val):L6470_transfer(0x06,2,val)
def L6470_setparam_maxspeed(val):L6470_transfer(0x07,2,val)
def L6470_setparam_minspeed(val):L6470_transfer(0x08,2,val)
def L6470_setparam_fsspd(val):L6470_transfer(0x15,2,val)
def L6470_setparam_kvalhold(val):L6470_transfer(0x09,1,val)
def L6470_setparam_kvalrun(val):L6470_transfer(0x0a,1,val)
def L6470_setparam_kvalacc(val):L6470_transfer(0x0b,1,val)
def L6470_setparam_kvaldec(val):L6470_transfer(0x0c,1,val)
def L6470_setparam_intspd(val):L6470_transfer(0x0d,2,val)
def L6470_setparam_stslp(val):L6470_transfer(0x0e,1,val)
def L6470_setparam_fnslpacc(val):L6470_transfer(0x0f,1,val)
def L6470_setparam_fnslpdec(val):L6470_transfer(0x10,1,val)
def L6470_setparam_ktherm(val):L6470_transfer(0x11,1,val)
def L6470_setparam_ocdth(val):L6470_transfer(0x13,1,val)
def L6470_setparam_stallth(val):L6470_transfer(0x14,1,val)
def L6470_setparam_stepmood(val):L6470_transfer(0x16,1,val)
def L6470_setparam_alareen(val):L6470_transfer(0x17,1,val)
def L6470_setparam_config(val):L6470_transfer(0x18,2,val)

# get parameter
def L6470_getparam_abspos():return L6470_getparam(0x01,3)
def L6470_getparam_elpos():return L6470_getparam(0x02,2)
def L6470_getparam_mark():return L6470_getparam(0x03,3)
def L6470_getparam_speed():return L6470_getparam(0x04,3)
def L6470_getparam_acc():return L6470_getparam(0x05,2)
def L6470_getparam_dec():return L6470_getparam(0x06,2)
def L6470_getparam_maxspeed():return L6470_getparam(0x07,2)
def L6470_getparam_minspeed():return L6470_getparam(0x08,2)
def L6470_getparam_fsspd():return L6470_getparam(0x15,2)
def L6470_getparam_kvalhold():return L6470_getparam(0x09,1)
def L6470_getparam_kvalrun():return L6470_getparam(0x0a,1)
def L6470_getparam_kvalacc():return L6470_getparam(0x0b,1)
def L6470_getparam_kvaldec():return L6470_getparam(0x0c,1)
def L6470_getparam_intspd():return L6470_getparam(0x0d,2)
def L6470_getparam_stslp():return L6470_getparam(0x0e,1)
def L6470_getparam_fnslpacc():return L6470_getparam(0x0f,1)
def L6470_getparam_fnslpdec():return L6470_getparam(0x10,1)
def L6470_getparam_ktherm():return L6470_getparam(0x11,1)
def L6470_getparam_adcout():return L6470_getparam(0x12,1)
def L6470_getparam_ocdth():return L6470_getparam(0x13,1)
def L6470_getparam_stallth():return L6470_getparam(0x14,1)
def L6470_getparam_stepmood():return L6470_getparam(0x16,1)
def L6470_getparam_alareen():return L6470_getparam(0x17,1)
def L6470_getparam_config():return L6470_getparam(0x18,2)
def L6470_getparam_status():return L6470_getparam(0x19,2)

# def L6470_write(channel, data):
#     data = struct.pack('B', data)
#     return wp.wiringPiSPIDataRW(channel, data)


def L6470_resetdevice():
    L6470_send_u(0x00) #nop命令
    L6470_send_u(0x00)
    L6470_send_u(0x00)
    L6470_send_u(0x00)
    L6470_send_u(0xc0)

def L6470_init():
    print('***** start spi test program *****')

    # SPI channel 0 を 1MHz で開始。
    #wp.wiringPiSetupGpio()
    wp.wiringPiSPISetup(0, L6470_SPI_SPEED)

    #デバイスのリセット
    L6470_resetdevice()

    # MAX_SPEED設定 最大回転スピード値(19bit) 初期値は 0x41
    L6470_setparam_maxspeed(0x20)

    # KVAL_HOLD設定。
    L6470_setparam_kvalhold(0xFF)

    # KVAL_RUN設定。
    L6470_setparam_kvalrun(0xFF)

    # KVAL_ACC設定。
    L6470_setparam_kvalacc(0xFF)

    # KVAL_DEC設定。
    L6470_setparam_kvaldec(0x40)

    # OCD_TH設定。
    L6470_setparam_ocdth(0x0F)

    # STALL_TH設定。
    L6470_setparam_stallth(0x7F)

def L6470_run(dir, speed):
    if(dir==1):
        L6470_transfer(0x51,3,speed)
    else:
        L6470_transfer(0x50,3,speed)

def L6470_move(dir, n_step):
    if(dir==1):
        L6470_transfer(0x41,3,n_step)
    else:
        L6470_transfer(0x40,3,n_step)

def L6470_goto(pos):
    L6470_transfer(0x60,3,pos)

def L6470_gotodia(dir, pos):
    if(dir==1):  
        L6470_transfer(0x69,3,pos)
    else: 
        L6470_transfer(0x68,3,pos)

def L6470_softstop():
    print('***** SoftStop. *****')
    L6470_transfer(0xB0, 0, 0)

def L6470_softhiz():
    print('***** Softhiz. *****')
    L6470_transfer(0xA8, 0, 0)

def L6470_transfer(add, bytes, val):
    data = [0, 0, 0]
    L6470_send(add)
    for i in range(bytes):
        data[i] = val & 0xff
        val = val >> 8

    if(bytes==3):
        L6470_send(data[2])

    if(bytes>=2):
        L6470_send(data[1])

    if(bytes>=1):
        L6470_send(data[0])

def L6470_send(add_or_val):
    while( io.digitalRead(BUSY_PIN) == 0 ):
        pass

    data = struct.pack('B', add_or_val)
    print(data)
    return wp.wiringPiSPIDataRW(L6470_SPI_CHANNEL, data)

def L6470_send_u(add_or_val):
    data = struct.pack('B', add_or_val)
    return wp.wiringPiSPIDataRW(L6470_SPI_CHANNEL, data)

def L6470_getparam(add, bytes):
    val=0
    send_add = add | 0x20
    L6470_send_u(send_add)
    for i in range(bytes-1):
        val = val << 8
        wp.digitalWrite(SS_PIN, 0) # ~SSイネーブル。
        val = val | wp.wiringPiSPIDataRW(L6470_SPI_CHANNEL, 0x00) # アドレスもしくはデータ送信。
        wp.digitalWrite(SS_PIN, 1) # ~SSディスエーブル 

    return val

if __name__=="__main__":
    speed = 3000
    
    L6470_init()

    try:
        while True:
            print("** Move %d **" % speed)
            L6470_run(0, speed)
            time.sleep(5)
            L6470_softstop()
            time.sleep(1)
            print("** Move %d **" % -speed)
            L6470_run(1, speed)
            time.sleep(5)
            L6470_softstop()
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nExit")
        L6470_softstop()
        L6470_softhiz()
        quit()
