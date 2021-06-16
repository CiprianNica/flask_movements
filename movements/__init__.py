from weakref import ProxyTypes
from flask import Flask

app = Flask(__name__)

from movements import views
