from collections import defaultdict
from datetime import datetime

import matplotlib.pyplot as plt
import seaborn as sns

from db import get_all_items


def create_full_pie_chart(categories, sizes):
    colors = sns.color_palette("husl", len(categories))

    plt.figure(figsize=(12, 8))
    wedges, _ = plt.pie(sizes, colors=colors, startangle=90, wedgeprops=dict(width=0.3))

    centre_circle = plt.Circle((0, 0), 0.70, fc="white")
    fig = plt.gcf()
    fig.gca().add_artist(centre_circle)

    plt.axis("equal")
    plt.title("Categories of Docker Hub Images", fontsize=16)

    plt.legend(wedges, categories, loc="center left", bbox_to_anchor=(1, 0, 0.5, 1))

    plt.savefig("docker_hub_categories_full_pie.png", dpi=300, bbox_inches="tight")
    plt.close()


def count_images_by_category(items):
    category_counts = defaultdict(int)
    for item in items:
        for category in item["categories"]:
            category_counts[category["name"]] += 1

    sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)

    output = "## Tổng số image theo categories:\n\n"
    for category, count in sorted_categories:
        output += f"- {category}: {count}\n"

    categories, sizes = zip(*sorted_categories)
    create_full_pie_chart(categories, sizes)

    output += "\n![Pie Chart of Docker Hub Categories](docker_hub_categories_pie.png)\n\n"

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
    items = get_all_items("images")
    markdown_report = generate_markdown_report(items)
    write_markdown_to_file(markdown_report)

    return


if __name__ == "__main__":
    main()
