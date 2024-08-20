from contextlib import contextmanager

from tinydb import Query, TinyDB

DB_FILENAME = "docker_hub_images_info.json"


@contextmanager
def get_db():
    db = TinyDB(DB_FILENAME)
    try:
        yield db
    finally:
        db.close()


def get_all_items(table_name):
    with get_db() as db:
        table = db.table(table_name)
        return table.all()


def save_to_db(images):
    with get_db() as db:
        table = db.table("images")
        for image in images:
            table.upsert(image, Query().id == image["id"])
            with open("image_ids.txt", "a") as f:
                f.write(image["id"] + "\n")


def count_images():
    with get_db() as db:
        table = db.table("images")
        return len(table)
