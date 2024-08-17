import asyncio
import json
import random
import time

import aiohttp
import requests
from fake_useragent import UserAgent
from tinydb import Query, TinyDB

ua = UserAgent()

SIZE = 25
URL_TEMPLATE = "https://hub.docker.com/api/search/v3/catalog/search?query=&extension_reviewed=&from={0}&size={1}"


def find_max_from_index(max_value=10000, tolerance=200):
    low = 0
    high = max_value

    while high - low > tolerance:
        mid = (low + high) // 2

        url = URL_TEMPLATE.format(mid, tolerance)
        resp = fetch_once(url)
        if resp:
            low = mid
        else:
            high = mid

        time.sleep(random.uniform(1, 3))
    return high


def get_urls():
    urls = []
    total_items = find_max_from_index()

    items_per_page = SIZE
    remaining_items = total_items % items_per_page
    full_pages = total_items // items_per_page

    for page in range(full_pages):
        start_index = page * items_per_page
        url = URL_TEMPLATE.format(start_index, items_per_page)
        urls.append(url)

    last_full_page_index = full_pages * items_per_page
    items_per_partial_page = 10
    partial_pages = remaining_items // items_per_partial_page

    for partial_page in range(partial_pages):
        start_index = last_full_page_index + partial_page * items_per_partial_page
        url = URL_TEMPLATE.format(start_index, items_per_partial_page)
        urls.append(url)

    return urls


def fetch_once(url, headers=None, timeout=10, max_retries=3):
    if headers is None:
        headers = {"User-Agent": ua.random}

    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            if response.status_code == 200:
                return response.text
            # elif response.status_code == 429:  # Too Many Requests
            #     wait_time = int(response.headers.get('Retry-After', 60))
            #     print(f"Rate limited. Waiting for {wait_time} seconds.")
            #     time.sleep(wait_time)
            # else:
            #     print(f"Unexpected status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")

        # wait for retrying
        time.sleep(random.uniform(1, 5))

    return None


async def fetch(session, url, headers=None, timeout=10, max_retries=3):
    if headers is None:
        headers = {"User-Agent": ua.random}

    for attempt in range(max_retries):
        try:
            async with session.get(url, headers=headers, timeout=timeout) as response:
                if response.status == 200:
                    return await response.text()
                # elif response.status == 429:  # Too Many Requests
                #     wait_time = int(response.headers.get('Retry-After', 60))
                #     print(f"Rate limited. Waiting for {wait_time} seconds.")
                #     await asyncio.sleep(wait_time)
                # else:
                #     print(f"Unexpected status code: {response.status}")
        except aiohttp.ClientError as e:
            print(f"Error fetching {url}: {e}")

        # wait for retrying
        await asyncio.sleep(random.uniform(1, 5))

    return None


async def crawl(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)


def save_to_db(db, images):
    table = db.table("images")
    for image in images:
        table.upsert(image, Query().id == id)


async def main():
    urls = get_urls()

    db_filename = "docker_hub_images_info.json"
    crawl_results = await crawl(urls)

    db = TinyDB(db_filename)
    for result in crawl_results:
        resp = json.loads(result)
        images = resp.get("results", [])
        save_to_db(db, images)
    db.close()

    print(f"Results saved to {db_filename}")


if __name__ == "__main__":
    asyncio.run(main())
