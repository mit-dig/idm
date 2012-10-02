#!/usr/bin/env python

import sys

import cgi
import cgitb
cgitb.enable()

import StringIO
from idm_query_functions import fetch_person_info

form = cgi.FieldStorage()
if form.has_key("username"):

	username = form.getvalue("username")
	if form.has_key("test_qa"):
		use_test_webservice = True
	else:
		use_test_webservice = False
	print "Content-type: text/html"
	print

	print "<html><head><title>IdM Demo</title><link rel='stylesheet' type='text/css' href='css/output.css' /></head><body> <img src='./img/idm_header_logo.png' alt='IDM' width='450' height='70'/> <br/> <br/> <br/><table>"
	
	g = fetch_person_info(username, use_test_webservice)

	for s, p, o in g:
		if str(p) != "http://www.w3.org/1999/02/22-rdf-syntax-ns#type":
			print "<tr>" + "<td><a href='" + p + "'>" + p.replace("urn:test:idmanagement.gov:icam:attribute:v1:","") + "</a></td>" + "<td><a href='" +  o + "'>" +  o.replace("file:///afs/csail.mit.edu/group/dig/www/data/2012/DHS/IdMTest/", "")+ "</a></td></tr>"
	
	print "</table></body></html>"



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

