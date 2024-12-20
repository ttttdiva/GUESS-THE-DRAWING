<<<<<<< HEAD
# game_logic.py

import random
from collections import Counter

from db import (add_answer, create_game, get_ai_answer, get_answers,
                get_final_image_url, get_game_info, get_players, get_state,
                get_topic, set_ai_answer, set_final_image, set_state)
from openai_helper import (analyze_image, check_answer_via_chat,
                           pick_human_final_answer_via_chat)

topics = [
    "イヌ",
    "ネコ",
    "ウサギ",
    "ハムスター",
    "リス",
    "サル",
    "チンパンジー",
    "ゴリラ",
    "コアラ",
    "カンガルー",
    "パンダ",
    "クマ",
    "ライオン",
    "トラ",
    "キリン",
    "ゾウ",
    "サイ",
    "カバ",
    "ウシ",
    "ウマ",
    "ブタ",
    "ヒツジ",
    "ヤギ",
    "シカ",
    "イノシシ",
    "ロバ",
    "ラクダ",
    "オオカミ",
    "キツネ",
    "ビーバー",
    "アザラシ",
    "ラッコ",
    "セイウチ",
    "カモノハシ",
    "ナマケモノ",
    "ミーアキャット",
    "ヤマアラシ",
    "ハリネズミ",
    "アルマジロ",
    "ワシ",
    "フクロウ",
    "ペンギン",
    "ダチョウ",
    "クジャク",
    "ハクチョウ",
    "アヒル",
    "ニワトリ",
    "ツル",
    "フラミンゴ",
    "ペリカン",
    "ハシビロコウ",
    "キウイ",
    "ハゲワシ",
    "キツツキ",
    "ワニ",
    "リクガメ",
    "ウミガメ",
    "トカゲ",
    "ヘビ",
    "カメレオン",
    "カエル",
    "サメ",
    "クジラ",
    "イルカ",
    "タツノオトシゴ",
    "マンボウ",
    "カニ",
    "エビ",
    "タコ",
    "イカ",
    "クラゲ",
    "ヒトデ",
    "キンギョ",
    "チョウ",
    "テントウムシ",
    "カブトムシ",
    "クワガタ",
    "ハチ",
    "アリ",
    "バッタ",
    "カマキリ",
    "トンボ",
    "クモ",
    "サソリ",
    "ユニコーン",
    "ペガサス",
    "ドラゴン",
    "フェニックス",
    "グリフィン",
    "リンゴ",
    "バナナ",
    "イチゴ",
    "パイナップル",
    "ブドウ",
    "スイカ",
    "メロン",
    "オレンジ",
    "レモン",
    "チェリー",
    "モモ",
    "ナシ",
    "キウイフルーツ",
    "マンゴー",
    "パパイヤ",
    "ココナッツ",
    "ニンジン",
    "ダイコン",
    "キュウリ",
    "ナス",
    "トマト",
    "キャベツ",
    "タマネギ",
    "ジャガイモ",
    "サツマイモ",
    "カボチャ",
    "トウモロコシ",
    "ブロッコリー",
    "アスパラガス",
    "マッシュルーム",
    "ハンバーガー",
    "ピザ",
    "ホットドッグ",
    "ドーナツ",
    "アイスクリーム",
    "カップケーキ",
    "パンケーキ",
    "クッキー",
    "オムライス",
    "オニギリ",
    "スシ",
    "タコヤキ",
    "オコノミヤキ",
    "ヤキザカナ",
    "クシカツ",
    "リンゴアメ",
    "ワッフル",
    "フライドポテト",
    "ギョウザ",
    "ハルマキ",
    "ニクマン",
    "チョコレート",
    "プレッツェル",
    "クロワッサン",
    "ショクパン",
    "ベーグル",
    "マカロン",
    "シュークリーム",
    "バゲット",
    "メロンパン",
    "カレーライス",
    "スパゲッティ",
    "ソバ",
    "ラーメン",
    "ピーナッツ",
    "アーモンド",
    "ソフトクリーム",
    "ケーキ",
    "バウムクーヘン",
    "マグカップ",
    "ティーポット",
    "ペットボトル",
    "ワイングラス",
    "コーヒーカップ",
    "ビールジョッキ",
    "クルマ",
    "バス",
    "トラック",
    "バイク",
    "ジテンシャ",
    "ヘリコプター",
    "ヒコウキ",
    "ロケット",
    "センスイカン",
    "フネ",
    "ヨット",
    "ボート",
    "シンカンセン",
    "ジョウキキカンシャ",
    "スクーター",
    "キキュウ",
    "モノレール",
    "トロリーバス",
    "ロメンデンシャ",
    "ショウボウシャ",
    "キュウキュウシャ",
    "パトカー",
    "フォークリフト",
    "ブルドーザー",
    "クレーンシャ",
    "ダンプカー",
    "トラクター",
    "イエ",
    "シロ",
    "ピラミッド",
    "エッフェルタワー",
    "トウキョウタワー",
    "スカイツリー",
    "トウダイ",
    "フウシャ",
    "イグルー",
    "テント",
    "イス",
    "テーブル",
    "ベッド",
    "ソファ",
    "タンス",
    "ホンダナ",
    "スプーン",
    "フォーク",
    "ナイフ",
    "ハシ",
    "フライパン",
    "ナベ",
    "ヤカン",
    "マナイタ",
    "ホウチョウ",
    "サラ",
    "ボウル",
    "コップ",
    "ティーカップ",
    "テーブルクロス",
    "テレビ",
    "レイゾウコ",
    "センタクキ",
    "ソウジキ",
    "デンシレンジ",
    "スイハンキ",
    "トースター",
    "ペン",
    "エンピツ",
    "ケシゴム",
    "ジョウギ",
    "ハサミ",
    "ノリ",
    "ホッチキス",
    "カッター",
    "セロハンテープ",
    "クリップ",
    "シャープペン",
    "マーカー",
    "クレヨン",
    "ボウシ",
    "ヤキュウボウ",
    "ニットボウ",
    "マフラー",
    "テブクロ",
    "クツ",
    "ナガグツ",
    "スリッパ",
    "メガネ",
    "サングラス",
    "ネクタイ",
    "マスク",
    "リュックサック",
    "バッグ",
    "ベルト",
    "カサ",
    "アマガッパ",
    "ハンマー",
    "ドライバー",
    "スパナ",
    "レンチ",
    "ペンチ",
    "ノコギリ",
    "シャベル",
    "スコップ",
    "オノ",
    "クギ",
    "ネジ",
    "ドリル",
    "ハシゴ",
    "ギター",
    "バイオリン",
    "ピアノ",
    "トランペット",
    "サックス",
    "フルート",
    "ドラム",
    "ハープ",
    "クラリネット",
    "ホルン",
    "サッカーボール",
    "バスケットボール",
    "ヤキュウボール",
    "テニスラケット",
    "ヤキュウバット",
    "ゴルフクラブ",
    "ボウリングピン",
    "バレーボール",
    "シャトル",
    "タッキュウラケット",
    "スキーバン",
    "スノーボード",
    "スケートボード",
    "フリスビー",
    "フラフープ",
    "アーチェリー",
    "ボクシンググローブ",
    "タイヨウ",
    "ツキ",
    "ホシ",
    "クモ",
    "ヤマ",
    "キ",
    "マツ",
    "サボテン",
    "ハナ",
    "ハッパ",
    "キノコ",
    "カイガラ",
    "シンゴウキ",
    "デンキュウ",
    "デンチ",
    "スマートフォン",
    "パソコン",
    "カメラ",
    "ウデドケイ",
    "スナドケイ",
    "コンパス",
    "チキュウギ",
    "ハート",
    "スペード",
    "カギ",
    "ナンドウジョウ",
    "オンプ",
    "パズル",
    "メガホン",
    "レコード",
    "カセットテープ",
    "ラジオ",
    "スピーカー",
    "マイク",
    "ギフトボックス",
    "バケツ",
    "ハンドベル",
    "トーチ",
    "ロウソク",
    "ルーペ",
    "ハンカチ",
    "ティッシュ",
    "ゴミバコ",
    "ノート",
    "ホン",
    "フウトウ",
    "マンネンヒツ",
    "メール",
    "カレンダー",
    "トケイ",
    "サイコロ",
    "チェスコマ",
    "チェスバン",
    "ショウギコマ",
    "イゴイシ",
    "トランプ",
    "ウノ",
    "モノポリー",
    "カルタ",
    "ハナフダ",
    "マージャン",
    "ドミノ",
    "ジェンガ",
    "ツイスター",
    "ボードゲーム",
    "ヨーヨー",
    "ケンダマ",
    "コマ",
    "タコ",
    "シャボンダマ",
    "ミズデッポウ",
    "パチンコ",
    "スーパーボール",
    "ジシャク",
    "マンゲキョウ",
    "ルービックキューブ",
    "ビリヤードダイ",
    "ビリヤードキュー",
    "ビリヤードボール",
    "ダーツボード",
    "ダーツ",
    "オセロバン",
    "ショウギバン",
    "イゴバン",
    "アコーディオン",
    "ハーモニカ",
    "リコーダー",
    "シェイカー",
    "アワダテキ",
    "フライガエシ",
    "オタマ",
    "ピーラー",
    "センヌキ",
    "コルクヌキ",
    "ケイリョウカップ",
    "ケイリョウスプーン",
    "トング",
    "チャコシ",
    "サンカクコーナー",
    "スリコギ",
    "スリバチ",
    "ミキサー",
    "ジューサー",
    "エッグスタンド",
    "バターケース",
    "アイスバケット",
    "スプレーボトル",
    "コロコロ",
    "クシ",
    "ヘアブラシ",
    "ドライヤー",
    "カミソリ",
    "デンキシェーバー",
    "ツメキリ",
    "ミミカキ",
    "メンボウ",
    "ケショウポーチ",
    "リップスティック",
    "マニキュア",
    "コウスイ",
    "ハンドクリーム",
    "フットボール",
    "アメフトヘルメット",
    "ヤキュウグローブ",
    "ヤキュウベース",
    "キャッチャーマスク",
    "ホッケースティック",
    "ホッケーパック",
    "ラクロススティック",
    "ツリザオ",
    "ツリバリ",
    "スイエイゴーグル",
    "スイエイキャップ",
    "シュノーケル",
    "フィン",
    "ダイビングボンベ",
    "スケートヘルメット",
    "ニーパッド",
    "エルボーパッド",
    "トザンブーツ",
    "トザンリュック",
    "トレッキングポール",
    "ジーピーエス",
    "チズ",
    "スリーピングバッグ",
    "カラビナ",
    "テントウチ",
    "ロープ",
    "ザブトン",
    "クッション",
    "ザッキン",
    "カーペット",
    "ジュウタン",
    "カーテン",
    "ブラインド",
    "ショウメンキョウ",
    "カガミ",
    "カイガ",
    "ポスター",
    "シャシンタテ",
    "ビールビン",
    "ワインビン",
    "シャンパンボトル",
    "コップザラ",
    "メンキョショウ",
    "パスポート",
    "ホケンショウ",
    "クレジットカード",
    "デビットカード",
    "プリペイドカード",
    "ギフトカード",
    "ショウヒンケン",
    "ビールケン",
    "コメケン",
    "トショカード",
    "クオカード",
    "スイカ",
    "パスモ",
    "イコカ",
    "トイカ",
    "マナカ",
    "ハヤカケン",
    "キタカ",
    "スゴカ",
    "ニモカ",
    "リンカイスイカ",
    "モバイルスイカ",
    "アップルペイ",
    "グーグルペイ",
    "ペイペイ",
    "ラインペイ",
    "ディーバライ",
    "エーユーペイ",
    "ラクテンペイ",
    "メルペイ",
    "ウィーチャットペイ",
    "アリペイ",
    "カラフルペン",
    "キーホルダー",
    "シュリンケンサック",
    "モップ",
    "ホウキ",
    "チリトリ",
    "ゴムテブクロ",
    "センメンキ",
    "シャワーヘッド",
    "バスタブ",
    "ハブラシ",
    "ハミガキコ",
    "セッケン",
    "タオル",
    "アイロン",
    "アイロンダイ",
    "ミシン",
    "ハンガー",
    "イトマキ",
    "ハリ",
    "ボタン",
    "ファスナー",
    "アンゼンピン",
    "メジャー",
    "カセツトウ",
    "ハンガキ",
    "ハサミカッター",
    "ウケザラ",
    "サラダボウル",
    "スプラッシュガード",
    "ランチョンマット",
    "ドアノブ",
    "ドア",
    "マド",
    "カギアナ",
    "デンチュウ",
    "デンセン",
    "ガイトウ",
    "フンスイ",
    "ベンチ",
    "チョウコク",
    "オフィスビル",
    "コウジョウ",
    "ソウコ",
    "シヨウカイドウ",
    "ヨウチエン",
    "ホイクエン",
    "ショウガッコウ",
    "チュウガッコウ",
    "コウコウ",
    "ダイガク",
    "トショカン",
    "ビジュツカン",
    "ハクブツカン",
    "スイゾクカン",
    "ドウブツエン",
    "ショクブツエン",
    "ユウエンチ",
    "スキージョウ",
    "ビーチ",
    "コウエン",
    "テイエン",
    "スタジアム",
    "ヤキュウジョウ",
    "サッカージョウ",
    "ケイバジョウ",
    "タイイクカン",
    "プール",
    "オンセン",
    "セントウ",
    "コンビニ",
    "スーパー",
    "デパート",
    "モール",
    "イチバ",
    "エキ",
    "バステイ",
    "クウコウ",
    "ミナト",
    "チュウシャジョウ",
    "トイレ",
    "ハシ",
    "ドウロ",
    "オウダンホドウ",
    "シンゴウ",
    "デンシンバシラ",
    "デンセン",
    "ガイトウ",
    "フンスイ",
    "ベンチ",
    "ホウムセンター",
    "ディーアイワイ",
    "スポーツヨウヒンテン",
    "アウトドアショップ",
    "ジテンシャヤ",
    "バイクショップ",
    "カーヨウヒンテン",
    "ガソリンスタンド",
    "センシャジョウ",
    "シュウリコウジョウ",
    "カーディーラー",
    "レンタカー",
    "フドウサンヤ",
    "ホケンヤ",
    "ユウビンキョク",
    "タクハイビンセンター",
    "ハイソウセンター",
    "ブツリュウソウコ",
    "インターネットカフェ",
    "マンガキッサ",
    "ゲームセンター",
    "パチンコテン",
    "スロットテン",
    "マージャンソウ",
    "ボウリングジョウ",
    "ビリヤードジョウ",
    "ダーツバー",
    "ゴルフジョウ",
    "ゴルフレンシュウジョウ",
    "テニスコート",
    "バスケットコート",
    "バレーボールコート",
    "バドミントンコート",
    "タッキュウダイ",
    "ボクシングリング",
    "レスリングマット",
    "ジュウドウタタミ",
    "ケンドウジョウ",
    "キュウドウジョウ",
    "ジム",
    "サウナ",
    "ステージ",
    "ブタイ",
    "エイガカン",
    "プラネタリウム",
    "カガクカン",
    "ギャラリー",
    "イルカショー",
    "コウバン",
    "ショウボウシュッチョウショ",
    "クリニック",
    "デンタルクリニック",
    "ヤッキョク",
    "ドラッグストア",
    "ブンボウグテン",
    "ホンヤ",
    "コフルホンヤ",
    "レコードショップ",
    "シーディーショップ",
    "ガッキテン",
    "ハナヤ",
    "ヤオヤ",
    "サカナヤ",
    "ニクヤ",
    "ケーキヤ",
    "ヨウガシテン",
    "ワガシテン",
    "デンキヤ",
    "カグヤ",
    "ジリツシホン",
    "スーツケース",
    "トランク",
    "ハイヤー",
    "バラ",
    "チューリップ",
    "ヒマワリ",
    "サクラ",
    "ウメ",
    "モミジ",
    "イチョウ",
    "シロツメクサ",
    "コスモス",
    "キク",
    "ボタン",
    "シャクヤク",
    "ガーベラ",
    "ラベンダー",
    "ローズマリー",
    "ミント",
    "バジル",
    "パセリ",
    "セロリ",
    "ネギ",
    "ニラ",
    "シソ",
    "オオバ",
    "タケノコ",
    "サンサイ",
    "シイタケ",
    "マツタケ",
    "シメジ",
    "エリンギ",
    "エノキ",
    "ポルチーニ",
    "トリュフ",
    "キャビア",
    "オマールエビ",
    "ズワイガニ",
    "タラバガニ",
    "カニカマ",
    "カニクリームコロッケ",
    "エビフライ",
    "カツドン",
    "テンドン",
    "オヤコドン",
    "ギュウドン",
    "タコス",
    "ブリトー",
    "ナチョス",
    "パエリア",
    "ガスパチョ",
    "クスクス",
    "ピロシキ",
    "ボルシチ",
    "ラザニア",
    "リゾット",
    "フィッシュアンドチップス",
    "ローストビーフ",
    "ローストチキン",
    "ブルスケッタ",
    "ティラミス",
    "エクレア",
    "シュークリーム",
    "ミルフィーユ",
    "クレープ",
    "マドレーヌ",
    "フィナンシェ",
    "カステラ",
    "ヨウカン",
    "マンジュウ",
    "モナカ",
    "ドラヤキ",
    "ワラビモチ",
    "オオバヤキ",
    "イマガワヤキ",
    "ニンギョウヤキ",
    "カルメヤキ",
    "カキゴオリ",
    "アンズアメ",
    "ワタガシ",
    "チョコバナナ",
    "リンゴアメ",
    "ポップコーン",
    "ヤキトウモロコシ",
    "フランクフルト",
    "ヤキソバ",
    "オデン",
    "ウメボシ",
    "タラコ",
    "メンタイコ",
    "チクワ",
    "カマボコ",
    "ハンペン",
    "オデンダネ",
    "ゴボウ",
    "レンコン",
    "ショウガ",
    "ニンニク",
    "ゴマ",
    "ダイズ",
    "コアズキ",
    "オカラ",
    "ドウフ",
    "ユバ",
    "ツミレ",
    "コンブ",
    "ワカメ",
    "ノリ",
    "ヒジキ",
    "タケヤブ",
    "カワラ",
    "イチョウバ",
    "マツバ",
    "シダ",
    "ハス",
    "スイレン",
    "アサガオ",
    "ヒルガオ",
    "ユリ",
    "バラエン",
    "ムギバタケ",
    "イネバタケ",
    "コメ",
    "コムギ",
    "ライムギ",
    "ソバ",
    "テンサイドウ",
    "アーモンドミルク",
    "ココナッツミルク",
    "ソイチーズ",
    "ビーガン",
    "カプレーゼ",
    "ニースサラダ",
    "スープカレー",
    "ワンタンスープ",
    "ミネストローネ",
    "ポタージュ",
    "クラムチャウダー",
    "オニオンスープ",
    "コンソメスープ",
    "トンジル",
    "スマシジル",
    "カニジル",
    "ハマグリジル",
    "シジミジル",
    "オジヤ",
    "ビリアニ",
    "プルコギ",
    "キムチ",
    "ビビンバ",
    "チヂミ",
    "サムゲタン",
    "カルビ",
    "ホルモン",
    "ジンギスカン",
    "ジャージャーメン",
    "レイメン",
    "クッパ",
    "トッポギ",
    "マッコリ",
    "ショウコウシュ",
    "サケ",
    "ショウチュウ",
    "ウイスキー",
    "ブランデー",
    "ジン",
    "ウォッカ",
    "テキーラ",
    "ラム",
    "カクテル",
    "クラフトビール",
    "ノンアルコール",
    "ハーブティー",
    "ジャスミンチャ",
    "ウーロンチャ",
    "プーアルチャ",
    "アールグレイ",
    "ダージリン",
    "ホウジチャ",
    "マッチャ",
    "コーヒー",
    "カフェラテ",
    "カプチーノ",
    "アメリカーノ",
    "フラットホワイト",
    "ドリップコーヒー",
    "インスタントコーヒー",
    "ココア",
    "ホットチョコレート",
    "ミルクセーキ",
    "シェイク",
    "スムージー",
    "フラッペ",
    "フローズンヨーグルト",
    "シャーベット",
    "ソルベ",
    "グラニータ",
    "アフォガート",
    "ジェラート",
    "パフェ",
    "サンデー",
    "ババロア",
    "ムース",
    "パンナコッタ",
    "グレープフルーツ",
    "カシス",
    "ブルーベリー",
    "ラズベリー",
    "ブラックベリー",
    "クランベリー",
    "アサイー",
    "ゴジベリー",
    "マルベリー",
    "ソラマメ",
    "エンドウマメ",
    "スナップエンドウ",
    "ラッカセイ",
    "ピスタチオ",
    "カシューナッツ",
    "マカダミアナッツ",
    "クルミ",
    "ヘーゼルナッツ",
    "ブラジルナッツ",
    "ピーカンナッツ",
    "カカオ",
    "カカオニブ",
    "ホワイトチョコレート",
    "ミルクチョコレート",
    "ダークチョコレート",
    "チョコスプレー",
    "チョコチップ",
    "チョコシロップ",
    "メープルシロップ",
    "アガベシロップ",
    "マヌカハニー",
    "クロミツ",
    "サントウ",
    "キビトウ",
    "テンサイトウ",
    "ジョウハクトウ",
    "グラニュートウ",
    "フントウ",
    "ワリバシ",
    "ツマヨウジ",
    "タケグシ",
    "クシ",
    "センス",
    "ウチワ",
    "ハエタタキ",
    "ゴキブリホイホイ",
    "ムシトリアミ",
    "ムシカゴ",
    "ミズデッポウ",
    "シャボンダマ",
    "ハナビ",
    "センコウハナビ",
    "ウチアゲハナビ",
    "ロケットハナビ",
    "ネズミハナビ",
    "ヒヨケシェード",
    "ワンポールテント",
    "ハンモック",
    "キャンプファイヤー",
    "タキビダイ",
    "バーベキューグリル",
    "チャコール",
    "チャッカザイ",
    "マッチ",
    "ライター",
    "ヒウチイシ",
    "フェザースティック",
    "トザングツ",
    "トザンリュック",
    "ミズトウ",
    "ホオンボトル",
    "クーラーボックス",
    "ホレイザイ",
    "オリタタミイス",
    "オリタタミテーブル",
    "カンイトイレ",
    "ケイタイシャワー",
    "スリーピングバッグ",
    "スリーピングパッド",
    "ポンチョ",
    "レインウェア",
    "ボウスイスプレー",
    "ムシヨケスプレー",
    "ヒヤケドメ",
    "ヘンコウサングラス",
    "ソウガンキョウ",
    "ボウエンキョウ",
    "ケンビキョウ",
    "カクダイキョウ",
    "チキュウギ",
    "ドウロチズ",
    "カーナビ",
    "ホウイジシャク",
    "ジーピーエスキキ",
    "スマートウォッチ",
    "オンドケイ",
    "シツドケイ",
    "キアツケイ",
    "コウドケイ",
    "マンゲキョウ",
    "ルービックキューブ",
    "ジグソーパズル",
    "クロスワード",
    "スウドク",
    "ショウギ",
    "イゴ",
    "チェス",
    "チェッカー",
    "オセロ",
    "トランプ",
    "ウノ",
    "ジンセイゲーム",
    "モノポリー",
    "カルタ",
    "ヒャクニンイッシュ",
    "ハナフダ",
    "マージャンパイ",
    "ドミノ",
    "ジェンガ",
    "ツイスターゲーム",
    "ボードゲーム",
    "アールピージーゲーム",
    "ヤキュウバン",
    "サッカーバン",
    "スヌーカー",
    "ソフトダーツ",
    "ホッケーゲーム",
    "エアホッケー",
    "ピンボール",
    "スロットマシン",
    "ガチャガチャ",
    "クレーンゲーム",
    "プラモデル",
    "ガンプラ",
    "ミニヨンク",
    "ラジコンカー",
    "ラジコンヘリ",
    "ショウガタドローン",
    "デンシャモケイ",
    "テツドウジオラマ",
    "シュノーケル",
    "ダイビングマスク",
    "フィン",
    "ウェットスーツ",
    "ドライスーツ",
    "スイチュウカメラ",
    "アクションカメラ",
    "ヘッドランプ",
    "エルイーディーランタン",
    "キャンドルランタン",
    "テマワシライト",
    "ソーラーライト",
    "カンデンチ",
    "ジュウデンチ",
    "ソーラーパネル",
    "ポータブルデンゲン",
    "ハツデンキ",
    "エンジン",
    "モーター",
    "プロペラ",
    "ジャイロスコープ",
    "センサー",
    "カメラレンズ",
    "ボウエンレンズ",
    "マクロレンズ",
    "コウカクレンズ",
    "ヒョウジュンレンズ",
    "イッキャク",
    "カメラストラップ",
    "レンズフード",
    "レンズキャップ",
    "シーディーカード",
    "シーエフカード",
    "メモリースティック",
    "エスエスディー",
    "ユーエスビーケーブル",
    "ディスプレイポートケーブル",
    "ビージーエーケーブル",
    "ディーブイアイケーブル",
    "ヒカリファイバーケーブル",
    "デンゲンタップ",
    "エンチョウコード",
    "テーブルタップ",
    "コンセント",
    "プラグ",
    "アダプター",
    "ヘンアツキ",
    "ヘンカンプラグ",
    "バッテリーチャージャー",
    "ソーラーチャージャー",
    "ハンドスピナー",
    "ストレスボール",
    "グリップトレーナー",
    "フィジェットキューブ",
    "ローラーシューズ",
    "プロテクションヘルメット",
    "グンテ",
    "サギョウフク",
    "アンゼンクツ",
    "ハンシャベスト",
    "ミリタリーブーツ",
    "メイサイフク",
    "ボウダンチョッキ",
    "ボウダンヘルメット",
    "ボウトウマスク",
    "ガスマスク",
    "スキューバタンク",
    "レギュレーター",
    "ビージージャケット",
    "ミニセンスイテイ",
    "スイチュウスクーター",
    "ギョグンタンチキ",
    "ジキコンパス",
    "サバイバルホイッスル",
    "ファーストエイドキット",
    "バンソウコウ",
    "ガーゼ",
    "ホウタイ",
    "ショウドクエキ",
    "セキガイセンタイオンケイ",
    "ケイタイケツアツケイ",
    "チュウシャキ",
    "チュウシャバリ",
    "カテーテル",
    "テンテキスタンド",
    "チョウシンキ",
    "イリョウヨウマスク",
    "イリョウヨウテブクロ",
    "フェイスシールド",
    "クルマイス",
    "マツバヅエ",
    "タンカ",
    "エーイーディー",
    "ディーブイディー",
    "ブルーレイディスク",
    "ブイエイチエステープ",
    "カセットテープ",
    "エルピーレコード",
    "イーピーレコード",
    "シングルシーディー",
    "エムディー",
    "フロッピーディスク",
    "ジップディスク",
    "スマートメディア",
    "コンパクトフラッシュ",
    "エックスディーピクチャーカード",
    "マイクロエスディーカード",
    "シムカード",
    "アイシーカード",
    "マイナンバーカード",
    "メンキョショウ",
    "パスポート",
    "ザイリュウカード",
    "ホケンショウ",
    "クレジットカード",
    "デビットカード",
    "プリペイドカード",
    "ギフトカード",
    "ショウヒンケン",
    "ビールケン",
    "コメケン",
    "トショカード",
    "クオカード",
    "スイカ",
    "パスモ",
    "イコカ",
    "トイカ",
    "マナカ",
    "ハヤカケン",
    "キタカ",
    "スゴカ",
    "ニモカ",
    "リンカイスイカ",
    "モバイルスイカ",
    "アップルペイ",
    "グーグルペイ",
    "ペイペイ",
    "ラインペイ",
    "ディーバライ",
    "エーユーペイ",
    "ラクテンペイ",
    "メルペイ",
    "ウィーチャットペイ",
    "アリペイ",
]

