from flask import Flask
from flask_restful import Resource, Api
from resources.weather import Weather
from resources.weathers import Weathers

app = Flask(__name__)
api = Api(app)

# restful中所有的路由都应该是名词
api.add_resource(Weather, '/weather')
api.add_resource(Weathers, '/weathers')

if __name__ == '__main__':
    app.run(debug=True, port=2379)
