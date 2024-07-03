import os
import functools

def TKMDeleteReminder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # A try-except block to avoid any unexceptions that may occur during the call to os.get_terminal_size()
        # Due to pytest not being able to process os.get_terminal_size() 
        # OSError: [Errno 25] Inappropriate ioctl for device
        try:width = os.get_terminal_size().columns
        except:width = 120
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