#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License 
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from apiclient.discovery import build
from google.appengine.api import users
from oauth2client.appengine import OAuth2Decorator
import webapp2

decorator = OAuth2Decorator(
	client_id='411488856174.apps.googleusercontent.com',
	client_secret='mW3BB9ibX7WiZfSnKSTQJ8X9',
	scope='https://www.googleapis.com/auth/admin.directory.group')

service = build('admin', 'directory_v1')

class Main(webapp2.RequestHandler):

	@decorator.oauth_required
	def get(self):
		
		html = """
			<h2>Mailing Group Example</h2>
			<form method="POST" action="/CreateMailingGroup">
				<b>Create Mailing Group</b><br>
				group name : <input name="name"><br>
				email for define mailing group : <input name="email"><br>
				<input type="submit" value="Submit">
			</form>
			<hr>
			<form method="POST" action="/InsertMail">
				<b>Insert Mail to Mailing Group</b><br>
				group id : <input name="key"><br>
				email : <input name="email"><br>
				<input type="submit" value="Submit">
			</form>
			<hr>
			<form method="POST" action="/DeleteMail">
				<b>Delete Mail from Mailing Group</b><br>
				group id : <input name="key"><br>
				email : <input name="email"><br>
				<input type="submit" value="Submit">
			</form>
			<hr>
			<form method="POST" action="/UpdateGroupDescription">
				<b>Update Group Description</b><br>
				group name : <input name="name"><br>
				email for define mailing group : <input name="email"><br>
				<input type="submit" value="Submit">
			</form>
			<hr>
			<form method="POST" action="/DeleteGroup">
				<b>Delete Mailing Group</b><br>
				group id : <input name="key"><br>
				<input type="submit" value="Submit">
			</form>
			<hr>
			<form method="POST" action="/GetMemberGroup">
				<b>Get Member Group</b><br>
				group id : <input name="key"><br>
				<input type="submit" value="Submit">
			</form>
		"""

		user = users.get_current_user()
		self.response.write("Sign-in as : " + user.email())
        	if not user:
            		self.redirect(users.create_login_url(self.request.uri))
		else:
			self.response.write(html)

class CreateMailingGroup(webapp2.RequestHandler):
	@decorator.oauth_required
	def post(self):
		http = decorator.http()
		email = self.request.get('email')
		name = self.request.get('name')
		params = {
			'email': email,
			'name' : name
		}
		result = service.groups().insert(body=params).execute(http=http)
		self.response.headers['Content-Type'] = 'text/json'
		self.response.write(result);

class InsertMail(webapp2.RequestHandler):
	@decorator.oauth_required
	def post(self):
		http = decorator.http()
		email = self.request.get('email')
		key = self.request.get('key')
		params = {
			'email': email,
			"role": "MEMBER"
		}
		result = service.members().insert(groupKey=key,body=params).execute(http=http)
		self.response.headers['Content-Type'] = 'text/json'
		self.response.write(result);

class DeleteMail(webapp2.RequestHandler):
	@decorator.oauth_required
	def post(self):
		http = decorator.http()
		email = self.request.get('email')
		key = self.request.get('key')
		result = service.members().delete(groupKey=key,memberKey=email).execute(http=http)
		self.response.headers['Content-Type'] = 'text/json'
		self.response.write(result);

class UpdateGroupDescription(webapp2.RequestHandler):
	@decorator.oauth_required
	def post(self):
		http = decorator.http()
		email = self.request.get('email')
		key = self.request.get('key')
		name = self.request.get('name')
		params = {
			'email': email,
			'name' : name
		}
		result = service.groups().update(groupKey=key,body=params).execute(http=http)
		self.response.headers['Content-Type'] = 'text/json'
		self.response.write(result);

class DeleteGroup(webapp2.RequestHandler):
	@decorator.oauth_required
	def post(self):
		http = decorator.http()
		key = self.request.get('key')
		result = service.groups().delete(groupKey=key).execute(http=http)
		self.response.headers['Content-Type'] = 'text/json'
		self.response.write(result);

class GetMemberGroup(webapp2.RequestHandler):
	@decorator.oauth_required
	def post(self):
		http = decorator.http()
		key = self.request.get('key')
		result = service.members().list(groupKey=key).execute(http=http)
		self.response.headers['Content-Type'] = 'text/json'
		self.response.write(result);


app = webapp2.WSGIApplication([
    ('/', Main),
    ('/CreateMailingGroup', CreateMailingGroup),
    ('/InsertMail',InsertMail),
    ('/DeleteMail',DeleteMail),
    ('/UpdateGroupDescription',UpdateGroupDescription),
    ('/DeleteGroup',DeleteGroup),
    ('/GetMemberGroup',GetMemberGroup),
    (decorator.callback_path, decorator.callback_handler()) 
], debug=True)
