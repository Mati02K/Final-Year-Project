import boto3

db = boto3.resource('dynamodb')
table = db.Table('products_table')

# response = table.get_item(
#     Key = {
#         'pid' : 101
#     }
# )

response = table.scan()

print(response)