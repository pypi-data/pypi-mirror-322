#!/usr/bin/env python
# coding=utf-8
'''
brief        :  
Author       : knightdby knightdby@163.com
Date         : 2023-02-24 18:22:41
FilePath     : /manifast/manifast/import_pkg.py
Description  : 
LastEditTime : 2024-05-12 07:13:13
LastEditors  : knightdby
Copyright (c) 2023 by Inc, All Rights Reserved.
'''

import os
import re
import cv2
import sys
import math
import time
import json
import random
import shutil
import matplotlib
import numpy as np
import pandas as pd
from glob import glob
from tqdm import tqdm
from loguru import logger
import os.path as osp
from easydict import EasyDict as edict
from PIL import Image, ImageDraw
from multiprocessing import Pool
from argparse import ArgumentParser
import matplotlib.pyplot as plt
from easydict import EasyDict as edict
if not os.getcwd().split('\\')[-1].find('notebooks') == -1:
    os.chdir('../')
sys.path.append(os.getcwd())
