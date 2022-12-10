from flask import Flask, render_template
import sqlite3

HOST_NAME = "localhost"
HOST_PORT = 80
DBFILE = "apartments.db"
app = Flask(__name__)


def get_offers():
    conn = sqlite3.connect(DBFILE)
    cursor = conn.cursor()
    cursor.execute("SELECT description, area, price, city, url FROM new_offers WHERE city = 'Gliwice' ORDER BY area")
    results = cursor.fetchall()
    conn.close()
    return results


@app.route("/")
def index():
    offers = get_offers()
    return render_template("apartaments.html", ofs=offers)


if __name__ == "__main__":
    app.run(HOST_NAME, HOST_PORT)
