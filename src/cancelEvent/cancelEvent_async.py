import aiohttp
import asyncio
import logging
import warnings
from aiohttp import ClientSession, TCPConnector
import time
import random

# 配置日志
logging.basicConfig(filename='cancel_event.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s', encoding='utf-8')

# 定义两台服务器的基础URL和端口范围
servers = [
    {"base_url": "https://192.168.1.1", "ports": [9996, 9997, 9998, 9999]},
    {"base_url": "https://192.168.1.2", "ports": [9996, 9997, 9998, 9999]}
]

# 定义请求头
headers = {
    "_appid": "20210005",
    "_sign": "10311202C73304527F418C0E9D0D90855F2CC87D0C79D0CF69BD589829A22AF7",
    "_timestamp": "1693814463784",
    "_nonce": "aaaaaaaaaaaaaaaaaa",
    "secret": "d72494cb22644694a9e2ac2ed8c71236",
    "Content-Type": "application/json"
}

# 忽略不安全的请求警告
warnings.filterwarnings("ignore", category=UserWarning, module='urllib3')

# 从文件读取单号
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

# 异步队列
queue = asyncio.Queue()
for order_id in order_ids:
    queue.put_nowait(order_id)

# 统计失败的任务
failed_orders = set()

async def cancel_event(session: ClientSession, order_id: str, server: dict, port: int, max_retries: int = 3):
    """
    向指定服务器和端口发送取消事件请求。
    """
    url = f"{server['base_url']}:{port}/itsm/api/analysis/cancelEvent"
    body = {"userId": "20250114111", "faultNo": order_id}

    for attempt in range(max_retries):
        try:
            start_time = time.monotonic()
            async with session.post(url, headers=headers, ssl=False, json=body, timeout=aiohttp.ClientTimeout(total=10)) as response:
                response_text = await response.text()
                elapsed_time = time.monotonic() - start_time
                log_message = (f"FaultNo: {order_id}, Server: {server['base_url']}, Port: {port}, "
                               f"Status Code: {response.status}, Response: {response_text}, Elapsed Time: {elapsed_time:.2f}s")

                if response.status == 200 and "操作异常" not in response_text:
                    logging.info(log_message)
                    return  # 成功后直接返回
                else:
                    logging.error(f"业务异常 - {log_message}")

        except asyncio.TimeoutError:
            logging.error(f"FaultNo: {order_id}, 请求超时。")
        except aiohttp.ClientError as e:
            logging.error(f"FaultNo: {order_id}, 请求错误: {e}")
        except Exception as e:
            logging.error(f"FaultNo: {order_id}, 未知错误: {e}")

        # 动态退避，增加重试间隔
        await asyncio.sleep(2 ** attempt + random.uniform(0, 1))

    # 记录失败任务
    failed_orders.add(order_id)

async def worker(session: ClientSession, worker_id: int):
    """
    从队列中获取任务并执行。
    """
    while not queue.empty():
        order_id = await queue.get()
        server = servers[worker_id % len(servers)]
        port = server["ports"][worker_id % len(server["ports"])]
        await cancel_event(session, order_id, server, port)
        queue.task_done()

async def main():
    """
    主函数，启动异步任务并监控执行时间。
    """
    start_time = time.monotonic()

    connector = TCPConnector(limit_per_host=20, limit=100)  # 并发限制
    async with ClientSession(connector=connector) as session:
        workers = [worker(session, i) for i in range(8)]  # 每台服务器4个端口，共8个 worker
        await asyncio.gather(*workers)

    total_time = time.monotonic() - start_time
    logging.info(f"所有单子作废请求已处理完毕，总耗时: {total_time:.2f}s")
    print(f"所有单子作废请求已处理完毕，总耗时: {total_time:.2f}s")

    if failed_orders:
        logging.warning(f"失败的单号: {len(failed_orders)} 个 - {failed_orders}")
        print(f"失败的单号: {len(failed_orders)} 个 - {failed_orders}")

if __name__ == "__main__":
    asyncio.run(main())
