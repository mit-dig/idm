#!/usr/bin/env python

import sys

import cgi
import cgitb
cgitb.enable()

from idm_query_functions import fetch_person_info

form = cgi.FieldStorage()
if form.has_key("cn"):
	# We need at least a common name
	dn = []
	for key in ("c", "st", "l", "o", "ou"):
		if form.has_key(key):
			for value in form.getlist(key):
				dn.append("%s=%s" % (key.upper(), value))
	for value in form.getlist("cn"):
		dn.append("CN=%s" % value)
	for key in ("t", "i", "g", "s", "d", "uid"):
		if form.has_key(key):
			for value in form.getlist(key):
				dn.append("%s=%s" % (key.upper(), value))
	if form.has_key("email"):
		for value in form.getlist("email"):
			dn.append("Email=%s" % value)
	
	print "Content-type: application/rdf+xml"
	print
	print fetch_person_info(", ".join(dn), use_test_webservice=True).serialize()

#	outfile = sys.stdout
#        username = form.getvalue("username")
#        outfile.write("Content-type: application/rdf+xml\n")
#	outfile.write(fetch_person_info(username))
#	sys.stdout = outfile

#	fetch_person_info(username)

#	f = open('idm_output.rdf', 'r')
#	f.write(fetch_person_info(username))
#	f.close()	

#	print "Location: http://dig.csail.mit.edu/2012/DHS/IdMTest/idm_output.rdf"

else:
        print "Content-type: text/html"
        print """
        <html>
        <body>
        <p>The response is:</p>"""
        print "<p>There was no input</p>"
        print """
        </body>
        </html>
        """

