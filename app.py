from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        test_name = request.form['test_name']
        result = request.form['result']
        date = request.form['date']
        level = request.form['level']
        min_value = request.form['min']
        max_value = request.form['max']

        print("მონაცემები მიღებულია:")
        print(f"ტესტი: {test_name}, შედეგი: {result}, თარიღი: {date}, დონე: {level}, მინ: {min_value}, მაქს: {max_value}")

        return f"მონაცემები მიღებულია ტესტისთვის: {test_name}"

    return render_template('form.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

