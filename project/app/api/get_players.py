from fastapi import APIRouter, HTTPException, Depends
from app.dependencies.security import verify_token

from typing import Dict, List
from pydantic import BaseModel, Field
import boto3

router = APIRouter()


@router.get('/multiplayer/get_players', tags=["Multiplayer"], dependencies=[Depends(verify_token)])
async def get_players():
    """
    Gets all the players for that week's competition

    ### Request Body

    ### Response
    - `user_stories`: List[Dict{"user_id": str, "s3_dir": str}]
    """

    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    table = dynamodb.Table('user_stories')

    # for player_story in params.user_stories:
    #     # Get the service resource.
    #     print(player_story)
    #     table.put_item(
    #         Item=player_story
    #     )

    return {
        "user_stories": table.scan()["Items"]
    }
