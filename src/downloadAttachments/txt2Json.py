import json

# 读取文件内容
try:
    with open('attachments.txt', 'r', encoding='utf-8-sig') as file:
        lines = file.readlines()
except FileNotFoundError:
    print("文件 attachments.txt 未找到。")
    exit(1)

# 解析每行并创建关联列表
mappings = []
for line in lines:
    # 去掉行末的换行符并尝试分割
    cleaned_line = line.strip()
    if cleaned_line:  # 确保不是空行
        # 尝试使用制表符或空格作为分隔符
        parts = cleaned_line.split('\t') if '\t' in cleaned_line else cleaned_line.split(' ', 1)
        if len(parts) == 2:  # 确保有两个部分
            mappings.append({
                'ID': parts[0],
                'FileName': parts[1]
            })
        else:
            print(f"警告：行 '{line}' 格式不正确，跳过。")

# 将列表转换为 JSON 格式并写入文件
if mappings:  # 只有当有数据时才写入 JSON
    with open('attachments.json', 'w', encoding='utf-8') as json_file:
        json.dump(mappings, json_file, ensure_ascii=False, indent=2)
    print("JSON 文件已生成，包含了所有的文件映射关系。")
else:
    print("没有有效的数据可以写入 JSON 文件。")