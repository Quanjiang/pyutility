#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2018 wesure.cn, Inc. All Rights Reserved
# author: QuanJiang (studentol<a>163.com) 2019-1-4
from __future__ import (absolute_import, division,print_function, unicode_literals)
from builtins import (
         bytes, dict, int, list, object, range, str,
         ascii, chr, hex, input, next, oct, open,
         pow, round, super,
         filter, map, zip)
from pyutility.ResPool import MDResPool
import time
class A:
    def run(self,*argv, **kwargs):
        print( *argv, **kwargs)
    
def createA():
    return A()

# pool_size = 2, max_overload = -1 (infinit), timeout = 2s
a = MDResPool(2,0,2)
a.set_generate_func(createA) # set connection power

m = {}
for ii in range(0, 50):
    m[ii] = a.connect()
    a.update_res()
    m[ii].run('xxx','xx','xxx') # call class A's run()
    print(m[ii].id)
    m[ii].close()
c1 = a.connect()
c1.run('xx')
c1.close()
c2 = a.connect()
c2.run('xx1')
c2.close()
print(len(a.core_pools_unuse),len(a.core_pools_inuse))


class B:
    def __del__(self):
        print('退出啦')
    def run(self):
        print('--')
        return 'xx'

    def __getattr__(self, item):
        return print

def test():
    a = B()
    return a

a = test()
# print(a)
a.xx('xx1')
time.sleep(3)
