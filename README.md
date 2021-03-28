# 掌门好老师 试卷导出工具

> 仅可作为方便老师导出试卷/课件等数据，请勿用作商业用途。

## 依赖

+ pycryptodome
+ requests
+ HTMLParser

### Example:
```python
from core.api import ZmTool


tool = ZmTool("手机", "老师端密码")

# 仅导出试卷：_type=0 / 仅导出答案：_type-1
tool.process_question(resource_id=123, _type=0)

# ls 课件文件夹，根目录传0
print(tool.list_doc_dir(parent_id=0))

# 导出课件
tool.process_doc(doc_id=123)
```

tips:
1. _type的取值：目前仅支持 `仅导出试卷（_type传入0）` 和 `仅导出答案（_type传入1）两种方式。`
2. resource_id的获取：核心原理是借用掌门老师端的接口`findResourceDetailById`，如何拿到其中的`resourceId`这里不进行赘述。
3. 相关配置可自行更改`utils/settings.py`

## 未来支持

+ 更多的数据导出格式，目前仅支持html。需要pdf的同学可chrome打开另存为pdf，效果较好。
+ `resourceId`的更为友好的获取方式。
+ 更多官方没做但很实用而老师手动做又很浪费时间的功能。

## 其他

+ zml解析由于复杂的样式导致导出的课件视觉效果不好，推荐根据接口拉下来的数据自己实现zml课件页面的渲染。
+ 如有侵权请联系删除，邮箱：vaskka@outlook.com
