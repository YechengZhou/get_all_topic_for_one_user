__author__ = 'Yecheng'

import sys

def get_cur_func():
    try:
        raise Exception
    except:
        f = sys.exc_info()[2].tb_frame.f_back
    return (f.f_code.co_name, f.f_lineno)

def callfunc():
    print get_cur_func()

if __name__ == '__main__':
    callfunc()