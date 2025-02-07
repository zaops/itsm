## 🚀 Tools列表

### Toll-1：事件单批量作废
- 位置：`/cancelEvent`
- 功能：
  - 通过POST请求，批量作废事件单
- 工具：
  - Python 3.12
  - 依赖三方库：aiohttp
- 文件说明：
  - `cancelEvent.py` 普通方式调用
  - `cancelEvent_async.py` 异步方式并发调用
  - `fault_nos.txt` 存放单号
  - `cancel_event.log`日志

### Toll-2：批量下载附件
- 位置：`/downloadAttachments`
- 功能：
  - 通过requests请求，批量下载附件
- 工具：
  - Python 3.12
  - 依赖三方库：requests
- 文件说明：
  - `main_downloader.py` 主脚本用于下载
  - `txt2Json.py` 将txt文件转换为json文件
  - `attachments.txt` 存放附件ID和附件名
  - `attachments.json` 转换后的json格式
  - `downloads(文件夹)` 存放已下载的附件
