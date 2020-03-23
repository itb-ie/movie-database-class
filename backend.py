import sqlite3


class Back(object):
    def __init__(self):
        db = sqlite3.connect("movies.db")
        cur = db.cursor()
        # let us create the table
        cur.execute("create table if not exists movies (id integer primary key, title varchar(20), year integer, director varchar(20), lead varchar(20))")
        db.commit()
        db.close()

    def add_to_db(self, title="", year=2000, director="", lead=""):
        db = sqlite3.connect("movies.db")
        cur = db.cursor()
        cur.execute("insert into movies values (NULL, ?, ?, ?, ?)", (title, year, director, lead))
        db.commit()
        db.close()

    def get_all(self):
        db = sqlite3.connect("movies.db")
        cur = db.cursor()
        cur.execute("select * from movies")
        rows = cur.fetchall()
        db.close()
        return rows


# only execute if I am runnig backend myself, not as I import the backend into the frontend
if __name__ == "__main__":
    # let us debug the backend
    db = Back()
    db.add_to_db("Star Wars", 1979, "George Lucas", "Mark Hamil")

