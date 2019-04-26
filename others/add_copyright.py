# coding=utf-8

import sys
from os import listdir
import os

COPYRIGHT = '''/*
 * Copyright (C) 2019  Ziwei Huang
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
 
'''


def transform_file(file_path):
    file = open(file_path, "r")
    content = file.read()
    file.close()

    file = open(file_path, "w")
    file.write(COPYRIGHT + content)
    file.close()


def transform_dir(dir_path):
    for name in listdir(dir_path):
        abspath = dir_path + os.sep + name
        if os.path.isdir(abspath):
            transform_dir(abspath)
        else:
            transform_file(abspath)


def main(path):
    if os.path.isdir(path):
        transform_dir(path)
    else:
        transform_file(path)


if __name__ == '__main__':
    main(sys.argv[1])
