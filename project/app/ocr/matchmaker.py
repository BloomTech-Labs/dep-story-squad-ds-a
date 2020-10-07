from pudb.remote import set_trace as st
# from remote_pdb import RemotePdb
# from ipdb import set_trace as st
# from pdb import set_trace as st
# from web_pdb import set_trace as st

import io
import os
from app.ocr.curve import FinalStoreDatabase
from typing import List
import boto3


if __name__ == "__main__":
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('user_stories')

    database = {"user_stories": table.scan()["Items"]}
    # st(term_size=(200, 50), host="0.0.0.0", port=4444)
    print_val = database["user_stories"]
    # print(print_val)
    print(
        FinalStoreDatabase(print_val)
    )
    # 