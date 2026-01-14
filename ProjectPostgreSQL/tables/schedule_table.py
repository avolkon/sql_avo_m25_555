from dbtable import *

class ScheduleTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "schedule"
    
    def columns(self):
        return {
            "id": ["serial", "PRIMARY KEY"],
            "cinema_id": ["integer", "NOT NULL", "REFERENCES cinema(id) ON DELETE CASCADE"],
            "hall": ["varchar(50)", "NOT NULL"],
            "start_datetime": ["timestamp", "NOT NULL"],
            "movie_id": ["integer", "NOT NULL", "REFERENCES movie(id) ON DELETE CASCADE"],
            "ticket_zone": ["varchar(50)", "DEFAULT 'standard'"],
            "ticket_price": ["decimal(8,2)", "CHECK (ticket_price >= 0)"]
        }
    
    def primary_key(self):
        return ['id']
    
    def table_constraints(self):
        return []
    
    def all_by_cinema_id(self, cinema_id):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE cinema_id = %s"
        sql += " ORDER BY start_datetime"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (cinema_id,))
        return cur.fetchall()
    
    def all_by_movie_id(self, movie_id):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE movie_id = %s"
        sql += " ORDER BY start_datetime"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (movie_id,))
        return cur.fetchall()