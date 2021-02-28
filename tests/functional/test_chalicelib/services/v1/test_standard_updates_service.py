import unittest

from unittest_data_provider import data_provider

from chalicelib.config import get_config
from chalicelib.http_resources.request import ApiRequest
from chalicelib.logging import get_logger
from chalicelib.services.v1.standard_updates_service import StandardUpdatesService
from tests import ROOT_DIR
from tests.functional.functionaltestutils import BaseFunctionalTestCase
from tests.functional.helpers.connection_helper import ConnectionHelper, DynamoDBHelper
from tests.unit.testutils import get_function_name


def get_request():
    request = ApiRequest()
    request.limit = 2

    request2 = ApiRequest()
    request2.limit = 2
    request2.offset = 1

    return (request,), (request2,),


def get_connection():
    connection = ConnectionHelper().get_dynamodb_local_connection()
    return connection


class StandardUpdatesServiceTestCase(BaseFunctionalTestCase):
    EXECUTE_FIXTURE = True
    CONFIG = None

    @classmethod
    def setUpClass(cls):
        cls.CONFIG = get_config()

        # fixture
        if cls.EXECUTE_FIXTURE:
            logger = get_logger()
            table_name = get_config().DYNAMODB_TABLE_NAME

            DynamoDBHelper.drop_table(connection=get_connection(), table_name=table_name)
            logger.info(f'table {table_name}')

            file_name = ROOT_DIR + '/tests/datasets/nosql/create.table.standard-update-checker-dynamodb-StandardUpdatesTable.json'
            DynamoDBHelper.create_table(connection=get_connection(),
                                        table_name=table_name,
                                        file_name=file_name)
            logger.info(f'table {table_name} created')

            file_name = ROOT_DIR + '/tests/datasets/seeders/seeder.standard-update-checker-dynamodb-StandardUpdatesTable.json'
            DynamoDBHelper.sow_table(connection=get_connection(), table_name=table_name,
                                     file_name=file_name)
            logger.info(f'table {table_name} populated')

    @data_provider(get_request)
    def test_list(self, request):
        self.logger.info('Running test: %s', get_function_name(__name__))
        service = StandardUpdatesService(logger=self.logger, config=self.CONFIG, connection=get_connection())
        data = service.list(request)
        # print(len(data))
        self.assertIsNotNone(data)
        # self.assertTrue(len(data) == request.limit)

    @data_provider(get_request)
    def test_count(self, request):
        """

        :param (ApiRequest) request:
        :return:
        """
        self.logger.info('Running test: %s', get_function_name(__name__))
        service = StandardUpdatesService(logger=self.logger, config=self.CONFIG, connection=get_connection())
        data = service.count(request)

        self.assertIsNotNone(data)
        self.assertTrue(data > 0)


if __name__ == '__main__':
    unittest.main()