def start_game(drawer_id: int) -> str:
    topic = random.choice(topics)
    game_id = create_game(drawer_id, topic)
    return game_id

def record_answer(game_id: str, player_id: int, answer: str):
    add_answer(game_id, player_id, answer)

def submit_final_image(game_id: str, url: str):
    set_final_image(game_id, url)

# def analyze_ai_answer(game_id: str):
#     url = get_final_image_url(game_id)
#     ai_guess = analyze_image(url)
#     set_ai_answer(game_id, ai_guess)

import asyncio


async def analyze_ai_answer_async(game_id: str):
    # analyze_ai_answerの中身を、同期的なopenAI API呼び出し部分のみ別関数にしてto_threadで呼ぶ
    return await asyncio.to_thread(analyze_ai_answer_sync, game_id)

def analyze_ai_answer_sync(game_id: str):
    # 現行のanalyze_ai_answer処理を同期的に行う関数として定義
    image_url = get_final_image_url(game_id)
    ai_guess = analyze_image(image_url)  
    set_ai_answer(game_id, ai_guess)

def judge_winner(game_id: str):
    topic = get_topic(game_id)
    ai_ans = get_ai_answer(game_id)
    answers = get_answers(game_id)

    if not answers:
        # 人間回答なし -> AI勝利
        return ("AI", None, topic)

    # 全ての人間回答(answer部分のみ)をリスト化
    human_answers = [a[1] for a in answers]

    # Chat APIで最多回答を抽出（pick_human_final_answer_via_chat関数使用前提）
    chosen = pick_human_final_answer_via_chat(human_answers)
    human_correct = check_answer_via_chat(chosen, topic)
    ai_correct = check_answer_via_chat(ai_ans, topic)

    # 人間勝利条件: 人間正解 & AI不正解
    if human_correct and not ai_correct:
        return ("HUMAN", chosen, topic)
    else:
