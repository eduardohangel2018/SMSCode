import os


DEBUG = True
SECRET_KEY = 'secret$'

# Conexão e Apontamento do banco
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///code.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
