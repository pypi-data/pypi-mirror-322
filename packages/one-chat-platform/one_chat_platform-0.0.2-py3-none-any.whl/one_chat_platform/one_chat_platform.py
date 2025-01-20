# import requests
# import json
# import urllib3
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# class OneMoniBot:
#     def __init__(self, token: str):
#         self.url = "https://one-platform.one.th/chat/api/v1/chatbot-api/message"
#         self.headers = {
#             'Authorization': f"Bearer {token}",
#             'Content-Type': 'application/json'
#         }

#     def send_message(self, message: str, to: str):
#         """ส่งข้อความไปยัง OneMoni"""
#         payload = {
#             "to": to,
#             "type": "text",
#             "message": message
#         }
#         requests.post(self.url, headers=self.headers, data=json.dumps(payload), verify=False)

# one_chat_platform/one_chat.py

from .message_sender import MessageSender


class OneChatPlatform:
    def __init__(self, authorization_token: str):
        self.message_sender = MessageSender(authorization_token)

    def send_message(
        self, to: str, bot_id: str, message: str, custom_notification: str = None
    ):
        return self.message_sender.send_message(
            to, bot_id, message, custom_notification
        )