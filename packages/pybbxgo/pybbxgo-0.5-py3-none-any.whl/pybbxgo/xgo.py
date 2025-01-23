import sys
import time
import serial
from .constants import *
from .utils import * 
from termcolor import cprint

__all__ = [
    "XGO",
]


class XGO():
    """일반 IDE와 주피터노트북에서 사용가능한 클래스 
    """
    LEFT_FRONT = 0
    RIGHT_FRONT = 1
    RIGHT_HIND = 2
    LEFT_HIND = 3
    PACE_NORMAL = 0
    PACE_SLOW = 1
    PACE_HIGH = 2
    GAIT_TROT = 0x00
    GAIT_WALK = 0x01
    GAIT_HIGH_WALK = 0x02
    GAIT_SLOW_TROT = 0x03

    def __init__(self, port=None, baud=57600, verbose=False):
        self.__verbose = verbose
        self.__port = port
        self.__baud = baud;
        self.__serial = None
        self._packetIndex = 1;
        self.display = self.Display(self)
        self.pin = self.PIN()

        self.__sensors = {
            'switch': [0, 0],
            'mic': 0,
            'lightSensor': [0, 0],
            'touchSensor': [0, 0, 0],
            'mpuSensor': [0, 0, 0, 0], # left, right, top, bottom
        };

    def connect(self, timeout=5):
        try: 

            if not self.__port and self.__verbose:
                raise ValueError("Could not find port.")

            cprint(f'👽 XGO Connect PORT={self.__port}, BAUD={self.__baud}', "green")

            sr = serial.Serial(self.__port, self.__baud, timeout=timeout)
            sr.flush()
            self.__serial = sr
            return self.__serial
    
        except Exception as e:
            cprint(f'👽 Error(XGO): {e}', 'green')

    

    def close(self):
        '''close후 exit()함수를 호출함 
        '''
        try:
            if self.__serial and self.__serial.is_open:
                self.__serial.flush()
                self.__serial.close()
                cprint(f'🔥 Close (XGO) {self.__port}', 'red')
        except Exception as e:
            cprint(f'Error(XGO): {e}', 'red')
        finally:
            sys.exit(0)


    def disconnect(self):
        try:
            if self.__serial and self.__serial.is_open:
                self.__serial.flush()
                self.__serial.close()
                cprint(f'🔥 Disconnect(XGO) {self.__port}', 'red')
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
                # self.__process_return()
                return None



    def __get_index(self):
        self._packetIndex = (self._packetIndex + 1) % 256  # 0~255 사이에서 순환
        return self._packetIndex
    
    def __send_read(self, command):
        self.__send(command)
        wait(100)
        packet = self.read_data()
        self.__processReportPacket(packet)
    

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
            command[BBPACKET.INDEX] = self.__controller._XGO__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_COLOR
            command[BBPACKET.DATA1] = r
            command[BBPACKET.DATA2] = g
            command[BBPACKET.DATA3] = b
            self.__controller._XGO__send(command)


        def symbol(self, symbol, color):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._XGO__get_index()
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
            self.__controller._XGO__send(command)

        def row(self, row, symbol, color):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._XGO__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_ROW
            command[BBPACKET.DATA1] = symbol
            command[BBPACKET.DATA2] = r
            command[BBPACKET.DATA3] = g
            command[BBPACKET.DATA4] = b
            command[BBPACKET.DATA5] = row
            self.__controller._XGO__send(command)

        def bright(self, bright):
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._XGO__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_BRIGHT
            command[BBPACKET.DATA1] = bright
            self.__controller._XGO__send(command)

        def char(self, symbol, color='#0000FF'):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._XGO__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_CHAR
            command[BBPACKET.DATA1] = ord(symbol)
            command[BBPACKET.DATA2] = r
            command[BBPACKET.DATA3] = g
            command[BBPACKET.DATA4] = b
            self.__controller._XGO__send(command)


        def num(self, symbol, color):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._XGO__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED;
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_NUM;
            command[BBPACKET.DATA1] = int(symbol);
            command[BBPACKET.DATA2] = r;
            command[BBPACKET.DATA3] = g;
            command[BBPACKET.DATA4] = b;
            self.__controller._XGO__send(command)

        def xy(self, coordX, coordY, color):
            r, g, b = self.__color(color)
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__controller._XGO__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED;
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_XY;
            command[BBPACKET.DATA1] = r;
            command[BBPACKET.DATA2] = g;
            command[BBPACKET.DATA3] = b;
            command[BBPACKET.DATA4] = coordX;
            command[BBPACKET.DATA5] = coordY;
            self.__controller._XGO__send(command)

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
            command[BBPACKET.INDEX] = self.__controller._XGO__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.MATRIX_LED
            command[BBPACKET.DATA0] = ACTION_MODE.DISPLAY_EFFECT
            command[BBPACKET.DATA1] = no
            command[BBPACKET.DATA2] = 1     # 아두이노에서 사용하는 값
            self.__controller._XGO__send(command)

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
    # -------------------------------------------------------   
    # pass 
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
    # XGO 로봇 관련 동작
    # -------------------------------------------------------   
    def forward(self, speed=50, runtime=0):
        '''로봇을 앞으로 이동 시킴 
        speed : 0 ~ 100 사이의 값을 입력 
        runtime : 0 이외의 값은 그 시간이 경과 후 멈춘다.
        0x30
        '''
        speed = int(map(speed, 0, 100, 128, 255))
        print('xgo FORWARD SPEED :', speed)

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.XGO
        command[BBPACKET.DATA0] = ACTION_MODE.XGO_FORWARD
        command[BBPACKET.DATA1] = speed
        self.__send(command)

        if runtime > 0:
            self.wait(runtime * 1000)
            self.move_stop()

    def backward(self, speed=50, runtime=0):
        '''로봇을 뒤로 이동 시킴 
        speed : 0 ~ 100 사이의 값을 입력 
        0x30
        '''
        speed = int(map(speed, 0, 100, 128, 0))
        print('xgo BACKWARD SPEED :', speed)

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.XGO
        command[BBPACKET.DATA0] = ACTION_MODE.XGO_BACKWARD
        command[BBPACKET.DATA1] = speed
        self.__send(command)

        if runtime > 0:
            self.wait(runtime * 1000)
            self.move_stop()

    def move_stop(self):
        '''
        0x30
        '''
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.XGO
        command[BBPACKET.DATA0] = ACTION_MODE.XGO_MOVE_STOP
        self.__send(command)

    def action(self, code=XGO_ACTION.DEFAULT_POSTURE, wait=False):
        '''정해진 동작을 진행한다. 
        code : 동작 코드 (문자열)
        wait : 동작이 완료될 때까지 새로운 명령을 보내지 않음
        0x3E
        '''
        action = XGO_ACTION_CODE[code]
        action_time = XGO_ACTION_TIME[code]
        print(action, action_time)

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.XGO
        command[BBPACKET.DATA0] = ACTION_MODE.XGO_ACTION
        command[BBPACKET.DATA1] = action
        self.__send(command)

        if wait:
            self.wait(XGO_ACTION_TIME[code]*1000)

    def reset(self):
        """
        초기 자세로 돌아감.
        """
        self.action(XGO_ACTION.DEFAULT_POSTURE)
        time.sleep(1)


    def right(self, speed=50, runtime=0):
        '''로봇의 입장에서 오른쪽으로 옆걸음으로 이동 시킴 
        speed : 0 ~ 100 사이의 값을 입력 
        0x31
        '''
        speed = int(map(speed, 0, 100, 128, 0))
        print('xgo LEFT SPEED :', speed)

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.XGO
        command[BBPACKET.DATA0] = ACTION_MODE.XGO_LEFT
        command[BBPACKET.DATA1] = speed
        self.__send(command)

        if runtime > 0:
            self.wait(runtime * 1000)
            self.shift_stop()

    def left(self, speed=50, runtime=0):
        '''로봇의 입장에서 왼쪽으로 옆걸음으로 이동 시킴 
        speed : 0 ~ 100 사이의 값을 입력 
        0x31
        '''
        speed = int(map(speed, 0, 100, 128, 255))
        print('xgo RIGHT SPEED :', speed)

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.XGO
        command[BBPACKET.DATA0] = ACTION_MODE.XGO_RIGHT
        command[BBPACKET.DATA1] = speed
        self.__send(command)

        if runtime > 0:
            self.wait(runtime * 1000)
            self.shift_stop()

    def shift_stop(self):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.XGO
        command[BBPACKET.DATA0] = ACTION_MODE.XGO_SHIFT_STOP
        self.__send(command)

    def turn_left(self, speed=50, runtime=0):
        '''로봇 방향을 왼쪽으로 회전  
        speed : 0 ~ 100 사이의 값을 입력 
        0x32
        '''
        speed = int(map(speed, 0, 100, 128, 256))
        print('xgo TURN LEFT SPEED :', speed)

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.XGO
        command[BBPACKET.DATA0] = ACTION_MODE.XGO_TURN_LEFT
        command[BBPACKET.DATA1] = speed
        self.__send(command)

        if runtime > 0:
            self.wait(runtime * 1000)
            self.turn_stop()

    def turn_right(self, speed=50, runtime=0):
        '''로봇 방향을 왼쪽으로 회전  
        speed : 0 ~ 100 사이의 값을 입력 
        0x32
        '''
        speed = int(map(speed, 0, 100, 128, 0))
        print('xgo TURN RIGHT SPEED :', speed)

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.XGO
        command[BBPACKET.DATA0] = ACTION_MODE.XGO_TURN_RIGHT
        command[BBPACKET.DATA1] = speed
        self.__send(command)

        if runtime > 0:
            self.wait(runtime * 1000)
            self.turn_stop()

    def turn_stop(self):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.XGO
        command[BBPACKET.DATA0] = ACTION_MODE.XGO_TURN_STOP
        self.__send(command)

    def stop(self):
        self.move_stop()
        self.shift_stop()
        self.turn_stop()  

    def leg_lift(self, data):
        '''로봇의 제자리 걸음
        data : 제자리 걸음의 높이를 제어하는 값
        0 : 동작을 중단, 1~255 : 값이 클수록 발을 더 높이 들고 내린다.
        0x3C mark_time lef_lift
        '''
        if data != 0:
            data = conver2u8(data, [10, 25], min_value=1)

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.XGO
        command[BBPACKET.DATA0] = ACTION_MODE.XGO_MARKTIME
        command[BBPACKET.DATA1] = 0x3C
        command[BBPACKET.DATA2] = data
        self.__send(command)


    def __translation(self, dir, data):
        dir = dir.lower()
       
        print(dir, data)

        val = 0
        # "TRANSLATION_LIMIT": [25, 18, [60, 110]],
        if dir == 'x':
            # Math.map(distance, -35, 35, 0, 255)
            val = conver2u8(data, [-25, 25])
        elif dir == 'y':
            # Math.map(distance, -18, 18, 0, 255)
            val = conver2u8(data, [-18, 18])
        elif dir == 'z':
            # Math.map(distance, 75, 115, 0, 255)
            val = conver2u8(data, [60, 110])

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.XGO
        command[BBPACKET.DATA0] = ACTION_MODE.XGO_TRANSLATION
        if dir == 'x':
            command[BBPACKET.DATA1] = 0x33
        elif dir == 'y':
            command[BBPACKET.DATA1] = 0x33  # 0x34
        elif dir == 'z':
            command[BBPACKET.DATA1] = 0x33  # 0x35

        command[BBPACKET.DATA2] = val
        self.__send(command)

    def trans(self, dir, data):
        """
        다리를 고정시키고, 몸을 x, y, z 축으로 평형하게 움직임 
        x = [-25, 25], y=[-18, 18], z=[60, 110]

        0x33
        """
        if isinstance(dir, list):
            if len(dir) != len(data):
                print("방향과 데이터의 개수가 일치하지 않습니다!")
                return

            for i in range(len(data)):
                self.__translation(dir[i].lower(), data[i])
        else:
            self.__translation(dir.lower(), data)    



    def __attitude(self, dir, data):
        dir = dir.lower()

        print(dir, data)

        val = 0
        # "ATTITUDE_LIMIT": [20, 10, 12],  ['r', 'p', 'y']
        if dir == 'x':
            # Math.map(angle, -20, 20, 0, 255)
            val = conver2u8(data, [-20, 20])
        elif dir == 'y':
            # Math.map(angle, -20, 20, 0, 255)
            val = conver2u8(data, [-10, 10])
        elif dir == 'z':
            # Math.map(angle, -20, 20, 0, 255)
            val = conver2u8(data, [-12, 12])

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.XGO
        command[BBPACKET.DATA0] = ACTION_MODE.XGO_ATTITUDE
        if dir == 'x':
            command[BBPACKET.DATA1] = 0x36 
        elif dir == 'y':
            command[BBPACKET.DATA1] = 0x36 # 0x37
        elif dir == 'z':
            command[BBPACKET.DATA1] = 0x36 # 0x38

        command[BBPACKET.DATA2] = val
        self.__send(command)
        

    def attitude(self, dir, data):
        """
        다리를 고정시키고, 몸을 비튼다.
        r = [-20, 20], p = [-10, 10], y = [-12, 12]
        0x36
        """
        if isinstance(dir, list):
            if len(dir) != len(data):
                print("방향과 데이터의 개수가 일치하지 않습니다!")
                return
            for i in range(len(data)):
                self.__attitude(dir[i], data[i])
        else:
            self.__attitude(dir, data)

    def leg(self, leg_id, xval, yval, zval):
        """
        로봇 개의 한쪽 다리의 3축 움직임을 제어
        left_front : 0, (앞 왼) 
        right_front: 1  (앞 오)
        right_hind : 2  (뒤 오)
        left_hind : 3   (뒤 왼)
        """
        xval = int(map(xval, -25, 25, 0, 255))
        yval = int(map(yval, -18, 18, 0, 255))
        zval = int(map(zval, 60, 110, 0, 255))
        
        if leg_id == XGO.LEFT_FRONT:
            # left_front - X
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.XGO
            command[BBPACKET.DATA0] = ACTION_MODE.XGO_LEG
            command[BBPACKET.DATA1] = 0x40  # X 
            command[BBPACKET.DATA2] = xval
            self.__send(command)
            # left_front - Y
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.XGO
            command[BBPACKET.DATA0] = ACTION_MODE.XGO_LEG
            command[BBPACKET.DATA1] = 0x41  # Y 
            command[BBPACKET.DATA2] = yval
            self.__send(command)
            # left_front - Z
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.XGO
            command[BBPACKET.DATA0] = ACTION_MODE.XGO_LEG
            command[BBPACKET.DATA1] = 0x42  # Z 
            command[BBPACKET.DATA2] = zval
            self.__send(command)

        elif leg_id == XGO.RIGHT_FRONT:
            # right_front - X
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.XGO
            command[BBPACKET.DATA0] = ACTION_MODE.XGO_LEG
            command[BBPACKET.DATA1] = 0x43  # X 
            command[BBPACKET.DATA2] = xval
            self.__send(command)
            # right_front - Y
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.XGO
            command[BBPACKET.DATA0] = ACTION_MODE.XGO_LEG
            command[BBPACKET.DATA1] = 0x44  # Y 
            command[BBPACKET.DATA2] = yval
            self.__send(command)
            # right_front - Z
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.XGO
            command[BBPACKET.DATA0] = ACTION_MODE.XGO_LEG
            command[BBPACKET.DATA1] = 0x45  # Z 
            command[BBPACKET.DATA2] = zval
            self.__send(command)
        elif leg_id == XGO.RIGHT_HIND:
            # right_hind - X
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.XGO
            command[BBPACKET.DATA0] = ACTION_MODE.XGO_LEG
            command[BBPACKET.DATA1] = 0x46  # X 
            command[BBPACKET.DATA2] = xval
            self.__send(command)
            # right_hind - Y
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.XGO
            command[BBPACKET.DATA0] = ACTION_MODE.XGO_LEG
            command[BBPACKET.DATA1] = 0x47  # Y 
            command[BBPACKET.DATA2] = yval
            self.__send(command)
            # right_hind - Z
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.XGO
            command[BBPACKET.DATA0] = ACTION_MODE.XGO_LEG
            command[BBPACKET.DATA1] = 0x48  # Z 
            command[BBPACKET.DATA2] = zval
            self.__send(command)
        
        elif leg_id == XGO.LEFT_HIND:
            # left_hind - X
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.XGO
            command[BBPACKET.DATA0] = ACTION_MODE.XGO_LEG
            command[BBPACKET.DATA1] = 0x49  # X 
            command[BBPACKET.DATA2] = xval
            self.__send(command)
            # left_hind - Y
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.XGO
            command[BBPACKET.DATA0] = ACTION_MODE.XGO_LEG
            command[BBPACKET.DATA1] = 0x4A  # Y 
            command[BBPACKET.DATA2] = yval
            self.__send(command)
            # left_hind - Z
            command = NULL_COMMAND_PACKET[:]
            command[BBPACKET.INDEX] = self.__get_index()
            command[BBPACKET.ACTION] = ACTION_CODE.XGO
            command[BBPACKET.DATA0] = ACTION_MODE.XGO_LEG
            command[BBPACKET.DATA1] = 0x4B  # Z 
            command[BBPACKET.DATA2] = zval
            self.__send(command)
        

    def pace(self, mode):
        """
        걸음걸이의 빠르기를 변경한다.
        0x3D
        """
        value = 0x00
        if mode == XGO.PACE_NORMAL:
            value = 0x00
        elif mode == XGO.PACE_SLOW:
            value = 0x01
        elif mode == XGO.PACE_HIGH:
            value = 0x02
        else:
            print("잘못된 설정입니다.")
            return

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.XGO
        command[BBPACKET.DATA0] = ACTION_MODE.XGO_EXE
        command[BBPACKET.DATA1] = 0x3D
        command[BBPACKET.DATA2] = value
        self.__send(command)   

    def gait_type(self, mode):
        """
        걸음걸이 타입 설정 
        GAIT_TROT = 0x00
        GAIT_WALK = 0x01
        GAIT_HIGH_WALK = 0x02
        GAIT_SLOW_TROT = 0x03

        0x09
        """
        value = 0x00
        if mode == XGO.GAIT_TROT:
            value = 0x00
        elif mode == XGO.GAIT_WALK:
            value = 0x01
        elif mode == XGO.GAIT_HIGH_WALK:
            value = 0x02
        elif mode == XGO.GAIT_SLOW_TROT:
            value = 0x03
        else:
            print("잘못된 설정입니다.")
            return

        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.XGO
        command[BBPACKET.DATA0] = ACTION_MODE.XGO_EXE
        command[BBPACKET.DATA1] = 0x09
        command[BBPACKET.DATA2] = value
        self.__send(command)       

    # -------------------------------------------------------
    # Marqueen 
    # -------------------------------------------------------   
    def marq_forward(self, speed=50):
        command = NULL_COMMAND_PACKET[:]
        command[BBPACKET.INDEX] = self.__get_index()
        command[BBPACKET.ACTION] = ACTION_CODE.ACT_MARQUEEN
        command[BBPACKET.DATA0] = ACTION_MODE.MARQN_FORWARD
        command[BBPACKET.DATA1] = 50
        self.__send(command)
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
# -.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.-.
def search(data, list):
    for i in range(len(list)):
        if data == list[i]:
            return i + 1
    return -1


def conver2u8(data, limit, min_value=0):
    """
    입력 데이터를 주어진 범위(limit) 내에서 정규화하고, 이를 0에서 255 사이의 값으로 매핑하는 것
    """
    max_value = 0xff
    if not isinstance(limit, list):
        limit = [-limit, limit]
    if data >= limit[1]:
        return max_value
    elif data <= limit[0]:
        return min_value
    else:
        return int(255 / (limit[1] - limit[0]) * (data - limit[0]))
    
def clamp(value, min_value, max_value):
    return max(min_value, min(value, max_value))

