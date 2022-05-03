import mysql.connector, datetime, requests, json
from get_product import Products
from exceptionClasses import AuthError
from random import randint

def convert(results):
    details = {}
    itr = 1
    for result in results:
        result = list(result)
        result[8] = result[8].strftime("%m/%d/%Y, %H:%M:%S")
        details[itr] = result
        itr += 1
    return details

def generateOTP(length):
    range_start = 10 ** (length - 1)
    range_end = (10 ** length) - 1
    return randint(range_start, range_end)

class Checkout:
    def __init__(self):
        self.dataBase = mysql.connector.connect(
            host = "sql503.main-hosting.eu",
            user = "u347396496_matiantolak",
            passwd = "!Pkb8*nH6",
            database = "u347396496_drobot"
        )
        self.MSG_API_URL = "https://www.fast2sms.com/dev/bulk"
        self.API_KEY = "3aO84tliq1ycM5Hd2Nv9JUZwkXTGjxpPgfWYKLCuzFE7QInsboZrsB8NFW7lLHcfmhuXbGYM9pv13IQ0"

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

    def getLastBookedItem(self):
        self.cursorObject = self.dataBase.cursor()
        query = "SELECT mobileno,pid,quantity FROM checkout ORDER BY oid DESC LIMIT 1"
        self.cursorObject.execute(query)
        res = self.cursorObject.fetchall()
        self.dataBase.commit()
        self.cursorObject.close()
        return res[0]

    def sendSMS(self, mobileNo):
        otp = generateOTP(length = 6)
        msg =  "Your Package has arrived your destination. Your OTP for the order is " + str(otp)
        payload = {'sender_id': 'FSTSMS',
                   'message': msg,
                   'language': 'english',
                   'route': 'p',
                   'numbers': str(mobileNo)
                   }

        headers = {
            'authorization': self.API_KEY,
            'Content-Type': "application/x-www-form-urlencoded",
            'Cache-Control': "no-cache",
        }
        response = requests.request("POST", self.MSG_API_URL, data=payload, headers=headers)
        result = json.loads(response.text)
        return result['return']

    def update(self):
        # Decrement the stock in Dynamo DB
        p = Products()
        details = self.getLastBookedItem()
        mobno = details[0]
        pid = details[1]
        count = details[2]
        p.decrement(pid, count = count)

        #Then Confirm the Order has been delivered
        self.cursorObject = self.dataBase.cursor()
        query = "UPDATE checkout SET isDelivered = 1 ORDER BY oid DESC LIMIT 1"
        self.cursorObject.execute(query)
        self.cursorObject.close()
        self.dataBase.commit()
        self.dataBase.close()

        #Then send SMS
        res = self.sendSMS(mobileNo = mobno)
        if res:
            return "Success"
        else:
            raise AuthError("Not able to send SMS")

    def fetch(self):
        self.cursorObject = self.dataBase.cursor()
        query = "SELECT * FROM checkout"
        self.cursorObject.execute(query)
        res = self.cursorObject.fetchall()
        self.cursorObject.close()
        output = convert(res)
        return output