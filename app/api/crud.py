from sqlalchemy import select, insert, delete, update
from .db import Secrets, db
import asyncio

async def get_access_token():
    stmt = select(Secrets.access_token)
    return await db.fetch_val(stmt)

async def get_refresh_token():
    stmt = select(Secrets.refresh_token)
    return await db.fetch_val(stmt)

async def create_secret(refresh_token: str, access_token: str):
    #delete the old secret pair
    stmt = delete(Secrets)
    await db.execute(stmt)

    #insert the new secret pair
    stmt = insert(Secrets).values(refresh_token=refresh_token, access_token=access_token)
    await db.execute(stmt)


if __name__ == '__main__':
    asyncio.run(get_access_token())