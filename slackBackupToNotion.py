import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
import json
from datetime import datetime, timezone

# SlackのAPIトークンとチャンネルID
SLACK_API_TOKEN = "xoxb-6724847132404-6774207657345-TfiNiey12O9Ssn1yZjF2fcne"
SLACK_CHANNEL_ID = "C06NAMNUDSR"

# NotionのIntegrationトークンとデータベースID
NOTION_API_TOKEN = "secret_lkjHU975pUPbbnk1wrJrk2J1uiPGel2nK0oSDNyCkTJ"
NOTION_DATABASE_ID = "b963d1ba0ef6409bb4bd53c4f5d6c61f"

# Slackクライアントの初期化
slack_client = WebClient(token=SLACK_API_TOKEN)

# Slackからメッセージを取得する関数
def get_slack_messages():
    try:
        result = slack_client.conversations_history(channel=SLACK_CHANNEL_ID)
        messages = result["messages"]
        # メッセージのテキスト、投稿日時、投稿者の情報を含む辞書のリストを作成
        texts = [item['text'] for item in messages]
        timestamps = [item['ts'] for item in messages]
        users = [item['user'] for item in messages]
        return texts, timestamps, users
    except SlackApiError as e:
        print(f"Error fetching Slack messages: {e.response['error']}")

    

# UNIXタイムスタンプをISO 8601形式に変換する関数
def convert_to_iso8601(timestamp):
    # UNIXタイムスタンプをdatetimeオブジェクトに変換
    dt_object = datetime.utcfromtimestamp(float(timestamp))
    # UTC時刻を表すために'Z'を付ける
    return dt_object.isoformat() + 'Z'

# NotionAPIにリクエストする用のheaderを設定
headers = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Notionに新しいページを作成する関数
def create_notion_page(texts, timestamps, users):
    url = f"https://api.notion.com/v1/pages"
    for text, timestamp, user in zip(texts, timestamps, users):
        # UNIXタイムスタンプをISO 8601形式に変換
        dt_object = datetime.fromtimestamp(float(timestamp), timezone.utc)
        data = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties": {
                "Message": {"title": [{"text": {"content": text}}]},
                "Date": {"date": {"start": dt_object.isoformat()}},
                "User": {"rich_text": [{"text": {"content": user}}]}
            }
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code != 200:
            print(f"Error creating Notion page: {response.content}")

# メインの処理
def main():
    texts, timestamps, users = get_slack_messages()
    create_notion_page(texts, timestamps, users)

# スクリプトの実行
if __name__ == "__main__":
    main()