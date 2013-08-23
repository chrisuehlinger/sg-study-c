#!/usr/bin/env python 
"""
ideone.com
API sample

This script shows how to use ideone api.
"""

program = """#include<stdio.h>

int main()
{
	//Write "Hello World"

	return 1;
}"""

link ="6L4ws7"

from SOAPpy import WSDL, SOAPProxy
import urllib2
from xml.dom import minidom

# creating wsdl client
wsdlObject = WSDL.Proxy('http://ideone.com/api/1/service.wsdl')
wsdlObject.soapproxy.config.debug = 1

# calling test method

response = wsdlObject.testFunction('sgstudyingc','sg1234')
#response = wsdlObject.createSubmission('sgstudyingc', 'sg1234', program, 11, 'no input', True, True)
#response = wsdlObject.getSubmissionStatus('sgstudyingc', 'sg1234', link)
#response = wsdlObject.getSubmissionDetails('sgstudyingc', 'sg1234', link, False, False, True, True, True)

testFunction = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope
  SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"
  xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
  xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance"
  xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
  xmlns:xsd="http://www.w3.org/1999/XMLSchema"
>
<SOAP-ENV:Body>
<ns1:testFunction xmlns:ns1="http://ideone.com/api/1/service" SOAP-ENC:root="1">
<v1 xsi:type="xsd:string">sgstudyingc</v1>
<v2 xsi:type="xsd:string">sg1234</v2>
</ns1:testFunction>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

createSubmission = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope
  SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"
  xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
  xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance"
  xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
  xmlns:xsd="http://www.w3.org/1999/XMLSchema"
>
<SOAP-ENV:Body>
<ns1:createSubmission xmlns:ns1="http://ideone.com/api/1/service" SOAP-ENC:root="1">
<v1 xsi:type="xsd:string">sgstudyingc</v1>
<v2 xsi:type="xsd:string">sg1234</v2>
<v3 xsi:type="xsd:string">#include&lt;stdio.h&gt;

int main()
{
	//Write "Hello World"
	printf("Hello World!\\n");
	return 0;
}</v3>
<v4 xsi:type="xsd:integer">11</v4>
<v5 xsi:type="xsd:string">no input</v5>
<v6 xsi:type="xsd:boolean">true</v6>
<v7 xsi:type="xsd:boolean">true</v7>
</ns1:createSubmission>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

getSubmissionStatus = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope
  SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"
  xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
  xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance"
  xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
  xmlns:xsd="http://www.w3.org/1999/XMLSchema"
>
<SOAP-ENV:Body>
<ns1:getSubmissionStatus xmlns:ns1="http://ideone.com/api/1/service" SOAP-ENC:root="1">
<v1 xsi:type="xsd:string">sgstudyingc</v1>
<v2 xsi:type="xsd:string">sg1234</v2>
<v3 xsi:type="xsd:string">dG5TJ0</v3>
</ns1:getSubmissionStatus>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

getSubmissionDetails = """<?xml version="1.0" encoding="UTF-8"?>
<SOAP-ENV:Envelope
  SOAP-ENV:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/"
  xmlns:SOAP-ENC="http://schemas.xmlsoap.org/soap/encoding/"
  xmlns:xsi="http://www.w3.org/1999/XMLSchema-instance"
  xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/"
  xmlns:xsd="http://www.w3.org/1999/XMLSchema"
>
<SOAP-ENV:Body>
<ns1:getSubmissionDetails xmlns:ns1="http://ideone.com/api/1/service" SOAP-ENC:root="1">
<v1 xsi:type="xsd:string">sgstudyingc</v1>
<v2 xsi:type="xsd:string">sg1234</v2>
<v3 xsi:type="xsd:string">dG5TJ0</v3>
<v4 xsi:type="xsd:boolean">false</v4>
<v5 xsi:type="xsd:boolean">false</v5>
<v6 xsi:type="xsd:boolean">true</v6>
<v7 xsi:type="xsd:boolean">true</v7>
<v8 xsi:type="xsd:boolean">true</v8>
</ns1:getSubmissionDetails>
</SOAP-ENV:Body>
</SOAP-ENV:Envelope>"""

# response = urllib2.urlopen(urllib2.Request('http://ideone.com/api/1/service', createSubmission))
# xmldoc = minidom.parseString(response.read())
# link = xmldoc.getElementsByTagName('item')[1].getElementsByTagName('value')[0].firstChild.nodeValue

# response = urllib2.urlopen(urllib2.Request('http://ideone.com/api/1/service', getSubmissionStatus))
# xmldoc = minidom.parseString(response.read())
# status = xmldoc.getElementsByTagName('item')[1].getElementsByTagName('value')[0].firstChild.nodeValue
# result = xmldoc.getElementsByTagName('item')[2].getElementsByTagName('value')[0].firstChild.nodeValue

response = urllib2.urlopen(urllib2.Request('http://ideone.com/api/1/service', getSubmissionDetails))
xmldoc = minidom.parseString(response.read())

print xmldoc.toprettyxml()

for item in xmldoc.getElementsByTagName('item'):
 	print item.getElementsByTagName('key')[0].firstChild.nodeValue
 	print item.getElementsByTagName('value')[0].firstChild.nodeValue