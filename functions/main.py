import os
from flask import Flask, request
from main import app  # Import your Flask app from the root directory

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
