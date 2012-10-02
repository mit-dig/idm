import sys

import xml.etree.ElementTree
import OpenSSL.crypto
import Crypto.PublicKey.RSA, Crypto.Cipher.PKCS1_v1_5, Crypto.Cipher.AES
import getpass, base64

def decrypt_soap(soap, myCertificates):
    # Parse the SOAP with etree.
    tree = xml.etree.ElementTree.XML(soap)
    
    # Sanity check.
    if tree.tag != '{http://schemas.xmlsoap.org/soap/envelope/}Envelope':
        raise Exception('not a soapenv:Envelope!')
    
    # Ignore the soapenv:Header for now.
    
    # Dig into the saml2:EncryptedAssertion to get the encrypted data
    body = tree.find('{http://schemas.xmlsoap.org/soap/envelope/}Body')
    if body is None:
        raise Exception('could not find soapenv:Body')
    response = body.find('{urn:oasis:names:tc:SAML:2.0:protocol}Response')
    if response is None:
        raise Exception('could not find saml2:Response')
    assertion = response.find('{urn:oasis:names:tc:SAML:2.0:assertion}EncryptedAssertion')
    if assertion is None:
        raise Exception('could not find saml2:EncryptedAssertion')
    data = assertion.find('{http://www.w3.org/2001/04/xmlenc#}EncryptedData')
    if data is None:
        raise Exception('could not find xenc:EncryptedData')
    
    # Get the encryption method for the payload.
    method = data.find('{http://www.w3.org/2001/04/xmlenc#}EncryptionMethod')
    if method is None:
        raise Exception('could not find xenc:EncryptionMethod for xenc:EncryptedData')
    method = method.get('Algorithm')
    # TODO: This should choose an appropriate algorithm based on the method.
    if method != 'http://www.w3.org/2001/04/xmlenc#aes128-cbc':
        raise Exception('xenc:EncryptedData not encrypted with AES128-CBC')

    # Get the cipher data for the payload.
    cipherData = data.find('{http://www.w3.org/2001/04/xmlenc#}CipherData')
    if cipherData is None:
        raise Exception('could not find xenc:CipherData for xenc:EncryptedData')
    cipherValue = cipherData.find('{http://www.w3.org/2001/04/xmlenc#}CipherValue')
    if cipherValue is None:
        raise Exception('could not find xenc:CipherValue for xenc:EncryptedData')
    encryptedData = cipherValue.text

    # Get the encryption key for the payload.
    keyinfo = data.find('{http://www.w3.org/2000/09/xmldsig#}KeyInfo')
    if keyinfo is None:
        raise Exception('could not find ds:KeyInfo for xenc:EncryptedData')
    enckey = keyinfo.find('{http://www.w3.org/2001/04/xmlenc#}EncryptedKey')
    if enckey is None:
        raise Exception('could not find xenc:EncryptedKey')

    # Get the encryption method for the key.
    keymethod = enckey.find('{http://www.w3.org/2001/04/xmlenc#}EncryptionMethod')
    if keymethod is None:
        raise Exception('could not find xenc:EncryptionMethod for xenc:EncryptedKey')
    keymethod = keymethod.get('Algorithm')
    # TODO: This should choose an appropriate algorithm based on the method.
    if keymethod != 'http://www.w3.org/2001/04/xmlenc#rsa-1_5':
        raise Exception('xenc:EncryptedKey not encrypted with RSA')
    
    # Get the certificate subjectName for the certificate to use.
    enckeykeyinfo = enckey.find('{http://www.w3.org/2000/09/xmldsig#}KeyInfo')
    if enckeykeyinfo is None:
        raise Exception('could not find ds:KeyInfo for xenc:EncryptedKey')
    x509data = enckeykeyinfo.find('{http://www.w3.org/2000/09/xmldsig#}X509Data')
    if x509data is None:
        raise Exception('could not find ds:X509Data for xenc:EncryptedKey')
    subjectName = x509data.find('{http://www.w3.org/2000/09/xmldsig#}X509SubjectName')
    if subjectName is None:
        raise Exception('could not find ds:X509SubjectName for xenc:EncryptedKey')
    subjectName = subjectName.text
    subjectName = tuple(sorted(dict([x.split('=') for x in subjectName.split(', ')]).items()))
    if subjectName not in myCertificates:
        raise Exception('subjectName was not found in myCertificates')
    
    # Get the cipher data for the key.
    cipherData = enckey.find('{http://www.w3.org/2001/04/xmlenc#}CipherData')
    if cipherData is None:
        raise Exception('could not find xenc:CipherData for xenc:EncryptedKey')
    cipherValue = cipherData.find('{http://www.w3.org/2001/04/xmlenc#}CipherValue')
    if cipherValue is None:
        raise Exception('could not find xenc:CipherValue for xenc:EncryptedKey')
    cipherValue = cipherValue.text
    
    # This is as far as pyOpenSSL can get us.  To do decryption, we
    # invoke pycrypto using an inconvenient (and almost certainly
    # insecure) workaround to pass the private key between the two.

    
    key = myCertificates[subjectName].get_privatekey()
    pem = OpenSSL.crypto.dump_privatekey(OpenSSL.crypto.FILETYPE_PEM, key)
    key = Crypto.PublicKey.RSA.importKey(pem)
    

    # Now we can decrypt the key in the SOAP.
    # PKCS#1 v1.5 maybe?
    cipher = Crypto.Cipher.PKCS1_v1_5.new(key)
    sentinel = "blah"
    decryptedKey = cipher.decrypt(base64.b64decode(cipherValue), sentinel)

    # IV is the first 16 bytes of the encrypted data.
    encryptedData = base64.b64decode(encryptedData)
    iv = encryptedData[:16]
    encryptedData = encryptedData[16:]

    # Finally, we can decrypt the payload with the decrypted key.
    cipher = Crypto.Cipher.AES.new(decryptedKey,
                                   mode=Crypto.Cipher.AES.MODE_CBC,
                                   # Need some dummy IV I guess.
                                   IV=iv)
    data = cipher.decrypt(encryptedData)

    # Last byte says how many bytes of padding there were in the last block.
    if ord(data[-1]) <= 16:
        data = data[:-ord(data[-1])]
    return data


