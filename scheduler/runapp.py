from app import create_app
from flask.ext.restful import Api

# from scheduler.app import app
def run():
    app = create_app()

    api = Api(app)

    app.run(debug=True)

if __name__ == '__main__':
    run()