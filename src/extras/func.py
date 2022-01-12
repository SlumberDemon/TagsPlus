import os
from deta import Deta
from typing import Union

deta = Deta(os.getenv('DETA'))

# Guild

async def guild_create_tag(guildId: int, item: Union[list, dict], key: str):
    db = deta.Base(f'Guild-{guildId}')
    db.insert({'item': item}, key)

async def guild_edit_tag(guildId: int, item: Union[list, dict], key: str):
    db = deta.Base(f'Guild-{guildId}')
    db.put({'item': item}, key)

async def guild_get_tag(guildId: int, key: str):
    db = deta.Base(f'Guild-{guildId}')
    return db.get(key)

async def guild_delete_tag(guildId: int, key: str):
    db = deta.Base(f'Guild-{guildId}')
    db.delete(key)

# Global

async def global_create_tag(item: Union[list, dict], key: str):
    db = deta.Base(f'Global')
    db.insert({'item': item}, key)

async def global_edit_tag(item: Union[list, dict], key: str):
    db = deta.Base(f'Global')
    db.put({'item': item}, key)

async def global_get_tag(key: str):
    db = deta.Base(f'Global')
    return db.get(key)

async def global_delete_tag(key: str):
    db = deta.Base(f'Global')
    db.delete(key)

