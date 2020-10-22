# from pudb.remote import set_trace as st
# from remote_pdb import RemotePdb
# from ipdb import set_trace as st
# from pdb import set_trace as st
# from web_pdb import set_trace as st

import io
import os
from app.ocr.curve import Pipeline
from typing import List
import boto3


if __name__ == "__main__":
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('user_stories')

    database = table.scan()["Items"]

    # print(table.scan())
    print(f"Pipeline output: {Pipeline(database)}")

