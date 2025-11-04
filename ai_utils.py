import random

def generate_health_summary(patient):
    tips = [
        "Maintain regular exercise to improve heart health.",
        "Drink enough water and maintain a balanced diet.",
        "Avoid stress and get 7–8 hours of sleep.",
        "Monitor your blood pressure regularly.",
        "Schedule follow-up visits as recommended."
    ]

    condition_advice = {
        "diabetes": "Maintain stable blood sugar levels by avoiding excess sugars.",
        "hypertension": "Reduce salt intake and monitor your BP daily.",
        "asthma": "Keep your inhaler nearby and avoid dusty environments.",
        "anemia": "Eat foods rich in iron like spinach and red meat."
    }

    condition_key = patient.condition.lower()
    condition_message = condition_advice.get(condition_key, "Maintain a healthy lifestyle and visit your doctor regularly.")

    tip = random.choice(tips)
    return f"AI Summary for {patient.name}: {condition_message} Also, {tip}"
