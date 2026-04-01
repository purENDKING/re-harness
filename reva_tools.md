# ReVa-MCP 工具列表

> 共计 **67** 个工具

---

## 1. `get-symbols-count`

**Get Symbols Count**（获取符号总数）

获取程序中符号的总数量（在调用 get-symbols 之前使用以规划分页）

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `includeExternal` | `boolean` |  | `False` | 是否在计数中包含外部符号 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `filterDefaultNames` | `boolean` |  | `True` | 是否过滤掉 Ghidra 生成的默认名称（如 FUN_、DAT_ 等） |

---

## 2. `get-symbols`

**Get Symbols**（获取符号列表）

分页获取程序中的符号（先用 get-symbols-count 确定总数）

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `includeExternal` | `boolean` |  | `False` | 是否在结果中包含外部符号 |
| `startIndex` | `integer` |  | `0` | 分页起始索引（从 0 开始） |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `filterDefaultNames` | `boolean` |  | `True` | 是否过滤掉 Ghidra 生成的默认名称（如 FUN_、DAT_ 等） |
| `maxCount` | `integer` |  | `200` | 返回的最大符号数（建议每次获取 200 个） |

---

## 3. `get-strings-count`

**Get Strings Count**（获取字符串总数）

获取程序中字符串的总数量（在调用 get-strings 之前使用以规划分页）

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |

---

## 4. `get-strings`

**Get Strings**（获取字符串列表）

分页获取程序中的字符串，可选通过正则表达式过滤或按相似度排序。先用 get-strings-count 确定总数。

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `searchString` | `string` |  | - | 按与此字符串的相似度排序结果（与 regexPattern 互斥） |
| `startIndex` | `integer` |  | `0` | 分页起始索引（从 0 开始） |
| `includeReferencingFunctions` | `boolean` |  | `False` | 包含引用每个字符串的函数列表（每个字符串最多 100 个） |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `regexPattern` | `string` |  | - | 过滤匹配此正则表达式的字符串（与 searchString 互斥） |
| `maxCount` | `integer` |  | `100` | 返回的最大字符串数（建议每次最多 100 个） |

---

## 5. `get-function-count`

**Get Function Count**（获取函数总数）

获取程序中函数的总数量（在调用 get-functions 之前使用以规划分页）

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `filterDefaultNames` | `boolean` |  | `True` | 是否过滤掉 Ghidra 生成的默认名称（如 FUN_、DAT_ 等） |

---

## 6. `get-functions`

**Get Functions**（获取函数列表）

获取程序中的函数列表（先用 get-function-count 确定总数）

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `startIndex` | `integer` |  | `0` | 分页起始索引（从 0 开始） |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `filterDefaultNames` | `boolean` |  | `True` | 是否过滤掉 Ghidra 生成的默认名称（如 FUN_、DAT_ 等） |
| `untagged` | `boolean` |  | `False` | 仅返回没有标签的函数（与 filterByTag 互斥） |
| `filterByTag` | `string` |  | - | 仅返回具有此标签的函数 |
| `maxCount` | `integer` |  | `100` | 返回的最大函数数（建议每次最多 100 个） |
| `verbose` | `boolean` |  | `False` | 返回完整函数详情。为 false 时返回紧凑结果（名称、地址、大小、标签等） |

---

## 7. `get-functions-by-similarity`

**Get Functions by Similarity**（按相似度获取函数）

分页获取程序中的函数，按与给定函数名的相似度排序（先用 get-function-count 确定总数）

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `searchString` | `string` | ✓ | - | 用于比较相似度的函数名 |
| `startIndex` | `integer` |  | `0` | 分页起始索引（从 0 开始） |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `filterDefaultNames` | `boolean` |  | `True` | 是否过滤掉 Ghidra 生成的默认名称 |
| `maxCount` | `integer` |  | `100` | 返回的最大函数数 |
| `verbose` | `boolean` |  | `False` | 返回完整函数详情 |

---

## 8. `set-function-prototype`

**Set Function Prototype**（设置函数原型）

使用 C 风格函数签名设置或更新函数原型。可以创建新函数或更新现有函数。

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `signature` | `string` | ✓ | - | C 风格函数签名（如 'int main(int argc, char** argv)'） |
| `location` | `string` | ✓ | - | 函数所在的地址或符号名 |
| `createIfNotExists` | `boolean` |  | `True` | 如果位置不存在函数则创建 |

