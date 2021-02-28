from chalicelib import APP_NAME, APP_VERSION, APP_ARCH_VERSION
from chalicelib.config import get_config
from chalicelib.database import get_connection
from chalicelib.logging import get_logger
from chalicelib.nosql.repositories.v1.standard_updates import StandardUpdatesRepository


class UpdateSynchronizerService:
    DEBUG = False
    ENTITY = None
    SOURCE_REPOSITORY = StandardUpdatesRepository
    VALIDATOR = None

    def __init__(self, logger=None, config=None, connection=None):
        # logger
        self.logger = logger if logger is not None else get_logger()
        # configurations
        self.config = config if config is not None else get_config()
        # database connection
        self.connection = connection if connection is not None else get_connection()

        if self.DEBUG:
            self._source_repository = self.SOURCE_REPOSITORY(self.connection, self.config.DYNAMODB_TABLE_NAME, logger)
        else:
            self._source_repository = self.SOURCE_REPOSITORY(self.connection, self.config.DYNAMODB_TABLE_NAME)

    def get_datasources(self):
        return self._source_repository.list(where={'synchronized':False})

    def execute(self):
        self.logger.info('---------------------------------------------------------------')
        self.logger.info('{} - {} - {}'.format(APP_NAME, APP_VERSION, APP_ARCH_VERSION))
        self.logger.info('{} - {}'.format('UpdateSynchronizerService', 'execute'))
        self.logger.info('---------------------------------------------------------------')
        self.logger.info('Starting...')

        result = True

        datasource = self.get_datasources()
        print(datasource)

        return result