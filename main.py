import aiohttp
import asyncio
import json
from tinydb import TinyDB, Query


def get_urls():
    return [
        "https://hub.docker.com/api/search/v3/catalog/search?query=&extension_reviewed=&from=0&size=25",
        "https://hub.docker.com/api/search/v3/catalog/search?query=&extension_reviewed=&from=25&size=25",
    ]


async def fetch(session, url):
    try:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
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
        images = resp.get('results', [])
        save_to_db(db, images)
    db.close()

    print(f"Results saved to {db_filename}")


if __name__ == "__main__":
    asyncio.run(main())
