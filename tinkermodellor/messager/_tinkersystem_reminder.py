import os
import functools

def TinkerSystemReminder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        width = os.get_terminal_size().columns
        message = "*** TinkerModellor Tinker System Reader is running ***"
        print("******************************************************".center(width))
        print(message.center(width))
        print("******************************************************".center(width))
        print('\n\n')

        result = func(*args, **kwargs)

        message = "***TinkerModellor Tinker System Reader is finished ***"
        print("******************************************************".center(width))
        print(message.center(width))
        print("******************************************************".center(width))
        print('\n')
        return result

    return wrapper