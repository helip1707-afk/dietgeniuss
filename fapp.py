from flask import Flask, render_template, request
import math, sqlite3, datetime

app = Flask(__name__)

# 🔹 DATABASE
conn = sqlite3.connect("fitness.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY,
    name TEXT,
    weight REAL,
    date TEXT
)
""")
conn.commit()

# 🔹 HOME
@app.route('/')
def index():
    return render_template("index.html")

# 🔹 CALCULATE
@app.route('/calculate', methods=['POST'])
def calculate():
    name = request.form['name']
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    age = int(request.form['age'])
    gender = request.form['gender']
    activity = request.form['activity']

    bmi = weight / ((height/100)**2)

    # CATEGORY + SUGGESTION
    if bmi < 18.5:
        category = "Underweight"
        suggestion = "Focus on weight gain with nutritious food."
        workout = "Light strength training + yoga."
    elif bmi < 25:
        category = "Normal"
        suggestion = "Maintain your lifestyle."
        workout = "Mix cardio + strength (3-4 days)."
    elif bmi < 30:
        category = "Overweight"
        suggestion = "Start gradual fat loss."
        workout = "Cardio + light strength (5 days)."
    else:
        category = "Obese"
        suggestion = "Focus on fat loss urgently."
        workout = "Walking + low impact cardio."

    # BMR
    if gender == "male":
        bmr = 10*weight + 6.25*height - 5*age + 5
    else:
        bmr = 10*weight + 6.25*height - 5*age - 161

    # TDEE
    factors = {"sedentary":1.2,"light":1.375,"moderate":1.55,"active":1.725}
    tdee = bmr * factors.get(activity,1.2)

    return render_template("result.html",
        name=name, weight=weight,
        bmi=round(bmi,2),
        category=category,
        tdee=round(tdee,2),
        suggestion=suggestion,
        workout=workout
    )

# 🔹 GOAL
@app.route('/goal', methods=['POST'])
def goal():
    weight = float(request.form['weight'])
    goal_weight = float(request.form['goal_weight'])
    tdee = float(request.form['tdee'])
    duration = int(request.form['duration'])

    calories = tdee - ((weight-goal_weight)*7700)/(duration*7)

    protein = goal_weight * 1.5
    carbs = (calories * 0.4)/4
    fat = (calories * 0.3)/9

    return render_template("goal.html",
        calories=round(calories,2),
        protein=round(protein,2),
        carbs=round(carbs,2),
        fat=round(fat,2)
    )

# 🔹 TRACK DAILY WEIGHT
@app.route('/track', methods=['POST'])
def track():
    name = request.form['name']
    weight = float(request.form['weight'])
    date = str(datetime.date.today())

    cursor.execute("INSERT INTO progress (name,weight,date) VALUES (?,?,?)",
                   (name,weight,date))
    conn.commit()

    return f"<a href='/progress/{name}'>View Progress</a>"

# 🔹 PROGRESS GRAPH
@app.route('/progress/<name>')
def progress(name):
    cursor.execute("SELECT date,weight FROM progress WHERE name=?", (name,))
    data = cursor.fetchall()

    dates = [d[0] for d in data]
    weights = [d[1] for d in data]

    return render_template("progress.html",
                           name=name,
                           dates=dates,
                           weights=weights)

# 🔹 PLAN
@app.route('/plan')
def plan():
    workout_plan = [
        {"day": i+1, "task": task} for i, task in enumerate([
            "Stretch + Walk",
            "Cardio",
            "Upper Body",
            "Lower Body",
            "Core",
            "Yoga",
            "Rest"
        ] * 4 + ["HIIT", "Full Body"])
    ]

    diet_plan = {
        "Monday": ["Poha", "Roti + Sabji", "Khichdi"],
        "Tuesday": ["Upma", "Rice + Dal", "Paneer"],
        "Wednesday": ["Oats", "Veg", "Dal Rice"],
        "Thursday": ["Paratha", "Sabji", "Khichdi"],
        "Friday": ["Idli", "Rajma", "Roti"],
        "Saturday": ["Daliya", "Dal", "Soup"],
        "Sunday": ["Light", "Light", "Salad"]
    }

    return render_template("plan.html",
        workout_plan=workout_plan,
        diet_plan=diet_plan
    )

if __name__ == "__main__":
    app.run(debug=True)
