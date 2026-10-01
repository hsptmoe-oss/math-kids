from flask import Flask, render_template, request, jsonify
import random
import math

app = Flask(__name__)

def generate_choices(ans):
    choices = set([ans])
    while len(choices) < 4:
        if isinstance(ans, float):
            wrong = round(ans + random.choice([-1.5, -0.5, 0.5, 1.5, 2.0, -2.0, 10, -10]), 2)
            if wrong < 0: wrong = abs(wrong)
        else:
            offset = random.randint(1, max(10, int(ans * 0.2)))
            wrong = ans + random.choice([-offset, offset, 10, -10])
            if wrong < 0: wrong = abs(wrong)
        if wrong != ans:
            choices.add(wrong)
    choices_list = list(choices)
    random.shuffle(choices_list)
    return choices_list

@app.route('/')
def index():
    grades = [
        {"id": "k", "name": "ថ្នាក់មត្តេយ្យ (Kindergarten)", "color": "#FF6B6B", "icon": "🧸"},
        {"id": "1", "name": "ថ្នាក់ទី១ (Grade 1)", "color": "#4ECDC4", "icon": "🍎"},
        {"id": "2", "name": "ថ្នាក់ទី២ (Grade 2)", "color": "#45B7D1", "icon": "🎈"},
        {"id": "3", "name": "ថ្នាក់ទី៣ (Grade 3)", "color": "#FDCB6E", "icon": "🌟"},
        {"id": "4", "name": "ថ្នាក់ទី៤ (Grade 4)", "color": "#6C5CE7", "icon": "🚀"},
        {"id": "5", "name": "ថ្នាក់ទី៥ (Grade 5)", "color": "#A8E6CF", "icon": "🔬"},
        {"id": "6", "name": "ថ្នាក់ទី៦ (Grade 6)", "color": "#FF8ED4", "icon": "🏆"},
    ]
    return render_template('index.html', grades=grades)

@app.route('/grade/<grade_id>')
def grade_dashboard(grade_id):
    grades_info = {
        "k": {"name": "ថ្នាក់មត្តេយ្យ", "color": "#FF6B6B", "icon": "🧸"},
        "1": {"name": "ថ្នាក់ទី១", "color": "#4ECDC4", "icon": "🍎"},
        "2": {"name": "ថ្នាក់ទី២", "color": "#45B7D1", "icon": "🎈"},
        "3": {"name": "ថ្នាក់ទី៣", "color": "#FDCB6E", "icon": "🌟"},
        "4": {"name": "ថ្នាក់ទី៤", "color": "#6C5CE7", "icon": "🚀"},
        "5": {"name": "ថ្នាក់ទី៥", "color": "#A8E6CF", "icon": "🔬"},
        "6": {"name": "ថ្នាក់ទី៦", "color": "#FF8ED4", "icon": "🏆"},
    }
    info = grades_info.get(grade_id, grades_info["1"])
    return render_template('grade_dashboard.html', grade_id=grade_id, info=info)

@app.route('/lesson/<grade_id>')
def lesson_view(grade_id):
    if grade_id == 'k':
        return render_template('lesson_k.html')
    else:
        return render_template('lesson.html', grade_id=grade_id)

@app.route('/exercise/<grade_id>')
def exercise_view(grade_id):
    if grade_id == 'k':
        return render_template('kindergarten.html', mode='normal')
    else:
        return render_template('grade.html', grade_id=grade_id, mode='normal')

@app.route('/exercise_mcq/<grade_id>')
def exercise_mcq_view(grade_id):
    if grade_id == 'k':
        return render_template('kindergarten_mcq.html')
    else:
        return render_template('grade_mcq.html', grade_id=grade_id)

@app.route('/exercise_challenge/<grade_id>')
def exercise_challenge_view(grade_id):
    return render_template('grade_challenge.html', grade_id=grade_id)

