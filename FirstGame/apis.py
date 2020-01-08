from django.http import JsonResponse
from .table import Table
from .player import Player
from .game import Game
import random

games = {}


def get_empty_player_game():
    for key in games.keys():
        game = games[key]
        if game.table.hasEmptyPlayer():
            return game

    game = Game()
    t = Table()
    game.table = t
    games[t.code] = game
    return game


def check_game(code, callback, **var_dict):
    game = games.get(code)
    if code <= 0 or game is None:
        return JsonResponse(build_resp(-1, "Game not found"))
    else:
        return callback(game, **var_dict)


def build_resp(code, msg, data={}):
    return {
        "code": code,
        "msg": msg,
        "data": data
    }


def enter(request):
    game = get_empty_player_game()
    default_name = str(random.randint(1000, 999999))
    name = request.GET.get("name", default=default_name)
    name = name if name != "" else default_name
    player = Player(name)
    if game.enterPlayer(player) == 0:
        return JsonResponse(build_resp(0, "请求成功", game.toDict()))
    else:
        return JsonResponse(build_resp(-1, "昵称不能和对手一样", {}))


def __ready(game, role):
    if role is None:
        return JsonResponse(build_resp(-1, "参数错误", {}))
    if game.ready(role) == 0:
        return JsonResponse(build_resp(0, "请求成功", game.toDict()))
    else:
        return JsonResponse(build_resp(-1, "参数错误", {}))


def __play(game, role, position):
    # role = vardict["role"]
    # position = None
    if role is None or position is None:
        return JsonResponse(build_resp(-1, "参数错误", {}))
    if game.play(role, position) >= 0:
        return JsonResponse(build_resp(0, "请求成功", game.toDict()))
    else:
        return JsonResponse(build_resp(-1, "参数错误", {}))


def ready(request):
    table_code = int(request.GET.get("tableCode", default=-1))
    role = request.GET.get("role", default="")
    return check_game(table_code, __ready, role=role)


def play(request):
    table_code = int(request.GET.get("tableCode", default=-1))
    role = request.GET.get("role", default="")
    position = int(request.GET.get("position", default=-1))
    return check_game(table_code, __play, role=role, position=position)
