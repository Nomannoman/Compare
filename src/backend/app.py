from __init__ import create_app
from flask_cors import CORS
from flask_script import Manager,Server

app = create_app()
CORS(app)
manager = Manager(app)
manager.add_command('runserver',Server(host="127.0.0.1",port = 8084))

manager.run()
