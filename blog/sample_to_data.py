

# -*- coding: utf-8 -*-
import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

#import sys
#import importlib
#importlib.reload

from konlpy.tag import Twitter

def sample_to_data(input):
    twitter =Twitter()
    string=""
    for word,tag in twitter.pos(input):
        if(tag=="Noun"):
            if(len(word) > 1):
                string=string+word+" "

    return string

#print(sample_to_data("문장분류프로그램"))
