import os
from deta import Deta
from typing import Union

deta = Deta(os.getenv('DETA'))

# Guild


async def guild_create_tag(guild_id: int, item: Union[list, dict], owner: str, name: str):
#    print('Test message 1')
    db = deta.Base(f'Guild-{guild_id}')
#    check = await guild_get_tag(guild_id=guild_id, tag=name)
#    print('Test message 2')
#    if check['name'] == str(name):
#        print('Test message 3')
#    else:
#        print('Test message 4')
    db.insert({'item': item, 'owner': owner, 'name': name})

async def guild_edit_tag(guild_id: int, item: Union[list, dict], owner: str, name: str):
    db = deta.Base(f'Guild-{guild_id}')
    db.put({'item': item, 'owner': owner, 'name': name})

async def guild_delete_tag(guild_id: int, key: str):
    db = deta.Base(f'Guild-{guild_id}')
    db.delete(key)
    

async def guild_get_tag_by_id(guild_id: int, key: str):
    db = deta.Base(f'Guild-{guild_id}')
    return db.get(key)

async def guild_get_tag_by_name(guild_id: int, name: str):
    db = deta.Base(f'Guild-{guild_id}')
    return db.fetch({'name': name})

async def guild_get_tag(guild_id: int, tag: str):
    try:
        data = await guild_get_tag_by_name(guild_id, name=tag)
        for item in data.items:
            name = item
        return name
    except:
        pass
    try:
        id = await guild_get_tag_by_id(guild_id, key=tag)
        return id
    except:
        pass


async def guild_fetch_user(guild_id: int, owner: str):
    db = deta.Base(f'Guild-{guild_id}')
    return db.fetch({'owner': owner})

async def guild_fetch_tag(guild_id: int, key: str):
    db = deta.Base(f'Guild-{guild_id}')
    return db.fetch({'key': key})