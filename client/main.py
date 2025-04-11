
import os
import hashlib
import pymysql
from uuid import uuid4 as random_uuid, UUID
from datetime import datetime

db = pymysql.connect(
    host="127.0.0.1", port=3306, user="root", password="password",
    database="kxpage"
)

TARGET_STORE = "../images/"

def add_single_record(
    name: str, time: str, image_path: str, href: str,
    primary: bool = False
) -> UUID:
    if not time:
        dtime = datetime.now()
    else:
        dtime = datetime.strptime(time, "%Y/%m/%d %H:%M:%S")
    time_str = dtime.strftime("%Y-%m-%d %H:%M:%S")
    primary = 1 if primary else 0
    if image_path:
        _, ext = os.path.split(image_path)[1].split(".")

        with open(image_path, "rb") as rd:
            image_data = rd.read()
        sha = hashlib.sha256()
        sha.update(image_data)
        sha_result = sha.hexdigest()
        sha_path = f"{sha_result}.{ext}"

        with open(
            os.path.join(TARGET_STORE, sha_path), "wb"
        ) as wt:
            wt.write(image_data)
    else:
        sha_path = ""
    record_uuid = random_uuid()
    cursor = db.cursor()
    cursor.execute(
f"""INSERT INTO `events`(`uuid`,`ev_time`,`ev_title`,`ev_href`,`show_image`,`image_hash`)
VALUES('{str(record_uuid)}','{time_str}','{name}','{href}',{primary},'{sha_path}');"""
    )
    cursor.close()
    db.commit()

if __name__ == '__main__':

    add_single_record(
        "测试活动",
        "",
        "./image.png",
        "https://www.baidu.com",
        True
    )