@app.route('/api/math/k')
def get_k_math():
    objects = [
        {"name": "ផ្លែប៉ោម", "verb": "ផ្លែ", "emoji1": "🍎", "emoji2": "🍏"},
        {"name": "ឡានក្មេងលេង", "verb": "គ្រឿង", "emoji1": "🚗", "emoji2": "🚕"},
        {"name": "ប៉េងប៉ោង", "verb": "ផ្លែ", "emoji1": "🎈", "emoji2": "🎈"},
        {"name": "ផ្កា", "verb": "ទង", "emoji1": "🌻", "emoji2": "🌷"},
        {"name": "សត្វឆ្មា", "verb": "ក្បាល", "emoji1": "🐱", "emoji2": "😸"},
        {"name": "ស្ករគ្រាប់", "verb": "គ្រាប់", "emoji1": "🍬", "emoji2": "🍭"}
    ]
    obj = random.choice(objects)
    
    num1 = random.randint(1, 5)
    num2 = random.randint(1, 5)
    ans = num1 + num2
    
    choices = set([ans])
    while len(choices) < 3:
        wrong = ans + random.randint(-2, 3)
        if wrong > 0 and wrong != ans:
            choices.add(wrong)
    choices_list = list(choices)
    random.shuffle(choices_list)
    
    return jsonify({
        "question": f"តើមាន{obj['name']}ប៉ុន្មាន{obj['verb']} សរុប បើអ្នកមាន {num1} ហើយមិត្តភក្តិឱ្យ {num2} ទៀត?",
        "num1": num1,
        "num2": num2,
        "answer": ans,
        "choices": choices_list,
        "type": "addition",
        "emoji1": obj["emoji1"],
        "emoji2": obj["emoji2"]
    })

