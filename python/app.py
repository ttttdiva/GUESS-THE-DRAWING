# app.py
import asyncio
import base64
import os
import time
import uuid
from io import BytesIO
from typing import Any, Dict

import discord
import uvicorn
# GAMESはdb.pyからインポート
from db import (GAMES, add_answer, get_ai_answer, get_answers,
                get_final_image_url, get_game_info, get_players, get_state,
                get_topic, set_ai_answer, set_final_image, set_state)
from discord.ext import commands
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, Form, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from game_logic import (analyze_ai_answer_async, analyze_image, judge_winner,
                        record_answer, start_game, submit_final_image)
from PIL import Image

load_dotenv(find_dotenv())
token = os.environ["Discord_TOKEN"]

app = FastAPI()

app.mount("/static", StaticFiles(directory="../web/static"), name="static")
templates = Jinja2Templates(directory="../web/templates")

rooms = {}

@app.get("/drawer/{room_id}")
async def get_drawer_page(room_id: str):
    return templates.TemplateResponse("drawer.html", {"request": {}, "room_id": room_id})

@app.get("/viewer/{room_id}")
async def get_viewer_page(room_id: str):
    return templates.TemplateResponse("viewer.html", {"request": {}, "room_id": room_id})

@app.get("/time_left/{game_id}")
async def time_left(game_id: str):
    if game_id not in GAMES:
        return {"time_left": 0}
    start_time = GAMES[game_id].get("start_time")
    if not start_time:
        return {"time_left": 0}
    elapsed = time.time() - start_time
    remaining = 120 - int(elapsed)
    if remaining < 0:
        remaining = 0
    return {"time_left": remaining}

@app.post("/submit_image")
async def submit_image(game_id: str = Form(...), img_data: str = Form(...)):
    header, encoded = img_data.split(",",1)
    img_bytes = base64.b64decode(encoded)
    img = Image.open(BytesIO(img_bytes))
    filename = f"{game_id}_{uuid.uuid4().hex}.png"
    save_path = f"../web/static/{filename}"
    img.save(save_path)

    # Web上のURL
    image_url = f"http://localhost:10096/static/{filename}"
    # set_final_imageにURLを渡す
    set_final_image(game_id, image_url)

    GAMES[game_id]["final_image_submitted"] = True

    # ここで出題者が描画完了を押したことによる画像送信（Discord）を行う
    # ctxを取得してDiscordへ画像を送る
    ctx = GAMES[game_id].get("ctx")
    if ctx:
        # 画像のみ送信、まだジャッジはしない
        # Discordに画像を貼り付けるにはdiscord.Fileを利用
        # ローカルファイルsave_pathをFileオブジェクトに
        await ctx.followup.send("描画が完了しました！", file=discord.File(save_path))
        # ※ジャッジはしない、あくまで画像送信のみ

    return {"status": "ok", "image_url": image_url}

@app.websocket("/ws/draw/{room_id}")
async def websocket_draw_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    if room_id not in rooms:
        rooms[room_id] = {
            "drawer_ws": websocket,
            "viewers_ws": [],
            "history": []  # 過去の描画イベントを蓄積
        }
    else:
        rooms[room_id]["drawer_ws"] = websocket
    try:
        while True:
            data = await websocket.receive_text()
            # dataはJSON文字列、ここで必要ならパース
            # ただし後続でviewerにも送るのでパース＆リファレンスで実行する
            rooms[room_id]["history"].append(data)
            for vws in rooms[room_id]["viewers_ws"]:
                await vws.send_text(data)
    except WebSocketDisconnect:
        if room_id in rooms:
            rooms[room_id]["drawer_ws"] = None

@app.websocket("/ws/view/{room_id}")
async def websocket_view_endpoint(websocket: WebSocket, room_id: str):
    await websocket.accept()
    if room_id not in rooms:
        rooms[room_id] = {
            "drawer_ws": None,
            "viewers_ws": [websocket],
            "history": []
        }
    else:
        rooms[room_id]["viewers_ws"].append(websocket)
        # 接続した観戦者に過去の描画履歴を全て送信
        for event in rooms[room_id]["history"]:
            await websocket.send_text(event)
    try:
        while True:
            data = await websocket.receive_text()
            # 観戦者から送られる予定はないが、念のため無視
    except WebSocketDisconnect:
        if room_id in rooms and websocket in rooms[room_id]["viewers_ws"]:
            rooms[room_id]["viewers_ws"].remove(websocket)

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Bot(intents=intents)

current_game_id = None

async def create_blank_image():
    img = Image.new("RGB", (200, 200), (255,255,255))
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    filename = f"blank_{uuid.uuid4().hex}.png"
    save_path = f"../web/static/{filename}"
    with open(save_path, 'wb') as f:
        f.write(buf.read())
    # ローカルパスはsave_path
    # ここでimage_urlも生成（もし必要なら）
    image_url = f"http://localhost:10096/static/{filename}"
    return image_url, save_path

