import urllib2
import sys

from lxml.etree import Element, SubElement, tostring
import xml.etree.ElementTree as ET
import lxml.etree
from decrypt import run_test_scenario
import datetime
from rdflib.graph import Graph
from rdflib.term import URIRef, Literal
from rdflib.namespace import Namespace, RDF
import hashlib
import base64
import OpenSSL

def make_soap_file(distinguished_name):

	#	print soap_request_user
	#        name = "CN=Geordi LaForge + UID=9000000006"
	#        OU = ["OU=People", "OU=FEMA", "OU=Directorate of Homeworld Security"]
	#        O = "O=Starfleet"
	#        C = "C=UFP"
	
	envelope = ET.Element("soapenv:Envelope", {"xmlns:saml":"urn:oasis:names:tc:SAML:2.0:assertion", 
				"xmlns:samlp":"urn:oasis:names:tc:SAML:2.0:protocol",
				"xmlns:soapenv":"http://schemas.xmlsoap.org/soap/envelope/"})
	
	
	headerTag = ET.SubElement(envelope, 'soapenv:Header')
	bodyTag = ET.SubElement(envelope, 'soapenv:Body')
	now = datetime.datetime.now()
	issueInstant = now.strftime("%Y-%m-%dT%H:%M:%SZ")	
	
	attributeQuery = ET.SubElement(bodyTag, 'samlp:AttributeQuery',
	                        {"Destination":"urn:test:idmanagement.gov:icam:bae:v2:starfleet",
	                         "ID":"_soapui449590",
	                         "IssueInstant":issueInstant,
	                         "Version":"2.0"})
	issuer = ET.SubElement(attributeQuery, 'saml:Issuer')
	issuer.text = 'urn:test:idmanagement.gov:icam:bae:v2:MIT_DP'
	
	#TODO add ds signature in for authentication
	#signature = SubElement(attributeQuery, 'ds:Signature')
	
	subject = ET.SubElement(attributeQuery, 'saml:Subject')
	
	nameID = ET.SubElement(subject, 'saml:NameID', {'Format':"urn:oasis:names:tc:SAML:1.1:nameid-format:X509SubjectName"})
	
	nameID.text = distinguished_name
	
	return ET.tostring(envelope)

