# Backup_SlackToNotionについて
Slackのチャンネル投稿をNotionのDBに格納するPythonスクリプト

現状、一つのチャンネルしかNotionに送信できない
今後、全てのチャンネルの投稿を取得してNotionに送れるようにする ← NotionのDBを用意してコネクトしないとAPIで触れないから無理かも...？ ← 親ページからCreate DBでいけるかも？


~~現在はメッセージしか送れません、画像や動画は今後追加する~~
チャンネルに投稿された画像・動画、ファイルを確認可能なリンクとしてNotionに送信する機能を追加

## Install
ターミナルで以下のライブラリをインストールする

pip install slack-sdk

pip install requests

pip install datetime

## Setting
Slack、Notionのトークンを取得する必要あり

Notionのコネクトに接続する必要あり