---

## 9. `get-undefined-function-candidates`

**Get Undefined Function Candidates**（获取未定义函数候选）

查找可执行内存中被引用但未定义为函数的有效指令地址。包括 CALL 引用和 DATA 引用（函数指针、回调、异常处理程序）。

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `startIndex` | `integer` |  | `0` | 分页起始索引（从 0 开始） |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `maxCandidates` | `integer` |  | `100` | 返回的最大候选数 |
| `minReferenceCount` | `integer` |  | `1` | 成为候选所需的最小引用数 |

---

## 10. `create-function`

**Create Function**（创建函数）

在指定地址创建函数，Ghidra 会自动分析代码确定函数体、参数和返回类型。

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `address` | `string` | ✓ | - | 创建函数的地址（如 '0x401000'） |
| `name` | `string` |  | - | 可选的函数名。如未提供，Ghidra 将生成默认名称 |

---

## 11. `function-tags`

**Function Tags**（函数标签管理）

管理函数标签，用于对函数进行分类（如 'AI'、'rendering'）。

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `mode` | `string` | ✓ | - | 操作：'get'（获取）、'set'（替换）、'add'（添加）、'remove'（删除）、'list'（列出所有） |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `function` | `string` |  | - | 函数名或地址（get/set/add/remove 模式必需） |
| `tags` | `array` |  | - | 标签名列表 |

---

## 12. `get-data`

**Get Data**（获取数据）

获取程序中指定地址或符号的数据

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `addressOrSymbol` | `string` | ✓ | - | 地址或符号名（如 '0x00400000' 或 'main'） |

---

## 13. `apply-data-type`

**Apply Data Type**（应用数据类型）

将数据类型应用到程序中的指定地址或符号

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `dataTypeString` | `string` | ✓ | - | 数据类型的字符串表示（如 'char**'、'int[10]'） |
| `archiveName` | `string` |  | - | 数据类型归档名称（可选，默认搜索所有归档） |
| `addressOrSymbol` | `string` | ✓ | - | 地址或符号名 |

---

## 14. `create-label`

**Create Label**（创建标签）

在程序中的指定地址创建标签

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `setAsPrimary` | `boolean` |  | `True` | 如果地址存在其他标签，是否将此标签设置为主标签 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `addressOrSymbol` | `string` | ✓ | - | 地址或符号名 |
| `labelName` | `string` | ✓ | - | 标签名称 |

---

## 15. `get-decompilation`

**Get Function Decompilation**（获取函数反编译代码）

获取函数的反编译代码，支持行范围。默认 50 行以节省上下文。

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionNameOrAddress` | `string` | ✓ | - | 函数名、地址或符号 |
| `includeCallers` | `boolean` |  | `False` | 包含调用此函数的函数列表 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `offset` | `integer` |  | `1` | 开始读取的行号（从 1 开始） |
| `includeDisassembly` | `boolean` |  | `False` | 是否包含汇编列表 |
| `includeIncomingReferences` | `boolean` |  | `True` | 是否包含传入交叉引用 |
| `limit` | `integer` |  | `50` | 返回的行数 |
| `includeReferenceContext` | `boolean` |  | `True` | 是否包含调用函数的代码上下文片段 |
| `includeComments` | `boolean` |  | `False` | 是否包含注释 |
| `includeCallees` | `boolean` |  | `False` | 包含此函数调用的函数列表 |
| `signatureOnly` | `boolean` |  | `False` | 仅返回签名/元数据，不返回反编译代码 |

---

## 16. `search-decompilation`

**Search Function Decompilations**（搜索反编译代码）

在程序中所有函数的反编译代码中搜索模式

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `overrideMaxFunctionsLimit` | `boolean` |  | `False` | 是否覆盖最大函数限制（谨慎使用） |
| `maxResults` | `integer` |  | `50` | 返回的最大搜索结果数 |
| `caseSensitive` | `boolean` |  | `False` | 是否区分大小写 |
| `pattern` | `string` | ✓ | - | 要搜索的正则表达式模式 |

---

## 17. `rename-variables`

**Rename Function Variables**（重命名函数变量）

重命名反编译函数中的变量

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionNameOrAddress` | `string` | ✓ | - | 函数名、地址或符号 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `variableMappings` | `object` | ✓ | - | 旧变量名到新变量名的映射 |

