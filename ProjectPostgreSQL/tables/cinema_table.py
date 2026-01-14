from dbtable import *

class CinemaTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "cinema"
    
    def columns(self):
        return {
            "id": ["serial", "PRIMARY KEY"],
            "name": ["varchar(100)", "NOT NULL"],
            "address": ["varchar(255)", "NOT NULL"]
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
    
    def find_by_id(self, cinema_id):
        sql = "SELECT * FROM " + self.table_name() + " WHERE id = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (cinema_id,))
        return cur.fetchone()
    
    def delete_by_id(self, cinema_id):
        sql = "DELETE FROM " + self.table_name() + " WHERE id = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (cinema_id,))
        self.dbconn.conn.commit()