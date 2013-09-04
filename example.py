from utils import db
import utils
import user
import logging
import string
from ideoneclient import IdeoneClient
import os
import json

class Example(utils.Model):
	name        = db.StringProperty(required=True)
	url         = db.StringProperty(required=True)
	description = db.TextProperty(required=True)
	start_code  = db.TextProperty(required=True)
	takes_input = db.BooleanProperty(default=False)

	@classmethod
	def warmup(cls):
		if Example.query().count()==0:
			logging.info("Warming up Examples")
			path = os.path.join(os.path.dirname(__file__), 'json', 'examples.json')
			warmups = json.loads(open(path, 'r').read())

			for e in warmups:
				example = Example(name=e['name'], 
									url=e['url'], 
									description=string.replace(e['description'], '\n', '<br>'),
									start_code=db.Text(e['start_code']),
									takes_input=e['takes_input'])
				example.put()

class AddExampleHandler(user.AdminHandler):
	def admin_get(self):
		upload_url = blobstore.create_upload_url('/upload')
		page = {'topic_name': 'Create an Example'}
		self.render_with_user("addexample.html", {'page':page})

	def admin_post(self):
		start_code=string.replace(self.request.get('start_code'), '\r', '')

		description = self.request.get('description')
		description = string.replace(description, '\r', '')
		description = string.replace(description, '\n', '<br>')

		example = Example(	name=self.request.get('name'), 
							url=self.request.get('url'), 
							description=description,
							start_code=start_code
						 )
		example.put()
		time.sleep(5)
		self.redirect('/example/'+exercise.url)

class ExampleHandler(user.UserHandler):
	def user_get(self, *args):
		pagename = args[0]
		if pagename is None:
			example_list = Example.query().order('name')
			page = {'url':'examples', 'topic_name':'Practice Examples'}
			self.render_with_user("exampleindex.html", {'page':page, 'examples':example_list})
		else:
			example = Example.query().filter("url = ",pagename).get()
			if example is None:
				self.write("No Example named '%s'" % pagename)
			else:
				logging.info("Serving example: " + repr(example.name))
				logging.info("Serving example: " + repr(example.start_code))
				logging.info("Serving example: " + repr(example.description))
				self.render_with_user("example.html", {'page':example})

	def user_post(self, *args):
		pagename = args[0]
		if args[0] is None:
			pagename=""

		submission = self.request.get('code')

		message = ''
		client = IdeoneClient()
		response = client.submit(submission, self.request.get('input'))
		if (response['error'] != "OK" or 
			int(response['result']) != 15 or 
			response['output'] is None):
				message = response['error_message']

		response['message'] = message

		self.write_json(response);