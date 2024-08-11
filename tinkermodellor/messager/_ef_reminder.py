import os
import functools

def TKMEFGridReminder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #set a default width , in case of the terminal size is not available
        try:
            width = os.get_terminal_size().columns
        except:
            width = 120
        message = f"**** TinkerModellor Is Computing Electric Field ******"   
        message2 = "********************* Grid Task **********************"
        print("******************************************************".center(width))
        print(message.center(width))
        print(message2.center(width))
        print("******************************************************".center(width))
        print('\n')

        result = func(*args, **kwargs)

        message = f"****** TinkerModellor Electric Field Computing Is Done ********"
        print("******************************************************".center(width))
        print(message.center(width))
        print("******************************************************".center(width))
        print('\n')
        return result

    return wrapper

def TKMEFPointReminder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #set a default width , in case of the terminal size is not available
        try:
            width = os.get_terminal_size().columns
        except:
            width = 120
        message = "**** TinkerModellor Is Computing Electric Field ******"   
        message2 ="******************** Point Task **********************"
        print("******************************************************".center(width))
        print(message.center(width))
        print(message2.center(width))
        print("******************************************************".center(width))
        print('\n')

        result = func(*args, **kwargs)

        message = "**** TinkerModellor Is Computing Electric Field ******"   
        print("******************************************************".center(width))
        print(message.center(width))
        print("******************************************************".center(width))
        print('\n')
        return result

    return wrapper

def TKMEFBondReminder(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        #set a default width , in case of the terminal size is not available
        try:
            width = os.get_terminal_size().columns
        except:
            width = 120
        message =  "**** TinkerModellor Is Computing Electric Field ******"   
        message2 = "********************* Bond Task **********************"
        print("******************************************************".center(width))
        print(message.center(width))
        print(message2.center(width))
        print("******************************************************".center(width))
        print('\n')

        result = func(*args, **kwargs)

        message = "**** TinkerModellor Is Computing Electric Field ******" 
        print("******************************************************".center(width))
        print(message.center(width))
        print("******************************************************".center(width))
        print('\n')
        return result

    return wrapper