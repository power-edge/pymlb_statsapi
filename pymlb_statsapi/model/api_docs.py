"""
created by nikos at 4/21/21
"""
from serde import fields, Model

from .base import MLBStatsAPIModel, APIModelBase


class DocsAPIModel(APIModelBase):
    position: fields.Int()


class ApiDocsModel(MLBStatsAPIModel):

    # authorizations: fields.Dict()
    # info: fields.Int()
    url: fields.Str()
    api_doc: fields.Str()
    apis: fields.List(DocsAPIModel)
