""" 
libary for checko.ru API functions.
Documentation: https://github.com/io451/pycheckoapi/wiki
Author: https://github.com/webcartel-https
"""
import os
import sys

current_py = sys.version_info[:2]
minimum_py = (3, 10)

if current_py < minimum_py: 
    print(f""" 
[pycheckoapi] Текущая версия Python не поддерживается.\n
[pycheckoapi] Ваша версия Python:{current_py}\n   
[pycheckoapi] Минимальная поддерживаемая версия: {minimum_py}      
[pycheckoapi] Пожалуйста, обновите версию Python и попробуйте снова""")

try:
    import requests
except ImportError:
    print("[pycheckoapi] Не удалось импортировать библиотеку requests, убедитесь, что она установлена.")

requests_vers = requests.__version__.split(".")[:2]
rq_integer = tuple(map(int,requests_vers))
if rq_integer < (2, 25):
    print("[pycheckoapi] Ваша версия requests не поддерживается.\nОбновите requests до последней версии!")

try:
    import pycheckoapi
    import pycheckoapi.api
    import pycheckoapi.exceptions as exceptions
    import pycheckoapi.link
except ImportError as IE:
    print(f"[pycheckoapi] Невозможно импортировать модули библиотеки.\nПодробнее: {repr(IE)}\nУбедитесь, что библиотека установлена корректно.")

from pycheckoapi.__version__ import (
    __author__,
    __author_email__,
    __version__,
    __url__,
    __description__,
    __title__  
)



