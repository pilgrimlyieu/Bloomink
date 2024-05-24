import json

def generate_tags_file():
    # 打开并读取 poetry.json 文件
    with open('poetries.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        poetries = data['poetries']

    # 创建一个字典来存储每个标签及其相关的诗词
    tags_dict = {}

    # 遍历每个诗词
    for poetry in poetries:
        # 遍历每个诗词的每个标签
        for tag in poetry['tags']:
            # 如果标签不在字典中，则在字典中添加该标签
            if tag not in tags_dict:
                tags_dict[tag] = []
            # 将诗词的 id 和 star 添加到该标签的诗词列表中
            tags_dict[tag].append({'id': poetry['id'], 'star': poetry['star']})

    # 创建一个新的列表，其中每个元素是一个字典，包含 tid、tag、sum 和 poems
    tags = []
    for tid, (tag, poems) in enumerate(tags_dict.items()):
        # 对每个标签的诗词列表按 star 排序
        poems.sort(key=lambda x: x['star'], reverse=True)
        # 为每首诗词添加 pid
        for pid, poem in enumerate(poems):
            poem['pid'] = pid
        # 将标签添加到列表中
        tags.append({'tid': tid, 'tag': tag, 'sum': len(poems), 'poems': poems})

    # 对标签列表按前十首诗词的 star 总数排序
    tags.sort(key=lambda x: sum(poem['star'] for poem in x['poems'][:10]), reverse=True)

    # 将新的列表保存到 tags.json 文件中
    with open('tags.json', 'w', encoding='utf-8') as file:
        json.dump({'tags': tags}, file, ensure_ascii=False, indent=4)

# 调用函数
generate_tags_file()
