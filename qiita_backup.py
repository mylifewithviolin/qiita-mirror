import os
import re
import requests

QIITA_API = "https://qiita.com/api/v2"
TOKEN = os.environ.get("QIITA_TOKEN")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}"
}

def fetch_items():
    """Qiita API から全記事を取得（ページング対応）"""
    items = []
    page = 1

    while True:
        url = f"{QIITA_API}/authenticated_user/items?page={page}&per_page=100"
        res = requests.get(url, headers=HEADERS)

        if res.status_code != 200:
            print("Error:", res.text)
            break

        data = res.json()
        if not data:
            break

        items.extend(data)
        page += 1

    return items


def sanitize(name):
    """ファイル名に使えない文字を置換"""
    return re.sub(r'[\\/*?:\"<>|]', '_', name)


def download_image(url, path):
    """画像をダウンロード"""
    img = requests.get(url).content
    with open(path, "wb") as f:
        f.write(img)


def save_item(item):
    """記事を Markdown + 画像付きで保存"""
    title = sanitize(item["title"])
    item_id = item["id"]

    dir_name = f"{item_id}_{title}"
    os.makedirs(dir_name, exist_ok=True)

    body = item["body"]

    # 画像URL抽出
    pattern = r'!

\[(.*?)\]

\((https://qiita-user-contents\.imgix\.net/.*?)\)'
    matches = re.findall(pattern, body)

    if matches:
        img_dir = os.path.join(dir_name, "images")
        os.makedirs(img_dir, exist_ok=True)

        for idx, (_, img_url) in enumerate(matches, start=1):
            img_name = f"{idx:03}.png"
            img_path = os.path.join(img_dir, img_name)

            download_image(img_url, img_path)

            # Markdown の画像URLを書き換え
            body = body.replace(img_url, f"./images/{img_name}")

    # Markdown 保存
    md_path = os.path.join(dir_name, "article.md")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(body)


def main():
    print("Fetching Qiita items...")
    items = fetch_items()
    print(f"Found {len(items)} items.")

    for item in items:
        print("Saving:", item["title"])
        save_item(item)

    print("Done.")


if __name__ == "__main__":
    main()
