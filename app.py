from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# ბაზის ფაილის მისამართი
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# მონაცემთა მოდელი
class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(100))
    result = db.Column(db.String(100))
    date = db.Column(db.String(20))
    level = db.Column(db.String(20))
    min = db.Column(db.String(20))
    max = db.Column(db.String(20))

# მთავარი გვერდი - ფორმა
@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        test_name = request.form['test_name']
        result = request.form['result']
        date = request.form['date']
        level = request.form['level']
        min_value = request.form['min']
        max_value = request.form['max']

        # მონაცემის შენახვა
        new_result = TestResult(
            test_name=test_name,
            result=result,
            date=date,
            level=level,
            min=min_value,
            max=max_value
        )
        db.session.add(new_result)
        db.session.commit()

        return f"ტესტი '{test_name}' წარმატებით შენახულია!"

    return render_template('form.html')

# შედეგების გვერდი
@app.route('/results')
def results():
    all_results = TestResult.query.all()
    return render_template('results.html', results=all_results)

# ბაზის შექმნა და აპის გაშვება
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
