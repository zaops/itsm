## 🚀 项目列表

### 项目1：事件单批量作废
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
