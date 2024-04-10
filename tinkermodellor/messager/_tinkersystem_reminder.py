import os
import functools

def TinkerSystemReminder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        width = os.get_terminal_size().columns
        message = "*** TinkerModellor Tinker System Reader Is Running ***"
        print("******************************************************".center(width))
        print(message.center(width))
        print("******************************************************".center(width))
        print('\n')

        result = func(*args, **kwargs)

        message = "***TinkerModellor Tinker System Reader Is Finished ***"
        print("******************************************************".center(width))
        print(message.center(width))
        print("******************************************************".center(width))
        print('\n')
        return result

    return wrapper