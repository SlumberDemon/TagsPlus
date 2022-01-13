import os
from deta import Deta
from typing import Union

deta = Deta(os.getenv('DETA'))


async def guild_create_tag(guild_id: int, item: Union[list, dict], key: str):
    db = deta.Base(f'Guild-{guild_id}')
    db.insert({'item': item}, key)


async def guild_edit_tag(guild_id: int, item: Union[list, dict], key: str):
    db = deta.Base(f'Guild-{guild_id}')
    db.put({'item': item}, key)


async def guild_get_tag(guild_id: int, key: str):
    db = deta.Base(f'Guild-{guild_id}')
    return db.get(key)


async def guild_delete_tag(guild_id: int, key: str):
    db = deta.Base(f'Guild-{guild_id}')
    db.delete(key)
