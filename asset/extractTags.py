import os
import json

# 创建一个空字典来存储标签和对应的诗词信息
tags_dict = {}

source_folder = "./poetry"
target_folder = "./tag"
star_count = 10

# 遍历文件夹中的每个 JSON 文件
for filename in os.listdir(source_folder):
    with open(os.path.join(source_folder, filename), "r", encoding="utf-8") as f:
        data = json.load(f)
        tags = data["tags"]
        for tag in tags:
            if tag not in tags_dict:
                tags_dict[tag] = []
            tags_dict[tag].append({"id": data["id"], "star": data["star"]})

# 对字典中的每个标签，将其诗词列表按照 star 数递减的顺序排序
for tag, poems in tags_dict.items():
    tags_dict[tag] = sorted(poems, key=lambda x: x["star"], reverse=True)
    for pid, poem in enumerate(tags_dict[tag], start=1):
        poem["pid"] = pid

# 计算每个标签的前几首诗词的 star 总和
tag_star_sum = {
    tag: sum(poem["star"] for poem in poems[:star_count])
    for tag, poems in tags_dict.items()
}

# 根据 star 总和排序标签
sorted_tags = sorted(tag_star_sum.items(), key=lambda x: x[1], reverse=True)

# 将排序后的数据写入新的 JSON 文件
for tid, (tag, _) in enumerate(sorted_tags, start=1):
    poems = tags_dict[tag]
    with open(
        os.path.join(target_folder, f"{tid:03d}-{tag}.json"), "w", encoding="utf-8"
    ) as f:
        json.dump(
            {"tid": tid, "tag": tag, "sum": len(poems), "poems": tags_dict[tag]},
            f,
            ensure_ascii=False,
            indent=4,
        )
