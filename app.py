import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_bio_health_key'
DB_NAME = 'database.db'

# --- Database Initialization ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    
    # Create tables
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT)''')
                    
    c.execute('''CREATE TABLE IF NOT EXISTS admin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE,
                    password TEXT)''')
                    
    c.execute('''CREATE TABLE IF NOT EXISTS health_checks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    check_type TEXT,
                    result_data TEXT,
                    advice TEXT,
                    timestamp DATETIME)''')
                    
    c.execute('''CREATE TABLE IF NOT EXISTS disease_rules (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    disease_name TEXT,
                    symptoms TEXT,
                    precautions TEXT)''')
                    
    c.execute('''CREATE TABLE IF NOT EXISTS first_aid (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    emergency_type TEXT,
                    steps TEXT)''')
                    
    c.execute('''CREATE TABLE IF NOT EXISTS health_tips (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tip TEXT)''')

    # Insert default admin
    c.execute("SELECT * FROM admin WHERE username='admin'")
    if not c.fetchone():
        c.execute("INSERT INTO admin (username, password) VALUES ('admin', 'admin123')")

    # Insert default sample data for disease rules
    c.execute("SELECT count(*) FROM disease_rules")
    if c.fetchone()[0] == 0:
        diseases = [
            ("Cold", "Cough, Sneezing, Sore Throat", "Rest, drink warm fluids, take Vitamin C."),
            ("Fever", "High Temperature, Chills, Body Ache", "Stay hydrated, take paracetamol, rest."),
            ("Flu", "Fever, Cough, Fatigue, Muscle Aches", "Complete rest, antiviral medications if prescribed, fluids."),
            ("Allergy", "Sneezing, Runny Nose, Itchy Eyes", "Avoid allergens, take antihistamines."),
            ("Dehydration", "Dry Mouth, Extreme Thirst, Dark Urine", "Drink plenty of water and electrolytes."),
            ("Food Poisoning", "Nausea, Vomiting, Diarrhea, Stomach Cramps", "Stay hydrated, eat bland foods, avoid dairy.")
        ]
        c.executemany("INSERT INTO disease_rules (disease_name, symptoms, precautions) VALUES (?, ?, ?)", diseases)

    # Insert default sample data for first aid
    c.execute("SELECT count(*) FROM first_aid")
    if c.fetchone()[0] == 0:
        first_aids = [
            ("burns", "1. Cool the burn under running water for 10 mins. 2. Cover with a sterile, non-fluffy dressing. 3. Do not apply ice or ointments."),
            ("cuts", "1. Wash hands. 2. Stop bleeding by applying pressure. 3. Clean the wound with water. 4. Apply a bandage."),
            ("choking", "1. Give 5 back blows between shoulder blades. 2. Give 5 abdominal thrusts (Heimlich maneuver). 3. Call emergency if it doesn't clear."),
            ("fainting", "1. Lay the person flat on their back. 2. Elevate their legs. 3. Loosen tight clothing. 4. Wait for them to recover."),
            ("fracture", "1. Do not move the injured area. 2. Apply a splint if possible to keep it still. 3. Apply ice pack wrapped in cloth. 4. Seek medical help.")
        ]
        c.executemany("INSERT INTO first_aid (emergency_type, steps) VALUES (?, ?)", first_aids)

    conn.commit()
    conn.close()

# Helper to log health checks
def log_health_check(check_type, result_data, advice):
    if 'session_id' not in session:
        session['session_id'] = os.urandom(16).hex()
    
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO health_checks (session_id, check_type, result_data, advice, timestamp) VALUES (?, ?, ?, ?, ?)",
              (session['session_id'], check_type, result_data, advice, datetime.now()))
    conn.commit()
    conn.close()

# --- Routes ---

@app.route('/')
def index():
    return render_template('dashboard.html')

@app.route('/bmi', methods=['GET', 'POST'])
def bmi():
    if request.method == 'POST':
        try:
            height_cm = float(request.form['height'])
            weight_kg = float(request.form['weight'])
            height_m = height_cm / 100
            bmi_val = round(weight_kg / (height_m * height_m), 2)
            
            if bmi_val < 18.5:
                category = "Underweight"
                advice = "You should eat more nutrient-rich foods to gain weight healthily."
            elif 18.5 <= bmi_val < 24.9:
                category = "Normal"
                advice = "Great! Maintain your healthy lifestyle and balanced diet."
            elif 25 <= bmi_val < 29.9:
                category = "Overweight"
                advice = "Consider a calorie deficit diet and regular exercise to reduce weight."
            else:
                category = "Obese"
                advice = "Please consult a healthcare provider for a structured weight loss plan."
                
            result_str = f"BMI: {bmi_val} - {category}"
            log_health_check("BMI", result_str, advice)
            
            return render_template('result.html', title="BMI Result", result=result_str, advice=advice, back_url=url_for('bmi'))
        except ValueError:
            flash("Invalid input. Please enter numbers.")
            
    return render_template('bmi.html')

@app.route('/disease', methods=['GET', 'POST'])
def disease():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT disease_name, symptoms, precautions FROM disease_rules")
    rules = c.fetchall()
    conn.close()
    
    # Extract unique symptoms for the form
    all_symptoms = set()
    for row in rules:
        symps = [s.strip() for s in row[1].split(',')]
        all_symptoms.update(symps)
        
    if request.method == 'POST':
        user_symptoms = request.form.getlist('symptoms')
        
        if not user_symptoms:
            flash("Please select at least one symptom.")
            return render_template('disease.html', symptoms=sorted(all_symptoms))
            
        best_match = None
        max_score = 0
        
        for row in rules:
            disease_name = row[0]
            rule_symptoms = [s.strip() for s in row[1].split(',')]
            precautions = row[2]
            
            score = len(set(user_symptoms).intersection(set(rule_symptoms)))
            if score > max_score:
                max_score = score
                best_match = (disease_name, precautions)
                
        if best_match and max_score > 0:
            result_str = f"Predicted Disease: {best_match[0]} (Matched {max_score} symptoms)"
            advice = f"Precautions: {best_match[1]}"
        else:
            result_str = "No specific disease matched."
            advice = "Please consult a doctor if symptoms persist."
            
        log_health_check("Disease Prediction", result_str, advice)
        return render_template('result.html', title="Disease Prediction Result", result=result_str, advice=advice, back_url=url_for('disease'))

    return render_template('disease.html', symptoms=sorted(all_symptoms))

@app.route('/bp', methods=['GET', 'POST'])
def bp():
    if request.method == 'POST':
        try:
            sys = int(request.form['systolic'])
            dia = int(request.form['diastolic'])
            
            if sys < 90 and dia < 60:
                category = "Low BP (Hypotension)"
                advice = "Increase fluid and salt intake. Stand up slowly."
            elif sys <= 120 and dia <= 80:
                category = "Normal BP"
                advice = "Your blood pressure is in a healthy range. Keep it up!"
            elif 120 < sys <= 129 and dia <= 80:
                category = "Elevated BP"
                advice = "Adopt a healthier lifestyle to prevent hypertension."
            elif 130 <= sys <= 139 or 80 < dia <= 89:
                category = "High BP (Hypertension Stage 1)"
                advice = "Reduce sodium intake, exercise regularly, and consult a doctor."
            elif sys >= 140 or dia >= 90:
                category = "High BP (Hypertension Stage 2)"
                advice = "Immediate medical consultation is recommended."
            else:
                category = "Unusual Reading"
                advice = "Please check again or consult a doctor."
                
            result_str = f"Blood Pressure: {sys}/{dia} mmHg - {category}"
            log_health_check("Blood Pressure", result_str, advice)
            return render_template('result.html', title="BP Result", result=result_str, advice=advice, back_url=url_for('bp'))
        except ValueError:
            flash("Invalid input. Please enter numbers.")
            
    return render_template('bp.html')

@app.route('/diabetes', methods=['GET', 'POST'])
def diabetes():
    if request.method == 'POST':
        try:
            age = int(request.form['age'])
            bmi = float(request.form['bmi'])
            fasting_sugar = float(request.form['sugar'])
            family_history = request.form['family'] == 'yes'
            activity = request.form['activity'] == 'low'
            
            risk_score = 0
            if age > 45: risk_score += 2
            elif age > 30: risk_score += 1
            
            if bmi > 25: risk_score += 2
            if fasting_sugar > 100: risk_score += 3
            if fasting_sugar > 125: risk_score += 5
            if family_history: risk_score += 2
            if activity: risk_score += 1
            
            if risk_score <= 3:
                category = "Low Risk"
                advice = "Keep maintaining a healthy diet and lifestyle."
            elif risk_score <= 6:
                category = "Medium Risk"
                advice = "Consider increasing physical activity and reducing sugar intake."
            else:
                category = "High Risk"
                advice = "Please consult a healthcare professional for a proper diabetes test."
                
            result_str = f"Diabetes Risk: {category}"
            log_health_check("Diabetes Risk", result_str, advice)
            return render_template('result.html', title="Diabetes Result", result=result_str, advice=advice, back_url=url_for('diabetes'))
            
        except ValueError:
            flash("Invalid input.")
            
    return render_template('diabetes.html')

@app.route('/nutrition', methods=['GET', 'POST'])
def nutrition():
    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            goal = request.form['goal']
            activity = request.form['activity']
            
            # Rule based protein calculation (g per kg)
            multiplier = 0.8 # default sedentary
            if activity == 'moderate': multiplier = 1.2
            elif activity == 'high': multiplier = 1.6
            
            if goal == 'muscle': multiplier += 0.4
            elif goal == 'loss': multiplier += 0.2
            
            protein = round(weight * multiplier, 2)
            
            result_str = f"Estimated Daily Protein: {protein} grams"
            advice = f"Based on your weight ({weight}kg), activity level, and goal. Ensure you also balance your macros with carbs and healthy fats."
            
            log_health_check("Nutrition Calculator", result_str, advice)
            return render_template('result.html', title="Nutrition Result", result=result_str, advice=advice, back_url=url_for('nutrition'))
            
        except ValueError:
            flash("Invalid input.")
            
    return render_template('nutrition.html')

@app.route('/water', methods=['GET', 'POST'])
def water():
    if request.method == 'POST':
        try:
            ph = float(request.form['ph'])
            tds = float(request.form['tds'])
            turbidity = float(request.form['turbidity'])
            
            status = "Safe"
            reasons = []
            
            if not (6.5 <= ph <= 8.5):
                status = "Unsafe"
                reasons.append("pH is outside safe range (6.5 - 8.5).")
            if tds > 500:
                if tds > 1000:
                    status = "Unsafe"
                elif status != "Unsafe":
                    status = "Suspicious"
                reasons.append("TDS is high (Safe < 500 mg/L).")
            if turbidity > 5:
                status = "Unsafe"
                reasons.append("Turbidity is high (Safe < 5 NTU).")
                
            if status == "Safe":
                advice = "The water quality meets basic safe parameters."
            else:
                advice = " ".join(reasons) + " Avoid drinking without purification."
                
            result_str = f"Water Quality: {status}"
            log_health_check("Water Quality", result_str, advice)
            return render_template('result.html', title="Water Quality Result", result=result_str, advice=advice, back_url=url_for('water'))
            
        except ValueError:
            flash("Invalid input.")
            
    return render_template('water.html')

@app.route('/firstaid', methods=['GET', 'POST'])
def firstaid():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT emergency_type FROM first_aid")
    emergencies = [row[0] for row in c.fetchall()]
    conn.close()
    
    if request.method == 'POST':
        etype = request.form['emergency']
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT steps FROM first_aid WHERE emergency_type=?", (etype,))
        res = c.fetchone()
        conn.close()
        
        if res:
            result_str = f"First Aid for: {etype.capitalize()}"
            advice = res[0]
            return render_template('result.html', title="First Aid Guide", result=result_str, advice=advice, back_url=url_for('firstaid'))
            
    return render_template('firstaid.html', emergencies=emergencies)

@app.route('/report')
def report():
    session_id = session.get('session_id')
    checks = []
    if session_id:
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT check_type, result_data, advice, timestamp FROM health_checks WHERE session_id=? ORDER BY timestamp DESC", (session_id,))
        checks = c.fetchall()
        conn.close()
        
    return render_template('report.html', checks=checks)

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = sqlite3.connect(DB_NAME)
        c = conn.cursor()
        c.execute("SELECT * FROM admin WHERE username=? AND password=?", (username, password))
        admin = c.fetchone()
        conn.close()
        
        if admin:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            flash("Invalid Credentials")
            
    return render_template('admin_login.html')

@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

@app.route('/admin_dashboard')
def admin_dashboard():
    if not session.get('admin_logged_in'):
        return redirect(url_for('admin_login'))
        
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT * FROM health_checks ORDER BY timestamp DESC")
    all_checks = c.fetchall()
    
    c.execute("SELECT * FROM disease_rules")
    rules = c.fetchall()
    
    c.execute("SELECT * FROM first_aid")
    first_aids = c.fetchall()
    
    conn.close()
    
    return render_template('admin_dashboard.html', checks=all_checks, rules=rules, first_aids=first_aids)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
