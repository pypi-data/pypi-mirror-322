# feigua-data-collection
飞瓜智投数据采集工具

## 安装
```bash
pip install feigua-data-collection
```

## 使用方法
### 连接浏览器
```python
from PxxDataCollection import Collector

collector = Collector()
collector.connect_browser(port=9527)

```

### 获取团队管理数据

在获取数据之前可以现在浏览器中打开目标页面, 这样子就可以直接使用已打开的页面

```python
# 获取 团队管理-主播排行-主播排行 数据
result = collector.team_manage.anchor.get__anchor_rank__detail(
    begin_date='2025-01-20', end_date='2025-01-20'
)

# ... 其他数据获取方法与上面类似
```