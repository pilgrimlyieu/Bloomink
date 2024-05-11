# 保留 star 前 1000 的诗词（原数据 72000+）

import os
import json
import heapq


def keep_top_star_files(directory, count):
    # 创建一个列表来存储 (star, filename) 对
    star_files = []

    # 遍历目录中的所有文件
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), "r") as f:
            data = json.load(f)
            star = data.get("star", 0)
            star_files.append((star, filename))

    # 只保留 star 数量排名前 count 的文件
    top_star_files = set(file for star, file in heapq.nlargest(count, star_files))

    # 删除 star 数量不在前 count 的文件
    for filename in os.listdir(directory):
        if filename.endswith(".json") and filename not in top_star_files:
            os.remove(os.path.join(directory, filename))


# 使用函数
count = 1000
source = "./poetry"
keep_top_star_files(source, count)
