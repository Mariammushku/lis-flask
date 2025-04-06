from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Render-ის გარემოს ცვლადი
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# მოდელი
class TestResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_name = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    level = db.Column(db.String(20), nullable=False)
    min = db.Column(db.String(20), nullable=False)
    max = db.Column(db.String(20), nullable=False)
    lot_number = db.Column(db.String(50), nullable=False)

# მთავარი გვერდი
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

        if not all([test_name, result, date, level, min_value, max_value, lot_number]):
            return "<h3 style='color:red;'>გთხოვთ შეავსოთ ყველა ველი.</h3><a href='/'><button>დაბრუნება</button></a>"

        new_result = TestResult(
            test_name=test_name,
            result=result,
            date=date,
            level=level,
            min=min_value,
            max=max_value,
            lot_number=lot_number
        )
        db.session.add(new_result)
        db.session.commit()

        return f"""
        <h2>ტესტი '{test_name}' წარმატებით შენახულია!</h2>
        <a href='/'><button>მთავარ გვერდზე დაბრუნება</button></a>
        """

    return render_template('form.html')

# შედეგების გვერდი
@app.route('/results')
def results():
    all_results = TestResult.query.all()
    return render_template('results.html', results=all_results)

# ბაზის შექმნა ლოკალურად
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0')
