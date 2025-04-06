from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(_name_)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class TestResult(db.Model):
    _tablename_ = 'test_result_v3'
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(100))
    lot_number = db.Column(db.String(50))
    result = db.Column(db.String(100))
    date = db.Column(db.String(20))
    level = db.Column(db.String(20))
    min = db.Column(db.String(20))
    max = db.Column(db.String(20))

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

        # ცარიელი ველები არ შეინახოს
        if not all([test_name, lot_number, result, date, level, min_value, max_value]):
            return render_template('form.html', error="გთხოვ შეავსო ყველა ველი!")

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

        return render_template('success.html', test_name=test_name)

    return render_template('form.html')

@app.route('/results')
def results():
    all_results = TestResult.query.all()
    return render_template('results.html', results=all_results)

if _name_ == '_main_':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')