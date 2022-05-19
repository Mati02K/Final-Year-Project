from email_validator import validate_email, EmailNotValidError
from exceptionClasses import AuthError

class Order:
    def __init__(self, name, mobno, email, pid, quantity, amt, location, isDelivered = False):
        if len(name) < 2:
            raise AuthError("Please enter a proper name")
        else:
            self.name = name

        if len(mobno) != 10:
            raise AuthError("Please enter a proper mobile number")
        else:
            self.mobno = mobno

        if self.validateEmail(email):
            self.email = email
        else:
            raise EmailNotValidError

        if int(pid) > 100 and int(pid) < 111:
            self.pid = int(pid)
        else:
            raise AuthError("Wrong Product Id")

        self.quantity = int(quantity)

        self.amt = int(amt)

        self.location = location

        self.isDelivered = isDelivered

    def validateEmail(self, email):
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False
