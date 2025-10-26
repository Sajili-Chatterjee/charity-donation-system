from app import app, db
from models.models import Donor, Charity, Campaign, Donation, FundsDistribution
from sqlalchemy.exc import IntegrityError

def add_sample_data():
    with app.app_context():
        # Optionally drop and recreate tables (WARNING: deletes all data)
        # db.drop_all()
        # db.create_all()

        # Donors data, avoid duplicates by checking before insert
        donors = [
            {'name': 'Sajili Chatterjee', 'email': 'sajili@example.com', 'contact': '9876543210', 'payment_mode': 'UPI'},
            # Add other donors here...
        ]

        for donor_data in donors:
            existing_donor = Donor.query.filter_by(email=donor_data['email']).first()
            if not existing_donor:
                donor = Donor(**donor_data)
                db.session.add(donor)
            else:
                print(f"Donor with email {donor_data['email']} already exists. Skipping insert.")

        # Similarly add Charity, Campaign, Donation, FundsDistribution ensuring no duplicates or handle errors accordingly

        try:
            db.session.commit()
            print("Sample data added successfully.")
        except IntegrityError as e:
            db.session.rollback()
            print(f"Error occurred during commit: {e}")

if __name__ == "__main__":
    add_sample_data()
