import os
from deta import Deta
from typing import Union

deta = Deta(os.getenv('DETA'))

# Guild


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

# Global

class AuxFunc:

    def __init__(self):
        self.deta = Deta(os.getenv('DETA'))
        self.db = self.deta.Base('_PUBLIC_TAGS')
        self.cache = self.db.get('all')  # soon implement cache for more efficiency

    async def push_public_tag(self, item: Union[list, dict], key: str):
        return self.db.put({'item': item}, key)

    async def fetch_public_tag(self, key: str):
        data = self.db.get(key)
        if data:
            return data['item']
        else:
            return None

