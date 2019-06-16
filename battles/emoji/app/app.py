from flask import Flask, render_template, request
import db, os, json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/translate', methods=['POST'])
def translate():
    data = json.loads(request.data.decode())
    if data['type'] == 'toText':
        result = data['emoji']
        for rec in db.get_translations('emoji'):
            result = result.replace(rec['emoji'], rec['text'].lower() + ' ')
        result = result.replace('  ', '')
    elif data['type'] == 'toEmoji':
        result = data['text'].lower()
        for rec in db.get_translations('text'):
            if rec['text'].lower() in result:
                result = result.replace(rec['text'].lower(), rec['emoji'])
        result = result.replace(' ', '')
    return result


@app.route('/new', methods=['POST'])
def new():
    data = json.loads(request.data.decode())
    if len(data['emoji']) > 0 and len(data['text']) > 0:
        db.add_new(data['emoji'], data['text'])
    return '0'


if __name__ == '__main__':
    app.run('0.0.0.0', port=32307)

