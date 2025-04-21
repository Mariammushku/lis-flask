from flask import Flask, render_template, request, redirect, send_from_directory, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test_results.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    branch = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(200), nullable=True)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        recalibrated = request.form.get('recalibrated') == 'on'
        
        uploaded_file = request.files['file']
        file_path = None

        if uploaded_file and uploaded_file.filename != '':
            filename = secure_filename(uploaded_file.filename)
            uploaded_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_path = filename

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
            branch=request.form['branch'],
            file_path=file_path
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

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
