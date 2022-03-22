from http.client import EXPECTATION_FAILED
import os
from tabnanny import check
from deta import Deta
from typing import Union

deta = Deta(os.getenv('DETA'))

# Guild


async def guild_create_tag(guild_id: int, item: Union[list, dict], owner: str, name: str):
    db = deta.Base(f'Guild-{guild_id}')
    data = db.fetch({'name': name})
    check = await guild_get_tag_name(guild_id=guild_id, tag=name)
    if check == name:
        print('Test message')
    else:
        print('Test message 1')
        db.insert({'item': item, 'owner': owner, 'name': name})


async def guild_edit_tag(guild_id: int, item: Union[list, dict], key: str):
    db = deta.Base(f'Guild-{guild_id}')
    db.put({'item': item}, key)


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

async def guild_get_tag_content(guild_id: int, tag: str):
    try:
        data = await guild_get_tag_by_name(guild_id, name=tag)
        for item in data.items:
            name = item['item'][0]['content']
    except:
        pass
    try:
        id = await guild_get_tag_by_id(guild_id, key=tag)
        return id['item'][0]['content']
    except:
        pass


async def guild_get_tag_name(guild_id: int, tag: str):
    try:
        data = await guild_get_tag_by_name(guild_id, name=tag)
        for item in data.items:
            name = item['name']
        return name
    except:
        pass
    try:
        id = await guild_get_tag_by_id(guild_id, key=tag)
        return id['name']
    except:
        pass


async def guild_delete_tag(guild_id: int, key: str):
    db = deta.Base(f'Guild-{guild_id}')
    db.delete(key)

async def guild_fetch_user(guild_id: int, owner: str):
    db = deta.Base(f'Guild-{guild_id}')
    return db.fetch({'owner': owner})

async def guild_fetch_tag(guild_id: int, key: str):
    db = deta.Base(f'Guild-{guild_id}')
    return db.fetch({'key': key})