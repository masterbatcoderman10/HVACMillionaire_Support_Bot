from sqlalchemy import select, insert, delete, update
from .db import Secrets, db
import asyncio
from datetime import datetime, timezone

async def get_access_token():
    # Connect to the database
    stmt = select(Secrets.access_token, Secrets.creation_time)
    result = await db.fetch_one(stmt)
    if result:
        access_token = result.access_token
        creation_time = result.creation_time
        return access_token, creation_time
    else:
        print("No result found.")

async def get_refresh_token():
    stmt = select(Secrets.refresh_token)
    return await db.fetch_val(stmt)

async def create_secret(refresh_token: str, access_token: str):
    #delete the old secret pair
    stmt = delete(Secrets)
    await db.execute(stmt)

    #insert the new secret pair
    creation_time = datetime.now(timezone.utc)
    stmt = insert(Secrets).values(refresh_token=refresh_token, access_token=access_token, creation_time=creation_time)
    await db.execute(stmt)


if __name__ == '__main__':
    print(asyncio.run(get_access_token()))