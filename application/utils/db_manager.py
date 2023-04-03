from config.config import settings
from fastapi import FastAPI
from typing import List
import asyncpg


def jsonify(records):
    """
    Parse asyncpg record response into JSON format
    """
    list_return = []
    for r in records:
        items = r.items()
        list_return.append({i[0]: i[1].rstrip() if type(
            i[1]) == str else i[1] for i in items})
    return list_return


async def execute(query: str, params: List = [], debug: bool = False) -> dict or [dict] or str:
    if debug:
        import pdb; pdb.set_trace()
    db = await asyncpg.connect(f"postgres://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.DATABASE_PORT}/{settings.POSTGRES_DB}")
    query_result = []

    try:
        if 'select' in query.lower() or 'returning' in query.lower():
            query_result = await db.fetch(query, *params)
            query_result = jsonify(query_result)
        else:
            await db.execute(query, *params)
    except Exception as e:
        print(f"{e}")
    finally:
        if db:
            try:
                await db.close()
            except:
                pass
    return query_result
