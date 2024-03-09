# Backup_SlackToNotionについて
Slackのチャンネル投稿をNotionのDBに格納するPythonスクリプト

現状、一つのチャンネルしかNotionに送信できない
今後、全てのチャンネルの投稿を取得してNotionに送れるようにする

~~現在はメッセージしか送れません、画像や動画は今後追加する~~
チャンネルに投稿された画像・動画、ファイルを確認可能なリンクとしてNotionに送信する機能を追加

## install
ターミナルで以下のライブラリをインストールする

pip install slack-sdk

pip install requests

pip install datetime