@app.route('/api/math/<int:grade>')
def get_grade_math(grade):
    # Singapore Math Standards
    if grade == 1:
        # Addition and subtraction within 100
        num1 = random.randint(10, 99)
        num2 = random.randint(1, 50)
        op = random.choice(['+', '-'])
    elif grade == 2:
        # Add/Sub within 1000, Multiplication basics
        op = random.choice(['+', '-', '*'])
        if op in ['+', '-']:
            num1 = random.randint(100, 999)
            num2 = random.randint(10, 500)
        else:
            num1 = random.randint(2, 10)
            num2 = random.choice([2, 3, 4, 5, 10])
    elif grade == 3:
        # Add/Sub within 10000, Mult 2-digit by 1-digit, Div exact
        if random.random() < 0.3: # 30% chance of word problem
            if random.choice([True, False]):
                a = random.randint(100, 999)
                b = random.randint(100, 999)
                question_str = f"សាលារៀនមានសិស្សប្រុស {a} នាក់ និងសិស្សស្រី {b} នាក់។ តើសាលារៀនមានសិស្សសរុបប៉ុន្មាននាក់?"
                ans = a + b
            else:
                a = random.randint(500, 1000)
                b = random.randint(100, a - 1)
                question_str = f"កសិដ្ឋានមួយមានមាន់ {a} ក្បាល ហើយលក់ចេញបាន {b} ក្បាល។ តើនៅសល់មាន់ប៉ុន្មានក្បាល?"
                ans = a - b
            return jsonify({"question": question_str, "answer": ans, "choices": generate_choices(ans), "layout": "word"})
            
        op = random.choice(['+', '-', '*', '/'])
        if op in ['+', '-']:
            num1 = random.randint(1000, 9999)
            num2 = random.randint(100, 5000)
        elif op == '*':
            num1 = random.randint(11, 99)
            num2 = random.randint(2, 9)
        else:
            num2 = random.randint(2, 9)
            ans_temp = random.randint(11, 99)
            num1 = num2 * ans_temp
    elif grade == 4:
        # Mult 3-digit by 2-digit, long division
        if random.random() < 0.3:
            if random.choice([True, False]):
                a = random.randint(15, 99) * 100
                b = random.randint(5, 12)
                question_str = f"សៀវភៅមួយក្បាលមានតម្លៃ {a} រៀល។ តើសៀវភៅ {b} ក្បាលមានតម្លៃប៉ុន្មានរៀលសរុប?"
                ans = a * b
            else:
                b = random.randint(5, 15)
                ans = random.randint(10, 50)
                a = ans * b
                question_str = f"គ្រូបង្រៀនមានស្ករគ្រាប់ {a} គ្រាប់ ចែកឱ្យសិស្ស {b} នាក់ស្មើៗគ្នា។ តើសិស្សម្នាក់ទទួលបានប៉ុន្មានគ្រាប់?"
            return jsonify({"question": question_str, "answer": ans, "choices": generate_choices(ans), "layout": "word"})
            
        op = random.choice(['*', '/'])
        if op == '*':
            num1 = random.randint(100, 999)
            num2 = random.randint(10, 99)
        else:
            num2 = random.randint(2, 15)
            ans_temp = random.randint(100, 999)
            num1 = num2 * ans_temp
    elif grade == 5:
        # Decimal operations
        if random.random() < 0.3:
            if random.choice([True, False]):
                a = round(random.uniform(5, 20), 2)
                b = round(random.uniform(3, 10), 2)
                question_str = f"សុខទិញបន្លែអស់ {a}$ និងទិញផ្លែឈើអស់ {b}$។ តើគាត់ចំណាយប្រាក់សរុបប៉ុន្មានដុល្លារ?"
                ans = round(a + b, 2)
            else:
                a = round(random.uniform(10, 30), 1)
                b = round(random.uniform(5, 15), 1)
                question_str = f"ដីមួយកន្លែងមានបណ្តោយ {a} ម៉ែត្រ និងទទឹង {b} ម៉ែត្រ។ តើដីនោះមានក្រឡាផ្ទៃប៉ុន្មានម៉ែត្រការ៉េ?"
                ans = round(a * b, 2)
            return jsonify({"question": question_str, "answer": ans, "choices": generate_choices(ans), "layout": "word"})
            
        op = random.choice(['+', '-', '*'])
        if op in ['+', '-']:
            num1 = round(random.uniform(10, 100), 2)
            num2 = round(random.uniform(1, 50), 2)
        else:
            num1 = round(random.uniform(1, 20), 1)
            num2 = random.randint(2, 15)
    else:
        # Grade 6: Order of operations, harder decimals, percentages
        if random.random() < 0.4: # 40% chance of word problem
            if random.choice([True, False]):
                ans = random.randint(10, 50)
                a = ans * 2
                b = random.choice([10, 20, 25, 40, 50])
                a = int(ans * (100 / b))
                question_str = f"សាលាមួយមានសិស្សសរុប {a} នាក់ ដែលក្នុងនោះ {b}% ជាសិស្សស្រី។ តើមានសិស្សស្រីចំនួនប៉ុន្មាននាក់?"
            else:
                ans = random.randint(10, 40)
                a = random.randint(5, 20)
                b = 3 * ans + a
                question_str = f"បើ ៣ ដងនៃទម្ងន់របស់ចាបូ បូកនឹង {a} ស្មើនឹង {b} គីឡូក្រាម។ តើចាបូមានទម្ងន់ប៉ុន្មានគីឡូក្រាម?"
            return jsonify({"question": question_str, "answer": ans, "choices": generate_choices(ans), "layout": "word"})
            
        type_q = random.choice(['decimal_div', 'order_op'])
        if type_q == 'decimal_div':
            op = '/'
            num2 = random.choice([0.2, 0.4, 0.5, 2, 4, 5])
            ans_temp = round(random.uniform(10, 50), 1)
            num1 = round(num2 * ans_temp, 2)
        else:
            # order of operations: a * b + c or a + b * c
            a = random.randint(5, 20)
            b = random.randint(2, 10)
            c = random.randint(10, 100)
            pattern = random.choice(["{} * {} + {}", "{} + {} * {}"])
            question_str = pattern.format(a, b, c)
            ans = eval(question_str)
            return jsonify({
                "question": f"{question_str} = ?",
                "answer": ans,
                "choices": generate_choices(ans),
                "layout": "horizontal"
            })

    if op == '-' and num1 < num2:
        num1, num2 = num2, num1
        
    ans = eval(f"{num1} {op} {num2}")
    if isinstance(ans, float):
        ans = round(ans, 2)
        
    # Format the display correctly for floats
    str_num1 = f"{num1:.2f}".rstrip('0').rstrip('.') if isinstance(num1, float) else str(num1)
    str_num2 = f"{num2:.2f}".rstrip('0').rstrip('.') if isinstance(num2, float) else str(num2)
    
    layout = "vertical" if grade <= 3 else "horizontal"
    
    return jsonify({
        "question": f"{str_num1} {op} {str_num2} = ?",
        "num1": str_num1,
        "num2": str_num2,
        "op": op,
        "answer": ans,
        "choices": generate_choices(ans),
        "layout": layout
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
