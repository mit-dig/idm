#!/usr/bin/python

import cgi
import cgitb
from xmp import *

cgitb.enable()

def main():

    form = cgi.FieldStorage()
    uri = form.getvalue("uri" , "")

    print "Content-type:application/rdf+xml\n"
    xmp = extractXMPFromURI(uri)
    
    print xmp
    
if __name__ == "__main__":
  main()
