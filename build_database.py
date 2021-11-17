import os
from datetime import datetime
from config import db

# Create the database
db.create_all()
db.session.commit()