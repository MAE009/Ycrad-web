# app.py - Service web adapté pour Render
from flask import Flask, send_from_directory
import os
import sys

app = Flask(__name__)

# Configuration pour éviter les erreurs PyGame en mode web
try:
    import pygame
    PYGAME_AVAILABLE = True
except ImportError:
    PYGAME_AVAILABLE = False
    print("PyGame non disponible, mode minimal activé")

@app.route('/')
def serve_index():
    return send_from_directory('.', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    if path.startswith('assets/'):
        return send_from_directory('.', path)
    return send_from_directory('.', path)

@app.route('/status')
def status():
    return {
        'status': 'online',
        'pygame_available': PYGAME_AVAILABLE,
        'version': '1.0.0'
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port, debug=False)