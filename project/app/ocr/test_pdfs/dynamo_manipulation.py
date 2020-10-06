from boto3 import resource

dynamodb = resource('dynamodb')
table = dynamodb.Table('user_stories')

database = {"user_stories": table.scan()["Items"]}
# st(term_size=(200, 50), host="0.0.0.0", port=4444)
print_val = database["user_stories"]
# print(print_val)
print(
    FinalStoreDatabase(print_val)
)
# 