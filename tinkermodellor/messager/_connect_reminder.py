import os
import functools

def TKMConnectReminder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        width = os.get_terminal_size().columns
        message = "********* TinkerModellor is Connecting Atoms *********"
        print("******************************************************".center(width))
        print(message.center(width))
        print("******************************************************".center(width))
        print('\n')

        result = func(*args, **kwargs)

        message = "****** TinkerModellor Connecting Atoms Is Done *******"
        print("******************************************************".center(width))
        print(message.center(width))
        print("******************************************************".center(width))
        print('\n')
        return result

    return wrapper