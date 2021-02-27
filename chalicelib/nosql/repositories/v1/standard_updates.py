from chalicelib.enums.messages import MessagesEnum
from chalicelib.exceptions import DatabaseException


class StandardUpdatesRepository:
    def __init__(self, connection, table_name, logger=None):
        """
        :param (pytrine.dbal.connection.Connection) connection:
        """

        self._connection = connection
        self._logger = logger
        self.table_name = table_name
        self._table = self._connection.Table(self.table_name)

    def get(self, record_uuid, fields=None):
        response = None
        try:
            response = self._table.get_item(Key={
                'uuid': record_uuid
            })
        except Exception as err:
            if self._logger:
                self._logger.error(err)

        return response['Item'] if 'Item' in response else None

    def list(self, where, offset=None, limit=None, fields=None, sort_by=None, order_by=None):
        scan_params = {}
        filter_expression = None
        expression_attributes_names = {}
        expression_attributes_values = {}

        if where:
            filter_expression = []
            for k, v in where.items():
                key = "#f_" + k
                val = ":f_" + k
                if isinstance(v, list):
                    expression_attributes_names[key] = k
                    val_array = []
                    i = 0
                    for value in v:
                        val = ":f_" + k + "_" + str(i)
                        val_array.append(val)
                        expression_attributes_values[val] = value
                        i += 1
                    filter_expression.append(key + " IN (" + ','.join(val_array) + ")")

                else:
                    filter_expression.append(key + " = " + val)
                    expression_attributes_names[key] = k
                    expression_attributes_values[val] = val
        #
        #     if startswith is not None:
        #         filter_expression = self._add_to_filter_expression(
        #             filter_expression, Attr('name').begins_with(startswith)
        #         )
        #     if media_type is not None:
        #         filter_expression = self._add_to_filter_expression(
        #             filter_expression, Attr('type').eq(media_type)
        #         )
        #     if label is not None:
        #         filter_expression = self._add_to_filter_expression(
        #             filter_expression, Attr('labels').contains(label)
        #         )
        if filter_expression:
            scan_params['FilterExpression'] = ','.join(filter_expression)
        if expression_attributes_names:
            scan_params['ExpressionAttributeNames'] = expression_attributes_names
        if expression_attributes_values:
            scan_params['ExpressionAttributeValues'] = expression_attributes_values
        response = self._table.scan(**scan_params)

        return response['Items']

    def count(self, where, sort_by, order_by):
        # Todo ver com filtros
        # print
        # dynamodb_table.query_count(
        #     index='first_name-last_name-index',  # Get indexes from indexes tab in dynamodb console
        #     first_name__eq='John',  # add __eq to your index name for specific search
        #     last_name__eq='Smith'  # This is your range key
        # )
        return {"total": self._table.item_count}

    def create(self, new_uuid, data):
        data['uuid'] = new_uuid
        result = self._table.put_item(Item=data)
        success = result and result['ResponseMetadata'] and result['ResponseMetadata']['HTTPStatusCode'] == 200
        return data if success else None

    def update(self, record_uuid, update_data):

        current = self.get(record_uuid=record_uuid)
        if not current:
            raise DatabaseException(MessagesEnum.INVALID_ENTITY_ID)

        for k, v in update_data.items():
            current[k] = v

        update_expression = []
        expression_attributes_names = {}
        expression_attributes_values = {}
        for k, v in current.items():
            # remove the key
            if k == 'uuid':
                continue

            key = "#upd_" + k
            val = ":upd_" + k
            update_expression.append(key + " = " + val)
            expression_attributes_names[key] = k
            expression_attributes_values[val] = v

        update_expression_str = "set " + ", ".join(update_expression)

        result = self._table.update_item(
            Key={
                'uuid': record_uuid
            },
            UpdateExpression=update_expression_str,
            ExpressionAttributeNames=expression_attributes_names,
            ExpressionAttributeValues=expression_attributes_values,
            ReturnValues="UPDATED_NEW"
        )
        success = result and result['ResponseMetadata'] and result['ResponseMetadata']['HTTPStatusCode'] == 200
        return current if success else None

    def delete(self, record_uuid):

        current = self.get(record_uuid=record_uuid)
        if not current:
            raise DatabaseException(MessagesEnum.INVALID_ENTITY_ID)

        result = self._table.delete_item(
            Key={
                'uuid': record_uuid
            }
        )
        success = result and result['ResponseMetadata'] and result['ResponseMetadata']['HTTPStatusCode'] == 200
        return success
