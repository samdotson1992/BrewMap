import cherrypy
import os, os.path
import string
import json
import psycopg2

DB_STRING="dbname='postgres' user='postgres' host='localhost' password='rascal1!'"
conn=psycopg2.connect(DB_STRING)
cur=conn.cursor()

    
class StringGenerator(object):
    @cherrypy.expose
    @cherrypy.tools.json_in() 
    def sign_in(self, urlParam1=None):
        json_sign_in = cherrypy.request.json
        print(cherrypy.request.json)
        try:
            cur.execute("INSERT INTO sign_in (username_login, email_login, password_login) VALUES (%s,%s,%s)",(json_sign_in['username_login'],json_sign_in['email_login'],json_sign_in['password_login']))
            conn.commit()
            return ""
        except:
            print("Error in inserting sign in data")
    
    @cherrypy.expose
    @cherrypy.tools.json_in() 
    def sign_up(self, urlParam1=None):
        json_sign_up = cherrypy.request.json
        print(cherrypy.request.json)
        try:
            cur.execute("INSERT INTO user_sign_up (username_signup, email_signup, password_signup, re_password_signup) VALUES (%s,%s,%s,%s)",(json_sign_up['username_signup'],json_sign_up['email_signup'],json_sign_up['password_signup'],json_sign_up['re_password_signup']))
            conn.commit()
            return ""
        except:
            print("Error in inserting sign up data")
    
    @cherrypy.expose
    def index(self):
        return open('index.html')    

    @cherrypy.expose
    def about(self):
        return open('about.html')
    
    @cherrypy.expose
    def breweries_list(self):
        return open('breweries_list.html')
    
    @cherrypy.expose
    def join(self):
        return open('join.html')
    
    
    

    
def cleanup_database():
    """
    Destroy the `user_string` table from the database
    on server shutdown.
    """
    try:
        cur.execute("DROP TABLE sign_in")
        cur.execute("DROP TABLE user_sign_up")
        conn.commit()
    except:
        print("Error in dropping tables")

def setup_database():
    """
    Create the `user_data` table in the database
    on server startup
    """
    try:
        cur.execute("CREATE TABLE sign_in (ID INTEGER NOT NULL PRIMARY KEY, username_login varchar(255), email_login varchar(255), password_login varchar(255))")
        cur.execute("CREATE TABLE user_sign_up (ID INTEGER NOT NULL PRIMARY KEY, username_signup varchar(255), email_signup varchar(255), password_signup varchar(255), re_password_signup varchar(255))")
        conn.commit()
    except:
        print("Error in creating tables")
        cleanup_database()

if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '127.0.0.2',
                        'server.socket_port': 8000,
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