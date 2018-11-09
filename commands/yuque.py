"""自动创建语雀邀请链接，和邀请加入技术组

Usage:
  yuque.py invite
  yuque.py add-to-tech-team <name>
  yuque.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""
import os
import sys

from contextlib import asynccontextmanager

import asyncio
import docopt
from pyppeteer import launch
from pyppeteer.browser import Browser

cwd = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, cwd)

from gt.config import YUQUE_CONFIG


@asynccontextmanager
async def new_browser():
    browser = await launch(args=['--no-sandbox', '--disable-dev-shm-usage'])
    try:
        yield browser
    finally:
        await browser.close()


async def get_invitation_url() -> str:
    async with new_browser() as browser:
        await login(browser)

        page = await browser.newPage()
        await page.goto('https://xcf.yuque.com/admin/dashboard/manage/member')

        await page.click('.btn-invite')
        await asyncio.sleep(1)
        url = await page.querySelectorEval('.invite-link .url', 'el => el.innerText')

        return url


async def add_to_tech_team(name: str):
    async with new_browser() as browser:
        await login(browser)

        page = await browser.newPage()
        await page.goto('https://xcf.yuque.com/all/members')

        await page.click('.members-setting-add button')
        await asyncio.sleep(1)
        await page.type('.ant-modal-body input', name)
        await asyncio.sleep(3)
        await page.click('.select-by-search-menu .larkicon.larkicon-add')


async def login(browser: Browser):
    page = await browser.newPage()
    await page.goto('https://xcf.yuque.com/login')
    await asyncio.sleep(1)
    await page.type('#login', YUQUE_CONFIG.USERNAME)
    await page.type('#password', YUQUE_CONFIG.PASSWORD)
    await page.click('button')
    await page.waitForNavigation()


def invite():
    url = asyncio.run(get_invitation_url())
    print(url, flush=True)


def add_to_team(name):
    asyncio.run(add_to_tech_team(name))


if __name__ == '__main__':
    arguments = docopt.docopt(__doc__, version='0.1')
    if arguments.get('invite'):
        invite()
    elif arguments.get('add-to-tech-team'):
        add_to_team(arguments.get('<name>'))
