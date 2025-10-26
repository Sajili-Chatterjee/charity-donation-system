import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, jsonify
from config import Config
from models.models import db, Donor, Charity, Campaign, Donation, FundsDistribution
import google.generativeai as genai
from sqlalchemy import text

load_dotenv()

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.before_request
def enable_foreign_keys():
    try:
        db.session.execute(text('PRAGMA foreign_keys=ON'))
    except Exception as e:
        print("Foreign key pragma failed:", e)

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('message', '')
    if not user_input:
        return jsonify({'reply': 'Please enter a question.'})
    try:
        context = "Website data:\n"
        for c in Campaign.query.all():
            context += f"Campaign: {c.name}, Goal: ₹{c.goal_amount}, Raised: ₹{c.raised_amount}\n"
        for d in Donation.query.all():
            donor = Donor.query.get(d.donor_id)
            if donor:
                context += f"Donor: {donor.name}, Amount: ₹{d.amount}\n"
        prompt = f"{context}\nUser question: {user_input}"
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        reply = getattr(response, "text", "I'm here to help, but I didn’t get a valid response.")
    except Exception as e:
        print("Gemini API Error:", e)
        reply = "Sorry, I couldn't process your request right now."
    return jsonify({'reply': reply})

@app.route('/')
def home():
    return render_template("index.html")

@app.route("/campaigns")
def campaigns_page():
    campaigns = Campaign.query.all()
    return render_template("campaigns.html", campaigns=campaigns)

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/chatbot_page')
def chatbot_page():
    return render_template('chatbot.html')

@app.route('/donate/<int:id>', methods=["GET", "POST"])
def donate(id):
    campaign = Campaign.query.get_or_404(id)
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        contact = request.form["contact"]
        payment_mode = request.form["payment"]
        amount = float(request.form["amount"])
        # Add your DB update logic here
        return redirect(url_for("thankyou"))
    return render_template("donate.html", campaign=campaign)

@app.route('/thankyou')
def thankyou():
    return render_template('thankyou.html')

# Vercel will expose the app object for serverless execution
app = app
