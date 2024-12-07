from sqlmodel import Session, select
# from utils.wraper import ResponseWraper, UserSchema, LoginUserSchema
# from utils.status_code import Http, Message
from models.user import User
# from utils.auth import auth_wrapper, get_password_hash, verify_password, encode_token, decode_token
from fastapi import HTTPException
from schemas.query import SearchRequest
import httpx
import requests

GRAPHQL_URL = "https://graphql.anilist.co"


async def search_controller(search: SearchRequest):
    try:
        query = """
        query ($name: String, $genre: String) {
            Page(page: 1, perPage: 10) {
                media(search: $name, genre_in: [$genre], type: ANIME) {
                    id
                    title {
                        romaji
                        english
                        native
                    }
                    description
                    genres
                    format
                    status
                    episodes
                    averageScore
                    popularity
                }
            }
        }
        """

        variables = {
            "name": search.name,  
            "genre": search.genre  
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                GRAPHQL_URL,
                json={"query": query, "variables": variables},
                headers={"Content-Type": "application/json"}
            )
        return response.json()
    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Catch Error found")
    

    
def get_recommendation(session, payload):
    try:
        id = payload['id']
        statement = select(User).where(User.id == id)
        user = session.exec(statement).first()
        joined_string = ''.join(user.genres)
        cleaned_string = joined_string.strip('{}')
        split_items = cleaned_string.split(',')

        query = """
            query ($genre: [String]) {
                Page(page: 1, perPage: 10) {
                    media(genre_in: $genre, type: ANIME) {
                        id
                        title {
                            romaji
                            english
                            native
                        }
                        description
                        genres
                        format
                        status
                        episodes
                        averageScore
                        popularity
                    }
                }
            }
        """
        
        # Set up the variables for the query
        variables = {
            "genre": split_items  # Ensure it's always a list
        }
  
        response = requests.post(
            GRAPHQL_URL,
            json={"query": query, "variables": variables},
            headers={"Content-Type": "application/json"}
        )
        return response.json()

    except HTTPException as http_err:
        raise http_err
    except Exception as error:
        print(error)
        raise HTTPException(status_code=500, detail="Catch Error found")