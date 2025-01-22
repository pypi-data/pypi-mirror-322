from requests import request
import random
from .constants import _constant_info
import asyncio

async def regions(cookies: str) -> dict:
    """
    Get a list of all regions for Honkai Star Rail.

    Args:
        cookies (str): User cookies to authenticate request.

    Returns:
        dict: A list of all regions for Honkai Star Rail.
    """
    requestHeader = {
        'Cookie': cookies,
        'Origin': 'https://act.hoyolab.com',
        'Connection': 'keep-alive',
        'Referer': 'https://act.hoyolab.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-us,en;q=0.9',
        'x-rpc-language': 'en-us',
    }

    regions = request("GET", "https://api-account-os.hoyolab.com/account/binding/api/getAllRegions?game_biz=hkrpg_global", headers=requestHeader).json()

    return regions

async def act_calender(server: str, uid: int, cookies: str) -> dict:
    """
    Get the act calender for Honkai Star Rail.

    Args:
        server (str): The server the player is on.
        uid (int): The user id of the player being searched for.
        cookies (str): User cookies to authenticate request.

    Returns:
        dict: The act calender for Honkai Star Rail.
    """
    requestHeader = {
        'Cookie': cookies,
        'Origin': 'https://act.hoyolab.com',
        'Connection': 'keep-alive',
        'Referer': 'https://act.hoyolab.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-us,en;q=0.9',
        'x-rpc-language': 'en-us',
    }

    data = {
        "server": server,
        "role_id": uid,
        "lang": "en-us",
    }

    await asyncio.sleep(random.randint(1, 5))

    gameData = _constant_info["starrail"]

    act_calender = request("GET", f"{gameData['chronicle']}/get_act_calender", headers=requestHeader, params=data).json()

    return act_calender

async def overview(server: str, uid: int, cookies: str) -> dict:
    """
    Get an overview of the player's game data.

    Args:
        server (str): The server the player is on.
        uid (int): The user id of the player being searched for.
        cookies (str): User cookies to authenticate request.
    
    Returns:
        dict: An overview of the player's game data.
    """
    requestHeader = {
        'Cookie': cookies,
        'Origin': 'https://act.hoyolab.com',
        'Connection': 'keep-alive',
        'Referer': 'https://act.hoyolab.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-us,en;q=0.9',
        'x-rpc-language': 'en-us',
    }

    gameData = _constant_info["starrail"]

    await asyncio.sleep(random.randint(1, 5))

    index = request("GET", f"{gameData['chronicle']}/index?server={server}&role_id={uid}&lang=en-us", headers=requestHeader).json()
    return index

async def characters(server: str, uid: int, cookies: str) -> dict:
    """
    Get the player's character data for Honkai Star Rail.

    Args:
        server (str): The server the player is on.
        uid (int): The user id of the player being searched for.
        cookies (str): User cookies to authenticate request.

    Returns:
        dict: Data of all characters owned by the specified player.
    """
    requestHeader = {
        'Cookie': cookies,
        'Origin': 'https://act.hoyolab.com',
        'Connection': 'keep-alive',
        'Referer': 'https://act.hoyolab.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-us,en;q=0.9',
        'x-rpc-language': 'en-us',
    }

    gameData = _constant_info["starrail"]

    await asyncio.sleep(random.randint(1, 5))

    characters = request("GET", f"{gameData['chronicle']}/avatar/info?server={server}&role_id={uid}&lang=en-us&need_wiki=true", headers=requestHeader).json()
    return characters

async def simulated_universe(server: str, uid: int, cookies: str) -> dict:
    """
    Get the player's simulated universe data for Honkai Star Rail.

    Args:
        server (str): The server the player is on.
        uid (int): The user id of the player being searched for.
        cookies (str): User cookies to authenticate request.

    Returns:
        dict: Data of the player's simulated universe progress.
    """
    requestHeader = {
        'Cookie': cookies,
        'Origin': 'https://act.hoyolab.com',
        'Connection': 'keep-alive',
        'Referer': 'https://act.hoyolab.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-us,en;q=0.9',
        'x-rpc-language': 'en-us',
    }

    data = {
        "server": server,
        "role_id": uid,
        "lang": "en-us",
        "need_detail": True,
    }

    await asyncio.sleep(random.randint(1, 5))

    gameData = _constant_info["starrail"]

    gold_and_gears = request("GET", f"{gameData['chronicle']}/rogue_nous", headers=requestHeader, params=data).json()

    await asyncio.sleep(random.randint(0.1, 0.3))

    swarm_disaster = request("GET", f"{gameData['chronicle']}/rogue_locust", headers=requestHeader, params=data).json()

    await asyncio.sleep(random.randint(0.1, 0.3))

    unknowable_domain = request("GET", f"{gameData['chronicle']}/rogue_magic", headers=requestHeader, params=data).json()

    await asyncio.sleep(random.randint(0.1, 0.3))  

    simulated_universe = request("GET", f"{gameData['chronicle']}/rogue", headers=requestHeader, params=data).json()

    await asyncio.sleep(random.randint(0.1, 0.3))   

    divergent_universe = request("GET", f"{gameData['chronicle']}/rogue_tourn", headers=requestHeader, params=data).json()

    await asyncio.sleep(random.randint(0.1, 0.3))   

    response = {
        "divergent_universe": divergent_universe,
        "simulated_universe": simulated_universe,
        "expansion_module" : {
            "gold_and_gears": gold_and_gears,
            "swarm_disaster": swarm_disaster,
            "unknowable_domain": unknowable_domain
        }
    }

    return response

async def treasures_lightward(server: str, uid: int, cookies: str) -> dict:
    """
    Get the player's treasures of lightward data for Honkai Star Rail.

    Args:
        server (str): The server the player is on.
        uid (int): The user id of the player being searched for.
        cookies (str): User cookies to authenticate request.

    Returns:
        dict: Data of the player's treasures of lightward progress.
    """
    requestHeader = {
        'Cookie': cookies,
        'Origin': 'https://act.hoyolab.com',
        'Connection': 'keep-alive',
        'Referer': 'https://act.hoyolab.com/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-us,en;q=0.9',
        'x-rpc-language': 'en-us',
    }

    data = {
        "server": server,
        "role_id": uid,
        "lang": "en-us",
        "need_all": False,
        "schedule_type": 1,
    }

    await asyncio.sleep(random.randint(1, 5))

    gameData = _constant_info["starrail"]

    apocalyptic_shadow = request("GET", f"{gameData['chronicle']}/challenge_boss", headers=requestHeader, params=data).json()

    await asyncio.sleep(random.randint(0.1, 0.3))

    pure_fiction = request("GET", f"{gameData['chronicle']}/challenge_story", headers=requestHeader, params=data).json()

    await asyncio.sleep(random.randint(0.1, 0.3))

    forgotten_hall = request("GET", f"{gameData['chronicle']}/challenge", headers=requestHeader, params=data).json()

    response = {
        "apocalyptic_shadow": apocalyptic_shadow,
        "pure_fiction": pure_fiction,
        "forgotten_hall": forgotten_hall
    }

    return response