=======
# game_logic.py

import random
from collections import Counter

from db import (add_answer, create_game, get_ai_answer, get_answers,
                get_final_image_url, get_game_info, get_players, get_state,
                get_topic, set_ai_answer, set_final_image, set_state)
from openai_helper import (analyze_image, check_answer_via_chat,
                           pick_human_final_answer_via_chat)

topics = [
    "イヌ",
    "ネコ",
    "ウサギ",
    "ハムスター",
    "リス",
    "サル",
    "チンパンジー",
    "ゴリラ",
    "コアラ",
    "カンガルー",
    "パンダ",
    "クマ",
    "ライオン",
    "トラ",
    "キリン",
    "ゾウ",
    "サイ",
    "カバ",
    "ウシ",
    "ウマ",
    "ブタ",
    "ヒツジ",
    "ヤギ",
    "シカ",
    "イノシシ",
    "ロバ",
    "ラクダ",
    "オオカミ",
    "キツネ",
    "ビーバー",
    "アザラシ",
    "ラッコ",
    "セイウチ",
    "カモノハシ",
    "ナマケモノ",
    "ミーアキャット",
    "ヤマアラシ",
    "ハリネズミ",
    "アルマジロ",
    "ワシ",
    "フクロウ",
    "ペンギン",
    "ダチョウ",
    "クジャク",
    "ハクチョウ",
    "アヒル",
    "ニワトリ",
    "ツル",
    "フラミンゴ",
    "ペリカン",
    "ハシビロコウ",
    "キウイ",
    "ハゲワシ",
    "キツツキ",
    "ワニ",
    "リクガメ",
    "ウミガメ",
    "トカゲ",
    "ヘビ",
    "カメレオン",
    "カエル",
    "サメ",
    "クジラ",
    "イルカ",
    "タツノオトシゴ",
    "マンボウ",
    "カニ",
    "エビ",
    "タコ",
    "イカ",
    "クラゲ",
    "ヒトデ",
    "キンギョ",
    "チョウ",
    "テントウムシ",
    "カブトムシ",
    "クワガタ",
    "ハチ",
    "アリ",
    "バッタ",
    "カマキリ",
    "トンボ",
    "クモ",
    "サソリ",
    "ユニコーン",
    "ペガサス",
    "ドラゴン",
    "フェニックス",
    "グリフィン",
    "リンゴ",
    "バナナ",
    "イチゴ",
    "パイナップル",
    "ブドウ",
    "スイカ",
    "メロン",
    "オレンジ",
    "レモン",
    "チェリー",
    "モモ",
    "ナシ",
    "キウイフルーツ",
    "マンゴー",
    "パパイヤ",
    "ココナッツ",
    "ニンジン",
    "ダイコン",
    "キュウリ",
    "ナス",
    "トマト",
    "キャベツ",
    "タマネギ",
    "ジャガイモ",
    "サツマイモ",
    "カボチャ",
    "トウモロコシ",
    "ブロッコリー",
    "アスパラガス",
    "マッシュルーム",
    "ハンバーガー",
    "ピザ",
    "ホットドッグ",
    "ドーナツ",
    "アイスクリーム",
    "カップケーキ",
    "パンケーキ",
    "クッキー",
    "オムライス",
    "オニギリ",
    "スシ",
    "タコヤキ",
    "オコノミヤキ",
    "ヤキザカナ",
    "クシカツ",
    "リンゴアメ",
    "ワッフル",
    "フライドポテト",
    "ギョウザ",
    "ハルマキ",
    "ニクマン",
    "チョコレート",
    "プレッツェル",
    "クロワッサン",
    "ショクパン",
    "ベーグル",
    "マカロン",
    "シュークリーム",
    "バゲット",
    "メロンパン",
    "カレーライス",
    "スパゲッティ",
    "ソバ",
    "ラーメン",
    "ピーナッツ",
    "アーモンド",
    "ソフトクリーム",
    "ケーキ",
    "バウムクーヘン",
    "マグカップ",
    "ティーポット",
    "ペットボトル",
    "ワイングラス",
    "コーヒーカップ",
    "ビールジョッキ",
    "クルマ",
    "バス",
    "トラック",
    "バイク",
    "ジテンシャ",
    "ヘリコプター",
    "ヒコウキ",
    "ロケット",
    "センスイカン",
    "フネ",
    "ヨット",
    "ボート",
    "シンカンセン",
    "ジョウキキカンシャ",
    "スクーター",
    "キキュウ",
    "モノレール",
    "トロリーバス",
    "ロメンデンシャ",
    "ショウボウシャ",
    "キュウキュウシャ",
    "パトカー",
    "フォークリフト",
    "ブルドーザー",
    "クレーンシャ",
    "ダンプカー",
    "トラクター",
    "イエ",
    "シロ",
    "ピラミッド",
    "エッフェルタワー",
    "トウキョウタワー",
    "スカイツリー",
    "トウダイ",
    "フウシャ",
    "イグルー",
    "テント",
    "イス",
    "テーブル",
    "ベッド",
    "ソファ",
    "タンス",
    "ホンダナ",
    "スプーン",
    "フォーク",
    "ナイフ",
    "ハシ",
    "フライパン",
    "ナベ",
    "ヤカン",
    "マナイタ",
    "ホウチョウ",
    "サラ",
    "ボウル",
    "コップ",
    "ティーカップ",
    "テーブルクロス",
    "テレビ",
    "レイゾウコ",
    "センタクキ",
    "ソウジキ",
    "デンシレンジ",
    "スイハンキ",
    "トースター",
    "ペン",
    "エンピツ",
    "ケシゴム",
    "ジョウギ",
    "ハサミ",
    "ノリ",
    "ホッチキス",
    "カッター",
    "セロハンテープ",
    "クリップ",
    "シャープペン",
    "マーカー",
    "クレヨン",
    "ボウシ",
    "ヤキュウボウ",
    "ニットボウ",
    "マフラー",
    "テブクロ",
    "クツ",
    "ナガグツ",
    "スリッパ",
    "メガネ",
    "サングラス",
    "ネクタイ",
    "マスク",
    "リュックサック",
    "バッグ",
    "ベルト",
    "カサ",
    "アマガッパ",
    "ハンマー",
    "ドライバー",
    "スパナ",
    "レンチ",
    "ペンチ",
    "ノコギリ",
    "シャベル",
    "スコップ",
    "オノ",
    "クギ",
    "ネジ",
    "ドリル",
    "ハシゴ",
    "ギター",
    "バイオリン",
    "ピアノ",
    "トランペット",
    "サックス",
    "フルート",
    "ドラム",
    "ハープ",
    "クラリネット",
    "ホルン",
    "サッカーボール",
    "バスケットボール",
    "ヤキュウボール",
    "テニスラケット",
    "ヤキュウバット",
    "ゴルフクラブ",
    "ボウリングピン",
    "バレーボール",
    "シャトル",
    "タッキュウラケット",
    "スキーバン",
    "スノーボード",
    "スケートボード",
    "フリスビー",
    "フラフープ",
    "アーチェリー",
    "ボクシンググローブ",
    "タイヨウ",
    "ツキ",
    "ホシ",
    "クモ",
    "ヤマ",
    "キ",
    "マツ",
    "サボテン",
    "ハナ",
    "ハッパ",
    "キノコ",
    "カイガラ",
    "シンゴウキ",
    "デンキュウ",
    "デンチ",
    "スマートフォン",
    "パソコン",
    "カメラ",
    "ウデドケイ",
    "スナドケイ",
    "コンパス",
    "チキュウギ",
    "ハート",
    "スペード",
    "カギ",
    "ナンドウジョウ",
    "オンプ",
    "パズル",
    "メガホン",
    "レコード",
    "カセットテープ",
    "ラジオ",
    "スピーカー",
    "マイク",
    "ギフトボックス",
    "バケツ",
    "ハンドベル",
    "トーチ",
    "ロウソク",
    "ルーペ",
    "ハンカチ",
    "ティッシュ",
    "ゴミバコ",
    "ノート",
    "ホン",
    "フウトウ",
    "マンネンヒツ",
    "メール",
    "カレンダー",
    "トケイ",
    "サイコロ",
    "チェスコマ",
    "チェスバン",
    "ショウギコマ",
    "イゴイシ",
    "トランプ",
    "ウノ",
    "モノポリー",
    "カルタ",
    "ハナフダ",
    "マージャン",
    "ドミノ",
    "ジェンガ",
    "ツイスター",
    "ボードゲーム",
    "ヨーヨー",
    "ケンダマ",
    "コマ",
    "タコ",
    "シャボンダマ",
    "ミズデッポウ",
    "パチンコ",
    "スーパーボール",
    "ジシャク",
    "マンゲキョウ",
    "ルービックキューブ",
    "ビリヤードダイ",
    "ビリヤードキュー",
    "ビリヤードボール",
    "ダーツボード",
    "ダーツ",
    "オセロバン",
    "ショウギバン",
    "イゴバン",
    "アコーディオン",
    "ハーモニカ",
    "リコーダー",
    "シェイカー",
    "アワダテキ",
    "フライガエシ",
    "オタマ",
    "ピーラー",
    "センヌキ",
    "コルクヌキ",
    "ケイリョウカップ",
    "ケイリョウスプーン",
    "トング",
    "チャコシ",
    "サンカクコーナー",
    "スリコギ",
    "スリバチ",
    "ミキサー",
    "ジューサー",
    "エッグスタンド",
    "バターケース",
    "アイスバケット",
    "スプレーボトル",
    "コロコロ",
    "クシ",
    "ヘアブラシ",
    "ドライヤー",
    "カミソリ",
    "デンキシェーバー",
    "ツメキリ",
    "ミミカキ",
    "メンボウ",
    "ケショウポーチ",
    "リップスティック",
    "マニキュア",
    "コウスイ",
    "ハンドクリーム",
    "フットボール",
    "アメフトヘルメット",
    "ヤキュウグローブ",
    "ヤキュウベース",
    "キャッチャーマスク",
    "ホッケースティック",
    "ホッケーパック",
    "ラクロススティック",
    "ツリザオ",
    "ツリバリ",
    "スイエイゴーグル",
    "スイエイキャップ",
    "シュノーケル",
    "フィン",
    "ダイビングボンベ",
    "スケートヘルメット",
    "ニーパッド",
    "エルボーパッド",
    "トザンブーツ",
    "トザンリュック",
    "トレッキングポール",
    "ジーピーエス",
    "チズ",
    "スリーピングバッグ",
    "カラビナ",
    "テントウチ",
    "ロープ",
    "ザブトン",
    "クッション",
    "ザッキン",
    "カーペット",
    "ジュウタン",
    "カーテン",
    "ブラインド",
    "ショウメンキョウ",
    "カガミ",
    "カイガ",
    "ポスター",
    "シャシンタテ",
    "ビールビン",
    "ワインビン",
    "シャンパンボトル",
    "コップザラ",
    "メンキョショウ",
    "パスポート",
    "ホケンショウ",
    "クレジットカード",
    "デビットカード",
    "プリペイドカード",
    "ギフトカード",
    "ショウヒンケン",
    "ビールケン",
    "コメケン",
    "トショカード",
    "クオカード",
    "スイカ",
    "パスモ",
    "イコカ",
    "トイカ",
    "マナカ",
    "ハヤカケン",
    "キタカ",
    "スゴカ",
    "ニモカ",
    "リンカイスイカ",
    "モバイルスイカ",
    "アップルペイ",
    "グーグルペイ",
    "ペイペイ",
    "ラインペイ",
    "ディーバライ",
    "エーユーペイ",
    "ラクテンペイ",
    "メルペイ",
    "ウィーチャットペイ",
    "アリペイ",
    "カラフルペン",
    "キーホルダー",
    "シュリンケンサック",
    "モップ",
    "ホウキ",
    "チリトリ",
    "ゴムテブクロ",
    "センメンキ",
    "シャワーヘッド",
    "バスタブ",
    "ハブラシ",
    "ハミガキコ",
    "セッケン",
    "タオル",
    "アイロン",
    "アイロンダイ",
    "ミシン",
    "ハンガー",
    "イトマキ",
    "ハリ",
    "ボタン",
    "ファスナー",
    "アンゼンピン",
    "メジャー",
    "カセツトウ",
    "ハンガキ",
    "ハサミカッター",
    "ウケザラ",
    "サラダボウル",
    "スプラッシュガード",
    "ランチョンマット",
    "ドアノブ",
    "ドア",
    "マド",
    "カギアナ",
    "デンチュウ",
    "デンセン",
    "ガイトウ",
    "フンスイ",
    "ベンチ",
    "チョウコク",
    "オフィスビル",
    "コウジョウ",
    "ソウコ",
    "シヨウカイドウ",
    "ヨウチエン",
    "ホイクエン",
    "ショウガッコウ",
    "チュウガッコウ",
    "コウコウ",
    "ダイガク",
    "トショカン",
    "ビジュツカン",
    "ハクブツカン",
    "スイゾクカン",
    "ドウブツエン",
    "ショクブツエン",
    "ユウエンチ",
    "スキージョウ",
    "ビーチ",
    "コウエン",
    "テイエン",
    "スタジアム",
    "ヤキュウジョウ",
    "サッカージョウ",
    "ケイバジョウ",
    "タイイクカン",
    "プール",
    "オンセン",
    "セントウ",
    "コンビニ",
    "スーパー",
    "デパート",
    "モール",
    "イチバ",
    "エキ",
    "バステイ",
    "クウコウ",
    "ミナト",
    "チュウシャジョウ",
    "トイレ",
    "ハシ",
    "ドウロ",
    "オウダンホドウ",
    "シンゴウ",
    "デンシンバシラ",
    "デンセン",
    "ガイトウ",
    "フンスイ",
    "ベンチ",
    "ホウムセンター",
    "ディーアイワイ",
    "スポーツヨウヒンテン",
    "アウトドアショップ",
    "ジテンシャヤ",
    "バイクショップ",
    "カーヨウヒンテン",
    "ガソリンスタンド",
    "センシャジョウ",
    "シュウリコウジョウ",
    "カーディーラー",
    "レンタカー",
    "フドウサンヤ",
    "ホケンヤ",
    "ユウビンキョク",
    "タクハイビンセンター",
    "ハイソウセンター",
    "ブツリュウソウコ",
    "インターネットカフェ",
    "マンガキッサ",
    "ゲームセンター",
    "パチンコテン",
    "スロットテン",
    "マージャンソウ",
    "ボウリングジョウ",
    "ビリヤードジョウ",
    "ダーツバー",
    "ゴルフジョウ",
    "ゴルフレンシュウジョウ",
    "テニスコート",
    "バスケットコート",
    "バレーボールコート",
    "バドミントンコート",
    "タッキュウダイ",
    "ボクシングリング",
    "レスリングマット",
    "ジュウドウタタミ",
    "ケンドウジョウ",
    "キュウドウジョウ",
    "ジム",
    "サウナ",
    "ステージ",
    "ブタイ",
    "エイガカン",
    "プラネタリウム",
    "カガクカン",
    "ギャラリー",
    "イルカショー",
    "コウバン",
    "ショウボウシュッチョウショ",
    "クリニック",
    "デンタルクリニック",
    "ヤッキョク",
    "ドラッグストア",
    "ブンボウグテン",
    "ホンヤ",
    "コフルホンヤ",
    "レコードショップ",
    "シーディーショップ",
    "ガッキテン",
    "ハナヤ",
    "ヤオヤ",
    "サカナヤ",
    "ニクヤ",
    "ケーキヤ",
    "ヨウガシテン",
    "ワガシテン",
    "デンキヤ",
    "カグヤ",
    "ジリツシホン",
    "スーツケース",
    "トランク",
    "ハイヤー",
    "バラ",
    "チューリップ",
    "ヒマワリ",
    "サクラ",
    "ウメ",
    "モミジ",
    "イチョウ",
    "シロツメクサ",
    "コスモス",
    "キク",
    "ボタン",
    "シャクヤク",
    "ガーベラ",
    "ラベンダー",
    "ローズマリー",
    "ミント",
    "バジル",
    "パセリ",
    "セロリ",
    "ネギ",
    "ニラ",
    "シソ",
    "オオバ",
    "タケノコ",
    "サンサイ",
    "シイタケ",
    "マツタケ",
    "シメジ",
    "エリンギ",
    "エノキ",
    "ポルチーニ",
    "トリュフ",
    "キャビア",
    "オマールエビ",
    "ズワイガニ",
    "タラバガニ",
    "カニカマ",
    "カニクリームコロッケ",
    "エビフライ",
    "カツドン",
    "テンドン",
    "オヤコドン",
    "ギュウドン",
    "タコス",
    "ブリトー",
    "ナチョス",
    "パエリア",
    "ガスパチョ",
    "クスクス",
    "ピロシキ",
    "ボルシチ",
    "ラザニア",
    "リゾット",
    "フィッシュアンドチップス",
    "ローストビーフ",
    "ローストチキン",
    "ブルスケッタ",
    "ティラミス",
    "エクレア",
    "シュークリーム",
    "ミルフィーユ",
    "クレープ",
    "マドレーヌ",
    "フィナンシェ",
    "カステラ",
    "ヨウカン",
    "マンジュウ",
    "モナカ",
    "ドラヤキ",
    "ワラビモチ",
    "オオバヤキ",
    "イマガワヤキ",
    "ニンギョウヤキ",
    "カルメヤキ",
    "カキゴオリ",
    "アンズアメ",
    "ワタガシ",
    "チョコバナナ",
    "リンゴアメ",
    "ポップコーン",
    "ヤキトウモロコシ",
    "フランクフルト",
    "ヤキソバ",
    "オデン",
    "ウメボシ",
    "タラコ",
    "メンタイコ",
    "チクワ",
    "カマボコ",
    "ハンペン",
    "オデンダネ",
    "ゴボウ",
    "レンコン",
    "ショウガ",
    "ニンニク",
    "ゴマ",
    "ダイズ",
    "コアズキ",
    "オカラ",
    "ドウフ",
    "ユバ",
    "ツミレ",
    "コンブ",
    "ワカメ",
    "ノリ",
    "ヒジキ",
    "タケヤブ",
    "カワラ",
    "イチョウバ",
    "マツバ",
    "シダ",
    "ハス",
    "スイレン",
    "アサガオ",
    "ヒルガオ",
    "ユリ",
    "バラエン",
    "ムギバタケ",
    "イネバタケ",
    "コメ",
    "コムギ",
    "ライムギ",
    "ソバ",
    "テンサイドウ",
    "アーモンドミルク",
    "ココナッツミルク",
    "ソイチーズ",
    "ビーガン",
    "カプレーゼ",
    "ニースサラダ",
    "スープカレー",
    "ワンタンスープ",
    "ミネストローネ",
    "ポタージュ",
    "クラムチャウダー",
    "オニオンスープ",
    "コンソメスープ",
    "トンジル",
    "スマシジル",
    "カニジル",
    "ハマグリジル",
    "シジミジル",
    "オジヤ",
    "ビリアニ",
    "プルコギ",
    "キムチ",
    "ビビンバ",
    "チヂミ",
    "サムゲタン",
    "カルビ",
    "ホルモン",
    "ジンギスカン",
    "ジャージャーメン",
    "レイメン",
    "クッパ",
    "トッポギ",
    "マッコリ",
    "ショウコウシュ",
    "サケ",
    "ショウチュウ",
    "ウイスキー",
    "ブランデー",
    "ジン",
    "ウォッカ",
    "テキーラ",
    "ラム",
    "カクテル",
    "クラフトビール",
    "ノンアルコール",
    "ハーブティー",
    "ジャスミンチャ",
    "ウーロンチャ",
    "プーアルチャ",
    "アールグレイ",
    "ダージリン",
    "ホウジチャ",
    "マッチャ",
    "コーヒー",
    "カフェラテ",
    "カプチーノ",
    "アメリカーノ",
    "フラットホワイト",
    "ドリップコーヒー",
    "インスタントコーヒー",
    "ココア",
    "ホットチョコレート",
    "ミルクセーキ",
    "シェイク",
    "スムージー",
    "フラッペ",
    "フローズンヨーグルト",
    "シャーベット",
    "ソルベ",
    "グラニータ",
    "アフォガート",
    "ジェラート",
    "パフェ",
    "サンデー",
    "ババロア",
    "ムース",
    "パンナコッタ",
    "グレープフルーツ",
    "カシス",
    "ブルーベリー",
    "ラズベリー",
    "ブラックベリー",
    "クランベリー",
    "アサイー",
    "ゴジベリー",
    "マルベリー",
    "ソラマメ",
    "エンドウマメ",
    "スナップエンドウ",
    "ラッカセイ",
    "ピスタチオ",
    "カシューナッツ",
    "マカダミアナッツ",
    "クルミ",
    "ヘーゼルナッツ",
    "ブラジルナッツ",
    "ピーカンナッツ",
    "カカオ",
    "カカオニブ",
    "ホワイトチョコレート",
    "ミルクチョコレート",
    "ダークチョコレート",
    "チョコスプレー",
    "チョコチップ",
    "チョコシロップ",
    "メープルシロップ",
    "アガベシロップ",
    "マヌカハニー",
    "クロミツ",
    "サントウ",
    "キビトウ",
    "テンサイトウ",
    "ジョウハクトウ",
    "グラニュートウ",
    "フントウ",
    "ワリバシ",
    "ツマヨウジ",
    "タケグシ",
    "クシ",
    "センス",
    "ウチワ",
    "ハエタタキ",
    "ゴキブリホイホイ",
    "ムシトリアミ",
    "ムシカゴ",
    "ミズデッポウ",
    "シャボンダマ",
    "ハナビ",
    "センコウハナビ",
    "ウチアゲハナビ",
    "ロケットハナビ",
    "ネズミハナビ",
    "ヒヨケシェード",
    "ワンポールテント",
    "ハンモック",
    "キャンプファイヤー",
    "タキビダイ",
    "バーベキューグリル",
    "チャコール",
    "チャッカザイ",
    "マッチ",
    "ライター",
    "ヒウチイシ",
    "フェザースティック",
    "トザングツ",
    "トザンリュック",
    "ミズトウ",
    "ホオンボトル",
    "クーラーボックス",
    "ホレイザイ",
    "オリタタミイス",
    "オリタタミテーブル",
    "カンイトイレ",
    "ケイタイシャワー",
    "スリーピングバッグ",
    "スリーピングパッド",
    "ポンチョ",
    "レインウェア",
    "ボウスイスプレー",
    "ムシヨケスプレー",
    "ヒヤケドメ",
    "ヘンコウサングラス",
    "ソウガンキョウ",
    "ボウエンキョウ",
    "ケンビキョウ",
    "カクダイキョウ",
    "チキュウギ",
    "ドウロチズ",
    "カーナビ",
    "ホウイジシャク",
    "ジーピーエスキキ",
    "スマートウォッチ",
    "オンドケイ",
    "シツドケイ",
    "キアツケイ",
    "コウドケイ",
    "マンゲキョウ",
    "ルービックキューブ",
    "ジグソーパズル",
    "クロスワード",
    "スウドク",
    "ショウギ",
    "イゴ",
    "チェス",
    "チェッカー",
    "オセロ",
    "トランプ",
    "ウノ",
    "ジンセイゲーム",
    "モノポリー",
    "カルタ",
    "ヒャクニンイッシュ",
    "ハナフダ",
    "マージャンパイ",
    "ドミノ",
    "ジェンガ",
    "ツイスターゲーム",
    "ボードゲーム",
    "アールピージーゲーム",
    "ヤキュウバン",
    "サッカーバン",
    "スヌーカー",
    "ソフトダーツ",
    "ホッケーゲーム",
    "エアホッケー",
    "ピンボール",
    "スロットマシン",
    "ガチャガチャ",
    "クレーンゲーム",
    "プラモデル",
    "ガンプラ",
    "ミニヨンク",
    "ラジコンカー",
    "ラジコンヘリ",
    "ショウガタドローン",
    "デンシャモケイ",
    "テツドウジオラマ",
    "シュノーケル",
    "ダイビングマスク",
    "フィン",
    "ウェットスーツ",
    "ドライスーツ",
    "スイチュウカメラ",
    "アクションカメラ",
    "ヘッドランプ",
    "エルイーディーランタン",
    "キャンドルランタン",
    "テマワシライト",
    "ソーラーライト",
    "カンデンチ",
    "ジュウデンチ",
    "ソーラーパネル",
    "ポータブルデンゲン",
    "ハツデンキ",
    "エンジン",
    "モーター",
    "プロペラ",
    "ジャイロスコープ",
    "センサー",
    "カメラレンズ",
    "ボウエンレンズ",
    "マクロレンズ",
    "コウカクレンズ",
    "ヒョウジュンレンズ",
    "イッキャク",
    "カメラストラップ",
    "レンズフード",
    "レンズキャップ",
    "シーディーカード",
    "シーエフカード",
    "メモリースティック",
    "エスエスディー",
    "ユーエスビーケーブル",
    "ディスプレイポートケーブル",
    "ビージーエーケーブル",
    "ディーブイアイケーブル",
    "ヒカリファイバーケーブル",
    "デンゲンタップ",
    "エンチョウコード",
    "テーブルタップ",
    "コンセント",
    "プラグ",
    "アダプター",
    "ヘンアツキ",
    "ヘンカンプラグ",
    "バッテリーチャージャー",
    "ソーラーチャージャー",
    "ハンドスピナー",
    "ストレスボール",
    "グリップトレーナー",
    "フィジェットキューブ",
    "ローラーシューズ",
    "プロテクションヘルメット",
    "グンテ",
    "サギョウフク",
    "アンゼンクツ",
    "ハンシャベスト",
    "ミリタリーブーツ",
    "メイサイフク",
    "ボウダンチョッキ",
    "ボウダンヘルメット",
    "ボウトウマスク",
    "ガスマスク",
    "スキューバタンク",
    "レギュレーター",
    "ビージージャケット",
    "ミニセンスイテイ",
    "スイチュウスクーター",
    "ギョグンタンチキ",
    "ジキコンパス",
    "サバイバルホイッスル",
    "ファーストエイドキット",
    "バンソウコウ",
    "ガーゼ",
    "ホウタイ",
    "ショウドクエキ",
    "セキガイセンタイオンケイ",
    "ケイタイケツアツケイ",
    "チュウシャキ",
    "チュウシャバリ",
    "カテーテル",
    "テンテキスタンド",
    "チョウシンキ",
    "イリョウヨウマスク",
    "イリョウヨウテブクロ",
    "フェイスシールド",
    "クルマイス",
    "マツバヅエ",
    "タンカ",
    "エーイーディー",
    "ディーブイディー",
    "ブルーレイディスク",
    "ブイエイチエステープ",
    "カセットテープ",
    "エルピーレコード",
    "イーピーレコード",
    "シングルシーディー",
    "エムディー",
    "フロッピーディスク",
    "ジップディスク",
    "スマートメディア",
    "コンパクトフラッシュ",
    "エックスディーピクチャーカード",
    "マイクロエスディーカード",
    "シムカード",
    "アイシーカード",
    "マイナンバーカード",
    "メンキョショウ",
    "パスポート",
    "ザイリュウカード",
    "ホケンショウ",
    "クレジットカード",
    "デビットカード",
    "プリペイドカード",
    "ギフトカード",
    "ショウヒンケン",
    "ビールケン",
    "コメケン",
    "トショカード",
    "クオカード",
    "スイカ",
    "パスモ",
    "イコカ",
    "トイカ",
    "マナカ",
    "ハヤカケン",
    "キタカ",
    "スゴカ",
    "ニモカ",
    "リンカイスイカ",
    "モバイルスイカ",
    "アップルペイ",
    "グーグルペイ",
    "ペイペイ",
    "ラインペイ",
    "ディーバライ",
    "エーユーペイ",
    "ラクテンペイ",
    "メルペイ",
    "ウィーチャットペイ",
    "アリペイ",
]

