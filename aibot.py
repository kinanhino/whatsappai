import openai
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def get_chatgpt_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    print(response)
    return response.choices[0].message['content']

def generate_dalle_image(prompt):
    response = openai.Image.create(
        prompt=prompt,
        n=1,
        size="1024x1024"
    )
    return response['data'][0]['url']

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_message = request.values.get("Body", "").lower()
    gpt_response = get_chatgpt_response(incoming_message)

    res = MessagingResponse()
    if "create art" in incoming_message:
        image_url = generate_dalle_image(gpt_response)
        res.message(gpt_response).media(image_url)
    else:
        res.message(gpt_response)

    return str(res)

if __name__ == "__main__":
    app.run(debug=True)