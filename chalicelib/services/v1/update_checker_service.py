import json
import re
import uuid
from datetime import datetime, date

import xmltodict
from os import path

import requests
from chalicelib import APP_NAME, APP_VERSION, APP_ARCH_VERSION, helper
from chalicelib.boot import ROOT_DIR
from chalicelib.config import get_config
from chalicelib.database import get_connection
from chalicelib.helper import open_vendor_file
from chalicelib.logging import get_logger
from chalicelib.nosql.repositories.v1.standard_updates import StandardUpdatesRepository
from chalicelib.services.thread_executor import ThreadExecutor
from queue import Queue

from chalicelib.vos import StandardUpdateVO

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_identification(title):
    regex = '[A-Z/\s]+[0-9:./-]+[A-Za-z\s0-9]+-'
    res = re.search(regex, title)
    result = ""
    if res:
        result = res.group(0).rstrip('-').strip()
    return result


class UpdateCheckerService:
    DEBUG = False
    ENTITY = None
    REPOSITORY = StandardUpdatesRepository
    VALIDATOR = None

    def __init__(self, logger=None, config=None, connection=None):
        # logger
        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()
        # database connection
        self.connection = connection if connection is not None else get_connection()

        if self.DEBUG:
            self._repository = self.REPOSITORY(self.connection, self.config.DYNAMODB_TABLE_NAME, logger)
        else:
            self._repository = self.REPOSITORY(self.connection, self.config.DYNAMODB_TABLE_NAME)

        self.data_list = []
        self.updates = []
        self.queue = Queue()
        self.responses = []

    def get_datasources(self):
        with open_vendor_file('./datasources/standard.datasources.json', 'r') as f:
            stub_str = f.read()
        try:
            return json.loads(stub_str)
        except:
            raise Exception('Invalid JSON')

    def execute(self):
        self.logger.info('---------------------------------------------------------------')
        self.logger.info('{} - {} - {}'.format(APP_NAME, APP_VERSION, APP_ARCH_VERSION))
        self.logger.info('{} - {}'.format('UpdateCheckerService', 'execute'))
        self.logger.info('---------------------------------------------------------------')
        self.logger.info('Starting...')

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
                result = len(self.updates) > 0

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

        if responses:
            for response in responses:
                if response['response']['status_code'] == 200:
                    try:
                        rss_dict = xmltodict.parse(response['response']['text'])
                        data_list = self.extract_data(rss_dict)
                        self.data_list = self.data_list + data_list
                    except Exception as err:
                        self.logger.error(err)
            if len(self.data_list) > 0:
                self.updates = self.filter_data(self.data_list)
            if len(self.updates) > 0:
                self.save_data(self.updates)
        else:
            self.logger.error('There are no responses')

    def extract_data(self, rss_dict):
        data_list = []
        if 'rss' in rss_dict and 'channel' in rss_dict['rss']:
            for item in rss_dict['rss']['channel']['item']:
                vo = StandardUpdateVO()
                vo.title = item['title'] if 'title' in item else None
                vo.identification = get_identification(vo.title)
                vo.description = item['description'] if 'description' in item else None
                if 'pub_date' in item:
                    vo.publication_date = item['pub_date'] if 'pub_date' in item else date.today().isoformat()
                elif 'pubDate' in item:
                    vo.publication_date = item['pubDate'] if 'pubDate' in item else date.today().isoformat()
                vo.link = item['link'] if 'link' in item else None
                data_list.append(vo)
        return data_list

    def filter_data(self, data_list):
        block_size = 5
        updates = []
        data_dict = {item.identification:item for item in data_list}
        data_list_identifications = [item.identification for item in data_list]
        data_list_blocks = list(chunks(data_list_identifications, block_size))
        for block in data_list_blocks:
            self.logger.info("Filtering: {}".format(block))
            try:
                result = self._repository.list(where={"identification": block})
                if result:
                    # Remove os itens já existentes
                    for item in result:
                        identification = item['identification']
                        self.logger.info("Item skipped: {} already exists".format(identification))
                        block.remove(identification)
                for identification in block:
                    self.logger.info("Item for update: {}".format(identification))
                    updates.append(data_dict[identification])

            except Exception as err:
                self.logger.error(err)
        return updates

    def get_updates(self):
        return [item.to_dict() for item in self.updates]
        # return [item.identification for item in self.updates]

    def save_data(self, updates):
        result = False
        for item in updates:
            new_uuid = str(uuid.uuid4())
            if isinstance(item, StandardUpdateVO):
                result = self._repository.create(new_uuid=new_uuid, data=item.to_dict())
                if result:
                    self.logger.info("Item created with uuid: {}".format(new_uuid))
                item.uuid = new_uuid

        return result
