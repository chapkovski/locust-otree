from locust import HttpLocust, TaskSet, task, between
from gevent import GreenletExit
from locust.exception import StopLocust
from otree import __version__
# this is not the best - in case oTree decides to change the bot complete message later.

########### BLOCK: FOR OLD (<2.6)  otree version ##############################################################

BOT_COMPLETE_HTML_MESSAGE = b'''
<html>
    <head>
        <title>Bot completed</title>
    </head>
    <body>Bot completed</body>
</html>
'''
############ END OF: FOR OLD (<2.6)  otree version #############################################################



class OtreeApplication:
    def __init__(self, client, host=None):
        self.client = client
        self.start_url = host

    def first_page(self):
        with self.client.get(self.start_url, name=self.start_url, catch_response=True) as response:
            newlink = response.url
            if newlink != self.start_url and response.ok:
                response.success()

        status = True
        while status:
            name = ': '.join(newlink.strip('/').split('/')[-3:])
            with self.client.post(newlink, name=name, catch_response=True) as response:
                oldlink = newlink
                newlink = response.url
                # trying to catch OutOfRangeNotification for older otree versions
                if response.content == BOT_COMPLETE_HTML_MESSAGE and oldlink == newlink:
                    print('IM DONE')
                    status = False
                    response.success()
                elif newlink.split('/')[3] == 'OutOfRangeNotification':
                    with self.client.get(newlink, name='OutOfRangeNotification', catch_response=True) as final_response:
                        if final_response.ok:
                            final_response.success()
                            status = False

                elif  response.ok:
                    status = response.ok
                    response.success()
                else:
                    response.failure('oTree-Locust error')
                    status = False


class OtreeTaskSet(TaskSet):
    def on_start(self):
        self.otree_client = OtreeApplication(self.client, host=self.parent.host)

    @task(1)
    def start_bot(self):
        self.otree_client.first_page()
        raise StopLocust()


class WebsiteUser(HttpLocust):
    wait_time = between(5, 9)
    host = 'http://localhost:8000'
    task_set = OtreeTaskSet
