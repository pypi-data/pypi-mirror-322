#coding:UTF-8

import os
import inspect
import numpy as np
import platform
import ctypes

def load_lib():
    platf = platform.system().lower()
    print("Platform :", platf)

    lib_path = os.path.dirname(inspect.stack()[0].filename)+'/lib/'
    #print(lib_path)
    #import glob
    #name = glob.glob(lib_path+'*%s.so' % platf)
    #print(name)

    lib_name = 'testlib-%s.so' % platf
    print("Libname  :", lib_name)

    #>> Load library using ctypes
    #lib = ctypes.cdll.LoadLibrary(lib_path+lib_name)
    #>> Load library using numpy
    lib = np.ctypeslib.load_library(lib_name, lib_path)

    print('library loading was done.')
    #func = lib.libtest
    #func()
    #lib.libtest()
    return lib