---

## 18. `change-variable-datatypes`

**Change Variable Data Types**（更改变量数据类型）

更改反编译函数中变量的数据类型

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionNameOrAddress` | `string` | ✓ | - | 函数名、地址或符号 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `datatypeMappings` | `object` | ✓ | - | 变量名到新数据类型的映射 |
| `archiveName` | `string` |  | - | 数据类型归档名称（可选） |

---

## 19. `set-decompilation-comment`

**Add Decompilation Comment**（添加反编译注释）

在反编译代码的指定行设置注释

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionNameOrAddress` | `string` | ✓ | - | 函数名、地址或符号 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `commentType` | `string` |  | `eol` | 注释类型：'pre' 或 'eol'（行尾） |
| `comment` | `string` | ✓ | - | 注释文本 |
| `lineNumber` | `integer` | ✓ | - | 行号（从 1 开始） |

---

## 20. `get-callers-decompiled`

**Get Callers Decompiled**（获取调用者反编译代码）

反编译所有调用目标函数的函数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionNameOrAddress` | `string` | ✓ | - | 目标函数名或地址 |
| `startIndex` | `integer` |  | `0` | 分页起始索引 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `includeCallContext` | `boolean` |  | `True` | 是否突出显示调用行 |
| `maxCallers` | `integer` |  | `10` | 反编译的最大调用函数数 |

---

## 21. `get-referencers-decompiled`

**Get Referencers Decompiled**（获取引用者反编译代码）

反编译所有引用特定地址或符号的函数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `startIndex` | `integer` |  | `0` | 分页起始索引 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `maxReferencers` | `integer` |  | `10` | 反编译的最大引用函数数 |
| `addressOrSymbol` | `string` | ✓ | - | 目标地址或符号名 |
| `includeRefContext` | `boolean` |  | `True` | 是否包含引用行号 |
| `includeDataRefs` | `boolean` |  | `True` | 是否包含数据引用（读/写） |

---

## 22. `get-memory-blocks`

**Get Memory Blocks**（获取内存块）

获取所选程序的内存块

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |

---

## 23. `read-memory`

**Read Memory**（读取内存）

读取指定地址的内存

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `addressOrSymbol` | `string` | ✓ | - | 地址或符号名 |
| `length` | `integer` |  | `16` | 要读取的字节数 |
| `format` | `string` |  | `hex` | 输出格式：'hex'、'bytes' 或 'both' |

---

## 24. `get-current-program`

**Get Current Program**（获取当前程序）

获取 Ghidra 中当前活动的程序

无参数

---

## 25. `list-open-programs`

**List Open Programs**（列出打开的程序）

列出 Ghidra 中所有打开的程序

无参数

---

## 26. `list-project-files`

**List Project Files**（列出项目文件）

列出 Ghidra 项目中的文件和文件夹

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `folderPath` | `string` | ✓ | - | 文件夹路径（使用 '/' 表示根文件夹） |
| `recursive` | `boolean` |  | `False` | 是否递归列出 |

---

## 27. `checkin-program`

**Checkin Program**（提交程序到版本控制）

将程序提交到版本控制并附带提交消息

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | 程序路径（如 '/Hatchery.exe'） |
| `message` | `string` | ✓ | - | 提交消息 |
| `keepCheckedOut` | `boolean` |  | `False` | 提交后是否保持检出状态 |

---

## 28. `analyze-program`

**Analyze Program**（分析程序）

对程序运行 Ghidra 的自动分析

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | 程序路径 |

---

## 29. `change-processor`

**Change Processor**（更改处理器架构）

更改现有程序的处理器架构

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | 程序路径 |
| `languageId` | `string` | ✓ | - | 语言 ID（如 'x86:LE:64:default'） |
| `compilerSpecId` | `string` |  | - | 编译器规范 ID（可选） |

---

## 30. `import-file`

**Import File**（导入文件）

使用批量导入将文件、目录或归档导入 Ghidra 项目

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `path` | `string` | ✓ | - | 要导入的绝对文件路径 |
| `destinationFolder` | `string` |  | - | 项目目标文件夹（默认：根文件夹） |
| `recursive` | `boolean` |  | `True` | 是否递归导入 |
| `analyzeAfterImport` | `boolean` |  | `True` | 导入后是否运行自动分析 |
| `enableVersionControl` | `boolean` |  | `True` | 是否自动添加到版本控制 |

---

## 31. `capture-reva-debug-info`

**Capture ReVa Debug Information**（捕获 ReVa 调试信息）

创建包含 ReVa 调试信息的 zip 文件用于故障排除

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `message` | `string` |  | - | 描述问题的可选消息 |

---

## 32. `find-cross-references`

**Find Cross References**（查找交叉引用）

查找指向或来自内存位置、符号或函数的所有引用

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `location` | `string` | ✓ | - | 地址或符号名 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `direction` | `string` |  | `both` | 引用方向：'to'（传入）、'from'（传出）或 'both' |
| `includeFlow` | `boolean` |  | `True` | 是否包含流引用（调用、跳转、分支） |
| `includeData` | `boolean` |  | `True` | 是否包含数据引用（读、写） |
| `includeContext` | `boolean` |  | `False` | 是否包含反编译上下文片段 |
| `contextLines` | `integer` |  | `2` | 上下文片段的前后行数 |
| `limit` | `integer` |  | `100` | 每个方向返回的最大引用数 |

---

## 33. `get-data-type-archives`

**Get Data Type Archives**（获取数据类型归档）

获取特定程序的数据类型归档

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |

---

## 34. `get-data-types`

**Get Data Types**（获取数据类型）

从数据类型归档获取数据类型

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `archiveName` | `string` | ✓ | - | 数据类型归档名称 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `categoryPath` | `string` |  | `/` | 类别路径（如 '/Structure'） |
| `startIndex` | `integer` |  | `0` | 分页起始索引 |
| `maxCount` | `integer` |  | `100` | 返回的最大数据类型数 |
| `includeSubcategories` | `boolean` |  | `False` | 是否包含子类别 |

---

## 35. `get-data-type-by-string`

**Get Data Type by String**（通过字符串获取数据类型）

通过字符串表示获取数据类型

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `dataTypeString` | `string` | ✓ | - | 数据类型的字符串表示（如 'char**'） |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `archiveName` | `string` |  | - | 数据类型归档名称（可选） |

---

## 36. `parse-c-structure`

**Parse C Structure**（解析 C 结构体）

从 C 风格定义解析并创建或替换结构体

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `cDefinition` | `string` | ✓ | - | C 风格结构体定义 |
| `programPath` | `string` | ✓ | - | 程序路径 |
| `category` | `string` |  | - | 类别路径（默认：/） |

---

## 37. `validate-c-structure`

**Validate C Structure**（验证 C 结构体）

验证 C 风格结构体定义但不创建它

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `cDefinition` | `string` | ✓ | - | 要验证的 C 风格结构体定义 |

---

## 38. `get-structure-info`

**Get Structure Info**（获取结构体信息）

获取结构体或联合体的详细信息，包括其布局的 C 表示

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `structureName` | `string` | ✓ | - | 结构体名称 |
| `programPath` | `string` | ✓ | - | 程序路径 |

---

## 39. `list-structures`

**List Structures**（列出结构体）

列出程序中的结构体和联合体

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | 程序路径 |
| `startIndex` | `integer` |  | `0` | 分页起始索引 |
| `maxCount` | `integer` |  | `100` | 返回的最大结构体数 |
| `category` | `string` |  | - | 按类别路径过滤 |
| `nameFilter` | `string` |  | - | 按名称过滤（子串匹配） |
| `includeBuiltIn` | `boolean` |  | `False` | 是否包含内置类型 |

---

## 40. `apply-structure`

**Apply Structure**（应用结构体）

在指定地址应用结构体

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `structureName` | `string` | ✓ | - | 结构体名称 |
| `programPath` | `string` | ✓ | - | 程序路径 |
| `addressOrSymbol` | `string` | ✓ | - | 地址或符号名 |
| `clearExisting` | `boolean` |  | `False` | 是否清除现有数据 |

---

## 41. `delete-structure`

**Delete Structure**（删除结构体）

从程序中删除结构体

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `structureName` | `string` | ✓ | - | 要删除的结构体名称 |
| `programPath` | `string` | ✓ | - | 程序路径 |
| `force` | `boolean` |  | `False` | 即使被引用也强制删除 |

---

## 42. `parse-c-header`

**Parse C Header**（解析 C 头文件）

解析整个 C 头文件并创建所有结构体

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `headerContent` | `string` | ✓ | - | C 头文件内容 |
| `programPath` | `string` | ✓ | - | 程序路径 |
| `category` | `string` |  | - | 类别路径（默认：/） |

---

## 43. `set-comment`

**Set Comment**（设置注释）

在指定地址设置或更新注释

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `addressOrSymbol` | `string` | ✓ | - | 地址或符号名 |
| `commentType` | `string` |  | `eol` | 注释类型：'pre'、'eol'、'post'、'plate' 或 'repeatable' |
| `comment` | `string` | ✓ | - | 注释文本 |

---

## 44. `get-comments`

**Get Comments**（获取注释）

获取指定地址或地址范围内的注释

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `addressOrSymbol` | `string` |  | - | 地址或符号名 |
| `addressRange` | `object` |  | - | 地址范围 |
| `commentTypes` | `array` |  | - | 要获取的注释类型 |

---

## 45. `remove-comment`

**Remove Comment**（删除注释）

删除指定地址的特定注释

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `addressOrSymbol` | `string` | ✓ | - | 地址或符号名 |
| `commentType` | `string` | ✓ | - | 要删除的注释类型 |

---

## 46. `search-comments`

**Search Comments**（搜索注释）

搜索包含特定文本的注释

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `searchText` | `string` | ✓ | - | 要搜索的文本 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `caseSensitive` | `boolean` |  | `False` | 是否区分大小写 |
| `maxResults` | `integer` |  | `100` | 返回的最大结果数 |
| `commentTypes` | `array` |  | - | 要搜索的注释类型 |

---

## 47. `set-bookmark`

**Set Bookmark**（设置书签）

在指定地址设置或更新书签，用于跟踪重要位置

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `addressOrSymbol` | `string` | ✓ | - | 地址或符号名 |
| `comment` | `string` | ✓ | - | 书签注释文本 |
| `type` | `string` | ✓ | - | 书签类型（如 'Note'、'Warning'、'TODO'、'Bug'） |
| `category` | `string` |  | - | 书签类别 |

---

## 48. `get-bookmarks`

**Get Bookmarks**（获取书签）

获取指定地址或地址范围内的书签

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `addressOrSymbol` | `string` |  | - | 地址或符号名 |
| `addressRange` | `object` |  | - | 地址范围 |
| `type` | `string` |  | - | 按书签类型过滤 |
| `category` | `string` |  | - | 按书签类别过滤 |
| `maxResults` | `integer` |  | `200` | 返回的最大书签数 |

---

## 49. `remove-bookmark`

**Remove Bookmark**（删除书签）

删除特定书签

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `addressOrSymbol` | `string` | ✓ | - | 地址或符号名 |
| `type` | `string` | ✓ | - | 书签类型 |
| `category` | `string` |  | - | 书签类别 |

---

## 50. `search-bookmarks`

**Search Bookmarks**（搜索书签）

按文本、类型、类别或地址范围搜索书签

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `searchText` | `string` |  | - | 要在注释中搜索的文本 |
| `types` | `array` |  | - | 按书签类型过滤 |
| `categories` | `array` |  | - | 按书签类别过滤 |
| `addressRange` | `object` |  | - | 地址范围 |
| `maxResults` | `integer` |  | `100` | 返回的最大结果数 |

---

## 51. `list-bookmark-categories`

**List Bookmark Categories**（列出书签类别）

列出给定书签类型的所有类别

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `type` | `string` | ✓ | - | 书签类型 |

---

## 52. `list-imports`

**List Imports**（列出导入函数）

列出从外部库导入的所有函数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `startIndex` | `integer` |  | `0` | 分页起始索引 |
| `maxResults` | `integer` |  | `500` | 返回的最大导入数 |
| `groupByLibrary` | `boolean` |  | `True` | 是否按库名分组 |
| `libraryFilter` | `string` |  | - | 按库名过滤（不区分大小写） |

---

## 53. `list-exports`

**List Exports**（列出导出符号）

列出二进制文件导出的所有符号

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `startIndex` | `integer` |  | `0` | 分页起始索引 |
| `maxResults` | `integer` |  | `500` | 返回的最大导出数 |

---

## 54. `find-import-references`

**Find Import References**（查找导入引用）

查找调用特定导入函数的所有位置

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `importName` | `string` | ✓ | - | 导入函数名（不区分大小写） |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `libraryName` | `string` |  | - | 库名（可选，用于缩小范围） |
| `maxResults` | `integer` |  | `100` | 返回的最大结果数 |

---

## 55. `resolve-thunk`

**Resolve Thunk**（解析 Thunk）

跟踪 thunk 链找到实际目标函数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `address` | `string` | ✓ | - | Thunk 或跳转存根的地址 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |

---

## 56. `trace-data-flow-backward`

**Trace Data Flow Backward**（反向追踪数据流）

追踪地址处值的来源（常量、参数、内存加载等）

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `address` | `string` | ✓ | - | 要向后跟踪的函数内地址 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |

---

## 57. `trace-data-flow-forward`

**Trace Data Flow Forward**（正向追踪数据流）

追踪地址处值的去向（存储、函数调用、返回等）

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `address` | `string` | ✓ | - | 要向前跟踪的函数内地址 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |

---

## 58. `find-variable-accesses`

**Find Variable Accesses**（查找变量访问）

查找函数内变量的所有读写操作

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `variableName` | `string` | ✓ | - | 变量名 |
| `functionAddress` | `string` | ✓ | - | 函数地址 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |

---

## 59. `get-call-graph`

**Get Call Graph**（获取调用图）

获取函数周围的调用图，显示调用者和被调用者

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionAddress` | `string` | ✓ | - | 函数地址或名称 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `depth` | `integer` |  | `1` | 包含的层数（默认：1，最大：10） |

