import os
import functools

def TKMMergeReminder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        width = os.get_terminal_size().columns
        message = "******** TinkerModellor is Merging Two System ********"
        print("******************************************************".center(width))
        print(message.center(width))
        print("******************************************************".center(width))
        print('\n')

        result = func(*args, **kwargs)

        message = "***** TinkerModellor Merging Two System Is Done ******"
        print("******************************************************".center(width))
        print(message.center(width))
        print("******************************************************".center(width))
        print('\n')
        return result

    return wrapper