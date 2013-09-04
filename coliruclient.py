from xml.dom import minidom
import urllib, urllib2
from google.appengine.api import urlfetch
import json
import logging

class ColiruClient:
	def submit(self, submission, the_input=""):

		responseDict = {'error': 'OK', 
						'output':'', 
						'provider':'Powered by <a href="http://coliru.stacked-crooked.com/">Coliru</a> online compiler'}

		request = json.dumps({"cmd": "cat main.cpp > main.c; gcc-4.8 -Wall main.c", 
								"src": submission })
		response = None
		try:
			response = urlfetch.fetch(url='http://coliru.stacked-crooked.com/compile',
								method=urlfetch.POST,
								payload=request,
								deadline=10,
								headers={'Content-Type:':'application/json; charset=UTF-8'})
		except Exception, e:
			return {'error':'timeout compile'}

		if response and response.content:
			responseDict['cmpinfo'] = response.content

		if (responseDict.has_key('cmpinfo') and 
			responseDict['cmpinfo'] and 
			'error' in responseDict['cmpinfo']):
				responseDict['result'] = 11
				responseDict['error_message'] = 'compilation error - the program could not be executed due to compilation errors'
				return responseDict

		request = json.dumps({"cmd": "cat main.cpp > main.c; gcc-4.8 main.c && echo \"%s\" | ./a.out" % the_input, 
								"src": submission })
		response = None
		try:
			response = urlfetch.fetch(url='http://coliru.stacked-crooked.com/compile',
								method=urlfetch.POST,
								payload=request,
								deadline=10,
								headers={'Content-Type:':'application/json; charset=UTF-8'})
		except Exception, e:
			return {'error':'timeout run'}

		if response and response.content:
			responseDict['output'] = response.content
			responseDict['result'] = 15

		return responseDict