---

## 60. `get-call-tree`

**Get Call Tree**（获取调用树）

获取从函数开始的层次调用树

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionAddress` | `string` | ✓ | - | 函数地址或名称 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `direction` | `string` |  | `callees` | 遍历方向：'callers'（向上）或 'callees'（向下） |
| `maxDepth` | `integer` |  | `3` | 遍历的最大深度（默认：3，最大：10） |

---

## 61. `find-common-callers`

**Find Common Callers**（查找公共调用者）

查找调用所有指定目标函数的公共函数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionAddresses` | `array` | ✓ | - | 函数地址或名称列表 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |

---

## 62. `find-constant-uses`

**Find Constant Uses**（查找常量使用）

查找使用特定常量值的所有位置

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `value` | `string` | ✓ | - | 要搜索的常量值（支持十进制、十六进制、负数） |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `maxResults` | `integer` |  | `500` | 返回的最大结果数 |

---

## 63. `find-constants-in-range`

**Find Constants in Range**（查找范围内的常量）

查找指定范围内的所有常量值

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `minValue` | `string` | ✓ | - | 最小值（支持十进制或十六进制） |
| `maxValue` | `string` | ✓ | - | 最大值（支持十进制或十六进制） |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `maxResults` | `integer` |  | `500` | 返回的最大结果数 |

