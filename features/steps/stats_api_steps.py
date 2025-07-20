import json
from behave import given, then


@given("the StatsAPI endpoint {endpoint_name}")
def step_impl(context, endpoint_name):
    from pymlb_statsapi.model.stats_api import StatsAPI

    context.endpoint = getattr(StatsAPI, endpoint_name)
    context.endpoint_name = endpoint_name


@given("the api {api_name}")
def step_impl(context, api_name: str):
    context.api = getattr(context.endpoint, api_name)


@given("the path parameters {path_params}")
def step_impl(context, path_params: str):
    context.path_params = json.loads(path_params)


@given("the query parameters {query_params}")
def step_impl(context, query_params: str):
    context.query_params = json.loads(query_params)

@then("I can create an endpoint object")
def step_impl(context):
    kwargs = {}
    if hasattr(context, 'path_params'):
        kwargs['path_params'] = context.path_params
    if hasattr(context, 'query_params'):
        kwargs['query_params'] = context.query_params
    context.obj = context.api(**kwargs)


@then("I can get the endpoint object data")
def step_impl(context):
    obj = context.obj.get()
    assert obj.obj is not None, "The endpoint object data should not be None"
    print("%s: %s" % (
        context.endpoint_name,
        json.dumps(obj.obj, indent=2)
    ))