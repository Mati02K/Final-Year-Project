import boto3
from boto3.dynamodb.conditions import Key
from exceptionClasses import AuthError


class Products:
    def __init__(self):
        self.db = boto3.resource('dynamodb')
        self.table = self.db.Table('products_table')

    def scan(self):
        responses = self.table.scan()
        for response in responses['Items']:
            response['pid'] = int(response['pid'])
            response['stock'] = int(response['stock'])
            response['price'] = int(response['price'])
        return responses

    def getCurrentQuantity(self, pid):
        response = self.table.query(KeyConditionExpression=Key('pid').eq(pid))
        return response['Items'][0]['stock']

    def decrement(self, pid, count = 1):
        currQty = self.getCurrentQuantity(pid)
        if currQty < 1 or currQty < count:
            raise AuthError("Out Of Stock")
        elif currQty == count:
            currQty = currQty - count
            response = self.table.update_item(
                Key={'pid': pid},
                UpdateExpression="SET stock = :val, available = :st",
                ExpressionAttributeValues={":val": currQty, ":st" : False},
                ReturnValues="UPDATED_NEW")
            return response
        else:
            currQty = currQty - count
            response = self.table.update_item(
                Key = {'pid': pid},
                UpdateExpression = "SET stock = :val",
                ExpressionAttributeValues = {":val" : currQty},
                ReturnValues="UPDATED_NEW" )
            return response
