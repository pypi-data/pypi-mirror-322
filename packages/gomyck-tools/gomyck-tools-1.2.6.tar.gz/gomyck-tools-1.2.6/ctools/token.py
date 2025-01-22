#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'haoyang'
__date__ = '2025/1/21 16:01'

import time
import jwt

from ctools.dict_wrapper import DictWrapper

def gen_token(payload: {}, secret_key, expired: int=3600) -> str:
  payload.update({'exp': time.time() + expired})
  return jwt.encode(payload, secret_key, algorithm='HS256')

def get_payload(token, secret_key):
  try:
    payload = jwt.decode(token, secret_key, algorithms=['HS256'])
    return DictWrapper(payload)
  except Exception as e:
    return None

# if __name__ == '__main__':
#   token = gen_token({"xx": 123}, '123')
#   xx = get_payload(token, '123')
#   print(xx.xx)
