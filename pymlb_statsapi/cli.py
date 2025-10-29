# """Console script for mlb_statsapi."""
#
# import argparse
# import json
# import os.path
# import sys
# import traceback
#
# from pymlb_statsapi.model.stats_api import StatsAPIModelRegistry
# from pymlb_statsapi.utils.aws import StepFunctions
#
# AWS_STEP_FUNCTIONS_TASK_TOKEN = os.environ.get("AWS_STEP_FUNCTIONS_TASK_TOKEN")
#
#
# def runTask(run, **kwargs) -> dict:
#     try:
#         res = run(**kwargs)
#         StepFunctions().send_task_success(
#             taskToken=AWS_STEP_FUNCTIONS_TASK_TOKEN, output=json.dumps(res)
#         )
#         return res
#     except Exception as e:
#         StepFunctions().send_task_failure(
#             taskToken=AWS_STEP_FUNCTIONS_TASK_TOKEN,
#             error="States.TaskFailed",
#             cause=traceback.format_exc(),
#         )
#         raise e
#
#
# class Arguments:
#     @staticmethod
#     def date(add_argument: callable, *args, **kwargs):
#         from pymlb_statsapi.utils import get_current_mlb_date
#
#         add_argument(
#             "-d",
#             "--date",
#             *args,
#             type=str,
#             default=str(get_current_mlb_date()),
#             **kwargs,
#         )
#
#     @staticmethod
#     def gamePk(add_argument: callable, *args, **kwargs):
#         add_argument("--gamePk", *args, type=int, **kwargs)
#
#     @staticmethod
#     def gameType(add_argument: callable, *args, **kwargs):
#         add_argument("-gt", "--gameType", *args, type=str, **kwargs)
#
#     @staticmethod
#     def method(add_argument: callable, name, *args, **kwargs):
#         add_argument(
#             "-m",
#             "--method",
#             *args,
#             type=str,
#             required=True,
#             **kwargs,
#             help="StatsAPI Model method, choose from %s"
#             % [*StatsAPIModelRegistry.API_MAP[name].methods.keys()],
#         )
#
#     @staticmethod
#     def personIds(add_argument: callable, *args, **kwargs):
#         add_argument("-pi", "--personIds", *args, type=str, nargs="+", **kwargs)
#
#     @staticmethod
#     def personIdsJSON(add_argument: callable, *args, **kwargs):
#         add_argument(
#             "-pij", "--personIdsJSON", *args, type=str, nargs="+", **kwargs
#         )
#
#     @staticmethod
#     def rosterType(add_argument: callable, *args, **kwargs):
#         add_argument(
#             "-rt", "--rosterType", *args, type=str, default="depthChart", **kwargs
#         )
#
#     @staticmethod
#     def season(add_argument: callable, *args, **kwargs):
#         from pymlb_statsapi.utils import get_current_mlb_date
#
#         add_argument(
#             "--season",
#             *args,
#             type=int,
#             default=get_current_mlb_date().year,
#             **kwargs,
#         )
#
#     @staticmethod
#     def seasonIds(add_argument: callable, *args, **kwargs):
#         from pymlb_statsapi.utils import get_current_mlb_date
#
#         add_argument(
#             "--seasonIds",
#             *args,
#             type=int,
#             nargs="+",
#             default=get_current_mlb_date().year,
#             **kwargs,
#         )
#
#     @staticmethod
#     def seasonIdsJSON(add_argument: callable, *args, **kwargs):
#         from pymlb_statsapi.utils import get_current_mlb_date
#
#         add_argument(
#             "--seasonIdsJSON",
#             *args,
#             type=str,
#             default=json.dumps(
#                 [
#                     get_current_mlb_date().year,
#                 ]
#             ),
#             **kwargs,
#         )
#
#     @staticmethod
#     def sportId(add_argument: callable, *args, **kwargs):
#         add_argument("--sportId", *args, type=int, default=1, **kwargs)
#
#     @staticmethod
#     def startTime(add_argument: callable, *args, **kwargs):
#         add_argument("--startTime", *args, type=str, **kwargs)
#
#     @staticmethod
#     def teamIds(add_argument: callable, *args, **kwargs):
#         add_argument("-ti", "--teamIds", *args, type=int, nargs="+", **kwargs)
#
#     @staticmethod
#     def teamIdsJSON(add_argument: callable, *args, **kwargs):
#         add_argument("-tij", "--teamIdsJSON", *args, type=str, **kwargs)
#
#
# # noinspection PyPep8Naming
# def add_subparsers(parser):
#     subparsers = parser.add_subparsers(
#         help="application to run", dest="app", required=True
#     )
#     app_parsers = {}
#     for app in Apps.values():  # skip api_docs
#         name = app.__name__
#         app_parsers[name] = subparsers.add_parser(name)
#         Arguments.method(app_parsers[name].add_argument, name)
#
#     # "boxscore", "linescore", "liveGameV1", "liveGameDiffPatchV1", "playByPlay"
#     Arguments.date(app_parsers["Game"].add_argument, required=True)
#     Arguments.gamePk(app_parsers["Game"].add_argument)
#     Arguments.startTime(app_parsers["Game"].add_argument)
#     Arguments.sportId(app_parsers["Game"].add_argument)
#
#     Arguments.season(app_parsers["Person"].add_argument, required=False)
#     personIdsGroup = app_parsers["Person"].add_mutually_exclusive_group(
#         required=True
#     )
#     Arguments.personIds(personIdsGroup.add_argument)
#     Arguments.personIdsJSON(personIdsGroup.add_argument)
#
#     Arguments.date(app_parsers["Team"].add_argument)
#     Arguments.rosterType(app_parsers["Team"].add_argument, required=False)
#     Arguments.gameType(app_parsers["Team"].add_argument)
#     teamIdsGroup = app_parsers["Team"].add_mutually_exclusive_group(required=True)
#     Arguments.teamIds(teamIdsGroup.add_argument)
#     Arguments.teamIdsJSON(teamIdsGroup.add_argument)
#
#     Arguments.date(app_parsers["Schedule"].add_argument, required=True)
#     Arguments.sportId(app_parsers["Schedule"].add_argument)
#
#     Arguments.sportId(app_parsers["Season"].add_argument)
#     seasonIdsGroup = app_parsers["Season"].add_mutually_exclusive_group(
#         required=True
#     )
#     Arguments.seasonIds(seasonIdsGroup.add_argument)
#     Arguments.seasonIdsJSON(seasonIdsGroup.add_argument)
#
#     return subparsers
#
#
# def parse_args():
#     """Console script for mlb_statsapi."""
#     parser = argparse.ArgumentParser()
#     parser.add_argument("--indent", default=None, required=False, type=int)
#     parser.add_argument("--force", default=False, required=False, type=bool)
#
#     add_subparsers(parser)
#
#     return parser.parse_args()
#
#
# def Game(args: argparse.Namespace) -> dict:
#     from pymlb_statsapi import apps
#
#     return apps.Game.run(
#         date=args.date,
#         gamePk=args.gamePk,
#         startTime=args.startTime,
#         sportId=args.sportId,
#         method=args.method,
#     )
#
#
# def Schedule(args: argparse.Namespace) -> dict:
#     from pymlb_statsapi import apps
#
#     return apps.Schedule.run(
#         sportId=args.sportId, date=args.date, method=args.method
#     )
#
#
# def Team(args: argparse.Namespace) -> dict:
#     from pymlb_statsapi import apps
#
#     kwargs = {"api": args.app, "method": args.method, "force": args.force}
#     if args.method == "roster":
#         run = apps.Team.roster
#         kwargs["date"] = args.date
#         kwargs["rosterType"] = args.rosterType
#         kwargs["teamIds"] = (
#             json.loads(args.teamIdsJSON) if args.teamIds is None else args.teamIds
#         )
#         if args.gameType is not None:
#             kwargs["gameType"] = args.gameType
#     else:
#         raise NotImplementedError("Unknown %s method %s" % (args.app, args.method))
#     return run(**kwargs)
#
#
# def Person(args: argparse.Namespace) -> dict:
#     from pymlb_statsapi import apps
#
#     kwargs = {"api": args.app, "method": args.method, "force": args.force}
#     if args.method == "person":
#         run = apps.Person.person
#         if args.personIds is not None:
#             kwargs["personIds"] = args.personIds
#         else:
#             kwargs["personIds"] = [
#                 personId
#                 for personIds in args.personIdsJSON
#                 for personId in json.loads(personIds)
#             ]
#         kwargs["season"] = args.season
#     else:
#         raise NotImplementedError("Unknown %s method %s" % (args.app, args.method))
#     return run(**kwargs)
#
#
# def Season(args: argparse.Namespace) -> dict:
#     from pymlb_statsapi import apps
#
#     kwargs = {"api": args.app, "method": args.method, "force": args.force}
#     if args.method == "season":
#         run = apps.Season.season
#         kwargs["sportId"] = args.sportId
#         kwargs["seasonIds"] = (
#             json.loads(args.seasonIdsJSON)
#             if args.seasonIds is None
#             else args.seasonIds
#         )
#     else:
#         raise NotImplementedError("Unknown %s method %s" % (args.app, args.method))
#     return run(**kwargs)
#
#
# Apps = {
#     app.__name__: app
#     for app in (
#         Game,
#         Person,
#         Schedule,
#         Season,
#         Team,
#     )
# }
#
#
# def main() -> int:
#     try:
#         args = parse_args()
#         res = Apps[args.app](args)
#         if AWS_STEP_FUNCTIONS_TASK_TOKEN is not None:
#             StepFunctions().send_task_success(
#                 taskToken=AWS_STEP_FUNCTIONS_TASK_TOKEN, output=json.dumps(res)
#             )
#         print(json.dumps(res, indent=args.indent))
#         return 0
#     except Exception as e:
#         if AWS_STEP_FUNCTIONS_TASK_TOKEN is not None:
#             StepFunctions().send_task_failure(
#                 taskToken=AWS_STEP_FUNCTIONS_TASK_TOKEN,
#                 error="States.TaskFailed",
#                 cause=traceback.format_exc(),
#             )
#         raise e
#
#
# if __name__ == "__main__":
#     sys.exit(main())
