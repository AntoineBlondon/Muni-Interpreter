import os
import sys
import requests
import json

current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from muni_types import *


def get(url, headers=None, params=None, data=None, timeout=10):
    return Muni_List(json.loads(requests.get(url, headers=headers, params=params, data=data, timeout=timeout).text))