from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50), nullable=False)
    min = db.Column(db.Float, nullable=False)
    max = db.Column(db.Float, nullable=False)
    lot_number = db.Column(db.String(100), nullable=True)
    recalibrated = db.Column(db.Boolean, nullable=True)
    retest_result = db.Column(db.String(100), nullable=True)
    branch = db.Column(db.String(50), nullable=False)  # ➡️ ახალი ველი

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        recalibrated = request.form.get('recalibrated') == 'on'
        test_result = TestResult(
            test_name=request.form['test_name'],
            result=request.form['result'],
            date=request.form['date'],
            level=request.form['level'],
            min=request.form['min'],
            max=request.form['max'],
            lot_number=request.form['lot_number'],
            recalibrated=recalibrated,
            retest_result=request.form['retest_result'],
            branch=request.form['branch']  # ➡️ ფილიალი
        )
        db.session.add(test_result)
        db.session.commit()
        return redirect('/results')
    return render_template('form.html')

@app.route('/results')
def results():
    branch_filter = request.args.get('branch_filter')
    if branch_filter:
        test_results = TestResult.query.filter_by(branch=branch_filter).all()
    else:
        test_results = TestResult.query.all()
    return render_template('results.html', test_results=test_results)

if __name__ == '__main__':
    app.run(debug=True)
