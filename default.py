import re

"""
Human Sorting
http://nedbatchelder.com/blog/200712/human_sorting.html
Sort log file name by time order

@date 02/20/2012

@author Kate Rhodes
@adder Taeyeon Ki
"""
def tryint(s):
    try: 
        return int(s)
    except:
        return s
     

def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [ tryint(c) for c in re.split('([0-9]+)', s) ] 

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)
