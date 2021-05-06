import sys
# sys.path.append("/var/www/physmap/lib")
# sys.path.insert(0, "/var/www/physmap")
from physmap_logger import Logger 
from config import dao_config
import pymysql
import json 

class DAO(object):
    
    def __init__(self):
        self.dao_config = dao_config 
        self.connection = None 
        self.logger = Logger() 

    def connect(self):
        try:
            self.connection = pymysql.connect(
                self.dao_config["host"],
                self.dao_config["user"],
                self.dao_config["pass"],
                self.dao_config["db"]
            )
            return self.connection.cursor(pymysql.cursors.DictCursor)
        except Exception as e:
            self.logger.log(str(e))

    def by_title(self, title, deleted=False):
        cursor = self.connect() 
        query = "select * from surgeons where title = '%s' and deleted = %s" % (title, "1" if deleted else "0")
        print(query)
        cursor.execute(query)
        print("done")
        return cursor.fetchall()

    def update_training(self, _id, training):
        cursor = self.connect() 
        training = self.pymysql_escape(training)
        query = "update surgeons set training = %s where id = {}".format(_id)
        print(query)

        doit = cursor.execute(query, training)
        # self.connection.commit()
        

    def update(self, column, _id, new_value):
        cursor = self.connect() 
        escaped_value = self.pymysql_escape(new_value)
        query = "update surgeons set %s = %s where id = %s" % (column, escaped_value, _id)
        print(query)
        doit = cursor.execute(query)
        self.connection.commit()
        return doit

    def pymysql_escape_dict(self, surgeon_data):
        for key in surgeon_data:
            surgeon_data[key] = self.connection.escape(surgeon_data[key])
        return surgeon_data

    def pymysql_escape(self, data):
        return self.connection.escape(data)

    def get_surgeons(self, latlng=None):
        query = "select * from surgeons"
        cursor = self.connect()
        cursor.execute(query)
        surgeons = cursor.fetchall()
        return surgeons

    def by_name(self, name):
        cursor = self.connect()     
        query = "select * from surgeons where title like '{}'".format('%{0}%'.format(name))
        cursor.execute(query)
        return cursor.fetchall()

    def by_zip(self, zipcode):
        cursor = self.connect() 
        query = "select * from surgeons where zipcode = %s"
        cursor.execute(query, str(zipcode))
        surgeons = cursor.fetchall()
        return surgeons 

    def get_page_content(self, page_name):
        query = "select page_content from pages where page_name = %s"
        cursor = self.connect()
        cursor.execute(query, page_name)
        page_content = cursor.fetchone()
        
        return page_content['page_content'] if page_content else "There doesn't seem to be anything here"

    def get_latlngs(self, title):
        cursor = self.connect() 
        query = "select latlng from surgeons where title = %s"
        cursor.execute(query, title)
        return cursor.fetchall()

    def disconnect(self):
        try:
            self.connection.close()
        except Exception as e:
            print(str(e))
    

    