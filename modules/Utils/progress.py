# The MIT License (MIT)
# Copyright (c) 2016 Vladimir Ignatev
#
# Permission is hereby granted, free of charge, to any person obtaining 
# a copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the Software 
# is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included 
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
# PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE
# FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT
# OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import sys


def progress(count, total, status=''):
    red='\033[01;31m'
    gre='\033[02;32m'
    yel='\033[00;33m'
    blu='\033[01;34m'
    
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    
    percentage = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    
    if percentage <= 50:
        col = red
    elif percentage > 50 and percentage <= 80:
        col = yel
    elif percentage > 80 and percentage <= 99:
        col = gre
    else:
        col = blu
    
    sys.stdout.write('\r{0}[{1}] {2}%  {3}'.format(col, bar, percentage, status))
    sys.stdout.flush()