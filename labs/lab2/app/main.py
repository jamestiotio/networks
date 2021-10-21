#!/usr/bin/env python3
# SUTD 50.012 Networks Lab 2
# James Raphael Tiovalen (1004555)

from fastapi import FastAPI, Response, Depends, Header, File, UploadFile
from typing import Optional
import redis
import pickle
import secrets
import subprocess
import io
from starlette.responses import StreamingResponse
from models import BatchCharDelete, Character

app = FastAPI()


# Need to seed database with some initial data points/values
def get_redis_client():
    return redis.Redis(host="redis")


def get_all_character_ids(redis_client):
    all_character_ids = redis_client.smembers("/character/ids")
    all_character_ids = [int(x.decode("utf-8")) for x in all_character_ids]
    return all_character_ids


@app.get("/")
async def read_root(redis_client: redis.Redis = Depends(get_redis_client)):
    all_character_ids = get_all_character_ids(redis_client)
    if not all_character_ids:
        return "HMM, WHO IS SPEAKING? I SHALL NOT SPEAK TO YOU, YOU WHO ARE IN [[H E A V E N]]... WHILE WE SUFFER, YOU SIMPLY SIT IDLY ON YOUR THRONE."
    else:
        return "HI THERE ! WELCOME TO MY SHOP, my [esteem customer]!! IT'S ME, PHOTRON X. PHOTRON! EV3RY1'S FAVORITE [[Number 2 Rated Salesman2021]]"


@app.get("/fortunes")
async def get_fortune():
    output = subprocess.run(
        ["/usr/games/fortune"], shell=True, capture_output=True, universal_newlines=True
    )
    return output.stdout.strip()


@app.get("/characters")
async def get_characters(
    response: Response,
    redis_client: redis.Redis = Depends(get_redis_client),
    sortBy: Optional[str] = None,
    count: Optional[int] = None,
    offset: Optional[int] = None,
):
    all_character_ids = get_all_character_ids(redis_client)
    character_collection = []
    for character_id in all_character_ids:
        character = pickle.loads(redis_client.get(f"/character/{character_id}"))
        character_collection.append(character)

    if sortBy:
        if sortBy == "name":
            character_collection = sorted(character_collection, key=lambda x: x.name)
        elif sortBy == "id":
            character_collection = sorted(character_collection, key=lambda x: x.id)
        elif sortBy == "level":
            character_collection = sorted(character_collection, key=lambda x: x.level)
        else:
            response.status_code = 400
            return "Invalid sortBy query flag condition!"

    if offset:
        if offset > -1:
            character_collection = character_collection[offset:]
        else:
            response.status_code = 400
            return "Invalid offset!"

    if count:
        if count > 0:
            character_collection = character_collection[:count]
        else:
            response.status_code = 400
            return "Invalid count!"

    response.status_code = 200
    return character_collection


@app.get("/characters/{character_id}")
async def find_character(
    character_id: int,
    response: Response,
    redis_client: redis.Redis = Depends(get_redis_client),
):
    all_character_ids = get_all_character_ids(redis_client)

    if character_id in all_character_ids:
        character = pickle.loads(redis_client.get(f"/character/{character_id}"))
        response.status_code = 200
        return character

    response.status_code = 404
    return "YOU WERE NOT EVEN BORN!"


@app.post("/characters")
async def create_character(
    character: Character,
    response: Response,
    redis_client: redis.Redis = Depends(get_redis_client),
):
    all_character_ids = get_all_character_ids(redis_client)
    if character.id in all_character_ids:
        response.status_code = 400
        return "YOU ALREADY EXISTS!! THERE IS NO NEED TO [[recreate]] YOURSELF ANYMORE!"
    else:
        redis_client.sadd("/character/ids", character.id)
        redis_client.set(f"/character/{character.id}", pickle.dumps(character))
        response.status_code = 201
        return f"AND, YOU ARE BORN!! WELCOME TO THIS REALM, {character.name}!"


@app.delete("/characters/{character_id}")
async def delete_character(
    character_id: int,
    response: Response,
    password: Optional[str] = Header(None),
    redis_client: redis.Redis = Depends(get_redis_client),
):
    all_character_ids = get_all_character_ids(redis_client)
    character_collection = []
    for id in all_character_ids:
        character = pickle.loads(redis_client.get(f"/character/{id}"))
        character_collection.append(character)

    if character_id in all_character_ids:
        character = pickle.loads(redis_client.get(f"/character/{character_id}"))
    else:
        response.status_code = 404
        return "YOU WERE NOT EVEN BORN!"

    if password == str(character.password):
        redis_client.delete(f"/character/{character_id}")
        redis_client.srem("/character/ids", character_id)
        response.status_code = 200
        return "CHARACTER ERASED FROM EXISTENCE! DO YOU FEEL SUCH JOY FROM HANDLING [[lives]] SO TRIVIALLY..."
    else:
        response.status_code = 401
        return "UNAUTHORIZED ACCESS DETECTED! YOU ARE ACTUALLY NOT AN [esteemed customer]!! DEPART FROM HERE!"


@app.delete("/characters_batch")
async def delete_multiple_characters_within_levels(
    response: Response,
    info: BatchCharDelete,
    password: Optional[str] = Header(None),
    redis_client: redis.Redis = Depends(get_redis_client),
):
    all_character_ids = get_all_character_ids(redis_client)
    character_collection = []
    for character_id in all_character_ids:
        character = pickle.loads(redis_client.get(f"/character/{character_id}"))
        character_collection.append(character)

    character_passwords = [str(x.password) for x in character_collection]

    if password in character_passwords:
        if info.min_level:
            for character in character_collection:
                if int(character.level) >= info.min_level:
                    redis_client.delete(f"/character/{character.id}")
                    redis_client.srem("/character/ids", character.id)

        if info.max_level:
            for character in character_collection:
                if int(character.level) <= info.max_level:
                    redis_client.delete(f"/character/{character.id}")
                    redis_client.srem("/character/ids", character.id)

        response.status_code = 200
        return "MULTIPLE CHARACTERS HAVE BEEN REMOVED FROM EXISTENCE! [are you happy now!?!?]"

    else:
        response.status_code = 401
        return "UNAUTHORIZED ACCESS DETECTED! YOU ARE ACTUALLY NOT AN [esteemed customer]!! DEPART FROM HERE!"
