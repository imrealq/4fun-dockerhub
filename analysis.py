from collections import defaultdict
from datetime import datetime

from tinydb import TinyDB


def count_images_by_category(items):
    category_counts = defaultdict(int)
    for item in items:
        for category in item["categories"]:
            category_counts[category["name"]] += 1

    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)

    output = "## Tổng số image theo categories:\n\n"
    for category, count in sorted_categories:
        output += f"- {category}: {count}\n"

    return output


def top_by_category(items, num=5):
    category_items = defaultdict(list)
    for item in items:
        for category in item["categories"]:
            category_items[category["name"]].append((item["id"], item["star_count"]))

    output = f"\n## Top {num} mỗi category có star_count từ cao đến thấp:\n"
    for category, items in category_items.items():
        output += f"\n### {category}:\n"
        sorted_items = sorted(items, key=lambda x: x[1], reverse=True)[:num]
        for i, (id, star_count) in enumerate(sorted_items, 1):
            output += f"{i}. {id}: {star_count} stars\n"

    return output


def top_star_count(items, num=10):
    sorted_items = sorted(items, key=lambda x: x["star_count"], reverse=True)[:num]

    output = f"\n## Top {num} images có star count cao nhất:\n\n"
    for i, item in enumerate(sorted_items, 1):
        categories = ", ".join([cat["name"] for cat in item["categories"]])
        output += (
            f"{i}. **{item['id']}**: {item['star_count']} stars\n"
            f"   - Categories: {categories}\n"
            f"   - Description: {item['short_description']}\n\n"
        )

    return output


def generate_markdown_report(items):
    current_time = datetime.now().strftime("%Y-%m-%d")
    report = f"# Docker Image Analysis Report\n\n"
    report += f"**Ngày tạo:** {current_time}\n\n"
    report += "---\n\n"
    report += count_images_by_category(items)
    report += top_by_category(items)
    report += top_star_count(items, num=20)
    return report


def write_markdown_to_file(markdown_content, filename="README.md"):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown_content)
    print(f"Report has been written to {filename}")


def main():

    db_filename = "docker_hub_images_info.json"
    db = TinyDB(db_filename)

    table = db.table("images")
    items = table.all()
    markdown_report = generate_markdown_report(items)
    write_markdown_to_file(markdown_report)

    db.close()
    return


if __name__ == "__main__":
    main()
