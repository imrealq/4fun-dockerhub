from collections import defaultdict

from tinydb import TinyDB


def count_images_by_category(items):
    category_counts = defaultdict(int)
    for item in items:
        for category in item["categories"]:
            category_counts[category["name"]] += 1

    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
    print("Tổng số image theo categories:")
    for category, count in sorted_categories:
        print(f"\t{category}: {count}")


def top_by_category(items, num=5):
    category_items = defaultdict(list)
    for item in items:
        for category in item["categories"]:
            category_items[category["name"]].append((item["id"], item["star_count"]))

    print("\nTop 5 mỗi category có star_count từ cao đến thấp:")
    for category, items in category_items.items():
        print(f"\n\t{category}:")
        sorted_items = sorted(items, key=lambda x: x[1], reverse=True)[:num]
        for i, (id, star_count) in enumerate(sorted_items, 1):
            print(f"\t\t{i}. {id}: {star_count} stars")


def top_star_count(items, num=10):
    sorted_items = sorted(items, key=lambda x: x["star_count"], reverse=True)[:10]

    print(f"\nTop {num} images có star count cao nhất:")
    for i, item in enumerate(sorted_items, 1):
        categories = ", ".join([cat["name"] for cat in item["categories"]])
        print(
            f"{i}. {item['id']}: {item['star_count']} stars"
            + f"\n\t- Categories: {categories}"
            + f"\n\t- Description: {item['short_description']}"
        )


def main():

    db_filename = "docker_hub_images_info.json"
    db = TinyDB(db_filename)

    table = db.table("images")
    items = table.all()
    count_images_by_category(items)
    top_by_category(items)
    top_star_count(items)

    db.close()
    return


if __name__ == "__main__":
    main()
