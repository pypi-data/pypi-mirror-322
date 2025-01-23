import sys
import time
import serial
from .constants import *
from .utils import * 
from termcolor import cprint

__all__ = [
    "Maqueen",
]


class Maqueen():
    """마퀸을 제어하는 라이브러리
    """
    LED_LEFT = 0
    LED_RIGHT= 1
    LED_ALL = 2
    DIR_CW = 0 
    DIR_CCW= 1
    LOW = 0
    HIGH = 1
    SERVO_1 = 0
    SERVO_2 = 1

    RGB_0 = 0
    RGB_1 = 1
    RGB_2 = 2
    RGB_3 = 3

    RGB_BLACK = 0
    RGB_WHITE = 1
    RGB_RED=    2
    RGB_ORANGE= 3
    RGB_YELLOW= 4
    RGB_GREEN=  5
    RGB_BLUE = 6
    RGB_INGIGO= 7
    RGB_VIOLET= 8
    RGB_PURPLE = 9
    RGB_CYAN = 10
    

    
    def __init__(self, port=None, baud=57600, verbose=False):
        self.__verbose = verbose
        self.__port = port
        self.__baud = baud;
        self.__serial = None
        self.__packets = None
        self._packetIndex = 1
        self.display = self.Display(self)
        self.pin = self.PIN()

        self.__reserved_color = ['#000000','#FFFFFF','#FF0000','#FFA500','#FFFF00','#00FF00','#0000FF','#4B0082','#8A2BE2','#FF00FF','#00FFFF']

        self.__sensors = {
            'switch': [0, 0],
            'mic': 0,
            'lightSensor': [0, 0],
            'touchSensor': [0, 0, 0],
            'mpuSensor': [0, 0, 0, 0], # left, right, top, bottom
        };

    def connect(self, timeout=5):
        if not self.__port and self.__verbose:
             raise ValueError("Could not find port.")

        cprint(f'👽 Connect PORT={self.__port}, BAUD={self.__baud}', "green")

        sr = serial.Serial(self.__port, self.__baud, timeout=timeout)
        sr.flush()
        self.__serial = sr
        return True
    
    def close(self):
        if self.__serial.is_open():
            cprint(f'🔥 Close(XGO) {self.__port}', 'red')
            self.__serial.flush()
            self.__serial.close()

        if self.__verbose:
            print("XGO close(): Calling sys.exit(0): Hope to see you soon!")
        sys.exit(0)


    def disconnect(self):
        if self.__serial:
            try:
                if self.__serial.is_open():
                    cprint(f'🔥 Disconnect(XGO) {self.__port}', 'red')
                    self.__serial.flush()
                    self.__serial.close()
            except Exception as e:
                cprint(f'Error(XGO): {e}', 'red')
    
    def read_data(self):
        packet = []
        if self.__serial :
            
            while len(packet) < 20:
                if self.sr.inWaiting():
                    c = self.sr.read()
                    packet.append(ord(c))
                else:
                    time.sleep(.1)

        # print('return data length {0}'.format(len(data)))
        return packet

    def __process_return(self):
        packets = []
        if self.__serial :
            
            while len(packets) < 20:
                if self.__serial.inWaiting():
                    c = self.__serial.read()
                    packets.append(ord(c))
                else:
                    time.sleep(.1)
        return packets
        
    def __processReportPacket(self, packet):
        pass

    def __send(self, command):
        if self.__serial:
            if isinstance(command, list):
                try:
                    # print('SEND :', command)
                    self.__serial.write(bytes(bytearray(command)))
                    self.__serial.flush()
                except Exception as e:
                    print('An Exception occurred!', e)
                self.wait(100)
                self.__packets = self.__process_return()
        return None



    def __get_index(self):
        self._packetIndex = (self._packetIndex + 1) % 256  # 0~255 사이에서 순환
        return self._packetIndex
    

    def __send_read(self, command):
        self.__send(command)
        wait(100)
        packets = self.read_data()
        self.__processReportPacket(packets)
    

    # -------------------------------------------------------
    #   UTILS
    # -------------------------------------------------------
    def delay(self, ms):
        time.sleep(float(ms/1000))

    def wait(self, ms):
        delay(ms)
    # -------------------------------------------------------
    #   BOARD PINS
    # -------------------------------------------------------
    class PIN:
        def __init__(self):
            self.P0 = 10 
            self.P1 = 4
            self.P2 = 8
            self.P3 = 2
            self.P4 = 9
            self.P7 = 39
            self.P11 = 7
            self.P12 = 18
            self.SERVO = 16
            self.DCMOTOR = 46

    # -------------------------------------------------------
    #   DISPLAY (LED MATRIX)
    # -------------------------------------------------------
    class Display():
        def __init__(self, controler=None):
            self.__controller = controler
            # print(dir(self.__controller))
            # self.__init()

        def __color(self, color):
            if isinstance(color, str):
                r, g, b = (0, 0, 0)
                # Hex 색상 코드인 경우
                if color.startswith("#") and len(color) == 7:
                    r = int(color[1:3], 16)
                    g = int(color[3:5], 16)
                    b = int(color[5:7], 16)
                else:
                    raise ValueError("Invalid color string format. Expected format: '#RRGGBB'")
            elif (isinstance(color, list) or isinstance(color, tuple)) and len(color) == 3:
                # RGB 리스트인 경우
                r, g, b = color
                if not all(0 <= val <= 255 for val in (r, g, b)):
                    raise ValueError("RGB values must be between 0 and 255.")
            else:
                raise TypeError("Color must be a string in '#RRGGBB' format or a list [R, G, B].")
            return r, g, b

        def color(self, color):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Maqueen__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_COLOR
            command[BBPACKET.DATA1] = r
            command[BBPACKET.DATA2] = g
            command[BBPACKET.DATA3] = b
            self.__controller._Maqueen__send(command)


        def symbol(self, symbol, color):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Maqueen__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_SYMBOL
            command[BBPACKET.DATA1] = symbol[0]
            command[BBPACKET.DATA2] = symbol[1]
            command[BBPACKET.DATA3] = symbol[2]
            command[BBPACKET.DATA4] = symbol[3]
            command[BBPACKET.DATA5] = symbol[4]
            command[BBPACKET.DATA6] = r
            command[BBPACKET.DATA7] = g
            command[BBPACKET.DATA8] = b
            self.__controller._Maqueen__send(command)

        def row(self, row, symbol, color):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Maqueen__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_ROW
            command[BBPACKET.DATA1] = symbol
            command[BBPACKET.DATA2] = r
            command[BBPACKET.DATA3] = g
            command[BBPACKET.DATA4] = b
            command[BBPACKET.DATA5] = row
            self.__controller._Maqueen__send(command)

        def bright(self, bright):
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Maqueen__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_BRIGHT
            command[BBPACKET.DATA1] = bright
            self.__controller._Maqueen__send(command)

        def char(self, symbol, color='#0000FF'):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Maqueen__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_CHAR
            command[BBPACKET.DATA1] = ord(symbol)
            command[BBPACKET.DATA2] = r
            command[BBPACKET.DATA3] = g
            command[BBPACKET.DATA4] = b
            self.__controller._Maqueen__send(command)


        def num(self, symbol, color):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Maqueen__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED;
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_NUM;
            command[BBPACKET.DATA1] = int(symbol);
            command[BBPACKET.DATA2] = r;
            command[BBPACKET.DATA3] = g;
            command[BBPACKET.DATA4] = b;
            self.__controller._Maqueen__send(command)

        def xy(self, coordX, coordY, color):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Maqueen__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED;
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_XY;
            command[BBPACKET.DATA1] = r;
            command[BBPACKET.DATA2] = g;
            command[BBPACKET.DATA3] = b;
            command[BBPACKET.DATA4] = coordX;
            command[BBPACKET.DATA5] = coordY;
            self.__controller._Maqueen__send(command)

        def effect(self, no):
            """
            정해진 효과를 표시한다.
            
            Parameters:
                no (int): 효과 번호 (e.g., 0, 1, 2).
            Returns:
                0: 무지개 효과 
                1: 폭포 효과
                2: 와이퍼 효과 

            Example:
                None
            """
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._Maqueen__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_EFFECT
            command[BBPACKET.DATA1] = no
            command[BBPACKET.DATA2] = 1     # 아두이노에서 사용하는 값
            self.__controller._Maqueen__send(command)

        def clear(self):
            self.color("#000000")
    # --- END OF DIAPLAY ------------------------------------
    # -------------------------------------------------------
    # BUZZER
    # -------------------------------------------------------
    def note(self, note, time):
        # time 은 미리초 단위로 넘어온다.
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.BUZZER;
        command[BBPACKET.DATA0] = ACTION_MODE.BUZZER_NOTE;
        command[BBPACKET.DATA1] = note;

        ah = (time >> 8) & 0xff; # 상위 바이트
        al = time & 0xff;
        command[BBPACKET.DATA2] = ah;
        command[BBPACKET.DATA3] = al;
        self.__send(command)

    def melody(self, melody):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.BUZZER;
        command[BBPACKET.DATA0] = ACTION_MODE.BUZZER_MELODY;
        command[BBPACKET.DATA1] = melody;
        self.__send(command)

    def beep(self):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.BUZZER;
        command[BBPACKET.DATA0] = ACTION_MODE.BUZZER_BEEP;
        self.__send(command)

    # -------------------------------------------------------
    # BUTTON
    # -------------------------------------------------------    
    def button(self):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.BUTTON
        self.__send(command)
        packet = self.read_data()

        if self._packetIndex != packet[BBRETURN.INDEX]:
            print(ERROR.WRONG_PACKET_INDEX)
            return
        # print(self._packetIndex, ' ## ', packet[BBRETURN.INDEX])
        # print(split_and_join(packet))
        # A, B 버튼 동시 리턴 
        return packet[BBRETURN.DATA1]==1, packet[BBRETURN.DATA2]==1
       

    # -------------------------------------------------------
    # TOUCH SENSOR
    # -------------------------------------------------------    
    def touch(self):
        pass

    # -------------------------------------------------------
    # MPU
    # -------------------------------------------------------    
    def tilt(self):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.MPU_ACTION;
        self.__send(command)
        packet = self.read_data()
        if self._packetIndex != packet[BBRETURN.INDEX]:
            print(ERROR.WRONG_PACKET_INDEX)
            return
        return packet[13]==1,packet[14]==1,packet[15]==1,packet[16]==1
    # -------------------------------------------------------
    # 밝기 센서
    # -------------------------------------------------------   
    def light(self):
        # 0 ~ 1023
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.LIGHT_SENSOR;
        self.__send(command)
        packet = self.read_data()
        if self._packetIndex != packet[BBRETURN.INDEX]:
            print(ERROR.WRONG_PACKET_INDEX)
            return
        # 5, 6
        al = packet[5]
        ah = packet[6]
        l1 = (ah << 8) | al;

        # 7, 8
        al = packet[7]
        ah = packet[8]
        l2 = (ah << 8) | al;
        return l1, l2
    
    # -------------------------------------------------------
    # 소리 센서
    # -------------------------------------------------------   
    def mic(self):
       # 0 ~ 1023
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.MIC_SENSOR;
        self.__send(command)
        packet = self.read_data()
        if self._packetIndex != packet[BBRETURN.INDEX]:
            print(ERROR.WRONG_PACKET_INDEX)
            return
        # 5, 6
        al = packet[5]
        ah = packet[6]
        val = (ah << 8) | al;
        return val

    # -------------------------------------------------------
    # 디지털 입출력
    # LED1 : P8 (38)    LED2:P12(18)
    # -------------------------------------------------------   
    def digital_write(self, pin, val):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.DIGITAL
        command[BBPACKET.DATA0] = ACTION_MODE.DIGITAL_OUTPUT
        command[BBPACKET.DATA1] = pin
        command[BBPACKET.DATA2] = val
        self.__send(command)
    # -------------------------------------------------------
    # 아날로그 입출력
    # -------------------------------------------------------   
    # pass


    def dcmotor(self, pin, val):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ANALOG
        command[BBPACKET.DATA0] = ACTION_MODE.ANALOG_OUTPUT
        command[BBPACKET.DATA1] = pin
        # 0 ~ 1023
        ah = (val >> 8) & 0xff      # 상위 바이트
        al = val & 0xff
        command[BBPACKET.DATA2] = al    # 펌웨어에서 readShort 함수를 사용할려면 상위와 하위를 조심
        command[BBPACKET.DATA3] = ah
        self.__send(command)

    # 메인보드의 서버도 핀번호로 동작시키자 
    def servo(self, pin, val):
        
        if (pin == 0 or pin == 1) :
            # maqueen 본체 서보
            self.__maqn_servo(pin, val)
        else:
            # for bitblock
            self.__servo(pin, val)


    def __servo(self, pin, val):

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        if pin == self.pin.SERVO:
            command[BBPACKET.ACTION] = ACTION_CODE.MAIN_SERVO
        else:
            command[BBPACKET.ACTION] = ACTION_CODE.SERVO
        command[BBPACKET.DATA0] = pin;
        command[BBPACKET.DATA1] = val;
        self.__send(command)

    
    def ultrasonic(self, trig, echo):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ULTRASONIC
        command[BBPACKET.DATA0] = trig
        command[BBPACKET.DATA1] = echo
        self.__send(command)
        packet = self.read_data()
        if self._packetIndex != packet[BBRETURN.INDEX]:
            print(ERROR.WRONG_PACKET_INDEX)
            return
        return packet[5]
    
    def dht11(self, pin):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.TMPHUM
        command[BBPACKET.DATA0] = pin
        self.__send(command)
        packet = self.read_data()
        if self._packetIndex != packet[BBRETURN.INDEX]:
            print(ERROR.WRONG_PACKET_INDEX)
            return
        temp = packet[5]
        humi = packet[6]
        return temp, humi

    # -------------------------------------------------------
    # Marqueen 
    # -------------------------------------------------------   
    def forward(self, speed=50):
        speed = int(map(speed,0,100,0,255));

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ACT_MARQUEEN
        command[BBPACKET.DATA0] = ACTION_MODE.MARQN_FORWARD
        command[BBPACKET.DATA1] = speed
        self.__send(command)


    def backward(self, speed=50):
        speed = int(map(speed,0,100,0,255));

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ACT_MARQUEEN
        command[BBPACKET.DATA0] = ACTION_MODE.MARQN_BACKWARD
        command[BBPACKET.DATA1] = speed
        self.__send(command)        


    def stop(self):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ACT_MARQUEEN
        command[BBPACKET.DATA0] = ACTION_MODE.MARQN_MOVE_STOP
        self.__send(command)        
    

    def spin_left(self, speed=50):
        speed = int(map(speed,0,100,0,255));

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ACT_MARQUEEN
        command[BBPACKET.DATA0] = ACTION_MODE.MARQN_SPIN_LEFT
        command[BBPACKET.DATA1] = speed
        self.__send(command)       


    def spin_right(self, speed=50):
        speed = int(map(speed,0,100,0,255));
        
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ACT_MARQUEEN
        command[BBPACKET.DATA0] = ACTION_MODE.MARQN_SPIN_RIGHT
        command[BBPACKET.DATA1] = speed
        self.__send(command)       


    def left(self, speed=50):
        speed = int(map(speed,0,100,0,255));
        
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ACT_MARQUEEN
        command[BBPACKET.DATA0] = ACTION_MODE.MARQN_LEFT
        command[BBPACKET.DATA1] = speed
        self.__send(command)       


    def right(self, speed=50):
        speed = int(map(speed,0,100,0,255));
        
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ACT_MARQUEEN
        command[BBPACKET.DATA0] = ACTION_MODE.MARQN_RIGHT
        command[BBPACKET.DATA1] = speed
        self.__send(command)   


    def motor(self, dir, speed=50):
        '''
        CW :  0x00 
        CCW : 0x01 
        '''
        speed = int(map(speed,0,100,0,255));
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ACT_MARQUEEN
        command[BBPACKET.DATA0] = ACTION_MODE.MARQN_MOTOR
        command[BBPACKET.DATA1] = speed
        command[BBPACKET.DATA1] = dir
        self.__send(command)   


    def patrol(self):
        '''라인트레이서 센서의 값을 (왼쪽,오른쪽) 튜플의 형태로 리턴한다.
        '''
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        print(command[BBPACKET.INDEX])
        command[BBPACKET.ACTION] = ACTION_CODE.ACT_MARQUEEN
        command[BBPACKET.DATA0] = ACTION_MODE.MARQN_PATROL
        self.__send(command)   

        if command[BBPACKET.INDEX] == self.__packets[BBRETURN.INDEX]:
            return (self.__packets[BBRETURN.DATA1], self.__packets[BBRETURN.DATA2])
        else:
            return (0, 0)
        
    def led(self, dir, val):
        # LED_LEFT = 38  # P8
        # LED_RIGHT= 18  # P12
        if dir == 0:
            self.digital_write(38, val)
        elif dir == 1:
            self.digital_write(18, val)
        else:
            self.digital_write(38, val)
            self.digital_write(18, val)

    def distance(self):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ACT_MARQUEEN
        command[BBPACKET.DATA0] = ACTION_MODE.MAQN_ULTRASONIC
        self.__send(command)   
        if command[BBPACKET.INDEX] == self.__packets[BBRETURN.INDEX]:
            return self.__packets[BBRETURN.DATA1]
        else:
            return 0

    # servo()에서 불려진다.
    def __maqn_servo(self, pin, val):
        print("__maqn_servo")
        val = clamp(val, 0, 180)
        if pin == Maqueen.SERVO_1:
            pin = 0x14
        else:
            pin = 0x15

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ACT_MARQUEEN
        command[BBPACKET.DATA0] = ACTION_MODE.MAQN_SERVO
        command[BBPACKET.DATA1] = pin
        command[BBPACKET.DATA2] = val
        self.__send(command)

    def __color(self, color):
            if isinstance(color, str):
                r, g, b = (0, 0, 0)
                # Hex 색상 코드인 경우
                if color.startswith("#") and len(color) == 7:
                    r = int(color[1:3], 16)
                    g = int(color[3:5], 16)
                    b = int(color[5:7], 16)
                else:
                    raise ValueError("Invalid color string format. Expected format: '#RRGGBB'")
            elif (isinstance(color, list) or isinstance(color, tuple)) and len(color) == 3:
                # RGB 리스트인 경우
                r, g, b = color
                if not all(0 <= val <= 255 for val in (r, g, b)):
                    raise ValueError("RGB values must be between 0 and 255.")
            else:
                raise TypeError("Color must be a string in '#RRGGBB' format or a list [R, G, B].")
            return r, g, b
    
    def rgbled(self, pos, color):
        
        r, g, b = self.__color(self.__reserved_color[color])
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ACT_MARQUEEN
        command[BBPACKET.DATA0] = ACTION_MODE.MAQN_RGB
        command[BBPACKET.DATA1] = pos
        command[BBPACKET.DATA2] = r
        command[BBPACKET.DATA3] = g
        command[BBPACKET.DATA4] = b
        self.__send(command)

    def rgb_bright(self, val):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ACT_MARQUEEN
        command[BBPACKET.DATA0] = ACTION_MODE.MAQN_BRIGHT
        command[BBPACKET.DATA1] = val
        self.__send(command)

# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# def search(data, list):
#     for i in range(len(list)):
#         if data == list[i]:
#             return i + 1
#     return -1


# def conver2u8(data, limit, min_value=0):
#     """
#     입력 데이터를 주어진 범위(limit) 내에서 정규화하고, 이를 0에서 255 사이의 값으로 매핑하는 것
#     """
#     max_value = 0xff
#     if not isinstance(limit, list):
#         limit = [-limit, limit]
#     if data >= limit[1]:
#         return max_value
#     elif data <= limit[0]:
#         return min_value
#     else:
#         return int(255 / (limit[1] - limit[0]) * (data - limit[0]))
    
# def clamp(value, min_value, max_value):
#     return max(min_value, min(value, max_value))

