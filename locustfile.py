from locust import HttpLocust, TaskSet, task, between
from gevent import GreenletExit
from locust.exception import StopLocust



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
                print(f'GONNA GO TO {newlink}')
                # trying to catch OutOfRangeNotification
                if newlink.split('/')[3] == 'OutOfRangeNotification':
                    print('IM DONE')
                    status = False
                    response.success()
                elif response.ok:
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
