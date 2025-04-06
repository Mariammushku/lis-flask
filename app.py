from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Render-ის გარემოს ცვლადი
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# განახლებული მოდელი
class TestResult(db.Model):
    __tablename__ = 'test_result_v3'  # ახალი ცხრილი

    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(100))
    result = db.Column(db.String(100))
    date = db.Column(db.String(20))
    level = db.Column(db.String(20))
    min = db.Column(db.String(20))
    max = db.Column(db.String(20))
    lot_number = db.Column(db.String(50))
    recalibrated = db.Column(db.String(100))  # ახალი ველი
    retested = db.Column(db.String(100))      # ახალი ველი

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        test_name = request.form['test_name']
        result = request.form['result']
        date = request.form['date']
        level = request.form['level']
        min_value = request.form['min']
        max_value = request.form['max']
        lot_number = request.form['lot_number']
        recalibrated = request.form.get('recalibrated', '')
        retested = request.form.get('retested', '')

        if not all([test_name, result, date, level, min_value, max_value, lot_number]):
            return "<h3 style='color:red;'>გთხოვთ შეავსოთ ყველა ველი.</h3><a href='/'><button>დაბრუნება</button></a>"

        # შედეგის რეინჯში შემოწმება
        try:
            in_range = float(min_value) <= float(result) <= float(max_value)
        except ValueError:
            return "<h3 style='color:red;'>შედეგი, მინ და მაქს უნდა იყოს რიცხვები.</h3><a href='/'><button>დაბრუნება</button></a>"

        if in_range:
            recalibrated = ''
            retested = ''

        new_result = TestResult(
            test_name=test_name,
            result=result,
            date=date,
            level=level,
            min=min_value,
            max=max_value,
            lot_number=lot_number,
            recalibrated=recalibrated,
            retested=retested
        )
        db.session.add(new_result)
        db.session.commit()

        # ლამაზი შენახვის გვერდი
        return f"""
        <!DOCTYPE html>
        <html lang="ka">
        <head>
            <meta charset="UTF-8">
            <title>შენახვა წარმატებულია</title>
            <style>
                body {{
                    font-family: "Segoe UI", sans-serif;
                    background-color: #f4f4f4;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    justify-content: center;
                    height: 100vh;
                    margin: 0;
                }}
                .box {{
                    background-color: white;
                    padding: 30px 40px;
                    border-radius: 12px;
                    box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
                    text-align: center;
                }}
                h2 {{
                    color: #4CAF50;
                    margin-bottom: 25px;
                }}
                button {{
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 12px 25px;
                    font-size: 16px;
                    border-radius: 5px;
                    cursor: pointer;
                }}
                button:hover {{
                    background-color: #45a049;
                }}
            </style>
        </head>
        <body>
            <div class="box">
                <h2>ტესტი '<span style="color:#333;">{test_name}</span>' წარმატებით შენახულია!</h2>
                <a href="/"><button>მთავარ გვერდზე დაბრუნება</button></a>
            </div>
        </body>
        </html>
        """

    return render_template('form.html')

@app.route('/results')
def results():
    all_results = TestResult.query.all()
    return render_template('results.html', results=all_results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
