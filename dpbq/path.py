# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
from __future__ import unicode_literals

import os
import re


# Module API

def dataset2package(path):
    path = path.replace('__', os.path.sep)
    path += '.csv'
    return path


def package2dataset(path):
    path = os.path.splitext(path)[0]
    path = path.replace(os.path.sep, '__')
    path = re.sub('[^0-9a-zA-Z_]+', '_', path)
    return path
