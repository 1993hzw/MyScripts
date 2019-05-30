# coding=utf-8
import sys

if __name__ == '__main__':
    percent = float(sys.argv[1])
    print(hex(int(255 * percent + 0.5)))
