import unittest

from unittest_data_provider import data_provider

from chalicelib.config import get_config
from chalicelib.http_resources.request import ApiRequest
from chalicelib.logging import get_logger
from chalicelib.services.v1.update_checker_service import UpdateCheckerService
from tests import ROOT_DIR
from tests.functional.functionaltestutils import BaseFunctionalTestCase
from tests.functional.helpers.connection_helper import ConnectionHelper, DynamoDBHelper
from tests.unit.testutils import get_function_name


def get_request():
    request = ApiRequest()

    return (request,),


def get_connection():
    connection = ConnectionHelper().get_dynamodb_local_connection()
    return connection


class StandardManagerServiceTestCase(BaseFunctionalTestCase):
    EXECUTE_FIXTURE = False
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

    # @data_provider(get_request)
    # def test_list(self, request):
    #     self.logger.info('Running test: %s', get_function_name(__name__))
    #     service = StandardManagerService(logger=self.logger, config=self.CONFIG, connection=get_connection())
    #     data = service.list(request)
    #     self.assertTrue(len(data) == request.limit)

    def test_get_datasource(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        # TODO apenas fazer com mocks tá errado
        service = UpdateCheckerService(logger=self.logger, config=self.CONFIG, connection=get_connection())
        datasources = service.get_datasources()
        self.assertIsNotNone(datasources)

    def test_execute(self):
        self.logger.info('Running test: %s', get_function_name(__name__))
        service = UpdateCheckerService(logger=self.logger, config=self.CONFIG, connection=get_connection())
        result = service.execute()

        self.assertIsNotNone(result)
        self.logger.info("Total of updates: {}".format(len(service.updates)))
        self.assertGreater(len(service.updates), 0)


if __name__ == '__main__':
    unittest.main()
