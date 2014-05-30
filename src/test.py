__author__ = 'Yecheng'
"""
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

"""
T= int(raw_input())
test_list = []
for i in range(T):
    test_list.append(int(raw_input()))

def get_decent(num):
    y = 0 # times of 3 / 5
    x = num - 5*y # times of 5 / 3
    # 5*y + 3*x = num
    #found_flag = False
    while(5*y <= num):
        if (num - 5*y)%3 == 0:
           # found_flag = True
            return '5'*(num - 5*y) + '3'* y * 5
        else:
            #if
            y += 1
            x = num - 5*y

    return -1


for i in test_list:
    print get_decent(i)
