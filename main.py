import requests
import json
import datetime

BASE_URL = "https://qiita.com/api/v2/items"

with open(f"personal_config.json") as f:
    personal_config = f.read()

TOKEN = json.loads(personal_config)["token"]

def submit_article(path):
    with open(f"{path}/config.json") as f:
        conf = f.read()
    with open(f"{path}/item.md") as f:
        body = f.read()
    headers = {"Authorization": f"Bearer {TOKEN}"}
    item = json.loads(conf)
    item["body"] = body

    if item["id"] == "":
        res = requests.post(BASE_URL, headers=headers, json=item)
        with open(f"{path}/config.json", "w") as f:
            item["id"] = res.json()["id"]
            item["body"] = ""
            f.write(json.dumps(item))
        return res

    else:
        now = datetime.datetime.now()
        item["title"] += now.strftime("【%Y/%m/%d %H時更新】")
        item_id = item["id"]
        res = requests.patch(BASE_URL + f"/{item_id}", headers=headers, json=item)
        return res


if __name__ == "__main__":
    # res = submit_article("article", conf, body).json()
    res = submit_article("article")
    print(res["title"], res["url"])