from requests import request
import random
from .constants import _constant_info
import asyncio

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

    gameData = _constant_info["genshin"]

    await asyncio.sleep(random.randint(1, 5))

    index = request("GET", f"{gameData['chronicle']}/index?avatar_list_type=1&server={server}&role_id={uid}&lang=en-us", headers=requestHeader).json()
    return index

async def characters(server: str, uid: int, cookies: str) -> dict:
    """
    Gets the player's character data for genshin impact.

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

    data = {
        "role_id": uid,
        "server": server,
    }

    gameData = _constant_info["genshin"]

    await asyncio.sleep(random.randint(1, 5))

    characterData = request("POST", f"{gameData['chronicle']}/character/list", json=data, headers=requestHeader).json()
    return characterData

async def character_detailed(server: str, uid: int, character_id: int, cookies: str) -> dict:
    """
    Get detailed information of a user's owned character.

    Args:
        server (str): The server the player is on.
        uid (int): The user id of the player being searched for.
        character_id (int): The character's id.
        cookies (str): User cookies to authenticate request.
    
    Returns:
        dict: Detailed information of a user's owned character.
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
        "role_id": uid,
        "server": server,
        "character_id": [character_id]
    }

    gameData = _constant_info["genshin"]

    await asyncio.sleep(random.randint(1, 5))

    characterOverview = request("POST", f"{gameData['chronicle']}/character/detail", json=data, headers=requestHeader).json()
    return characterOverview

async def check_in(cookies: str, lang: str = "en-us") -> str:
    """
    Attempts daily check-in for the specified game given the users cookies.

    Args:
        cookies (str): User cookies to authenticate request.
        lang (str): Language to use for the check-in. Default is "en-us".

    Returns:
        str: A message indicating the result of the check-in.
    """
    requestHeader = {
        'Cookie': cookies,
        'Origin': 'https://act.hoyolab.com',
        'Connection': 'keep-alive',
        'Referer': 'https://act.hoyolab.com/',
        'Accept-Encoding': 'gzip, deflate, br',
    }

    gameData = _constant_info['genshin']

    await asyncio.sleep(random.randint(4,8))

    info = request("GET", f"{gameData['api_base']}/info?lang={lang}&act_id={gameData['act_id']}", headers=requestHeader).json()

    if info["retcode"] != 0:
        return f"Failed to get info: {info['message']}"
    
    rewards = request("GET", f"{gameData['api_base']}/home?lang={lang}&act_id={gameData['act_id']}", headers=requestHeader).json()

    if info["data"]["is_sign"]:
        obtained = rewards['data']['awards'][info['data']['total_sign_day'] - 1]
        resString = (f"Already checked-in today for {gameData['title']} \n"
            f"You received: {obtained['name']} x{obtained['cnt']} \n"
            f"Total check-in days: {info['data']['total_sign_day']}")
        return resString
    
    if gameData["title"] == "Genshin Impact" and info["data"]["first_bind"]:
        return f"Please manually check-in once for {gameData['title']}"

    await asyncio.sleep(random.randint(5,10))

    response = request("POST", f"{gameData['api_base']}/sign?lang={lang}&act_id={gameData['act_id']}", headers=requestHeader).json()

    new_info = request("GET", f"{gameData['api_base']}/info?lang={lang}&act_id={gameData['act_id']}", headers=requestHeader).json()

    if new_info["retcode"] != 0:
        return f"Failed to get info: {new_info['message']}"
    
    if not new_info["data"]["is_sign"]:
        return f"Failed to check-in: {response['message']}"
    
    obtained_items = rewards['data']['awards'][new_info['data']['total_sign_day'] - 1]
    resString = (f"Successfully checked-in for {gameData['title']} \n"
            f"Rewards: {obtained_items['name']} x{obtained_items['cnt']} \n"
            f"Total check-in days: {info['data']['total_sign_day']}")
    return resString

async def act_calender(server: str, uid: int, cookies: str) -> dict:
    """
    Get the act calender for genshin impact.

    Args:
        server (str): The server the player is on.
        uid (int): The user id of the player being searched for.
        cookies (str): User cookies to authenticate request.

    Returns:
        dict: Data of the genshin act calender.
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

    gameData = _constant_info["genshin"]

    act_calender = request("GET", f"{gameData['chronicle']}/act_calender", headers=requestHeader, params=data).json()

    return act_calender

async def spiral_abyss(server: str, uid: int, cookies: str) -> dict:
    """
    Get the player's spiral abyss data for genshin impact.

    Args:
        server (str): The server the player is on.
        uid (int): The user id of the player being searched for.
        cookies (str): User cookies to authenticate request.
    
    Returns:
        dict: Data of the player's spiral abyss progress.
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

    gameData = _constant_info["genshin"]

    await asyncio.sleep(random.randint(1, 5))

    abyssData = request("GET", f"{gameData['chronicle']}/spiralAbyss?server={server}&role_id={uid}&schedule_type=1", headers=requestHeader).json()
    return abyssData

async def imaginarium_theatre(server: str, uid: int, cookies: str) -> dict:
        """
        Get the player's imaginarium theatre data for genshin impact.

        Args:
            server (str): The server the player is on.
            uid (int): The user id of the player being searched for.
            cookies (str): User cookies to authenticate request.
        
        Returns:
            dict: Data of the player's imaginarium theatre progress.
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

        gameData = _constant_info["genshin"]

        await asyncio.sleep(random.randint(1, 5))

        abyssData = request("GET", f"{gameData['chronicle']}/role_combat?server={server}&role_id={uid}&need_detail=true", headers=requestHeader).json()
        return abyssData
