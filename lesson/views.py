import utils
from utils import index, db
import logging
from example.models import Example
import ideoneclient
from user.views import UserHandler, AdminHandler
import user.views
from user.models import User
import datetime, time

class LessonHandler(UserHandler):
	def user_get(self, *args):
		if args[0] is None:
			self.redirect('/')
		else:
			page = None
			for group in index:
				for topic in group['topics']:
					if topic['url']==args[0]:
						page = topic

			if page:
				inline_examples = []
				for e in page['examples']:
					ex = Example.query().filter('url = ', e).get()
					inline_examples.append(ex)
					logging.info(ex)

				now = datetime.datetime.now()
				now_stamp = int(time.mktime(now.timetuple()))
				self.render_with_user("lessons/" + args[0] + ".html", { 'page': page, 
																		'curr_time_formatted': time.strftime("%b %d %Y %H:%M:%S", now.timetuple()), 
																		'curr_timestamp': now_stamp,
																		'examples': inline_examples})
			else:
				page = {'url':'404', 'topic_name':"Error 404"}
				self.render_with_user("404.html", {'page': page})

	def user_post(self, *args):
		submission = self.request.get('code')
		message = ''
		client = ideoneclient.IdeoneClient()
		response = client.submit(submission, self.request.get('input'))
		if response['error'] != "OK" or int(response['result']) != 15 or response['output'] is None:
			message = response['error_message']

		response['message'] = message

		self.write_json(response);