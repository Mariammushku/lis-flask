from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TestResult(db.Model):
    __tablename__ = 'test_result_v2'
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(100))
    result = db.Column(db.Float)
    date = db.Column(db.String(20))
    level = db.Column(db.String(20))
    min = db.Column(db.Float)
    max = db.Column(db.Float)
    lot_number = db.Column(db.String(50))
    recalibrated = db.Column(db.String(10))   # "დიახ" ან "არა"
    retest_result = db.Column(db.String(20))  # რიცხვი ან ცარიელი

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
        retest_result = request.form.get('retest_result', '')

        # აუცილებელი ველების შემოწმება
        if not all([test_name, result, date, level, min_value, max_value, lot_number]):
            return "<h3 style='color:red;'>გთხოვთ შეავსოთ ყველა ველი.</h3><a href='/'><button>დაბრუნება</button></a>"

        # გადაყვანა რიცხვებად
        try:
            result_float = float(result)
            min_float = float(min_value)
            max_float = float(max_value)
        except ValueError:
            return "<h3 style='color:red;'>შედეგი, მინიმუმი და მაქსიმუმი უნდა იყოს რიცხვი.</h3><a href='/'><button>დაბრუნება</button></a>"

        # თუ შედეგი არ ზის რეინჯში → საჭიროა დამატებითი ველების შევსება
        if result_float < min_float or result_float > max_float:
            if not recalibrated or not retest_result:
                return "<h3 style='color:red;'>როდესაც შედეგი არ ჯდება ზღვარში, საჭიროა გადაკალიბრების და რეტესტის შევსება.</h3><a href='/'><button>დაბრუნება</button></a>"

        new_result = TestResult(
            test_name=test_name,
            result=result_float,
            date=date,
            level=level,
            min=min_float,
            max=max_float,
            lot_number=lot_number,
            recalibrated=recalibrated,
            retest_result=retest_result
        )
        db.session.add(new_result)
        db.session.commit()
        return render_template('success.html', test_name=test_name)

    return render_template('form.html')

@app.route('/results')
def results():
    all_results = TestResult.query.all()
    return render_template('results.html', results=all_results)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
