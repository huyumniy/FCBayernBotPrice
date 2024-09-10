from flask import Flask, request, Response 
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

app = Flask(__name__)
# Set up Slack API client
slack_token = "xoxb-773919780944-7687532530339-uiHc3Wps8ei6PmS8EirmtN3E"
slack_signing_secret = '89686c150358a5bd66fdd4030011b884'
client = WebClient(token=slack_token)


@app.route('/book', methods=['POST'])
def receive_message():
    send_to_group_channel(request.json['message'])

@app.route('/cookie', methods=['POST'])
def send_cookie():
    data, cookie, user_agent, proxy = request.json['data'], request.json['cookie'], request.json['ua'], request.json['proxy']

    send_cookie_to_group_channel(data, cookie, user_agent, proxy)
    


def send_to_group_channel(data):
    client.chat_postMessage(
        channel="#fcbayern-tickets-bot",
        text=f"{data}",
        parse="mrkdwn"
    )

def send_cookie_to_group_channel(data, cookies, ua, proxy):
    cookie_file = client.files_upload_v2(
            title="Cookies",
            filename="cookies.txt",
            content=str(cookies),
        )
    cookie_url = cookie_file.get("file").get("permalink")
    user_file = client.files_upload_v2(
        title="User-Agent",
        filename="userAgent.txt",
        content=str(ua),
    )
    user_url = user_file.get("file").get("permalink")
    
    client.chat_postMessage(
        channel="#fcbayern-tickets-bot",
        text=f"{data}\n*Proxy:* {proxy}\n*User-Agent:* {user_url}\n*Cookie:* {cookie_url}",
        parse="mrkdwn"
    )

if __name__ == '__main__':
    app.run(debug=True, port=40)
