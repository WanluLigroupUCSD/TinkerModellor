import os
import functools

def TKMDeleteReminder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #set a default width , in case of the terminal size is not available
        try:
            width = os.get_terminal_size().columns
        except:
            width = 120
        message = "********** TinkerModellor is Deleting Atoms **********"
        print("******************************************************".center(width))
        print(message.center(width))
        print("******************************************************".center(width))
        print('\n')

        result = func(*args, **kwargs)

        message = "******* TinkerModellor Deleting Atoms Is Done ********"
        print("******************************************************".center(width))
        print(message.center(width))
        print("******************************************************".center(width))
        print('\n')
        return result

    return wrapper