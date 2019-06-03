#!/usr/bin/env python3

import math
import os
import random
import traceback

from flask import Flask, request, Response, redirect, render_template

app = Flask(__name__)


LAT, LON = 55.766954, 37.734877

def dist(lat1, lon1, lat2, lon2):
    R = 6373.0
    lat1, lon1, lat2, lon2 = [math.radians(i) for i in (lat1, lon1, lat2, lon2)]
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


@app.route('/IMG_2223.jpg')
def image():
    return Response(open('IMG_2223.jpg', 'rb').read(), mimetype='image/jpeg')


@app.route('/')
def index():
    if not len(os.listdir("codes")):
        return "No codes set up! Create some empty files named /04[0-9]+/ in the codes/ directory next to app/"
    return render_template('index.html')


def do_check(request):
    try:
        lat_part = request.values.get('lat', '').strip()
        lon_part = request.values.get('lon', '').strip()
        code_part = request.values.get('code', '').strip()
        try:
            [int(i) for i in (lat_part, lon_part, code_part)]
        except ValueError:
            return "presentation-error"
        lat, lon, code = float("55." + lat_part), float("37." + lon_part), "04" + code_part

        try:
            suffix = "_" + str(random.randint(0, 10000000000000000))
            os.rename("codes/" + code, "codes/" + code + suffix)  # let's call it a lock
            if open("codes/" + code + suffix).read():
                return "code-wasted"
            else:
                open("codes/" + code + suffix, "w").write("%.9f,%.9f" % (lat, lon))
                if dist(LAT, LON, lat, lon) < 0.155:
                    return "correct"
                else:
                    return "incorrect"
        except FileNotFoundError:
            return "code-incorrect"
        finally:
            try:
                os.rename("codes/" + code + suffix, "codes/" + code)
            except FileNotFoundError:
                pass
    except:
        return traceback.format_exc()


@app.route('/check', methods=["POST"])
def check():
    return render_template('result.html', result=do_check(request))


if __name__ == "__main__":
    app.run()
