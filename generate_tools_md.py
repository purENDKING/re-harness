import sys
sys.path.insert(0, '.')
from adapters.static_reva.client import ReVaClient

# 中文翻译
translations = {
    "Get Symbols Count": "获取符号总数",
    "Get Symbols": "获取符号列表",
    "Get Strings Count": "获取字符串总数",
    "Get Strings": "获取字符串列表",
    "Get Function Count": "获取函数总数",
    "Get Functions": "获取函数列表",
    "Get Functions by Similarity": "按相似度获取函数",
    "Set Function Prototype": "设置函数原型",
    "Get Undefined Function Candidates": "获取未定义函数候选",
    "Create Function": "创建函数",
    "Function Tags": "函数标签管理",
    "Get Data": "获取数据",
    "Apply Data Type": "应用数据类型",
    "Create Label": "创建标签",
    "Get Function Decompilation": "获取函数反编译代码",
    "Search Function Decompilations": "搜索反编译代码",
    "Rename Function Variables": "重命名函数变量",
    "Change Variable Data Types": "更改变量数据类型",
    "Add Decompilation Comment": "添加反编译注释",
    "Get Callers Decompiled": "获取调用者反编译代码",
    "Get Referencers Decompiled": "获取引用者反编译代码",
    "Get Memory Blocks": "获取内存块",
    "Read Memory": "读取内存",
    "Get Current Program": "获取当前程序",
    "List Open Programs": "列出打开的程序",
    "List Project Files": "列出项目文件",
    "Checkin Program": "提交程序到版本控制",
    "Analyze Program": "分析程序",
    "Change Processor": "更改处理器架构",
    "Import File": "导入文件",
    "Capture ReVa Debug Information": "捕获ReVa调试信息",
    "Find Cross References": "查找交叉引用",
    "Get Data Type Archives": "获取数据类型归档",
    "Get Data Types": "获取数据类型",
    "Get Data Type by String": "通过字符串获取数据类型",
    "Parse C Structure": "解析C结构体",
    "Validate C Structure": "验证C结构体",
    "Get Structure Info": "获取结构体信息",
    "List Structures": "列出结构体",
    "Apply Structure": "应用结构体",
    "Delete Structure": "删除结构体",
    "Parse C Header": "解析C头文件",
    "Set Comment": "设置注释",
    "Get Comments": "获取注释",
    "Remove Comment": "删除注释",
    "Search Comments": "搜索注释",
    "Set Bookmark": "设置书签",
    "Get Bookmarks": "获取书签",
    "Remove Bookmark": "删除书签",
    "Search Bookmarks": "搜索书签",
    "List Bookmark Categories": "列出书签类别",
    "List Imports": "列出导入函数",
    "List Exports": "列出导出符号",
    "Find Import References": "查找导入引用",
    "Resolve Thunk": "解析Thunk",
    "Trace Data Flow Backward": "反向追踪数据流",
    "Trace Data Flow Forward": "正向追踪数据流",
    "Find Variable Accesses": "查找变量访问",
    "Get Call Graph": "获取调用图",
    "Get Call Tree": "获取调用树",
    "Find Common Callers": "查找公共调用者",
    "Find Constant Uses": "查找常量使用",
    "Find Constants in Range": "查找范围内的常量",
    "List Common Constants": "列出常用常量",
    "Analyze Vtable": "分析虚函数表",
    "Find Vtable Callers": "查找虚函数表调用者",
    "Find Vtables Containing Function": "查找包含函数的虚函数表",
}

client = ReVaClient()
result = client.ping()

md_content = """# ReVa-MCP 工具列表

> 共计 **67** 个工具

---

"""

for i, tool in enumerate(result['tools'], 1):
    title_cn = translations.get(tool.title, "")
    desc_en = tool.description

    md_content += f"""## {i}. `{tool.name}`

**{tool.title}** ({title_cn})

{desc_en}

"""

    # 参数表格
    required = tool.inputSchema.get('required', [])
    props = tool.inputSchema.get('properties', {})

    if props:
        md_content += """| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
"""
        for pname, pspec in props.items():
            ptype = pspec.get('type', 'any')
            pdesc = pspec.get('description', '').replace('\n', ' ').replace('|', '\\|')[:100]
            pdefault = pspec.get('default')
            is_required = pname in required

            type_str = f"`{ptype}`"
            req_str = "✓" if is_required else ""
            default_str = f"`{pdefault}`" if pdefault is not None else "-"

            md_content += f"| `{pname}` | {type_str} | {req_str} | {default_str} | {pdesc} |\n"

    md_content += "\n---\n\n"

with open('reva_tools.md', 'w', encoding='utf-8') as f:
    f.write(md_content)

print("已生成 reva_tools.md")