from flask import Flask, render_template, request

app = Flask(__name__)

# 🔹 HOME PAGE
from flask import Flask, render_template, request

@app.route('/', methods=['GET', 'HEAD'])
def index():
    if request.method == 'HEAD':
        return '', 200   # ✅ empty response for health check
    return render_template("index.html")
    


# 🔹 STEP 1: CALCULATE BMI, BMR, TDEE
@app.route('/calculate', methods=['POST'])
def calculate():

    name = request.form.get('name')
    weight = float(request.form.get('weight'))
    height = float(request.form.get('height'))
    age = int(request.form.get('age'))
    gender = request.form.get('gender')
    activity = request.form.get('activity')

    # 🔹 BMI
    bmi = weight / ((height / 100) ** 2)

    # 🔹 CATEGORY
    if bmi < 18.5:
        category = "Underweight"
        diet_advice = "Increase calorie intake and eat nutritious food."
    elif bmi < 25:
        category = "Normal"
        diet_advice = "Maintain your current lifestyle."
    elif bmi < 30:
        category = "Overweight"
        diet_advice = "Exercise regularly and control your diet."
    else:
        category = "Obese"
        diet_advice = "Consult a doctor and follow a strict diet."

    # 🔹 BMR
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    # 🔹 TDEE
    if activity == "sedentary":
        tdee = bmr * 1.2
    elif activity == "light":
        tdee = bmr * 1.375
    elif activity == "moderate":
        tdee = bmr * 1.55
    elif activity == "active":
        tdee = bmr * 1.725
    else:
        tdee = bmr * 1.9

    # 🔥 HEALTH RANGE
    min_weight = 18.5 * ((height / 100) ** 2)
    max_weight = 24.9 * ((height / 100) ** 2)

    if weight > max_weight:
        diff = weight - max_weight
        goal_msg = f"Lose {round(diff,1)} kg to reach healthy range"
    elif weight < min_weight:
        diff = min_weight - weight
        goal_msg = f"Gain {round(diff,1)} kg to reach healthy range"
    else:
        goal_msg = "You are already in healthy range"

    return render_template(
        "result.html",
        name=name,
        bmi=round(bmi, 2),
        category=category,
        bmr=round(bmr, 2),
        tdee=round(tdee, 2),
        diet_advice=diet_advice,
        weight=weight,
        min_weight=round(min_weight, 1),
        max_weight=round(max_weight, 1),
        goal_msg=goal_msg
    )


# 🔹 STEP 2: GOAL BASED PLAN
@app.route('/goal', methods=['POST'])
def goal():

    weight = float(request.form.get('weight'))
    tdee = float(request.form.get('tdee'))

    # ✅ SAFE INPUT HANDLING
    goal_weight = request.form.get('goal_weight')
    duration = request.form.get('duration')

    if goal_weight is None or duration is None:
        return "Error: Missing input"

    goal_weight = float(goal_weight)
    duration = int(duration)

    # 🔥 CALCULATIONS
    weight_diff = weight - goal_weight
    total_calorie_change = weight_diff * 7700
    daily_deficit = total_calorie_change / (duration * 7)

    calories = tdee - daily_deficit

    # 🔥 MACROS
    protein = goal_weight * 1.5
    carbs = (calories * 0.4) / 4
    fat = (calories * 0.3) / 9

    # 🔥 EXERCISE PLAN (AI BASED)
    if duration <= 4:
        exercise = "High Intensity (5-6 days/week)"
    elif duration <= 8:
        exercise = "Moderate + Cardio (4-5 days/week)"
    else:
        exercise = "Light + Consistent (3-4 days/week)"

    return render_template(
        "goal.html",
        calories=round(calories, 2),
        protein=round(protein, 2),
        carbs=round(carbs, 2),
        fat=round(fat, 2),
        exercise=exercise
    )


# 🔹 STEP 3: WEEKLY DIET PAGE
@app.route('/diet')
def diet():

    tdee = request.args.get('tdee')

    if tdee is None:
        tdee = 2000
    else:
        tdee = float(tdee)

    return render_template("diet.html", tdee=round(tdee, 2))


# 🔹 RUN APP
if __name__ == "__main__":
    app.run(debug=True)