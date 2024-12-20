# python/db.py
# 本当はRDBMSを使うべきですが、ここではシンプルにメモリ上でデータ管理。

import uuid
from typing import Any, Dict

# データ格納用辞書(超簡易)
GAMES: Dict[str, Dict[str, Any]] = {}

def create_game(drawer_id: int, topic: str) -> str:
    game_id = str(uuid.uuid4())
    GAMES[game_id] = {
        "drawer_id": drawer_id,
        "topic": topic,
        "players": [drawer_id],
        "state": "DRAWING",
        "answers": [],
        "ai_answer": None,
        "viewer_url": f"http://localhost:10096/viewer/{game_id}",
        "drawer_url": f"http://localhost:10096/drawer/{game_id}",
        "final_image_url": None
    }
    return game_id

def add_player(game_id: str, player_id: int):
    if player_id not in GAMES[game_id]["players"]:
        GAMES[game_id]["players"].append(player_id)

def add_answer(game_id: str, player_id: int, answer: str):
    GAMES[game_id]["answers"].append((player_id, answer))

def set_final_image(game_id: str, url: str):
    GAMES[game_id]["final_image_url"] = url

def get_final_image_path(game_id: str):
    return GAMES[game_id].get("final_image_url")

def set_state(game_id: str, state: str):
    GAMES[game_id]["state"] = state

def set_ai_answer(game_id: str, ans: str):
    GAMES[game_id]["ai_answer"] = ans

def get_game_info(game_id: str):
    return GAMES.get(game_id)

def get_topic(game_id: str):
    return GAMES[game_id]["topic"]

def get_drawer_id(game_id: str):
    return GAMES[game_id]["drawer_id"]

def get_final_image_url(game_id: str):
    return GAMES[game_id]["final_image_url"]

def get_ai_answer(game_id: str):
    return GAMES[game_id]["ai_answer"]

def get_answers(game_id: str):
    return GAMES[game_id]["answers"]

def get_players(game_id: str):
    return GAMES[game_id]["players"]

def get_state(game_id: str):
    return GAMES[game_id]["state"]
