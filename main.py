import webapp2
import logging
import json

from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
from google.appengine.api import mail

import base64
import random
import datetime
import requests
import requests_toolbelt.adapters.appengine

from secrets import GITHUB_PASSWORD, EMAIL_ACCOUNTS, MY_EMAIL_ACCOUNT, GOOGLE_APPS_ENGINE_EMAIL

requests_toolbelt.adapters.appengine.monkeypatch()


class HandleEmail(InboundMailHandler):
    def receive(self, message):
        matching_email_accounts = [acct_name for acct_name in EMAIL_ACCOUNTS if acct_name in message.sender]
        if not matching_email_accounts:
            logging.info('received message from: %s', message.sender)
            return

        plain_body = ''
        for _, plain in message.bodies('text/plain'):
            plain_body = plain.decode()

        date = datetime.datetime.now().strftime('%Y-%m-%d')

        post_title = (
            message.subject or
            str(random.randint(0, 1000))
        ).lower().replace(" ", "-").replace("re:", "")

        url = "https://api.github.com/repos/calcsam/blog-new/contents/pages/%s---%s/index.md" % (date, post_title)

        is_public = 'public' in message.to
        first_line = plain_body.split('\n')[0]
        tags_exist = 'tags:' in first_line

        tags = first_line.replace('tags:', '').replace('Tags:', '').replace(' ', '') if tags_exist else "null"
        date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        "2013-10-11T19:47:34.000Z"

        post_message = """---
        title: %s
        tags: %s
        date: "%s"
        layout: post
        draft: false
        public: %s
        ---
        %s
        """ % (
            post_title,
            tags,
            date,
            is_public,
            plain_body
        )).encode('UTF-8')

        logging.info('post_message: %s', post_message)

        form_fields = {
          'message': "adding %s" % post_title,
          'content': base64.b64encode(post_message),
        }

        logging.info('form_fields to be returned: %s', form_fields)

        headers = {
            "Authorization": "Basic %s" % base64.b64encode("sambhagwat:%s" % GITHUB_PASSWORD)
        }

        result = requests.put(url, headers=headers, data=json.dumps(form_fields))

        # log more
        logging.info('PUT to %s returned: %s', url, result.status_code)
        logging.info('Returned content: %s', result.content)

        response_body = "Your email has been received with Github status code %s and response %s" % (result.status_code, result.content)

        mail.send_mail(
           sender=GOOGLE_APPS_ENGINE_EMAIL,
           to=MY_EMAIL_ACCOUNT,
           subject="Re: %s" % message.subject,
           body=response_body
        )

application = webapp2.WSGIApplication([HandleEmail.mapping()], debug=True)
