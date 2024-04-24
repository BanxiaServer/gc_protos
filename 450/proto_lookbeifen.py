import re
import os

def find_message(data_types):
    messages = []

    for data_type, count in data_types.items():
        # 构建数据类型的正则表达式，例如：\buint32\b
        data_type_pattern = re.compile(r"\b" + data_type + r"\b")

        # 获取当前工作目录
        current_dir = os.path.dirname(__file__)
        
        # 读取 proto 文件
        proto_file = os.path.join(current_dir, "output.proto")
        with open(proto_file, "r") as file:
            proto_content = file.read()

        # 查找匹配项
        for match in data_type_pattern.finditer(proto_content):
            # 获取匹配结果的开始和结束位置
            data_type_start = match.start()
            data_type_end = match.end()

            # 提取字段名称
            field_name = proto_content[data_type_end:].split("=", 1)[0].strip()

            # 查找包含该字段的 message
            message_end = proto_content.find("}", data_type_end)
            message_start = proto_content.rfind("message", 0, data_type_start)
            message_content = proto_content[message_start:message_end + 1]

            # 计算该 message 中指定数据类型的出现次数
            type_count = message_content.count(data_type)

            # 如果出现次数符合要求且字段名称不为空，则将该 message 加入结果列表
            if type_count == count and field_name:
                messages.append(message_content)

    return messages

# 示例数据类型和出现次数
data_types = {
    "bool": 1,
    "uint32": 2
}

result = find_message(data_types)

if result:
    # 获取当前工作目录
    current_dir = os.path.dirname(__file__)
    output_path = os.path.join(current_dir, "output.proto")  # 输出文件路径
    os.makedirs(current_dir, exist_ok=True)  # 确保输出目录存在
    with open(output_path, "w") as f:
        for idx, message in enumerate(result):
            print(message)
            f.write(f"// Message {idx+1}\n")
            f.write(message)
            f.write("\n\n")
else:
    print("未找到符合条件的 message")
