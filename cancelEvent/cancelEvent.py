import requests
import json
import logging

# 配置日志
logging.basicConfig(filename='cancel_event.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

# 定义请求头
headers = {
    "_appid": "20210005",
    "_sign": "10311202C73304527F418C0E9D0D90855F2CC87D0C79D0CF69BD589829A22AF7",
    "_timestamp": "1693814463784",
    "_nonce": "aaaaaaaaaaaaaaaaaa",
    "secret": "d72494cb22644694a9e2ac2ed8c71236",
    "Content-Type": "application/json"
}

# 定义URL
url = "https://IP地址:端口/itsm/api/analysis/cancelEvent"

try:
    with open("fault_nos.txt", "r", encoding='utf-8') as f:
        order_ids = [line.strip() for line in f]
except FileNotFoundError:
    logging.error("fault_nos.txt 文件未找到。")
    print("错误：fault_nos.txt 文件未找到。")
    exit()
except Exception as e:
    logging.error(f"读取 fault_nos.txt 文件时发生错误: {e}")
    print(f"错误：读取 fault_nos.txt 文件时发生错误: {e}")
    exit()

# 批量作废接口调用
for order_id in order_ids:
    # 定义请求体
    body = {
        "userId": "20250114111",
        "faultNo": order_id
    }

    try:
        # 发送POST请求，设置超时时间
        response = requests.post(url, headers=headers, verify=False, data=json.dumps(body), timeout=(10, 30))
        response.raise_for_status() # 检查HTTP状态码，如果不是200则抛出异常

        # 打印并记录成功日志
        log_message = f"FaultNo: {order_id}, Status Code: {response.status_code}, Response: {response.text}"
        print(log_message)
        logging.info(log_message)

    except requests.exceptions.Timeout as e:
        error_message = f"FaultNo: {order_id}, 请求超时: {e}"
        print(error_message)
        logging.error(error_message)
        continue # 跳过当前循环，继续下一个单子

    except requests.exceptions.RequestException as e:
        error_message = f"FaultNo: {order_id}, 请求发生错误: {e}"
        print(error_message)
        logging.error(error_message)
        continue # 跳过当前循环，继续下一个单子
    except Exception as e:
        error_message = f"FaultNo: {order_id}, 发生未知错误: {e}"
        print(error_message)
        logging.error(error_message)
        continue

print("所有单子作废请求已处理完毕。")
logging.info("所有单子作废请求已处理完毕。")