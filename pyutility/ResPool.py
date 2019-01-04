#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2018 wesure.cn, Inc. All Rights Reserved
# author: QuanJiang (studentol<a>163.com) 2019-1-4


import time
import threading


class MDResPool:
    ''' 抽象的资源池概念
    '''
    class MDRes:
        def __init__(self,pool_obj,id, obj):
            ''' 抽象出来的系统资源
            
            '''
            self.pool_obj = pool_obj
            self.obj = obj
            self.id = id
            self._is_close_already = False

        def __getattr__(self, item):
            return getattr(self.obj,item)
        
        def close(self):
            if self._is_close_already:
                return
            self.pool_obj.close(self.id)
            self._is_close_already = True

        def __del__(self):
            if self._is_close_already:
                return
            self.pool_obj.close(self.id)
            self._is_close_already = True

    def __init__(self, pool_size=5,max_overflow=1, timeout = None):
        '''
        '''
        self.pool_size = pool_size
        self.max_overflow = max_overflow
        self.timeout = timeout
        self.lock =  threading.Lock()
        self.core_pools = {
            'key': {
                'status': 0,
                'wish_close': 0, # 标记是否下次关闭
                'obj': None, # 实际的对象

            }
        }
        self.core_pools_inuse = {}
        self.core_pools_unuse = []
    
    def set_generate_func(self,target=None, args=(),kwargs={}):
        self.gunerate_func = target
        self.gunerate_func_args = args
        self.gunnerate_func_kwargs = kwargs
    

    def connect(self):
        # 判断当前的使用数量
        endtime = self.timeout + time.time()
        while True and self.timeout is not None:
            remaining = endtime - time.time()
            if remaining <= 0.0:
                raise Exception('获取连接超时')
            
            self.lock.acquire()
            isNew = None
            len_unuse = len(self.core_pools_unuse)
            len_inuse = len(self.core_pools_inuse)
            if len_unuse > 0:
                isNew = False
            elif self.pool_size == 0:
                    isNew = True
            else:
                if len_inuse < self.pool_size:
                    isNew = True
                elif self.max_overflow == -1:
                    isNew = True
                elif (self.pool_size + self.max_overflow) - len_inuse >0:
                    isNew = True

            if isNew is None:
                self.lock.release()
                time.sleep(1)
                continue
            
            if isNew:
                obj = self.gunerate_func(*self.gunerate_func_args,** self.gunnerate_func_kwargs)
                id = str(int(time.time()*1000000))
                self.core_pools[id] = {}
                self.core_pools[id]['status'] = 1
                self.core_pools[id]['wish_close']  = 0
                self.core_pools[id]['obj'] = obj
                self.core_pools_inuse[id] = ''
            else:
                id = self.core_pools_unuse.pop()
                obj = self.core_pools[id]['obj']
                self.core_pools[id]['status'] = 1
                self.core_pools_inuse[id] = ''
            self.lock.release()
            break

        return MDResPool.MDRes(self,id, obj)
    
    def close(self, id):
        if id not in self.core_pools or id not in self.core_pools_inuse:
            raise  Exception('资源已经关闭或失效')
        self.lock.acquire()
        self.core_pools_inuse.pop(id)
        if self.core_pools[id]['wish_close'] == 1 or len(self.core_pools_inuse) > self.pool_size:
            del(self.core_pools[id]['obj'])
            self.core_pools.pop(id)
        else:
            self.core_pools[id]['status'] = 0
            self.core_pools_unuse.append(id)
        self.lock.release()

    def update_res(self,target=None, args=(),kwargs={}):
        ''' 用来热更新
        '''
        if target is not None:
            self.gunerate_func = target
        if args != ():
            self.gunerate_func_args = args
        if kwargs != {}:
            self.gunnerate_func_kwargs = kwargs
        
        self.lock.acquire()
        for key in self.core_pools:
            self.core_pools[key]['wish_close'] = 1
        self.lock.release()