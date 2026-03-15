from flask import Flask, render_template, jsonify, request
import math

app = Flask(__name__)

def calculate_dispatch(employees, cars):
    active_emps = [dict(e, picked=False) for e in employees]
    active_cars = [dict(c, used=0, path=[], pos={'x': 0, 'y': 0}) for c in cars]

    for car in active_cars:
        seats = 4
        while seats > 0:
            best = None
            min_dist = float('inf')
            for e in active_emps:
                if not e['picked']:
                    d = math.sqrt((e['x'] - car['pos']['x'])**2 + (e['y'] - car['pos']['y'])**2)
                    if d < min_dist:
                        min_dist = d
                        best = e
            
            if best and (car['used'] + min_dist) <= car['cap']:
                best['picked'] = True
                car['path'].append(best)
                car['used'] += min_dist
                car['pos'] = {'x': best['x'], 'y': best['y']}
                seats -= 1
            else:
                break
    return active_cars, [e for e in active_emps if not e['picked']]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dispatch', methods=['POST'])
def dispatch():
    data = request.json
    results, stranded = calculate_dispatch(data['employees'], data['cars'])
    return jsonify({'cars': results, 'stranded': stranded})

if __name__ == '__main__':
    import os
    # Railway automatically provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
