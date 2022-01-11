import os
from deta import Deta
from typing import Union

deta = Deta(os.getenv('DETA'))

async def guild_push_object(guildId: int, item: Union[list, dict], key: str):
    db = deta.Base(f'Guild-{guildId}')
    db.put({'item': item}, key)

async def guild_get_object(guildId: int, key: str):
    db = deta.Base(f'Guild-{guildId}')
    return db.get(key)

async def guild_fetch_objects(guildID: int, limit: int, query: str):
    db = deta.Base(f'Guild-{guildID}')
    return db.fetch(limit=limit, query=query)