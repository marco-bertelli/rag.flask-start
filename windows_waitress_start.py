from waitress import serve
from app import getFlaskApp

app = getFlaskApp()

print('Starting Waitress server on port 8080...')

serve(app, host='0.0.0.0', port=8080)