def make_soap_file_QA(distinguished_name):
	
	# Namespace Declaration
	SAML_NS = "urn:oasis:names:tc:SAML:2.0:assertion"
	SAML = "{%s}" % SAML_NS
	SAMLP_NS = "urn:oasis:names:tc:SAML:2.0:protocol"
	SAMLP = "{%s}" % SAMLP_NS
	SOAPENV_NS = "http://schemas.xmlsoap.org/soap/envelope/"
	SOAPENV = "{%s}" % SOAPENV_NS
	DS_NS = "http://www.w3.org/2000/09/xmldsig#" 
	DS = "{%s}" % DS_NS
	WSU_NS = "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-utility-1.0.xsd"
	WSU = "{%s}" % WSU_NS
	WSSE_NS = "http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd"
	WSSE = "{%s}" % WSSE_NS
	
	# Create outermost soap envelope with namespace map
	envelope = Element(SOAPENV + "Envelope", nsmap={"soapenv":SOAPENV_NS})
	
	# We don't fill header here yet until soapenv:Body is populated
	headerTag = SubElement(envelope, SOAPENV + "Header")
	
	# Create soap body and populate with sub elements
	bodyTag = SubElement(envelope, SOAPENV + "Body", {WSU+"Id":"id-soap-body"}, nsmap={"wsu":WSU_NS})
	now = datetime.datetime.now()
	issueInstant = now.strftime("%Y-%m-%dT%H:%M:%SZ")	
	
	attributeQuery = SubElement(bodyTag, SAMLP + "AttributeQuery", 
								{"Destination":"urn:test:idmanagement.gov:icam:bae:v2:starfleet",
								"ID":"_soapui449590",
								"IssueInstant":issueInstant,
								"Version":"2.0",
								WSU+"Id":"id-sampl-attribute-query"},
								nsmap={"sampl":SAMLP_NS, "saml":SAML_NS})
	
	issuer = SubElement(attributeQuery, SAML + 'Issuer')
	issuer.text = 'urn:test:idmanagement.gov:icam:bae:v2:MIT_DP'
	
	subject = SubElement(attributeQuery, SAML + 'Subject')
	
	nameID = SubElement(subject, SAML + 'NameID', Format="urn:oasis:names:tc:SAML:1.1:nameid-format:X509SubjectName")
	
	nameID.text = distinguished_name
	
	# Calculate digest value for Enveloped Signature of samlp:AttributeQuery
	digest = hashlib.sha1()
	digest.update(lxml.etree.tostring(attributeQuery, method='c14n', exclusive=True, with_comments=False))
	digest_value = base64.b64encode(digest.digest())
	
	# Prepare the ds:signature and insert digest_value 
	signature = SubElement(attributeQuery, DS + "Signature", nsmap={"ds":DS_NS})
	signedInfo = SubElement(signature, DS + "SignedInfo")
	canonicalizationMethod = SubElement(signedInfo, DS + "CanonicalizationMethod", Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#")
	signatureMethod = SubElement(signedInfo, DS + "SignatureMethod", Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1")
	reference = SubElement(signedInfo, DS + "Reference", URI="#id-sampl-attribute-query")
	transforms = SubElement(reference, DS + "Transforms")
	transform1 = SubElement(transforms, DS + "Transform", Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#")
	transform2 = SubElement(transforms, DS + "Transform", Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature")
	digestMethod = SubElement(reference, DS + "DigestMethod", Algorithm="http://www.w3.org/2000/09/xmldsig#sha1")
	digestValue = SubElement(reference, DS + "DigestValue")
	digestValue.text = digest_value
	
	# Get private key from pfx file stored on disk
	f = open('MIT_DP.pfx')
	pfx = f.read()
	f.close()
	f = open('passwords.txt', 'r')
	enc_password = f.read()
	f.close()
	password = base64.b64decode(enc_password)
	pkcs12 = OpenSSL.crypto.load_pkcs12(pfx, password)
	privatekey = pkcs12.get_privatekey()
	
	# Calculate signature value from SignedInfo Element then insert into ds:signature
	canonicalized_signedInfo = lxml.etree.tostring(signedInfo, method='c14n', exclusive=True, with_comments=False)
	signature_value = base64.b64encode(OpenSSL.crypto.sign(privatekey, canonicalized_signedInfo, "sha1"))
	signatureValue = SubElement(signature, DS + "SignatureValue")
	signatureValue.text = signature_value
	
	# Insert KeyInfo into ds:signature
	keyInfo = SubElement(signature, DS + "KeyInfo")
	securityTokenReference = SubElement(keyInfo, WSSE + "SecurityTokenReference", nsmap={"wsse":WSSE_NS})
	key_reference = SubElement(securityTokenReference, WSSE + "Reference", URI="#id-binary-security-token", ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3")
	
	# Now we insert proper security tags into the Header
	security = SubElement(headerTag, WSSE + "Security", {SOAPENV+"mustUnderstand":"1"}, nsmap={"wsse":WSSE_NS, "wsu":WSU_NS})
	timestamp = SubElement(security, WSU + "Timestamp", {WSU+"Id":"id-timestamp"})
	created = SubElement(timestamp, WSU + "Created")
	created.text = issueInstant
	
	# Get the certificate in der format
	cert = pkcs12.get_certificate()
	der = base64.b64encode(OpenSSL.crypto.dump_certificate(OpenSSL.crypto.FILETYPE_ASN1, cert))
	binarySecurityToken = SubElement(security, WSSE + "BinartySecurityToken", 
									{"EncodingType":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-soap-message-security-1.0#Base64Binary",
									 "ValueType":"http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3",
									 WSU+"Id":"id-binary-security-token"})
	binarySecurityToken.text = der
	
	# Now create the 2 detached signatures, one for the timestamp, the other for soapBody
	d_signature = SubElement(security, DS + "Signature", nsmap={"ds":DS_NS})
	d_signedInfo = SubElement(d_signature, DS + "SignedInfo")
	d_canonicalizationMethod = SubElement(d_signedInfo, DS + "CanonicalizationMethod", Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#")
	d_signatureMethod = SubElement(d_signedInfo, DS + "SignatureMethod", Algorithm="http://www.w3.org/2000/09/xmldsig#rsa-sha1")
	d_reference1 = SubElement(d_signedInfo, DS + "Reference", URI="#id-timestamp")
	d_transforms1 = SubElement(d_reference1, DS + "Transforms")
	d_transform1 = SubElement(d_transforms1, DS + "Transform", Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#")
	d_digestMethod1 = SubElement(d_reference1, DS + "DigestMethod", Algorithm="http://www.w3.org/2000/09/xmldsig#sha1")
	d_digestValue1 = SubElement(d_reference1, DS + "DigestValue")
	
	# Digest the timestamp and insert
	digest = hashlib.sha1()
	digest.update(lxml.etree.tostring(timestamp, method='c14n', exclusive=True, with_comments=False))
	d_digestValue1.text = base64.b64encode(digest.digest())
	
	# Continue to create second digest tag for soap body
	d_reference2 = SubElement(d_signedInfo, DS + "Reference", URI="#id-soap-body")
	d_transforms2 = SubElement(d_reference2, DS + "Transforms")
	d_transform2 = SubElement(d_transforms2, DS + "Transform", Algorithm="http://www.w3.org/2001/10/xml-exc-c14n#")
	d_digestMethod2 = SubElement(d_reference2, DS + "DigestMethod", Algorithm="http://www.w3.org/2000/09/xmldsig#sha1")
	d_digestValue2 = SubElement(d_reference2, DS + "DigestValue")
	
	# Digest soap body and insert
	digest = hashlib.sha1()
	digest.update(lxml.etree.tostring(bodyTag, method='c14n', exclusive=True, with_comments=False))
	d_digestValue2.text = base64.b64encode(digest.digest())
	
	# Calculate signature value from Detached SignedInfo Element then insert into detached ds:signature
	d_canonicalized_signedInfo = lxml.etree.tostring(d_signedInfo, method='c14n', exclusive=True, with_comments=False)
	d_signature_value = base64.b64encode(OpenSSL.crypto.sign(privatekey, d_canonicalized_signedInfo, "sha1"))
	d_signatureValue = SubElement(d_signature, DS + "SignatureValue")
	d_signatureValue.text = d_signature_value
	
	# Insert KeyInfo into detached ds:signature
	d_keyInfo = SubElement(d_signature, DS + "KeyInfo")
	d_securityTokenReference = SubElement(d_keyInfo, WSSE + "SecurityTokenReference")
	d_key_reference = SubElement(d_securityTokenReference, WSSE + "Reference", URI="#id-binary-security-token", ValueType="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-x509-token-profile-1.0#X509v3")
	
	#print tostring(envelope, pretty_print=True)
	return tostring(envelope)

def fetch_person_info(distinguished_name, use_test_webservice=False):
	if (use_test_webservice):
			soap_body = make_soap_file(distinguished_name)
			if soap_body == None: #There was an error in the request
				return None
			req = urllib2.Request(url='https://aplgig-xml.jhuapl.edu/ICAM/BAE/ExternalBAEService/v2.0/TEST', data=soap_body)
	else:
		soap_body = make_soap_file_QA(soap_request) #Change this depending on the soap request
		if soap_body == None: #There was an error in the request
			return None
		req = urllib2.Request(url='https://aplgig-xml.jhuapl.edu/ICAM/BAE/ExternalBAEService/v2.0/QA', data=soap_body)
	
	req.add_header('Content-Type', 'text/xml')
	resp = urllib2.urlopen(req)
	content = resp.read()
	
	decrypted_content = run_test_scenario(content)
	
	rdf_output = xml_to_RDF(decrypted_content)
	
	return rdf_output

def xml_to_RDF(xml_string):
	
	root = ET.fromstring(xml_string);
	
	store = Graph()
	
	# Bind a few prefix, namespace pairs.
	store.bind("dc", "http://http://purl.org/dc/elements/1.1/")
	store.bind("foaf", "http://xmlns.com/foaf/0.1/")
	
	# Create a namespace object for the Friend of a friend namespace.
	FOAF = Namespace("http://xmlns.com/foaf/0.1/")
	
	# Create an identifier to use as the subject for Donna.
	user = URIRef("#me")
	
	# Add triples using store's add method.
	store.add((user, RDF.type, FOAF["Person"]))
	
	for child in root:
		if "AttributeStatement" in child.tag:
			for child1 in child:
				for child2 in child1:
					if child1.attrib.get("Name") in ("urn:test:idmanagement.gov:icam:attribute:v1:designatedRole", "urn:test:idmanagement.gov:icam:attribute:v1:organizationName", "urn:test:idmanagement.gov:icam:attribute:v1:organizationUnitName", "urn:test:idmanagement.gov:icam:attribute:v1:givenName"):
						store.add((user, URIRef(child1.attrib.get("Name")),Literal(child2.text)))
					else:
						store.add((user, URIRef(child1.attrib.get("Name")),child2.text))
	
	rdf_output = store.serialize()
	
	return store

#Soap Request is a number 0-4 which sends the request for that person
#def fetch_person_info2(soap_request):
#        if soap_request < 0 or soap_request > 4:
#                return "ERROR: INVALID QUERY RANGE"
#	char_list = ["soap-jp.xml", "soap-gf.xml", "soap-dt.xml", "soap-bc.xml", "soap-wr.xml"]
#
#	fname = char_list[character]
#	#print 'querying for ', fname
#	f = open(fname)
#	soap_body = f.read()
#    
#	req = urllib2.Request(url='https://aplgig-xml.jhuapl.edu/ICAM/BAE/ExternalBAEService/v2.0/TEST', data=soap_body)
#	req.add_header('Content-Type', 'text/xml')
#	resp = urllib2.urlopen(req)
#	content = resp.read()
#	decrypted_content = run_test_scenario(content)
#	return content

def main():
	full_distinguished_name = "CN=Deanna Troi + UID=9000000004,OU=People,OU=DHS HQ,OU=Directorate of Homeworld Security,O=Starfleet,C=UFP"
	print fetch_person_info(full_distinguished_name, True)
	return

if __name__ == "__main__":
	main()
