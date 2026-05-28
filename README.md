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

# Mini Project Report

## Abstract
The rapid advancement of technology has enabled innovative solutions in healthcare. This project presents a "Smart Bio-Health Monitoring and Advisory System" developed using Python and Flask. It serves as an interactive platform for basic health assessments, utilizing rule-based AI logic to evaluate user inputs like BMI, symptoms, and blood pressure. The system provides immediate, actionable health advice and maintains a history of user interactions.

## Introduction
Monitoring personal health is crucial for early detection and prevention of diseases. However, accessing quick health advice can sometimes be challenging. This system bridges the gap by offering a user-friendly web application where individuals can self-assess common health metrics and receive instant feedback, promoting better lifestyle choices and prompt medical attention when necessary.

## Problem Statement
Many individuals lack easy access to preliminary health assessments and basic health awareness. Often, people ignore minor symptoms or abnormal health metrics (like slight changes in blood pressure or BMI) due to the inconvenience of visiting a clinic for minor concerns. There is a need for a readily available, easy-to-use tool that can provide initial health advice and risk assessment.

## Objectives
- To develop a web-based health monitoring application.
- To implement simple rule-based AI logic for preliminary disease prediction and risk assessment.
- To provide tools for BMI, Blood Pressure, Diabetes Risk, and Water Quality analysis.
- To offer a quick-reference First Aid guide.
- To allow users to generate and track their health reports.
- To provide an administrative interface for managing health rules and viewing records.

## Existing System
Currently, individuals rely on disparate mobile applications or search engines for health advice. These solutions are often fragmented, ad-heavy, or overly complex (utilizing advanced machine learning models requiring vast data). Many existing systems do not offer a unified dashboard combining multiple health tools into a single, cohesive educational platform.

## Proposed System
The proposed system is a unified web application that integrates multiple health calculators and advisors into a single dashboard. It uses straightforward rule-based logic (if-else conditions) to provide transparent and explainable health advice. Built with Flask and SQLite, it is lightweight, easy to deploy, and suitable for educational demonstrations.

## System Architecture
The application follows a standard Client-Server architecture:
- **Frontend (Client)**: HTML, CSS, JavaScript. Responsible for presenting the UI, collecting user inputs, and displaying results.
- **Backend (Server)**: Python Flask. Handles routing, processes form data, executes the rule-based logic, and interacts with the database.
- **Database**: SQLite. Stores health checks, disease rules, first aid instructions, and user session data.

## Modules
1. **Dashboard**: The main entry point with navigation to all tools.
2. **BMI Calculator**: Calculates Body Mass Index and categorizes it.
3. **Disease Predictor**: Matches user-selected symptoms to predefined disease rules.
4. **Blood Pressure Analyzer**: Evaluates systolic and diastolic pressure.
5. **Diabetes Risk Checker**: Calculates a risk score based on demographic and lifestyle factors.
6. **Nutrition Calculator**: Determines protein needs based on activity levels.
7. **Water Quality Checker**: Evaluates drinking water safety.
8. **First Aid Guide**: Retrieves instructions for specific emergencies.
9. **Health Report Generator**: Displays a log of the user's assessments.
10. **Admin Module**: Dashboard for system management and record viewing.

## Algorithm (Rule-Based AI Logic Example)
For Disease Prediction:
1. Input: List of symptoms selected by the user.
2. Process: For each disease in the database, compare the user's symptoms with the disease's known symptoms.
3. Calculate a match score (e.g., number of matching symptoms).
4. Output: The disease with the highest match score is predicted, along with associated precautions.

## Advantages
- Easy to use with a clean, responsive interface.
- Lightweight and fast due to the absence of heavy frameworks.
- Transparent decision-making (rule-based logic is easy to explain).
- All-in-one platform for basic health queries.
- Persists data allowing users to track their history.

## Applications
- Personal health tracking and self-assessment.
- Educational tool for students studying Biology for Engineers.
- Preliminary screening tool for general health awareness.

## Conclusion
The Smart Bio-Health Monitoring and Advisory System successfully demonstrates how simple web technologies and rule-based logic can be combined to create a valuable healthcare utility. It provides users with immediate, understandable health feedback, fostering better health awareness and proactive personal care.
