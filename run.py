from app import create_app
import os

app = create_app()
app.secret_key = os.environ.get('SECRET_KEY', 'dev-change-me')

if __name__ == '__main__':
    app.run(debug=True)