# -*- coding: utf-8 -*-

import os

def ensure_parent_dir_exist(filepath: str):
    os.makedirs(os.path.abspath(os.path.dirname(filepath)), exist_ok=True)
