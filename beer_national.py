import cherrypy
import os, os.path
import string
import json
import psycopg2

conn = psycopg2.connect("dbname=samsam  user=samsam")
cur=conn.cursor()
    
class StringGenerator(object):
    @cherrypy.expose
    @cherrypy.tools.json_in() 
    def users(self, typ=""):
        users = cherrypy.request.json
        print(cherrypy.request.json)
        try: 
            print(typ)
        except:
            print("What typ?")    
        if typ=="signUp":
            try:
                cur.execute("INSERT INTO user_sign_up (username_signup, email_signup, password_signup, re_password_signup) VALUES (%s,%s,%s,%s)",(users['username_signup'],users['email_signup'],users['password_signup'],users['re_password_signup']))
                cur.execute("SELECT * FROM user_sign_up WHERE username_signup="+users['username_signup']+ "OR email_signup="+users['email_signup'])
                conn.commit()
                if cur.fetchone()=="":
                    print("new user")
                else:
                    print("user already exists")   
                print(cur.fetchall())
            except (RuntimeError, TypeError, NameError):
                print("Error in inserting sign up data")
        elif typ=="signIn":        
            try:
                cur.execute("INSERT INTO sign_in (username_login, email_login, password_login) VALUES (%s,%s,%s)",(users['username_login'],users['email_login'],users['password_login']))
                conn.commit()
                cur.execute("SELECT * FROM sign_in")
                print(cur.fetchall())
            except (RuntimeError, TypeError, NameError):
                print("Error in inserting sign in data")
        else:
            print('Something with wrong with the signUp/sigIn')
    
    #@cherrypy.expose
    #@cherrypy.tools.json_in() 
    #def sign_up(self, urlParam1=None):
     #   json_sign_up = cherrypy.request.json
      #  print(cherrypy.request.json)
       # try:
        #    cur.execute("INSERT INTO user_sign_up (username_signup, email_signup, password_signup, re_password_signup) VALUES (%s,%s,%s,%s)",(json_sign_up['username_signup'],json_sign_up['email_signup'],json_sign_up['password_signup'],json_sign_up['re_password_signup']))
         #   conn.commit()
          #  cur.execute("SELECT * FROM user_sign_up")
           # print(cur.fetchall())
    #    except:
     #       print("Error in inserting sign up data")

    #@cherrypy.expose
    #@cherrypy.tools.json_out()
    #def user_profile(self, urlParam1=None):
    

    #@cherrypy.expose
    #@cherrypy.tools.json_in()
    #@cherrypy.tools.json_out()
    #def rank(self, urlParam1=None):
        #try:
            #cur.execute("SELECT * FROM breweries limit 20")
            #print(cur.fetchall())
            #data = cur.fetchall()
            #print(data)
            #obj=[]
            #for i in data:
            #	obj.append({"longitude":i[0], "latitude": i[1],"name":i[2]})
            #print(json.dumps(obj))
            #return json.dumps(obj)
        #except:
            #print("Error with GET")
            #conn.rollback()

    @cherrypy.expose
    @cherrypy.tools.json_in()
    @cherrypy.tools.json_out()
    def get_data(self,param=""):
        print(param)
        print(cherrypy.session.id)
        try:
            #param = cherrypy.request.json
            print(param)
            if param== "":
                cur.execute("SELECT * FROM breweries limit 15;")
            elif param=='sort_up':
                cur.execute("SELECT * FROM breweries ORDER BY name ASC limit 15;")
            elif param=='sort_down':
                cur.execute("SELECT * FROM breweries ORDER BY name DESC limit 15;")
            elif param=='next':
                cur.execute("SELECT * FROM breweries limit 15;")
            else:
                cur.execute("SELECT * FROM breweries limit 15;")
            data = cur.fetchall()
            print(data)
            obj=[]
            for i in data:
                obj.append({"longitude":i[0], "latitude": i[1],"name":i[2]})
            print(json.dumps(obj))
            return json.dumps(obj)
        except:
            cur.execute("SELECT * FROM breweries limit 15")
            #print(cur.fetchall())
            data = cur.fetchall()
            print(data)
            obj=[]
            for i in data:
                obj.append({"longitude":i[0], "latitude": i[1],"name":i[2]})
            print(json.dumps(obj))
            return json.dumps(obj)

            #print("Error with GET")
            #conn.rollback()

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
    
    @cherrypy.expose
    def profile(self):
        return open('profile.html')
    
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
        conn.rollback()

def setup_database():
    try:
        cur.execute("CREATE TABLE sign_in (username_login varchar(255), email_login varchar(255), password_login varchar(255))")
        cur.execute("CREATE TABLE user_sign_up (username_signup varchar(255), email_signup varchar(255), password_signup varchar(255), re_password_signup varchar(255))")
        conn.commit()
        
    except:
        print("Error in creating tables")
        conn.rollback()

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
