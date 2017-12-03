import cherrypy
import os
import os.path
import string
import json
import psycopg2
import hashlib

conn = psycopg2.connect("dbname=samsam  user=samsam")
cur = conn.cursor()
conn.autocommit = True


class StringGenerator(object):
    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def users(self, typ=""):
        users = cherrypy.request.json
        print(cherrypy.request.json)
        try:
            print(typ)
        except:
            print("What typ?")
        if typ == "signUp":
            cur.execute("(SELECT * FROM users_table WHERE username= %s OR email= %s)",
                        (str(users['username']), str(users['email'])))
            if cur.fetchone() == None:
                print("new user")
                cur.execute("INSERT INTO users_table (username, email, passwrd) VALUES (%s,%s,%s)",
                    (users['username'], users['email'], hashlib.md5((users['passwrd']).encode('utf-8')).hexdigest()))
                newUser = json.dumps({'username': users['username']})
                print(newUser)
                return [newUser]
            else:
                return json.dumps({'error': "User_already_exists"})
        elif typ == "signIn":
            cur.execute("SELECT username, likes_hop, likes_dark, no_like, likes_weird, likes_funky, likes_every FROM users_table WHERE username= %s AND passwrd= %s",
                        (users['username'], hashlib.md5((users['passwrd']).encode('utf-8')).hexdigest()))
            user_data = cur.fetchall()
            if user_data == []:
                noUser = json.dumps({'error': "no_username"})
                print("You don't exist", noUser)
                return [noUser]
            else:
                print(user_data)
                user_data_json = json.dumps({
                    "username": user_data[0],
                    "likes_hop": user_data[1],
                    "likes_dark": user_data[2],
                    "no_like": user_data[3],
                    "likes_weird": user_data[4],
                    "likes_funky": user_data[5],
                    "likes_every": user_data[6]
                })
                print(user_data_json)
                print("You exist!")
                return [user_data_json]
        else:
            print('Something with wrong with the signUp/sigIn')

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def get_data(self, param=""):
        print(cherrypy.session.id)
        n = 15
        try:
            print(param)
            if param == "":
                cur.execute("SELECT * FROM breweries limit 15;")
            elif param == 'sort_up':
                cur.execute(
                    "SELECT * FROM breweries ORDER BY name ASC limit 15;")
            elif param == 'sort_down':
                cur.execute(
                    "SELECT * FROM breweries ORDER BY name DESC limit 15;")
            elif param == 'next':
                n += 15
                cur.execute("SELECT * FROM breweries limit n;")
            else:
                cur.execute("SELECT * FROM breweries limit 15;")
            data = cur.fetchall()
            print(data)
        except:
            cur.execute("SELECT * FROM breweries limit 15")
            data = cur.fetchall()
            print(data)
        obj = []
        for i in data:
            obj.append({
                "longitude": i[0],
                "latitude": i[1],
                "name": i[2]
            })
        print(json.dumps(obj))
        return json.dumps(obj)

    @cherrypy.expose
    def index(self):
        return open('index.html')

    @cherrypy.expose
    def breweries_list(self):
        return open('breweries_list.html')

    @cherrypy.expose
    def join(self):
        return open('join.html')

    @cherrypy.expose
    def profile(self):
        return open('profile.html')


def cleanup_database():
    """
    Destroy the `user_string` table from the database
    on server shutdown.
    """
    try:
        cur.execute("DROP TABLE users_table")
    except:
        print("Error in dropping tables")


def setup_database():
    try:
        cur.execute("CREATE TABLE users_table (username varchar(255), email varchar(255), passwrd varchar(255), likes_hop BOOLEAN, likes_dark BOOLEAN, likes_funky BOOLEAN, likes_weird BOOLEAN, no_like BOOLEAN, likes_every BOOLEAN)")

    except:
        print("Error in creating tables")


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080,
                            'server.shutdown_timeout': 1
                            })
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    cherrypy.engine.subscribe('start', setup_database)
    cherrypy.engine.subscribe('stop', cleanup_database)
    cherrypy.quickstart(StringGenerator(), '/', conf)
