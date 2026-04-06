from app import create_app
import db


def main():
    app = create_app()
    with app.app_context():
        db.init_db()
        print(f"Initialized database at {app.config['DATABASE']}")


if __name__ == "__main__":
    main()
