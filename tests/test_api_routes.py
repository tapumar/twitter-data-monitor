from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
from flask import jsonify
import os

from app import app,db
from app.api_routes import *
from app.models import Actor
from modules.twitter_user import TwitterUser

app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
db.init_app(app)
# client = app.test_client()

class TestAPIRoutes():

    def setUp():
        print("Rodando setup...\n")
        with app.app_context():
            db.create_all()

    def tearDown():
        print("Rodando tear down...\n")
        db.drop_all()


    def test_api_get_actors(self):
        user = TwitterUser('CNN')
        user = Actor(user.id, user.username, user.name)

        with app.app_context():
            TestAPIRoutes.setUp()
            db.session.add(user)
            db.session.commit()
            response = api_get_actors()
            TestAPIRoutes.tearDown()

        assert '{"actors":["CNN"],"code":"200","length":1,"message":"Success"}\n' == response.get_data().decode()


    def test_api_actors_datetime(self):
        a = ActorReport('01/02/2018', None, None)
        b = ActorReport('02/02/2018', None, None)
        c = ActorReport('02/02/2018', None, None)

        with app.app_context():
            TestAPIRoutes.setUp()
            db.session.add(a)
            db.session.add(b)
            db.session.add(c)
            db.session.commit()
            response = api_get_actors_datetime()
            TestAPIRoutes.tearDown()

        assert '{"code":"200","dates":["01/02/2018","02/02/2018"],"message":"Success"}\n' or '{"code":"200","dates":["02/02/2018","01/02/2018"],"message":"Success"}\n' == response.get_data().decode()

    def test_api_get_actor_account_date_invalid_user(self):

        with app.app_context():
            TestAPIRoutes.setUp()
            response = api_get_actor_account_date('CNN', None)
            TestAPIRoutes.tearDown()

        # assert 1 == response.get_data().decode()
        assert '400' == json.loads(response.get_data().decode())['code']

    def test_api_get_actor_account_date(self):
        csv_content = 'nome;seguidores;tweets;seguindo;curtidas;retweets;favorites;hashtags;mentions\n923257662569148417;1715;146;193;104;0;0;;;\n'
        a = ActorReport('01-01-2018', '12:00', csv_content.encode())
        user = TwitterUser('Renova_BR')
        user = Actor(user.id, user.username, user.name)
        with app.app_context():
            TestAPIRoutes.setUp()
            db.session.add(a)
            db.session.add(user)
            db.session.commit()
            response = api_get_actor_account_date('Renova_BR', '01-01-2018')
            TestAPIRoutes.tearDown()

        assert '{"12:00":{"date":"01-01-2018","followers_count":"193","following_count":"104","likes_count":"0","name":"1715","tweets_count":"0","username":"146"},"code":"200","message":["Success"]}\n' == response.get_data().decode()