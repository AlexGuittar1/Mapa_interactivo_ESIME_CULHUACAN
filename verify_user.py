from app import app, db
from models import Usuario

def verify():
    with app.app_context():
        u = Usuario.query.filter_by(boleta="2025350215").first()
        if u:
            print(f"FOUND: {u.to_dict()}")
        else:
            print("NOT FOUND")

if __name__ == "__main__":
    verify()
