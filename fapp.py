from flask import Flask, render_template, request
import math

app = Flask(__name__)

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

    bmi = weight / math.pow(height/100, 2)

    # CATEGORY
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    # BMR
    if gender == "male":
        bmr = 10*weight + 6.25*height - 5*age + 5
    else:
        bmr = 10*weight + 6.25*height - 5*age - 161

    # TDEE
    factors = {
        "sedentary":1.2,
        "light":1.375,
        "moderate":1.55,
        "active":1.725
    }
    tdee = bmr * factors.get(activity,1.2)

    return render_template("result.html",
        name=name,
        weight=weight,
        bmi=round(bmi,2),
        category=category,
        tdee=round(tdee,2)
    )


# 🔹 GOAL PLAN
@app.route('/goal', methods=['POST'])
def goal():

    weight = float(request.form['weight'])
    goal_weight = float(request.form['goal_weight'])
    duration = int(request.form['duration'])
    tdee = float(request.form['tdee'])

    diff = weight - goal_weight
    calories = tdee - (diff * 7700)/(duration*7)

    protein = goal_weight * 1.5
    carbs = (calories * 0.4)/4
    fat = (calories * 0.3)/9

    return render_template("goal.html",
        calories=round(calories,2),
        protein=round(protein,2),
        carbs=round(carbs,2),
        fat=round(fat,2)
    )


# 🔹 30 DAY + 7 DAY PLAN
@app.route('/plan')
def plan():

    workout_plan = [
        {"day": i+1, "task": task} for i, task in enumerate([
            "Full Body Stretch + Walk",
            "Cardio (Jumping + Skipping)",
            "Upper Body Workout",
            "Lower Body Workout",
            "Core (Abs)",
            "Yoga",
            "Rest"
        ] * 4 + ["HIIT", "Full Body Challenge"])
    ]

    diet_plan = {
        "Monday": ["Poha + Tea", "Roti + Sabji + Dal", "Khichdi"],
        "Tuesday": ["Upma", "Rice + Dal", "Paneer"],
        "Wednesday": ["Oats", "Roti + Veg", "Dal Rice"],
        "Thursday": ["Paratha + Curd", "Sabji", "Khichdi"],
        "Friday": ["Idli", "Rajma Rice", "Roti Veg"],
        "Saturday": ["Daliya", "Roti Dal", "Soup"],
        "Sunday": ["Light + Cheat Meal", "Light Lunch", "Salad"]
    }

    return render_template("plan.html",
        workout_plan=workout_plan,
        diet_plan=diet_plan
    )


if __name__ == "__main__":
    app.run(debug=True)
