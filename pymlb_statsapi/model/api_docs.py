"""
created by nikos at 4/21/21
"""

from serde import fields

from .base import APIModelBase, MLBStatsAPIModel


class DocsAPIModel(APIModelBase):
    position: fields.Int()


class ApiDocsModel(MLBStatsAPIModel):
    # authorizations: fields.Dict()
    # info: fields.Int()
    url: fields.Str()
    api_doc: fields.Str()
    apis: fields.List(DocsAPIModel)
