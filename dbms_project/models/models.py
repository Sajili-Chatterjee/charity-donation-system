from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Donor(db.Model):
    __tablename__ = 'donor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(20))
    payment_mode = db.Column(db.String(50))

    donations = db.relationship('Donation', backref='donor', lazy=True)

    def __repr__(self):
        return f"<Donor {self.name} - {self.email}>"

class Charity(db.Model):
    __tablename__ = 'charity'

    id = db.Column(db.Integer, primary_key=True)
    org_name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text)
    proof_docs = db.Column(db.String(255))

    distributions = db.relationship('FundsDistribution', backref='charity', lazy=True)

    def __repr__(self):
        return f"<Charity {self.org_name}>"

class Campaign(db.Model):
    __tablename__ = 'campaign'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    goal_amount = db.Column(db.Float, nullable=False)
    raised_amount = db.Column(db.Float, default=0, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(50))

    donations = db.relationship('Donation', backref='campaign', lazy=True)
    distributions = db.relationship('FundsDistribution', backref='campaign', lazy=True)

    def __repr__(self):
        return f"<Campaign {self.title} - Status {self.status}>"

class Donation(db.Model):
    __tablename__ = 'donation'

    id = db.Column(db.Integer, primary_key=True)
    donor_id = db.Column(db.Integer, db.ForeignKey('donor.id'), nullable=False)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(50))

    def __repr__(self):
        return f"<Donation {self.amount} by Donor {self.donor_id}>"

class FundsDistribution(db.Model):
    __tablename__ = 'funds_distribution'

    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaign.id'), nullable=False)
    charity_id = db.Column(db.Integer, db.ForeignKey('charity.id'), nullable=False)
    amount_distributed = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"<FundsDistribution {self.amount_distributed} to Charity {self.charity_id}>"
