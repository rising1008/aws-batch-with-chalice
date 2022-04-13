import boto3
from boto3.dynamodb.conditions import Key


def clear():
    partitionKey = "dataType"
    sortKey = "dataId"

    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("rova-dev-master")
    tableKeyNames = [key.get("AttributeName") for key in table.key_schema]
    print(type(tableKeyNames))
    print(tableKeyNames)
    projectionExpression = ", ".join('#' + key for key in tableKeyNames)
    expressionAttrNames = {'#'+key: key for key in tableKeyNames}

    try:
        counter = 0
        page = table.scan(ProjectionExpression=projectionExpression, ExpressionAttributeNames=expressionAttrNames)
        with table.batch_writer() as batch:
            while page["Count"] > 0:
                counter += page["Count"]
                # Delete items in batches
                for itemKeys in page["Items"]:
                    batch.delete_item(Key=itemKeys)
                # Fetch the next page
                if 'LastEvaluatedKey' in page:
                    page = table.scan(
                        ProjectionExpression=projectionExpression, ExpressionAttributeNames=expressionAttrNames,
                        ExclusiveStartKey=page['LastEvaluatedKey'])
                else:
                    break

    except Exception as e:
        print('DynamoDBアイテム削除中に想定外のエラーが発生しました。')
        print(e)
        return False

    print('Dynamoアイテムの削除完了')

    return True

if __name__ == "__main__":
    clear()
