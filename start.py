import os
import sys
from app import create_app

# Opret app-instansen
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