def run_test_scenario(soap = None):
    # Read the test SOAP response if there is no soap file inputted.
    if soap == None:
        f = open('TEST_response.txt')
        soap = f.read()
        f.close()
    
    # Read the certificate and add it to my personal certificates.
    myCertificates = {}
    # The PEM is unnecessary probably.
#    f = open('cert_MIT_DP.pem')
#    pem = f.read()
#    f.close()
#    cert = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, pem)
#    # Gotta normalize the subject name (since no guarantee that the
#    # SOAP will have the right order)
#    name = cert.get_subject().get_components()
#    knownCertificates[tuple(sorted(name))] = cert
    
    # Read the encrypted private key.
    f = open('MIT_DP.pfx')
    pfx = f.read()
    f.close()
    #print "READ PFX"
    try:
        pkcs12 = OpenSSL.crypto.load_pkcs12(pfx)
    except OpenSSL.crypto.Error:
        # Need a password.
        # Is this secure?
	#### YOTAM'S MODIFICATION TO THE CODE:
	#### The bottom two lines are Ian's code which asks for a password. I commented these out to 
	#### load the password from an encrypted file.
        #password = getpass.getpass('Please input a password: ')
        #pkcs12 = OpenSSL.crypto.load_pkcs12(pfx, password)

	#NOTE: This is NOT very secure. Should use a more secure encryption scheme and find a way to hide the
	#encrypted password. 
	#read base64 encoding from file
	f = open('passwords.txt', 'r')
	enc_password = f.read()
	f.close()
	password = base64.b64decode(enc_password)
	pkcs12 = OpenSSL.crypto.load_pkcs12(pfx, password)	

    cert = pkcs12.get_certificate()
    # Gotta normalize the subject name (since no guarantee that the
    # SOAP will have the right order)
    name = cert.get_subject().get_components()
    myCertificates[tuple(sorted(name))] = pkcs12
    answer = decrypt_soap(soap, myCertificates)
    #print type(answer), "is answer type"
    return answer

if __name__ == '__main__':
    run_test_scenario()
