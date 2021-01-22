import json
from os import path

import requests
from chalicelib import APP_NAME, APP_VERSION, APP_ARCH_VERSION
from chalicelib.boot import ROOT_DIR
from chalicelib.logging import get_logger
from chalicelib.services.thread_executor import ThreadExecutor
from queue import Queue


class UpdateCheckerService:

    def __init__(self, logger=None):
        self.logger = logger if logger is not None else get_logger()
        self.updates = []
        self.queue = Queue()
        self.responses = []

    def get_datasources(self, root_dir=None):
        if not root_dir:
            root_dir = ROOT_DIR
        with open(path.join(root_dir, 'datasources/standard.datasources.json')) as f:
            stub_str = f.read()
        try:
            return json.loads(stub_str)
        except:
            raise Exception('Invalid JSON')

    def execute(self):
        self.logger.info('---------------------------------------------------------------')
        self.logger.info('{} - {} - {}'.format(APP_NAME, APP_VERSION, APP_ARCH_VERSION))
        self.logger.info('---------------------------------------------------------------')
        self.logger.info('Starting...')

        result = True

        datasources = self.get_datasources()
        if not datasources:
            raise Exception('No datasources found')
        else:

            for k, urls in datasources.items():
                if urls:
                    for url in urls:
                        self.queue.put(url)

            self.logger.info('Executing requests...')
            if self.queue.qsize() == 0:
                self.logger.info('Empty queue...')
                result = False
            else:
                executor = ThreadExecutor(self.queue, self.logger)
                executor.execute(self.do_request, self.on_finish)

        return result

    def do_request(self):
        self.logger.info('Executing a request')
        result = None
        if not self.queue.empty():
            url = self.queue.get()
            response = requests.get(url)
            result = {
                'url': url,
                'response': {
                    'status_code': response.status_code,
                    'text': response.text}
            }
        return result

    def on_finish(self, responses):
        self.logger.info('finished with responses')
        self.responses = responses
        # TODO fazer alguma coisa
        #print(responses)