async def schedule_judgement(game_id: str):
    await asyncio.sleep(120)  # 60秒待機
    if not GAMES[game_id]["judgement_done"]:
        if not GAMES[game_id]["final_image_submitted"]:
            blank_url = await create_blank_image()
            submit_final_image(game_id, blank_url)
        await do_judgement(game_id)
        GAMES[game_id]["judgement_done"] = True

def analyze_ai_answer_sync(game_id: str):
    # 同期的なOpenAI API呼び出しをここで実行
    image_url = get_final_image_url(game_id)
    ai_guess = analyze_image(image_url)
    set_ai_answer(game_id, ai_guess)

async def analyze_ai_answer_async(game_id: str):
    # 非同期で同期関数をスレッド実行
    await asyncio.to_thread(analyze_ai_answer_sync, game_id)

async def do_judgement(game_id: str):
    # 一度イベントループに戻して他のI/Oを処理させる
    await asyncio.sleep(0)

    # OpenAI API呼び出しを別スレッドで実行し、イベントループをブロックしない
    await analyze_ai_answer_async(game_id)

    # judge_winnerでwinner, chosen, topic取得
    winner, chosen, topic = judge_winner(game_id)
    final_url = get_final_image_url(game_id)
    ai_ans = get_ai_answer(game_id)  # AIが推測した回答を取得

    print("結果発表！")
    print(f"最終画像: {final_url}")
    print(f"正解: {topic}")
    print(f"人間の最多回答: {chosen}")
    print(f"AIの回答: {ai_ans}")
    print(f"勝者は... { '人間チーム' if winner=='HUMAN' else 'AI'} です！")

    ctx = GAMES[game_id].get("ctx")
    if ctx:
        await ctx.followup.send(f"""結果発表！
最終画像: {final_url}
正解: {topic}
人間の最多回答: {chosen if chosen else 'なし'}
AIの回答: {ai_ans}
勝者は... { '人間チーム' if winner=='HUMAN' else 'AI'} です！""")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.slash_command(name="start_game", description="ゲームを開始します。")
async def start_game_cmd(ctx: discord.ApplicationContext):
    await ctx.defer()
    global current_game_id
    drawer_id = ctx.author.id
    game_id = start_game(drawer_id)
    current_game_id = game_id

    set_state(game_id, "ANSWERING")
    GAMES[game_id]["judgement_done"] = False
    GAMES[game_id]["final_image_submitted"] = False
    GAMES[game_id]["ctx"] = ctx
    GAMES[game_id]["start_time"] = time.time()  # 開始時刻保存
    GAMES[game_id]["timer_task"] = asyncio.create_task(schedule_judgement(game_id))

    info = get_game_info(game_id)
    drawer_member = ctx.author
    try:
        await drawer_member.send(
            f"あなたは出題者です！お題: {info['topic']}\nこちらで絵を描いてください: {info['drawer_url']}"
        )
    except discord.Forbidden:
        await ctx.followup.send(f"{drawer_member.mention} さんにDMを送れませんでした。DMを有効にしてください。")

    await ctx.followup.send(f"ゲーム開始！観戦用URL: {info['viewer_url']}")

@bot.slash_command(name="answer", description="お題の答えを投稿します。")
async def answer_cmd(ctx: discord.ApplicationContext, answer: str):
    global current_game_id
    if current_game_id is None:
        # インタラクションが有効な間に応答するため、即時応答
        await ctx.respond("ゲームが開始されていません", ephemeral=True)
        return
    # 常に回答フェーズにするため、ここでget_stateを確認する必要がなくなりますが、
    # 念のため"ANSWERING"であることを前提とします。
    # 仮に他でstateを操作する場合に備え、チェックを残す場合はこうします。
    st = get_state(current_game_id)
    if st != "ANSWERING":
        # 即座にrespondできる場合はrespondを使う
        await ctx.respond("今は回答フェーズではありません")
        return
    record_answer(current_game_id, ctx.author.id, answer)

    # ここで応答が遅れている場合、すでにdeferしていたらfollowup.sendを使用
    # そうでなければrespondで問題ありません。
    await ctx.respond(f"{ctx.author.name} の回答: {answer} を受け付けました")

@bot.slash_command(name="end_game", description="ゲームを終了し結果を表示します。")
async def end_game_cmd(ctx: discord.ApplicationContext):
    global current_game_id
    if current_game_id is None:
        await ctx.respond("ゲームが開始されていません")
        return

    # ここでdeferしておくと、このコマンドの最初のレスポンスを後でfollowupで送れる
    await ctx.defer()

    set_state(current_game_id, "RESULT")
    if not GAMES[current_game_id]["judgement_done"]:
        if not GAMES[current_game_id]["final_image_submitted"]:
            blank_url, blank_local_path = await create_blank_image()
            submit_final_image(current_game_id, blank_url)
        await do_judgement(current_game_id)
        GAMES[current_game_id]["judgement_done"] = True

    # 最後のメッセージはrespondではなく、followup.sendを使用
    await ctx.followup.send("結果発表を行いました！")




async def main():
    config = uvicorn.Config(app, host="0.0.0.0", port=10096, log_level="info")
    server = uvicorn.Server(config)
    await asyncio.gather(
        server.serve(),
        bot.start(token)
    )

if __name__ == "__main__":
    asyncio.run(main())
