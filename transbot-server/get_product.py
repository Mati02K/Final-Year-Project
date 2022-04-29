import boto3

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
