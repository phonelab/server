import re

"""
Human Sorting
http://nedbatchelder.com/blog/200712/human_sorting.html
Sort log file name by time order

@date 02/20/2012

@author Kate Rhodes
@adder Taeyeon Ki
"""
"""
def tryint(s):
    try: 
        return int(s)
    except:
        return s
""" 
def alphanum_key(s):
    """ Turn a string into a list of string and number chunks.
        "z23a" -> ["z", 23, "a"]
    """
    return [int(c) if c.isdigit() else c for c in re.split('([0-9]+)', s) ] 

def sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)

def re_sort_nicely(l):
    """ Sort the given list in the way that humans expect.
    """
    l.sort(key=alphanum_key)
    l.reverse()

"""
Login and Logout function to control session

@date 03/05/2012

@author Taeyeon Ki
"""

def login(request):
  request.session[' ']
  return HttpResponse

def logout(request):
  del request.session[' ']
  return 
