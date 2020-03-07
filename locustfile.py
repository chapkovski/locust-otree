from locust import HttpLocust, TaskSet, task, between
from gevent import GreenletExit
from locust.exception import StopLocust

BOT_COMPLETE_HTML_MESSAGE = b'''
<html>
    <head>
        <title>Bot completed</title>
    </head>
    <body>Bot completed</body>
</html>
'''


class FooApplication():
    def __init__(self, client, joincode=None, host=None):
        self.client = client
        self.joincode = joincode
        if host is None:
            self.start_url= f'/join/{self.joincode}/'
        else:
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
                print(f'GONNA GO TO {newlink}')
                if response.content == BOT_COMPLETE_HTML_MESSAGE and oldlink == newlink:
                    print('IM DONE')
                    status = False
                    response.success()
                elif response.content != BOT_COMPLETE_HTML_MESSAGE:
                    status = response.ok
                    response.success()
                else:
                    response.failure()


class FooTaskSet(TaskSet):
    def on_start(self):
        self.foo = FooApplication(self.client, host=self.parent.host)

    @task(1)
    def login(self):
        self.foo.first_page()
        raise StopLocust()



class WebsiteUser(HttpLocust):
    wait_time = between(5, 9)
    host = 'http://localhost:8000'
    task_set = FooTaskSet
