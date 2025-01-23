import sys
import time
import math
import asyncio

__all__ = [
    "split_and_join",
    "delay",
    "wait",
    "clamp",
    "map",
]

def split_and_join(msg, separator=','):
    """바이트 배열을 문자열러 표시해서 확인하는 용도로 사용 

        Args:
            msg (bytearray): 확인할 바이트 배열 
        Returns:
            str
    """
    hex_string = msg.hex()
    if len(hex_string) % 2 != 0:
        print("주의: 문자열의 길이가 분할 단위로 나누어 떨어지지 않습니다.")
    split_str = [hex_string[i:i+2] for i in range(0, len(hex_string), 2)]
    return separator.join(split_str)


def delay(ms):
        """기다리기

        Args:
            ms (float): 밀리초
        Returns:
            None
        """
        time.sleep(ms/1000)


def wait(ms):
        """기다리기

        Args:
            ms (float): 밀리초
        Returns:
            None
        """
        time.sleep(ms/1000)

def clamp(value, mval=0, xval=180):
    """
    주어진 최대값과 최소값 사이의 범위로 조정하여 값을 반환 

    Parameters:
        value (int or float): 조정할 값
        mval  (int or float): 최소값
        xval  (int or float): 최대값

    Returns:
        int or float: 조정된 값 

    Example:
        result = clamp(200, 0, 180)
        print(result)  # Output: 180

        result = clamp(-50, 0, 180)
        print(result)  # Output: 0
    """
    return max(mval, min(xval, value))


def map(x, in_min, in_max, out_min, out_max):
    """
    Maps a value from one range to another, similar to Arduino's map() function.

    Args:
        x (float or int): Input value to map.
        in_min (float or int): Minimum value of the input range.
        in_max (float or int): Maximum value of the input range.
        out_min (float or int): Minimum value of the output range.
        out_max (float or int): Maximum value of the output range.

    Returns:
        float: Mapped value in the output range.
    """
    return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min


