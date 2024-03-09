import os
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import requests
import json
from datetime import datetime, timezone
from api_key import NOTION_API_TOKEN, NOTION_DATABASE_ID, SLACK_API_TOKEN, SLACK_CHANNEL_ID


# Slackクライアントの初期化
slack_client = WebClient(token=SLACK_API_TOKEN)

# Slackからメッセージを取得する関数
def get_slack_messages():
    try:
        result = slack_client.conversations_history(channel=SLACK_CHANNEL_ID)
        messages = result["messages"]
        # 'client_msg_id'がNoneじゃないときメッセージのテキスト、投稿日時、投稿者の情報、IDを含む辞書のリストを作成
        texts = [message["text"] for message in messages if message.get("client_msg_id") is not None]
        timestamps = [message["ts"] for message in messages if message.get("client_msg_id") is not None]
        users = [message["user"] for message in messages if message.get("client_msg_id") is not None]
        ids = [message["client_msg_id"] for message in messages if message.get("client_msg_id") is not None]
        urls = [message.get("files")[0]["url_private"] if message.get("files") else None for message in messages if message.get("client_msg_id") is not None]
        return texts, timestamps, users, ids, urls
    except SlackApiError as e:
        print(f"Error fetching Slack messages: {e.response['error']}")

# タイムスタンプをISO 8601形式の日付文字列に変換する関数
def convert_to_iso8601(timestamp):
    date_time = datetime.fromtimestamp(float(timestamp), timezone.utc)  # UTCに変換
    iso_date_time = date_time.isoformat(timespec='seconds')  # マイクロ秒を除外
    return iso_date_time

# NotionAPIにリクエストする用のheaderを設定
headers = {
    "Authorization": f"Bearer {NOTION_API_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def get_all_pages():
    url = f"https://api.notion.com/v1/databases/{NOTION_DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    if response.status_code != 200:
        print(f"Error getting Notion pages: {response.content}")
        return []
    return response.json().get('results', [])

# Slackからユーザー情報を取得する関数
def get_user_info(user_id):
    try:
        response = slack_client.users_info(user=user_id)
        if response['ok']:
            return response['user']['real_name']  # 'name' or 'real_name' could be used
        else:
            print(f"Failed to fetch user info: {response['error']}")
    except SlackApiError as e:
        print(f"Error fetching user info: {e.response['error']}")

def create_notion_page(texts, timestamps, users, ids, urls):
    url = f"https://api.notion.com/v1/pages"
    all_pages = get_all_pages()

    for text, timestamp, user, id, url_list in zip(texts, timestamps, users, ids, urls):
        # 既存のページに同じMessage_IDがある場合はNotionにページを作成しない
        if any(page['properties']['Message_ID']['title'][0]['text']['content'] == id for page in all_pages):
            print(f"Page with Message_ID {id} already exists in Notion")
        else:
            iso_timestamp = convert_to_iso8601(timestamp)
            data = {
                "parent": {"database_id": NOTION_DATABASE_ID},
                "properties": {
                    "Message": {"rich_text": [{"text": {"content": text}}]},
                    "Date": {"date": {"start": iso_timestamp}},
                    "User": {"rich_text": [{"text": {"content": user}}]},                    
                    "Message_ID": {"title": [{"text": {"content": id}}]},
                    # urlの中身が""じゃない場合のみURLをNotionに追加"
                    "URL": {"url": url_list or None}
                }
            }
            response = requests.post(url, headers=headers, data=json.dumps(data))
            if response.status_code != 200:
                print(f"Error creating Notion page: {response.content}")

# メインの処理
def main():
    texts, timestamps, user_ids, ids, urls = get_slack_messages()
    users = [get_user_info(user_id) for user_id in user_ids] # ユーザー情報からユーザー名を取得
    create_notion_page(texts, timestamps, users, ids, urls)

# スクリプトの実行
if __name__ == "__main__":
    main()