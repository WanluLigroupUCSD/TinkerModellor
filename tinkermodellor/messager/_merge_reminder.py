import os
import functools

def TKMMergeReminder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #set a default width , in case of the terminal size is not available
        try:
            width = os.get_terminal_size().columns
        except:
            width = 120
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