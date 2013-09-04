from xml.dom import minidom
import urllib, urllib2
from google.appengine.api import urlfetch
import time
from datetime import datetime
import utils
from utils import index, db
import logging

errorCodes = {
'OK': "Everything went ok.",
'AUTH_ERROR': "User name or user's password are invalid.",
'PASTE_NOT_FOUND': "Paste with specified link could not be found.",
'WRONG_LANG_ID': "Language with specified id does not exist.",
'ACCESS_DENIED': "Access to the resource id denied for the specified user. For example: the submission has \"user's\" visibility and can be accessed only by its author.",
'CANNOT_SUBMIT_THIS_MONTH_ANYMORE': "You have reached a monthly limit (see http://ideone.com/offer/users for details)",
'timeout': "The request timed out, try submitting again."
}

resultCodes = {
'0': "not running - the paste has been created with run parameter set to false",
'11': "compilation error - the program could not be executed due to compilation errors",
'12': "runtime error - the program finished because of the runtime error, for example: division by zero, array index out of bounds, uncaught exception",
'13': "time limit exceeded - the program didn't stop before the time limit",
'15': "Code runs successfully! (With no output)",
'17': "memory limit exceeded - the program tried to use more memory than it is allowed",
'19': "illegal system call - the program tried to call illegal system function",
'20': "internal error - some problem occurred on ideone.com; try to submit the paste again and if that fails too, then please contact us."
}

class IdeoneAccount(utils.Model):
	user=db.StringProperty(required=True)
	password=db.StringProperty(required=True)
	remaining=db.IntegerProperty(default=1000)
	next_update=db.DateTimeProperty()


class IdeoneClient(object):
	credentials = {'user': 'sgstudyingc', 'pass': 'sg1234', 'remaining':1000}

	def SOAPRequest(self, operation, input_parameters={}):
		parameters = dict(self.credentials.items() + input_parameters.items())

		request = utils.render_str("soap/" + operation + ".xml", parameters)
		response = None
		try:
			response = urlfetch.fetch(url='http://ideone.com/api/1/service',
								method=urlfetch.POST,
								payload=request,
								deadline=10,
								headers={'Content-Type:':'text/xml; charset=UTF-8'})
		except Exception, e:
			return {'error':'timeout'}
		
		xmldoc = minidom.parseString(response.content)

		responseDict = dict()
		for item in xmldoc.getElementsByTagName('item'):
			key = item.getElementsByTagName('key')[0].firstChild.nodeValue
			value = None
			if item.getElementsByTagName('value')[0].firstChild:
				value = item.getElementsByTagName('value')[0].firstChild.nodeValue
			responseDict[key] = value
		
		return responseDict

	def error(self, errorCode):
		errorString = "Ideone.com error: " + errorCode + " - " + errorCodes.get(errorCode, "Unkown Ideone.com error")
		logging.error(errorString)
		return {'error':errorCode, 'error_message':errorString}

	def change_account(self, account):
		self.credentials = {'user':account.user,
							'pass':account.password,
							'remaining':account.remaining}

	def test_account(self, account):
		self.credentials = {'user':account.user,
							'pass':account.password,
							'remaining':account.remaining}

		test = self.SOAPRequest("testFunction")

		[logging.info("Test:" + k + " " + test[k]) for k in test.keys()]

		if test['error'] and test['error'] == 'OK':
			return True

	def submit(self, program, the_input=""):
		parameters = {	'code': program,
						'input':the_input}
		response = self.SOAPRequest("createSubmission", parameters)
		if response['error'] != "OK":
			return self.error(response['error'])

		link = response['link']
		status = 100
		while int(status):
			time.sleep(1)
			logging.info("status: %s", status)
			response = self.SOAPRequest("getSubmissionStatus", {'link': link})
			if response['error'] != "OK":
				return self.error(response['error'])
			status = response['status']

		response = self.SOAPRequest("getSubmissionDetails", {'link': link})
		if response['error'] != "OK":
				return self.error(response['error'])
		result = response['result']

		if response['result'] != 15:
			response['error_message'] = resultCodes.get(result, "Oops!")
		elif not response.has_key('output') or not response['output']:
			response['error_message'] = 'Your program ran, but there was no output.'
		
		for k in response.keys():
			logging.info("Response - " + k + ": " + repr(response[k]))

		response['provider'] = 'Powered by <a href="http://ideone.com">www.ideone.com</a> &copy; by <a href="http://sphere-research.com"> Sphere Research Labs'
		return response