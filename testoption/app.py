# app.py
from flask import Flask # type: ignore
from flask import render_template,redirect,request # type: ignore
import json,os

app = Flask(__name__)
data_dir = 'testoption/data/result.json'
os.makedirs(os.path.dirname(data_dir), exist_ok=True) 

# budget management
def calculate(total: int, food: int, bar:int) -> int:
    """Tính tiền dựa trên số lượng và đơn giá."""
    return total - food - bar 

# load data from result.json
def load_data():
    if os.path.exists(data_dir):
        try:
            with open(data_dir, 'r', encoding='UTF-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
   
# save result to result.json
def save_result(result: int, total: int, food: int, bar: int) -> None:
    data = {
        'total': total,
        'food': food,
        'bar': bar,
        'remaining': result
    }
    existing_data = load_data()
    existing_data.append(data)
    try:
        with open(data_dir, 'w',encoding='UTF-8') as f:
            json.dump(existing_data, f, indent=4, ensure_ascii=False) 
    except IOError as e:
        print(f"Error saving result to JSON file: {e}")

@app.route('/')
def index():
    """Hiển thị trang chủ."""
    return render_template('result.html')

@app.route('/tinh_tien', methods=['POST', 'GET'])
def calcu():
    """Xử lý yêu cầu tính tiền."""
    if request.method == 'GET':
        return render_template('result.html')
    elif request.method == 'POST':
        total = int(request.form['total'])
        food = int(request.form['food'])
        bar = int(request.form['bar'])
        remaining = calculate(total, food,bar)
        save_result(remaining, total, food, bar)
        return render_template('result.html', remaining=remaining, total=total, food=food,bar=bar)

if __name__ == '__main__':
    app.run(debug=True)