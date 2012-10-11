#!/usr/bin/python
"""
Extract XMP metadata from JPEG and PDF files. The trick to extract the RDF content is based on
using a regular expression on the whole file (seen as a string). The idea of using regexp that way
for the purpose of XMP extraction came from U{Sean B. Palmer<http://purl.org/net/sbp/>} and 
U{Dan Brickley<mailto:danbri@w3.org>}.

Testing the file type is crude. A more sophisticated file type or
preferably, a more general library for all types of files to extract the XMP content would be way 
better at some point...

@author: Ivan Herman
"""
debug = True
import re,os,imghdr

def _searchXMLContent(b, uri) :
	"""
	Extract the XMP content from the byte stream, using a regular expression search
	@param b: byte stream of the image content
	@return: RDF data as a string
	@rtype: string
	"""
	rdfpat = r"(?sm)^.*(<rdf:RDF.*</rdf:RDF>)"
	r_rdf = re.compile(rdfpat)
	q = r_rdf.search(b)
	assert q != None, "Could not find the XMP content in the file"

        # to fix the <rdf:Description rdf:about=""> prob
        # LK 12/9/09 
        xmp = q.group(1)
        p = re.compile( 'rdf:about=""')
        replace_str = 'rdf:about="'+uri+'"'
        m = p.sub( replace_str, xmp)
        return m

def _testFile(fname) :
	"""Test whether the file is of a format that can have an XMP information.
	The test is based on the imghdr library of python. However, that library is not 
	foolproof, unfortunately, I have hit JPG files that are not recognized by imghdr while
	understood by all the usual image programs (I wonder whether this is related to Photoshop CS2,
	I have not seen such problems before). Consequently, if the imghdr test fails, the suffix of
	the file is also considered and the following suffixes are also updated as candidates: 'jpg', 'jpeg', 'JPG', 'JPEG',
	'pdf', 'PDF'. 
	
	I realize this is not really kosher, but I am not in the mood to debug imghdr (besides, pdf files are not
	considered at all by that one...)
	
	@param fname: the filename for the image or the pdf file
	@return: whether the file is of a proper format
	@rtype: Boolean
	"""
	suffixes = ['jpg','jpeg','pdf']
	hdr = imghdr.what(fname)
	if hdr == None or hdr != 'jpeg' :
		for sfx in suffixes :
			if fname.lower().endswith(sfx) :
				return True
		# if we got here then, unfortunately, this is not a valid file type
		return False
	else:
		return True
	
def extractXMPFromURI(uri) :
	"""Extract the XML RDF data for PDF and JPG files based on a URI, and return it as a string
	@param uri: the URI for the image
	@type uri: string
	@return: RDF data as a string
	@rtype: string
	"""
	import urllib2
	obj = urllib2.urlopen(uri)
	inf = obj.info()
	ftype = inf["content-type"].split(";")[0].strip()
	if ftype == "image/jpeg" or ftype == "application/pdf" :
		length =  int(inf["content-length"])
		p = obj.read(length)
		return _searchXMLContent(p, uri)		
	else :
		raise "Cannot manage this file type: %s" % ftype

def extractXMP(fname) :
	"""Extract the XMP RDF data for PDF and JPG files and return it as a string
	@param fname: the filename for the image or the pdf file
	@type fname: string	
	@return: RDF data as a string
	@rtype: string
	"""
	if _testFile(fname) :
		f = file(fname,'rb')
		return _searchXMLContent(f.read(), fname)
	else :
		raise "Unknown FileType", "Cannot manage this file type"
		
	
def extractXMPTriples(fname,triples = None) :
	"""Extract the XMP RDF data for PDF and JPG files and return and RDFLib triple store. If the
	triples parameter is not None, then it is considered to be an already existing triple store that
	has to be extended by the new set of triples.

	@param fname: the filename for the image or the pdf file
	@type fname: a string, denoting the file name
	@param triples: an RDFLib TripleStore (default: None)
	@type triples: rdflib.TripleStore	
	@return: triples
	@rtype: RDFLib TripleStore
	"""
	rdf = extractXMP(fname)
	# If it is at that point, no exception has been raised, ie, the rdf content exists
	#
	# Note the import here, not in the header; the module should be usable without RDFLib, too...
	from rdflib.TripleStore import TripleStore
	if triples == None :
		triples = TripleStore()
	# The logical thing to do would be to wrap rdf into a StringIO and load it into the triples
	# but that does not work with TripleStore, which expects a file name (or I have not found other means)
	# Ie, the rdf content should be stored in a temporary file. 
	tempfile = fname + "__.rdf"
	store = file(tempfile,"w")
	store.write(rdf)
	store.flush()
	store.close()
	triples.load(tempfile)
	try :
		# on Windows this may not work...
		os.remove(tempfile)
	except :
		# This works only when called from cygwin. However, is there anybody in his/her able mind
		# using Windows and python without some sort of a unix emulation ;-)
		os.system("rm %s" % tempfile)
	return triples
	
####################################################################################################
if __name__ == '__main__' :
	import sys
	if len(sys.argv) > 1 :
		fname = sys.argv[1]
	else :
		fname = "http://people.csail.mit.edu/oshani/test/test.pdf"
	triples = extractXMPFromURI(fname)
	print triples
	

