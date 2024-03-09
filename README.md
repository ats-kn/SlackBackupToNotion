# Backup_SlackToNotionについて
Slackのチャンネル投稿をNotionのDBに格納するPythonスクリプト

現状、一つのチャンネルしかNotionに送信できない
今後、全てのチャンネルの投稿を取得してNotionに送れるようにする

※現在はメッセージしか送れません、画像や動画は今後追加する

## install
ターミナルで以下のライブラリをインストールする

pip install slack-sdk

pip install requests

pip install datetime
