from marshmallow import Schema, fields

from chalicelib.http_resources.request_control import Pagination
from chalicelib.openapi.schemas import DeletionSchema, RequestControlSchema, MetaSchema, LinkSchema


class StandardUpdatesSchema(Schema):
    uuid = fields.UUID()
    identification = fields.Str(example="ISO 9001:2015")
    publication_date = fields.Date()
    title = fields.Str()
    description = fields.Str()
    link = fields.URL()
    synchronized = fields.Bool()


class UpdatesCheckResponseSchema(Schema):
    # data = fields.List(fields.Str(example="ISO 9001:2015"))
    data = fields.List(fields.Nested(StandardUpdatesSchema))
    control = fields.Nested(RequestControlSchema)
    meta = fields.Nested(MetaSchema)
    links = fields.List(fields.Nested(LinkSchema))


class UpdatesSyncResponseSchema(Schema):
    data = fields.List(fields.Nested(StandardUpdatesSchema))
    control = fields.Nested(RequestControlSchema)
    meta = fields.Nested(MetaSchema)
    links = fields.List(fields.Nested(LinkSchema))
