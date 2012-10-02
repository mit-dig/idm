#!/usr/bin/env python

import sys

import cgi
import cgitb
cgitb.enable()

import StringIO
from idm_query_functions import fetch_person_info

users = ["Geordi LaForge", "Deanna Troi", "William Riker", "Jean-Luc Picard", "Beverly Crusher", "Worf Rozhenko", "Lwaxana Troi", "Tam Elbrun"]

userDic = {"Geordi LaForge":"CN=Geordi LaForge + UID=9000000006,OU=People,OU=FEMA,OU=Directorate of Homeworld Security,O=Starfleet,C=UFP", 
	"Deanna Troi":"CN=Deanna Troi + UID=9000000004,OU=People,OU=DHS HQ,OU=Directorate of Homeworld Security,O=Starfleet,C=UFP",
	"William Riker":"CN=William Thomas Riker + UID=9000000003,OU=People,OU=DHS HQ,OU=Directorate of Homeworld",
	"Jean-Luc Picard":"CN=Jean Luc Picard + UID=9000000001,OU=People,OU=DHS HQ,OU=Directorate of Homeworld Security,O=Starfleet,C=UFP",
	"Beverly Crusher":"CN=Beverly Crusher + UID=9000000005,OU=People,OU=FEMA,OU=Directorate of Homeworld Security,O=Starfleet,C=UFP",
	"Worf Rozhenko": "CN=Worf Rozhenko + UID=9000000009,OU=People,OU=FEMA,OU=Directorate of Homeworld Security,O=Starfleet,C=UFP",
	"Lwaxana Troi":"CN=Lwaxana Troi + UID=8000000001,ou=People, ou=Betazed, o=Diplomatic Corps, C=UFP",
	"Tam Elbrun":"CN=Tam Elbrun + UID=8000000002,OU=People,OU=Betazed,O=Diplomatic Corps,C=UFP"
}

form = cgi.FieldStorage()
if form.has_key("username"):

	username = form.getvalue("username")
	fullname = userDic.get(username, "")
	if (fullname == ""):
		print "Content-type: text/html"
		print """
		<html>
		<body>
		<p>The response is:</p>"""
		print "<p>User not found</p>"
		print """
		</body>
		</html>
		"""
		sys.exit()
        
	if form.has_key("test_qa"):
		use_test_webservice = True
	else:
		use_test_webservice = True
	print "Content-type: text/html"
	print

	print "<html><head><title>IdM Demo</title><link rel='stylesheet' type='text/css' href='css/output.css' /></head><body> <img src='./img/idm_header_logo.png' alt='IDM' width='450' height='70'/> <br/> <br/> <br/><table>"
	
	g = fetch_person_info(fullname, use_test_webservice)

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