def start_game(drawer_id: int) -> str:
    # topic = random.choice(topics)
    topic = "りんご"
    game_id = create_game(drawer_id, topic)
    return game_id

def record_answer(game_id: str, player_id: int, answer: str):
    add_answer(game_id, player_id, answer)

def submit_final_image(game_id: str, url: str):
    set_final_image(game_id, url)

# def analyze_ai_answer(game_id: str):
#     url = get_final_image_url(game_id)
#     ai_guess = analyze_image(url)
#     set_ai_answer(game_id, ai_guess)

import asyncio


async def analyze_ai_answer_async(game_id: str):
    # analyze_ai_answerの中身を、同期的なopenAI API呼び出し部分のみ別関数にしてto_threadで呼ぶ
    return await asyncio.to_thread(analyze_ai_answer_sync, game_id)

def analyze_ai_answer_sync(game_id: str):
    # 現行のanalyze_ai_answer処理を同期的に行う関数として定義
    image_url = get_final_image_url(game_id)
    ai_guess = analyze_image(image_url)  
    set_ai_answer(game_id, ai_guess)

def judge_winner(game_id: str):
    topic = get_topic(game_id)
    ai_ans = get_ai_answer(game_id)
    answers = get_answers(game_id)

    if not answers:
        # 人間回答なし -> AI勝利
        return ("AI", None, topic)

    # 全ての人間回答(answer部分のみ)をリスト化
    human_answers = [a[1] for a in answers]

    # Chat APIで最多回答を抽出（pick_human_final_answer_via_chat関数使用前提）
    chosen = pick_human_final_answer_via_chat(human_answers)
    human_correct = check_answer_via_chat(chosen, topic)
    ai_correct = check_answer_via_chat(ai_ans, topic)

    # 人間勝利条件: 人間正解 & AI不正解
    if human_correct and not ai_correct:
        return ("HUMAN", chosen, topic)
    else:
>>>>>>> 6354baca9e6354cef8bfe39c1cd4f89f09594308
        return ("AI", chosen, topic)