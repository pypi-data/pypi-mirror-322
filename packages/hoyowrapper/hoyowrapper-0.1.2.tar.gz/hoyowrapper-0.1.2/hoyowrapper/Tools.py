from pyppeteer import launch
import asyncio
from .constants import _constant_info

async def _check_req(request, cookies_retrieved, page, res):
    if request.url.startswith(f"{_constant_info["genshin"]["api_base"]}/info?"):
        cookies = await page.cookies()
        if "ltuid_v2" in [cookie['name'] for cookie in cookies] and "ltoken_v2" in [cookie['name'] for cookie in cookies]:
            res[0] = cookies
            cookies_retrieved.set()
            return res[0]

async def login() -> str:
    """
    The function opens a new browser and waits for the user to log in to the genshin daily check-in page.

    Returns: user cookies
    """
    cookies_retrieved = asyncio.Event()
    res = [None]
    browser = await launch(
        headless=False, 
        executablePath=r"C:\Program Files\Google\Chrome\Application\chrome.exe", 
        args=['--disable-blink-features=AutomationControlled', '--no-sandbox', '--disable-dev-shm-usage']
        )
    
    await asyncio.sleep(1)
    page = await browser.newPage()
    await page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')

    page.on('request', lambda request: asyncio.ensure_future(_check_req(request, cookies_retrieved, page, res)))

    await page.goto(_constant_info["genshin"]["url"])
    await cookies_retrieved.wait()
    await asyncio.sleep(5)
    await browser.close()
    cookies = ""
    for cookie in res[0]:
        cookies += f"{cookie['name']}={cookie['value']}; "
    return cookies