#!/usr/bin/env python3

import traceback
import datetime
import random

from flask import Flask, request, Response, redirect, render_template

app = Flask(__name__)


def calc_check_digit(number):
    return number + str((10 - sum((3, 1)[i % 2] * int(n)
                         for i, n in enumerate(reversed(number)))) % 10)


@app.route('/')
def index():
    return """<style>input{font:inherit}body{font-size:30pt}</style><h1>Регистрация</h1>
              <form method=post action=reg>
              <p>Пользователь<br><input name=user>
              <p>Пароль<br><input name=pass type=password>
              <p>Подтверждение пароля<br><input name=pass2 type=password>
              <p><input type=submit value=Перейти> к подтверждению регистрации</form>"""


@app.route('/codes-soidjfsoidfjidsfoi')
def codes():
    return open('codes.txt').read()


@app.route('/reg', methods=["POST"])
def reg():
    if not request.form.get('user'):
        return "<style>input{font:inherit}body{font-size:30pt}</style>Неверные данные!", 500
    if len(request.form.get('pass', '')) < 5 or request.form.get('pass') != request.form.get('pass2'):
        return "<style>input{font:inherit}body{font-size:30pt}</style>Небезопасный пароль или пароли не совпадают!", 500
    codeno = len(open('codes.txt').read().splitlines()) + 1
    code = calc_check_digit('0421%08d' % (random.randint(0, 100000000)))
    open('codes.txt', 'a').write('%d,%s,%s\n' % (codeno, (datetime.datetime.now() + datetime.timedelta(seconds=10)).strftime("%Y-%m-%d %H:%M:%S"), code))
    return """<style>input{font:inherit}body{font-size:30pt}</style><h1>Подтверждение регистрации</h1>
              <form method=post action=confirm>
              <p>Код подтверждения номер <b>%d</b><br><input name=code id=a>
              <input type=hidden name=codeno value=%d>
              <p><input type=submit value=Зарегистрироваться></form>
              <script>document.getElementById('a').focus()</script>""" % (codeno, codeno)


@app.route('/confirm', methods=["POST"])
def confirm():
    entered_code = request.form.get('code')
    codes = [i.split(',') for i in open('codes.txt').read().strip().split("\n")]
    codes = {c: datetime.datetime.strptime(exp, "%Y-%m-%d %H:%M:%S") for num, exp, c in codes}
    if entered_code in codes and codes[entered_code] >= datetime.datetime.now().replace(microsecond=0):
        return "<style>input{font:inherit}body{font-size:30pt}</style><h1>Регистрация подтверждена</h1><p><tt>ugra_filin_podtverdi_podtverzhdayu</tt>" + "<p>%s</p>" % repr(datetime.datetime.now())
    elif entered_code in codes:
        return """<style>input{font:inherit}body{font-size:30pt}</style><h1>Срок действия кода истёк</h1><p>Срок действия кода был <b>%s</b>, а сейчас <b>%s</b>.<p><a href=/>Попробовать снова</a>""" % (codes[entered_code].strftime("%Y-%m-%d %H:%M:%S"), datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    else:
        return """<style>input{font:inherit}body{font-size:30pt}</style><h1>Код неверный</h1><p>Такого кода нет и не было никогда.<p><a href=/>Попробовать снова</a>"""


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=13301, debug=False)
