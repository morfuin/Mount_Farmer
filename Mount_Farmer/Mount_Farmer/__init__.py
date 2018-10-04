"""
The flask application package.
"""

from flask import Flask
app = Flask(__name__)
app.config.from_object('config_cosmos_db')

import Mount_Farmer.views