---

## 64. `list-common-constants`

**List Common Constants**（列出常用常量）

查找程序中最常用的常量值

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `topN` | `integer` |  | `50` | 返回的最常用常量数 |
| `minValue` | `string` |  | - | 最小值（可选，用于过滤小常量） |
| `includeSmallValues` | `boolean` |  | `False` | 是否包含小值（0-255） |

---

## 65. `analyze-vtable`

**Analyze Vtable**（分析虚函数表）

分析指定地址的虚函数表（vtable）

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `vtableAddress` | `string` | ✓ | - | 虚函数表地址 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `maxEntries` | `integer` |  | `200` | 读取的最大条目数 |

---

## 66. `find-vtable-callers`

**Find Vtable Callers**（查找虚函数表调用者）

查找可能通过虚函数表槽调用函数的所有间接调用

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionAddress` | `string` | ✓ | - | 通过虚函数表调用的函数地址或名称 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |
| `vtableAddress` | `string` |  | - | 虚函数表地址（可选） |
| `maxResults` | `integer` |  | `500` | 返回的最大结果数 |

---

## 67. `find-vtables-containing-function`

**Find Vtables Containing Function**（查找包含函数的虚函数表）

查找包含指向给定函数的指针的所有虚函数表

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionAddress` | `string` | ✓ | - | 要搜索的函数地址或名称 |
| `programPath` | `string` | ✓ | - | Ghidra 项目中程序的路径 |

---
