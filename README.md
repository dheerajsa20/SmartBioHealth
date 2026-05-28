# Smart Bio-Health Monitoring and Advisory System

## 1. Project Introduction
The **Smart Bio-Health Monitoring and Advisory System** is a comprehensive, web-based platform designed to assist users in assessing their basic health conditions using simple rule-based AI logic. It provides various modules for health analysis, such as BMI calculation, disease prediction, blood pressure analysis, diabetes risk checking, and water quality checking.

## 2. Features
- **BMI Calculator**: Determines body mass index and provides health advice.
- **Disease Prediction System**: Uses rule-based logic to predict common diseases from symptoms.
- **Blood Pressure Analyzer**: Classifies BP and provides safety advice.
- **Diabetes Risk Checker**: Assesses risk levels based on age, weight, and lifestyle factors.
- **Nutrition Calculator**: Estimates daily protein requirements.
- **Water Quality Checker**: Evaluates water safety based on pH, TDS, and turbidity.
- **First Aid Guide**: Quick lookup for common medical emergencies.
- **Health Report**: Tracks and summarizes past health checks.
- **Admin Dashboard**: Allows administrators to manage system rules, view user histories, and update tips.

## 3. How to Install
1. Ensure Python 3.x is installed on your system.
2. Clone or extract this repository into a folder.
3. Open a terminal or command prompt in the project folder.
4. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```
5. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## 4. How to Run
1. Run the Flask application:
   ```bash
   python app.py
   ```
2. The system will automatically create and initialize the database on the first run.
3. Open your browser and go to: **http://127.0.0.1:5000**

## 5. Admin Login Details
- **URL**: http://127.0.0.1:5000/admin_login
- **Username**: `admin`
- **Password**: `admin123`

---

