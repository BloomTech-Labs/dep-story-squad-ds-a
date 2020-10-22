from fastapi import APIRouter, HTTPException, Depends
from app.dependencies.security import verify_token

from typing import Dict, List
from pydantic import BaseModel, Field
import boto3

router = APIRouter()

class GetPlayersResponse(BaseModel):
    user_stories: List[Dict[str, str]] =\
        Field(..., example=[
                {
                    "user_id": "12322187",
                    "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12322187/story_5"
                },
                {
                    "user_id": "12323312",
                    "s3_dir": "new_stories_dataset/multiplayer/competitions/competition_43/username_12323312/story_2"
                },
            ]
        )


@router.get('/multiplayer/get_players', tags=["Multiplayer"], dependencies=[Depends(verify_token)], response_model=GetPlayersResponse)
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
