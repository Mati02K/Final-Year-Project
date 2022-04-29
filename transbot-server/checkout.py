import mysql.connector
import datetime

def convert(results):
    details = {}
    itr = 1
    for result in results:
        result = list(result)
        result[8] = result[8].strftime("%m/%d/%Y, %H:%M:%S")
        details[itr] = result
        itr += 1
    return details

class Checkout:
    def __init__(self):
        self.dataBase = mysql.connector.connect(
            host = "sql503.main-hosting.eu",
            user = "u347396496_matiantolak",
            passwd = "!Pkb8*nH6",
            database = "u347396496_drobot"
        )

    def add(self, order):
        self.cursorObject = self.dataBase.cursor()

        sql = "INSERT INTO checkout (name, mobileno, email, pid, quantity, amt, isDelivered, bookedat)\
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

        timestamp = datetime.datetime.now()

        val = (order.name, order.mobno, order.email, order.pid,
        order.quantity, order.amt, order.isDelivered, timestamp)

        self.cursorObject.execute(sql, val)
        self.cursorObject.close()
        self.dataBase.commit()
        self.dataBase.close()
        return "Success"

    def update(self):
        self.cursorObject = self.dataBase.cursor()
        query = "UPDATE checkout SET isDelivered = 1 ORDER BY oid DESC LIMIT 1"
        self.cursorObject.execute(query)
        self.dataBase.commit()
        self.dataBase.close()
        return "Success"

    def fetch(self):
        self.cursorObject = self.dataBase.cursor()
        query = "SELECT * FROM checkout"
        self.cursorObject.execute(query)
        res = self.cursorObject.fetchall()
        output = convert(res)
        return output