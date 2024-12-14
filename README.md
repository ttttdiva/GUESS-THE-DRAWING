![alt text](<icon/DALL·E 2024-12-14 20.41.34 - A bold and clean anime-inspired game icon focusing on the sketchpad and the 'GUESS THE DRAWING' logo. The design features the childlike bird drawing p.webp>)

## 概要
本プロジェクトは、outdraw.AIというゲームをDiscord BotとFastAPIを組み合わせ再現したお絵かき連想ゲームです。

1人の出題者が指定されたお題を絵で描き、他の参加者(人間)は回答でお題を当てます。同時に、AI（OpenAI API）も画像を解析してお題を推測します。

最終的に、AIが間違えて人間が正解すれば人間チームの勝利、それ以外はAIの勝利となります。


主な特徴:

- 出題者はWebキャンバスで絵を描いてDiscord経由で提示。
- 観戦者はリアルタイムで描画を閲覧可能（描画履歴を保持し途中参加でも過去の描画が再現可能）。
- 回答フェーズでは人間が文字で回答を行い、AIはChat APIで画像（ローカルファイル）から推測。
- Chat APIを用いて、回答が正解かどうか、最多人間回答抽出などをAIに任せる仕組み。
- 60秒経過で自動的に判定。/end_gameコマンドでも判定可能。
- タイマー表示機能、キャンバスリセット機能あり。

## 前提条件(セットアップする人のみ)

- Python 3.9以上
- OpenAI APIキー (環境変数 `OPENAI_API_KEY` で設定)
- Discord Bot用トークン (`Discord_TOKEN` 環境変数で設定)
- Node.js不要（HTML/JSは純粋なフロント）
- ホスティングサービスの利用(または自宅ルーターでのNAT/ポートフォワーディング)
 - ホスティング利用時は"localhost:8000"を使用するドメイン名に変更

## セットアップ

1. リポジトリをクローン


 ```bash

 git clone <このリポジトリのURL>

 cd project

 ```

2. setup.batを実行

## 実行方法

run.batを実行

これにより同一プロセス内でFastAPIサーバーとDiscord Botが起動します。

- FastAPI: `http://localhost:8000`
- Discord: Botが起動し、指定のサーバーでコマンドが使用可能に。

## 使い方(ゲームフロー)

1. Discordチャンネルで`/start_game`コマンドを実行

 - 出題者が選ばれ、出題者用URLと観戦用URLが表示・通知されます。

 - 出題者は出題者用URL(描画画面)を開き、1分以内にお題を絵で描きます。

 - 観戦者は観戦用URL(ビューア画面)を開くことでリアルタイムで描画観戦可能。

2. 出題者は「描画完了」ボタンで画像をDiscordに提示(任意のタイミング)

 - 60秒経過前なら画像のみ先行表示され、ジャッジは保留されます。

 - 観戦者(回答者)はDiscord上で`/answer`コマンドを用いて回答を投稿できます。

3. 60秒経過または`/end_game`コマンドで判定実行

 - AIはローカル保存された画像から推測し回答。

 - Chat APIにより人間側最多回答抽出と正解判定を行い、勝敗を表示します。

 - 人間が正解でAI不正解のみ人間勝利、それ以外（AI正解または両者不正解）はAI勝利。

## 主なファイル

- `app.py`: FastAPIサーバーとDiscord Botを同一プロセスで稼働。


WebSocket経由でリアルタイム描画共有、`/submit_image`ハンドリング、`do_judgement`実行など。
- `game_logic.py`: ゲームロジック（お題選択、AI回答解析呼び出し、勝敗判定）
- `db.py`: メモリ上のゲーム状態管理
- `openai_helper.py`: OpenAI Chat APIコール（回答判定、最多回答抽出、画像解析に利用）
- `web/templates/`: 出題者用・観戦者用HTMLテンプレート
- `web/static/js/`: drawer.js・viewer.jsで描画・観戦用のフロントロジック

## カスタマイズ

- `topics`リストを変更することでお題を増やせます。
- `check_answer_via_chat`, `pick_human_final_answer_via_chat`などを変更することで回答判定ロジックをカスタマイズできます。
- `model="gpt-4o-mini"`部分を変更して利用可能なモデルへ切り替え可能。

## 制限事項・注意点

- このゲームはあくまでサンプル実装であり、本番環境での利用にはセキュリティ・エラーハンドリング強化が必要です。
