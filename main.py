import openai
import requests
from flask import Flask, request, render_template, redirect

server = Flask(__name__)

openai.api_key = 'openai API keys'

def get_completion(question):
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"{question}\n",
            temperature=0.9,
            max_tokens=2048,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=None
        )
    except Exception as e:
        print(e)
        return e
    return response["choices"][0].text

def get_completion01(question01):
    try:
        response = openai.Image.create(
            model="image-alpha-001",
            prompt=f"{question01}\n",
            size="512x512")
    except Exception as e:

        print(e)
        return e
    
    return response["data"][0].url
@server.route('/', methods=['GET', 'POST'])
def get_request_json():
    if request.method == 'POST':
        question = request.form['question']
        question01 = request.form['question01']
        res = get_completion(question)
        res01 = get_completion01(question01)
        print("Q:\n", question)
        print("A:\n", res)

        page_id = 'fb id'          
        facebook_access_token = 'fb access_token'        
        if res !="" and res01 !="":
            post_url = 'https://graph.facebook.com/{}/photos'.format(page_id)
            payload = {
                'message': res,
                'access_token': facebook_access_token,
                'url':res01
                }
            r = requests.post(post_url, data=payload)            
            
        return render_template('chat.html', question=question, res=str(res),res01=str(res01),message="已上傳FB貼文")
        
    return render_template('chat.html', question=0)

if __name__ == '__main__':
    server.run(debug=True, host='0.0.0.0', port=3000)
