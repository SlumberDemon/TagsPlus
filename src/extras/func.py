import os
from deta import Deta
from typing import Union

deta = Deta(os.getenv('DETA'))

# Guild


async def guild_create_tag(guild_id: int, item: Union[list, dict], owner: str, key: str):
    db = deta.Base(f'Guild-{guild_id}')
    db.insert({'item': item, 'owner': owner}, key)


async def guild_edit_tag(guild_id: int, item: Union[list, dict], key: str):
    db = deta.Base(f'Guild-{guild_id}')
    db.put({'item': item}, key)


async def guild_get_tag(guild_id: int, key: str):
    db = deta.Base(f'Guild-{guild_id}')
    return db.get(key)


async def guild_delete_tag(guild_id: int, key: str):
    db = deta.Base(f'Guild-{guild_id}')
    db.delete(key)

async def guild_fetch_user(guild_id: int, owner: str):
    db = deta.Base(f'Guild-{guild_id}')
    return db.fetch({'owner': owner})

async def guild_fetch_tag(guild_id: int, key: str):
    db = deta.Base(f'Guild-{guild_id}')
    return db.fetch({'key': key})

async def get_tag_by_name(self, name: str):
    self.db = self.deta.Base('_PUBLIC_TAGS')
    raw = self.db.get(name)
    if raw:
        return raw
    return None

async def find_tags(self, query: str):
    results = []
    as_name = await self.get_tag_by_name(query)
    if as_name:
        results.append(as_name)

    return [i for n, i in enumerate(results) if i not in results[:n]]
