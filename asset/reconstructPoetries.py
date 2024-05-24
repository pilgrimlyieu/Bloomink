import os
import json

def combine_json_files(folder_path):
    # 创建一个空列表来存储所有的诗词数据
    poetries = []

    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 检查文件是否为 JSON 文件
        if filename.endswith('.json'):
            # 打开并读取 JSON 文件
            with open(os.path.join(folder_path, filename), 'r', encoding='utf-8') as file:
                data = json.load(file)
                # 将读取的数据添加到列表中
                poetries.append(data)

    # 按照 star 属性对列表中的数据进行排序
    poetries.sort(key=lambda x: x['star'], reverse=True)

    # 重新设置每个诗词的 id 为其在列表中的索引
    for i, poetry in enumerate(poetries):
        poetry['id'] = i

    # 将列表保存到一个新的 JSON 文件中
    with open('poetry.json', 'w', encoding='utf-8') as file:
        json.dump({'poetries': poetries}, file, ensure_ascii=False, indent=4)

# 调用函数，传入 JSON 文件所在的文件夹路径
combine_json_files('./poetry')
