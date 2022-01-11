import os
from deta import Deta
from typing import Union

deta = Deta(os.getenv('DETA'))

async def guild_create_tag(guildId: int, item: Union[list, dict], key: str):
    db = deta.Base(f'Guild-{guildId}')
    db.insert({'item': item}, key)

async def guild_get_tag(guildId: int, key: str):
    db = deta.Base(f'Guild-{guildId}')
    return db.get(key)

async def guild_delete_tag(guildID: int, key: str):
    db = deta.Base(f'Guild-{guildID}')
    db.delete(key)

