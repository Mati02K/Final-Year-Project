import mysql.connector, datetime, requests, json
from get_product import Products
from exceptionClasses import AuthError
from random import randint

def convert(results):
    details = {}
    itr = 1
    for result in results:
        result = list(result)
        result[10] = result[10].strftime("%m/%d/%Y, %H:%M:%S")
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
        self.MSG_API_URL = "https://www.fast2sms.com/dev/bulkV2"
        self.API_KEY = "QRv6xz4qNBHhLmpPT7bOcdVC3WS2rofKFAs8kEi9egwZIXM15D8dORYvo5hwuTrAPjIxVDFG6cC3XJmM"
        self.DROBOT_URL = "https://maker.ifttt.com/trigger/droboton/json/with/key/nhHxJBXLjWN_vgW_2_b39xXdUj2ZT5524L2Y3hl78Ip"

    def startDrobot(self):
        x = requests.get(self.DROBOT_URL)
        if (x.status_code == 200):
            return True
        return False
    
    def sendSMS(self, mobileNo, msg):
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

    def getLastBookedItem(self):
        self.cursorObject = self.dataBase.cursor()
        query = "SELECT mobileno,pid,quantity,oid FROM checkout ORDER BY oid DESC LIMIT 1"
        self.cursorObject.execute(query)
        res = self.cursorObject.fetchall()
        self.dataBase.commit()
        self.cursorObject.close()
        return res[0]

    def add(self, order):
        self.startDrobotStatus = self.startDrobot()

        self.cursorObject = self.dataBase.cursor()

        sql = "INSERT INTO checkout (name, mobileno, email, pid, quantity, amt, location, OTP, isDelivered, bookedat)\
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        timestamp = datetime.datetime.now()

        val = (order.name, order.mobno, order.email, order.pid,
        order.quantity, order.amt, order.location, order.otp, order.isDelivered, timestamp)

        self.cursorObject.execute(sql, val)
        self.cursorObject.close()

        # Send the SMS to the user about the order ID
        orderdetails = self.getLastBookedItem()
        orderid = orderdetails[3]
        msg = "Your Order id is " + str(orderid) + ".Use this ID to confirm the order. Thanks for using DROBOT"
        res = self.sendSMS(mobileNo = order.mobno, msg = msg)
        self.dataBase.commit()
        self.dataBase.close()
        if res:
            return "Success"
        else:
            raise AuthError("Not able to send SMS")

    def update(self):
        # Decrement the stock in Dynamo DB
        p = Products()
        details = self.getLastBookedItem()
        mobno = details[0]
        pid = details[1]
        count = details[2]
        p.decrement(pid, count = count)
        
        otp = generateOTP(length = 6)

        #Then add the OTP no to the order
        self.cursorObject = self.dataBase.cursor()
        query = f"UPDATE checkout SET OTP = {otp} ORDER BY oid DESC LIMIT 1"
        self.cursorObject.execute(query)
        self.cursorObject.close()
        self.dataBase.commit()
        self.dataBase.close()

        #Then send SMS
        msg =  "Your Package has arrived your destination. Your OTP for the order is " + str(otp)
        res = self.sendSMS(mobileNo = mobno, msg = msg)
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
    
    def checkOTP(self, oid, otp):
        self.cursorObject = self.dataBase.cursor()
        query = f"SELECT OTP FROM checkout WHERE oid = {oid}"
        self.cursorObject.execute(query)
        res = self.cursorObject.fetchall()
        self.dataBase.commit()
        if res[0][0] == otp:
            #success
            query = f"UPDATE checkout SET isDelivered = 1 WHERE oid = {oid}"
            self.cursorObject.execute(query)
            self.dataBase.commit()
            self.cursorObject.close()
            self.dataBase.close()
            return "Success"
        
        self.cursorObject.close()
        self.dataBase.close()
        return "Incorrect OTP"