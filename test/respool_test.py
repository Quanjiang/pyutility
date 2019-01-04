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

class A:
    def run(self,*argv, **kwargs):
        print( *argv, **kwargs)
    
def createA():
    return A()

# pool_size = 2, max_overload = -1 (infinit), timeout = 2s
a = MDResPool(2,-1,2)
a.set_generate_func(createA) # set connection power

m = {}
for ii in range(0, 50):
    m[ii] = a.connect()
    m[ii].run('xxx','xx','xxx') # call class A's run()
    print(m[ii].id)
    m[ii].close()
print(len(a.core_pools_unuse))
