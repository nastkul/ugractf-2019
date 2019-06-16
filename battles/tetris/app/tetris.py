#!/usr/bin/env python3

import traceback
import random
import time
import copy

from flask import Flask, request, Response, redirect, render_template, make_response, url_for, jsonify

app = Flask(__name__)

games = {}

shapes = [[[[1, 1, 1, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
           [[1, 0, 0, 0],
            [1, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0]],
           [[0, 1, 0, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
           [[0, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0]]],

          [[[1, 1, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0]],
           [[1, 0, 0, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
           [[0, 1, 0, 0],
            [0, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 0, 0]],
           [[1, 1, 1, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]],

          [[[1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0]],
           [[0, 0, 1, 0],
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
           [[1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 0, 0]],
           [[1, 1, 1, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]],

          [[[1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0]],
           [[0, 1, 1, 0],
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
           [[1, 0, 0, 0],
            [1, 1, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 0, 0]],
           [[0, 1, 1, 0],
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]],

          [[[1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
           [[0, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0]],
           [[1, 1, 0, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
           [[0, 1, 0, 0],
            [1, 1, 0, 0],
            [1, 0, 0, 0],
            [0, 0, 0, 0]]],

          [[[1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
           [[1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0]],
           [[1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
           [[1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0],
            [1, 0, 0, 0]]],

          [[[1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
           [[1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
           [[1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]],
           [[1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]]]


@app.route('/')
def index():
    if not request.cookies.get('session') or request.cookies.get('session') not in games:
        resp = make_response(redirect(url_for('index')))
        val = str(random.randint(0, 10000000000000))
        resp.set_cookie('session', value=val)
        games[val] = {"score": 0, "board": [[0 for j in range(10)] for i in range(20)],
                      "shape": random.randint(0, 6), "sx": 4, "sy": 0, "sr": random.randint(0, 3)}
        return resp
    return """
            <style>
                tt { white-space: nowrap }
                #tetris { margin: 0 auto; border-collapse: collapse }
                #tetris td { width: 25px; height: 25px; border: 1px solid black; }
                #tetris td.a { background: red; }
                #tetris td.f { background: black; }
                body { font-size: 18pt; }
            </style>
            <table id=tetris>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
                <tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td><td></td></tr>
            </table>
            <h1>Очки: 0, флаг: пока не заработан</h1>
            <p>Для флага надо 220 очков;<br>за одну линию 10 очков, за две — 30, за три — 80, за четыре — 150</p>
            <p>Управление по API GET-запросами: <tt>/control?method=left</tt>, <tt>/control?method=right</tt>,
                                                <tt>/control?method=rotate</tt>, <tt>/control?method=down</tt></p>
            <script src=https://cdnjs.cloudflare.com/ajax/libs/jquery/3.3.1/jquery.min.js type=text/javascript></script>
            <script>
                window.da = 0;
                window.setInterval(() => {
                    $.get("/get_state").done((d) => {
                        if (d.da > window.da) {
                            for (let i = 0; i < 20; ++i) {
                                for (let j = 0; j < 10; ++j) {
                                    $('#tetris td')[i*10+j].className = d.board[i][j];
                                }
                            }
                            $("h1").html("Очки: " + d.score + "; флаг: " + (d.flag || "пока не заработан"));
                            window.da = d.da;
                        }
                    });
                }, 100);
            </script>
            <button onclick="document.cookie = 'session=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;'; window.location = '/'">Переиграть</button>
            """


@app.route('/get_state')
def get_state():
    session = request.cookies.get('session')
    if not session:
        return "Session?"
    if session not in games:
        return "Session!?"
    board = [["f" if games[session]['board'][i][j] else ("a" if (0 <= j - games[session]['sx'] <= 3 and 0 <= i - games[session]['sy'] <= 3 and shapes[games[session]['shape']][games[session]['sr']][j - games[session]['sx']][i - games[session]['sy']]) else "") for j in range(10)] for i in range(20)]
    return jsonify({"score": games[session]['score'],
                    "flag": "ugra_nudge_and_switch_and_let_me_go" if games[session]['score'] >= 220 else None,
                    "board": board,
                    "da": time.time()})


@app.route('/control')
def control():
    session = request.cookies.get('session')
    if not session:
        return "Session?"
    if session not in games:
        return "Session!?"
    
    method = request.args.get('method')
    potgame = copy.deepcopy(games[session])

    if method == "left":
        potgame["sx"] -= 1
    elif method == "right":
        potgame["sx"] += 1
    elif method == "down":
        potgame["sy"] += 1
    elif method == "rotate":
        potgame["sr"] += 1
        potgame["sr"] %= 4

    shape = shapes[potgame['shape']][potgame['sr']]
    shape_w, shape_h = 0, 0
    for i in range(4):
        for j in range(4):
            if shape[i][j]:
                shape_w = max(shape_w, i)
                shape_h = max(shape_h, j)
    board_a = [[("a" if (0 <= j - potgame['sx'] <= 3 and 0 <= i - potgame['sy'] <= 3 and shape[j - potgame['sx']][i - potgame['sy']]) else "") for j in range(10)] for i in range(20)]
    equ = [[(board_a[i][j] == "a" and potgame["board"][i][j]) for j in range(10)] for i in range(20)]
    if not sum(sum(equ, [])) and potgame["sx"] >= 0 and potgame["sx"] + shape_w <= 9:
        games[session] = potgame
        return "OK"
    else:
        return "Invalid move", 400


@app.route('/tick')
def tick():
    for s in games:
        potgame = copy.deepcopy(games[s])
        potgame["sy"] += 1
        board_a = [[("a" if (0 <= j - potgame['sx'] <= 3 and 0 <= i - potgame['sy'] <= 3 and shapes[potgame['shape']][potgame['sr']][j - potgame['sx']][i - potgame['sy']]) else "") for j in range(10)] for i in range(20)]
        equ = [[(board_a[i][j] == "a" and potgame["board"][i][j]) for j in range(10)] for i in range(20)]
        shape = shapes[potgame['shape']][potgame['sr']]
        shape_w, shape_h = 0, 0
        for i in range(4):
            for j in range(4):
                if shape[i][j]:
                    shape_w = max(shape_w, i)
                    shape_h = max(shape_h, j)
        if sum(sum(equ, [])) or potgame["sy"] + shape_h >= 20:
            for i in range(4):
                for j in range(4):
                    if games[s]["sy"] + i <= 19 and games[s]["sx"] + j <= 9:
                        games[s]["board"][games[s]["sy"] + i][games[s]["sx"] + j] |= shapes[games[s]["shape"]][games[s]["sr"]][j][i]
            games[s]["shape"] = random.randint(0, 6)
            games[s]["sr"] = random.randint(0, 3)
            games[s]["sx"] = 4
            games[s]["sy"] = 0
        else:
            games[s] = potgame
        games[s]["board"] = [i for i in games[s]["board"] if i != [1,1,1,1,1,1,1,1,1,1]]
        if len(games[s]["board"]) < 20:
            games[s]["score"] += [0, 10, 30, 80, 150][20 - len(games[s]["board"])]
            games[s]["board"] = [[0,0,0,0,0,0,0,0,0,0] for i in range(20 - len(games[s]["board"]))] + games[s]["board"]
    return "Tick OK"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=13309, debug=False)
