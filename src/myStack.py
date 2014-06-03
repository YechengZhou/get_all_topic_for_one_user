# -*- coding: utf-8 -*-
"""
author: yecheng zhou
description:
    this is a self-made stack...
"""

class myStack():

    def __init__(self,size = 1000):
        self.stack = []
        self.top = -1
        self.maxsize = size
        self.size = 0

    def index(self,n):
        return self.stack[n]

    def is_full(self):
        return len(self.stack) == self.maxsize

    def is_empty(self):
        return len(self.stack) == 0

    def setSize(self, size):
        self.size = size

    def getSize(self):
        return self.size

    def push(self,data):
        if self.is_full():
            for i in self.stack:
                print i
            raise Exception,"This stack is full"
        else:
            self.stack.append(data)
            self.top += 1
            self.size = self.top + 1

    def pop(self):
        if self.is_empty():
            raise Exception,"This stack is empty"
        else:
            data = self.stack[-1]
            self.top -= 1
            self.size = self.top + 1
            del self.stack[-1]
            return data

    def Top(self):
        return self.top

    def empty(self):
        self.stack = []
        self.top = -1

    def __str__(self):
        temp_l = []
        for i in self.stack:
            temp_l.append(i)
        return '\n'.join(temp_l)


if __name__ == '__main__':
    s = myStack()
    s.push(1)
    print s.pop()
    s.pop()