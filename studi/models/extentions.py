from studi import app
from flask_sqlalchemy import SQLAlchemy

# if set to True(default) Falst-SQLAlchemy will track modifications of object and emit signals.
# This requires extra memory and can be disabled if not needed.
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/studi.db'
db = SQLAlchemy(app)




