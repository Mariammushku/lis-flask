from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# ბაზის მისამართი - Render-ის Environment Variable-დან
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# მონაცემთა მოდელი
class TestResult(db.Model):
    _tablename_ = 'test_result_v3'  # ახალი ცხრილის სახელი
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(100))
    result = db.Column(db.String(100))
    date = db.Column(db.String(20))
    level = db.Column(db.String(20))
    min = db.Column(db.String(20))
    max = db.Column(db.String(20))
    lot_number = db.Column(db.String(50))

# მთავარი გვერდი - ფორმა
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        test_name = request.form['test_name']
        lot_number = request.form['lot_number']
        result = request.form['result']
        date = request.form['date']
        level = request.form['level']
        min_value = request.form['min']
        max_value = request.form['max']

        # ცარიელი ველების შემოწმება
        if not all([test_name, lot_number, result, date, level, min_value, max_value]):
            return "<h3 style='color:red;'>გთხოვ შეავსო ყველა ველი!</h3><a href='/'><button>დაბრუნება</button></a>"

        new_result = TestResult(
            test_name=test_name,
            lot_number=lot_number,
            result=result,
            date=date,
            level=level,
            min=min_value,
            max=max_value
        )
        db.session.add(new_result)
        db.session.commit()

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

# შედეგების გვერდი
@app.route('/results')
def results():
    all_results = TestResult.query.all()
    return render_template('results.html', results=all_results)

# ბაზის შექმნა
if _name_ == '_main_':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')