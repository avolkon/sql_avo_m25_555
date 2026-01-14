from dbtable import *

class MovieTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "movie"
    
    def columns(self):
        return {
            "id": ["serial", "PRIMARY KEY"],
            "title": ["varchar(255)", "NOT NULL"],
            "genre": ["varchar(100)"],
            "duration": ["integer", "CHECK (duration > 0)"],
            "country": ["varchar(100)"],
            "studio": ["varchar(255)"],
            "min_age": ["integer", "CHECK (min_age >= 0)"]
        }
    
    def primary_key(self):
        return ['id']
    
    def find_by_position(self, num):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY " + ", ".join(self.primary_key())
        sql += " LIMIT 1 OFFSET %(offset)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": num - 1})
        return cur.fetchone()
    
    def find_by_id(self, movie_id):
        sql = "SELECT * FROM " + self.table_name() + " WHERE id = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (movie_id,))
        return cur.fetchone()
    
    def delete_by_id(self, movie_id):
        sql = "DELETE FROM " + self.table_name() + " WHERE id = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (movie_id,))
        self.dbconn.conn.commit()