from utils import db
import utils
import user
import logging
from ideoneclient import IdeoneClient

warmups = [{'name':'Hello World',
			'url':'hello',
			'description':'This program will output "Hello World".',
			'start_code':'#import<stdio.h>\n\nint main()\n{\n\tprintf("Hello World");\n\treturn 0;\n}'}]

class Example(utils.Model):
	name = db.StringProperty(required=True)
	url = db.StringProperty(required=True)
	description = db.TextProperty(required=True)
	start_code = db.TextProperty(required=True)

	@classmethod
	def warmup(cls):
		if db.Query(Example).count()==0:
			logging.info("Warming up Examples")
			for e in warmups:
				
				example = Example(name=e['name'], 
									url=e['url'], 
									description=string.replace(e['description'], '\n', '<br>'),
									start_code=e['start_code'])
				example.put()

class AddExampleHandler(user.AdminHandler):
	def admin_get(self):
		upload_url = blobstore.create_upload_url('/upload')
		page = {'topic_name': 'Create an Example'}
		self.render_with_user("addexample.html", {'page':page})

	def admin_post(self):
		example = Example(	name=self.request.get('name'), 
							url=self.request.get('url'), 
							description=string.replace(string.replace(self.request.get('description'), '\r', ''), '\n', '<br>'),
							start_code=string.replace(self.request.get('start_code'), '\r', '')
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
				logging.info("Serving example: " + repr(string.replace(example.start_code, '\r', '')))
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
		if response['error'] != "OK" or int(response['result']) != 15 or response['output'] is None:
			message = response['error_message']

		response['message'] = message

		self.write_json(response);