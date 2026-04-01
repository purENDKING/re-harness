# ReVa-MCP 工具列表

> 共计 **67** 个工具

---

## 1. `get-symbols-count`

**Get Symbols Count** (获取符号总数)

Get the total count of symbols in the program (use this before calling get-symbols to plan pagination)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `includeExternal` | `boolean` |  | `False` | Whether to include external symbols in the count |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program to get symbol count from |
| `filterDefaultNames` | `boolean` |  | `True` | Whether to filter out default Ghidra generated names like FUN_, DAT_, etc. |

---

## 2. `get-symbols`

**Get Symbols** (获取符号列表)

Get symbols from the selected program with pagination (use get-symbols-count first to determine total count)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `includeExternal` | `boolean` |  | `False` | Whether to include external symbols in the result |
| `startIndex` | `integer` |  | `0` | Starting index for pagination (0-based) |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program to get symbols from |
| `filterDefaultNames` | `boolean` |  | `True` | Whether to filter out default Ghidra generated names like FUN_, DAT_, etc. |
| `maxCount` | `integer` |  | `200` | Maximum number of symbols to return (recommend using get-symbols-count first and using chunks of 200 |

---

## 3. `get-strings-count`

**Get Strings Count** (获取字符串总数)

Get the total count of strings in the program (use this before calling get-strings to plan pagination)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program to get string count from |

---

## 4. `get-strings`

**Get Strings** (获取字符串列表)

Get strings from the selected program with pagination. Optionally filter by regex (regexPattern) or sort by similarity (searchString). Use get-strings-count first to determine total count.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `searchString` | `string` |  | - | Optional: sort results by similarity to this string (scored by longest common substring). Mutually e |
| `startIndex` | `integer` |  | `0` | Starting index for pagination (0-based) |
| `includeReferencingFunctions` | `boolean` |  | `False` | Include list of functions that reference each string (max 100 per string). |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program to get strings from |
| `regexPattern` | `string` |  | - | Optional: filter results to strings matching this regex pattern. Mutually exclusive with searchStrin |
| `maxCount` | `integer` |  | `100` | Maximum number of strings to return (recommended to use get-strings-count first and request chunks o |

---

## 5. `get-function-count`

**Get Function Count** (获取函数总数)

Get the total count of functions in the program (use this before calling get-functions to plan pagination)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program to get functions from |
| `filterDefaultNames` | `boolean` |  | `True` | Whether to filter out default Ghidra generated names like FUN_, DAT_, etc. |

---

## 6. `get-functions`

**Get Functions** (获取函数列表)

Get functions from the selected program (use get-function-count to determine the total count)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `startIndex` | `integer` |  | `0` | Starting index for pagination (0-based) |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program to get functions from |
| `filterDefaultNames` | `boolean` |  | `True` | Whether to filter out default Ghidra generated names like FUN_, DAT_, etc. |
| `untagged` | `boolean` |  | `False` | Only return functions with no tags (mutually exclusive with filterByTag) |
| `filterByTag` | `string` |  | - | Only return functions with this tag (applied after filterDefaultNames) |
| `maxCount` | `integer` |  | `100` | Maximum number of functions to return (recommended to use get-function-count first and request chunk |
| `verbose` | `boolean` |  | `False` | Return full function details. When false (default), returns compact results (name, address, sizeInBy |

---

## 7. `get-functions-by-similarity`

**Get Functions by Similarity** (按相似度获取函数)

Get functions from the selected program with pagination, sorted by similarity to a given function name (use get-function-count first to determine total count)

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `searchString` | `string` | ✓ | - | Function name to compare against for similarity (scored by longest common substring length between t |
| `startIndex` | `integer` |  | `0` | Starting index for pagination (0-based) |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program to get functions from |
| `filterDefaultNames` | `boolean` |  | `True` | Whether to filter out default Ghidra generated names like FUN_, DAT_, etc. |
| `maxCount` | `integer` |  | `100` | Maximum number of functions to return (recommended to use get-function-count first and request chunk |
| `verbose` | `boolean` |  | `False` | Return full function details. When false (default), returns compact results (name, address, sizeInBy |

---

## 8. `set-function-prototype`

**Set Function Prototype** (设置函数原型)

Set or update a function prototype using C-style function signatures. Can create new functions or update existing ones.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `signature` | `string` | ✓ | - | C-style function signature (e.g., 'int main(int argc, char** argv)') |
| `location` | `string` | ✓ | - | Address or symbol name where the function is located |
| `createIfNotExists` | `boolean` |  | `True` | Create function if it doesn't exist at the location |

---

## 9. `get-undefined-function-candidates`

**Get Undefined Function Candidates** (获取未定义函数候选)

Find addresses in executable memory with valid instructions that are referenced but not defined as functions. Includes both CALL references and DATA references (function pointers, callbacks, exception handlers). Use get-decompilation to preview candidates, then create-function to define them permanently.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `startIndex` | `integer` |  | `0` | Starting index for pagination (0-based) |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `maxCandidates` | `integer` |  | `100` | Maximum number of candidates to return (default: 100) |
| `minReferenceCount` | `integer` |  | `1` | Minimum number of references required to be a candidate (default: 1) |

---

## 10. `create-function`

**Create Function** (创建函数)

Create a function at an address with auto-detected signature. Ghidra will analyze the code to determine the function body, parameters, and return type. Use this after get-undefined-function-candidates to define discovered functions. For explicit signature control, use set-function-prototype instead.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `address` | `string` | ✓ | - | Address where the function should be created (e.g., '0x401000') |
| `name` | `string` |  | - | Optional name for the function. If not provided, Ghidra will generate a default name (FUN_xxxxxxxx) |

---

## 11. `function-tags`

**Function Tags** (函数标签管理)

Manage function tags. Tags categorize functions (e.g., 'AI', 'rendering'). Use mode='list' for all tags in program.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `mode` | `string` | ✓ | - | Operation: 'get' (tags on function), 'set' (replace), 'add', 'remove', 'list' (all tags in program) |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `function` | `string` |  | - | Function name or address (required for get/set/add/remove modes) |
| `tags` | `array` |  | - | Tag names (required for add; optional for set/remove). Empty/whitespace names are ignored. |

---

## 12. `get-data`

**Get Data** (获取数据)

Get data at a specific address or symbol in a program

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program containing the data |
| `addressOrSymbol` | `string` | ✓ | - | Address or symbol name to get data from (e.g., '0x00400000' or 'main') |

---

## 13. `apply-data-type`

**Apply Data Type** (应用数据类型)

Apply a data type to a specific address or symbol in a program

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `dataTypeString` | `string` | ✓ | - | String representation of the data type (e.g., 'char**', 'int[10]') |
| `archiveName` | `string` |  | `` | Optional name of the data type archive to search in. If not provided, all archives will be searched. |
| `addressOrSymbol` | `string` | ✓ | - | Address or symbol name to apply the data type to (e.g., '0x00400000' or 'main') |

---

## 14. `create-label`

**Create Label** (创建标签)

Create a label at a specific address in a program

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `setAsPrimary` | `boolean` |  | `True` | Whether to set this label as primary if other labels exist at the address |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program containing the address |
| `addressOrSymbol` | `string` | ✓ | - | Address or symbol name to create label at (e.g., '0x00400000' or 'main') |
| `labelName` | `string` | ✓ | - | Name for the label to create |

---

## 15. `get-decompilation`

**Get Function Decompilation** (获取函数反编译代码)

Get decompiled code for a function with line range support. Defaults to 50 lines to conserve context - start with small chunks (10-20 lines) then expand as needed using offset/limit. Updating variable data types and names can significantly improve decompilation quality. Use includeCallers/includeCallees to get caller/callee lists in one call (avoids separate tool invocations).

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionNameOrAddress` | `string` | ✓ | - | Function name, address, or symbol to decompile (e.g. 'main', '0x00401000', or 'start'). For addresse |
| `includeCallers` | `boolean` |  | `False` | Include list of functions that call this one (name, address, signature). Use for understanding funct |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program containing the function |
| `offset` | `integer` |  | `1` | Line number to start reading from (1-based). Defaults to 1. |
| `includeDisassembly` | `boolean` |  | `False` | Whether to include assembly listing alongside decompilation for sync |
| `includeIncomingReferences` | `boolean` |  | `True` | Whether to include incoming cross references to this function on the function declaration line |
| `limit` | `integer` |  | `50` | Number of lines to return. Defaults to 50 lines to conserve context. Use smaller chunks (10-20 lines |
| `includeReferenceContext` | `boolean` |  | `True` | Whether to include code context snippets from calling functions (requires includeIncomingReferences) |
| `includeComments` | `boolean` |  | `False` | Whether to include comments in the decompilation output |
| `includeCallees` | `boolean` |  | `False` | Include list of functions this one calls (name, address, signature). Use for understanding function  |
| `signatureOnly` | `boolean` |  | `False` | Return only signature/metadata without decompiled code. Saves output tokens. |

---

## 16. `search-decompilation`

**Search Function Decompilations** (搜索反编译代码)

Search for patterns across all function decompilations in a program. Returns function names and line numbers where patterns match. If looking for calls or references to data, try the cross reference tools first.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program to search |
| `overrideMaxFunctionsLimit` | `boolean` |  | `False` | Whether to override the maximum function limit for decompiler searches. Use with caution as large pr |
| `maxResults` | `integer` |  | `50` | Maximum number of search results to return |
| `caseSensitive` | `boolean` |  | `False` | Whether the search should be case sensitive |
| `pattern` | `string` | ✓ | - | Regular expression pattern to search for in decompiled functions |

---

## 17. `rename-variables`

**Rename Function Variables** (重命名函数变量)

Rename variables in a decompiled function

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionNameOrAddress` | `string` | ✓ | - | Function name, address, or symbol to rename variables in (e.g. 'main', '0x00401000', or 'start'). Fo |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program containing the function |
| `variableMappings` | `object` | ✓ | - | Mapping of old variable names to new variable names. Only rename the variables that need to be chang |

---

## 18. `change-variable-datatypes`

**Change Variable Data Types** (更改变量数据类型)

Change data types of variables in a decompiled function

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionNameOrAddress` | `string` | ✓ | - | Function name, address, or symbol to change variable data types in (e.g. 'main', '0x00401000', or 's |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program containing the function |
| `datatypeMappings` | `object` | ✓ | - | Mapping of variable names to new data type strings (e.g., 'char*', 'int[10]'). Only change the varia |
| `archiveName` | `string` |  | `` | Optional name of the data type archive to search for data types. If not provided, all archives will  |

---

## 19. `set-decompilation-comment`

**Add Decompilation Comment** (添加反编译注释)

Set a comment at a specific line in decompiled code. The comment will be placed at the address corresponding to the decompilation line.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionNameOrAddress` | `string` | ✓ | - | Function name, address, or symbol (e.g. 'main', '0x00401000', or 'start') |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program containing the function |
| `commentType` | `string` |  | `eol` | Type of comment: 'pre' or 'eol' (end-of-line) |
| `comment` | `string` | ✓ | - | The comment text to set |
| `lineNumber` | `integer` | ✓ | - | Line number in the decompiled function (1-based) |

---

## 20. `get-callers-decompiled`

**Get Callers Decompiled** (获取调用者反编译代码)

Decompile all functions that call a target function. Returns bulk decompilation results with optional call site highlighting. Use for understanding how a function is used throughout the codebase.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionNameOrAddress` | `string` | ✓ | - | Target function name or address to find callers for |
| `startIndex` | `integer` |  | `0` | Starting index for pagination (0-based) |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `includeCallContext` | `boolean` |  | `True` | Whether to highlight the line containing the call in each decompilation |
| `maxCallers` | `integer` |  | `10` | Maximum number of calling functions to decompile (default: 10) |

---

## 21. `get-referencers-decompiled`

**Get Referencers Decompiled** (获取引用者反编译代码)

Decompile all functions that reference a specific address or symbol. Useful for understanding how global variables, data, or code locations are used. Includes both code and data references by default.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `startIndex` | `integer` |  | `0` | Starting index for pagination (0-based) |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `maxReferencers` | `integer` |  | `10` | Maximum number of referencing functions to decompile (default: 10) |
| `addressOrSymbol` | `string` | ✓ | - | Target address or symbol name to find references to (e.g., '0x00401000', 'global_var', 'my_label') |
| `includeRefContext` | `boolean` |  | `True` | Whether to include reference line numbers in decompilation |
| `includeDataRefs` | `boolean` |  | `True` | Whether to include data references (reads/writes), not just calls |

---

## 22. `get-memory-blocks`

**Get Memory Blocks** (获取内存块)

Get memory blocks from the selected program

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path to the program in the Ghidra Project |

---

## 23. `read-memory`

**Read Memory** (读取内存)

Read memory at a specific address

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path to the program in the Ghidra Project |
| `addressOrSymbol` | `string` | ✓ | - | Address or symbol name to read from (e.g. '00400000' or 'main') |
| `length` | `integer` |  | `16` | Number of bytes to read |
| `format` | `string` |  | `hex` | Output format: 'hex', 'bytes', or 'both' |

---

## 24. `get-current-program`

**Get Current Program** (获取当前程序)

Get the currently active program in Ghidra


---

## 25. `list-open-programs`

**List Open Programs** (列出打开的程序)

List all programs currently open in Ghidra across all tools


---

## 26. `list-project-files`

**List Project Files** (列出项目文件)

List files and folders in the Ghidra project

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `folderPath` | `string` | ✓ | - | Path to the folder to list contents of. Use '/' for the root folder. |
| `recursive` | `boolean` |  | `False` | Whether to list files recursively |

---

## 27. `checkin-program`

**Checkin Program** (提交程序到版本控制)

Checkin (commit) a program to version control with a commit message

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path to the program to checkin (e.g., '/Hatchery.exe') |
| `message` | `string` | ✓ | - | Commit message for the checkin |
| `keepCheckedOut` | `boolean` |  | `False` | Whether to keep the program checked out after checkin |

---

## 28. `analyze-program`

**Analyze Program** (分析程序)

Run Ghidra's auto-analysis on a program

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path to the program to analyze (e.g., '/Hatchery.exe') |

---

## 29. `change-processor`

**Change Processor** (更改处理器架构)

Change the processor architecture of an existing program

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path to the program to modify (e.g., '/Hatchery.exe') |
| `languageId` | `string` | ✓ | - | Language ID for the new processor (e.g., 'x86:LE:64:default') |
| `compilerSpecId` | `string` |  | - | Compiler spec ID (optional, defaults to the language's default) |

---

## 30. `import-file`

**Import File** (导入文件)

Import files, directories, or archives into the Ghidra project using batch import

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `destinationFolder` | `string` |  | - | Project folder path for imported files (default: root folder) |
| `maxDepth` | `integer` |  | - | Maximum container depth to recurse into (default: 10) |
| `stripLeadingPath` | `boolean` |  | - | Omit the source file's leading path from imported file locations (default: true) |
| `path` | `string` | ✓ | - | Absolute file system path to import (file, directory, or archive). Use absolute paths to ensure prop |
| `enableVersionControl` | `boolean` |  | - | Automatically add imported files to version control (default: true) |
| `analyzeAfterImport` | `boolean` |  | - | Run auto-analysis after import (default: true) |
| `stripAllContainerPath` | `boolean` |  | - | Completely flatten container paths in imported file locations (default: false) |
| `mirrorFs` | `boolean` |  | - | Mirror the filesystem layout when importing (default: false) |
| `recursive` | `boolean` |  | - | Whether to recursively import from containers/archives (default: true) |

---

## 31. `capture-reva-debug-info`

**Capture ReVa Debug Information** (捕获ReVa调试信息)

Creates a zip file containing ReVa debug information for troubleshooting issues. Includes system info, Ghidra config, ReVa settings, MCP server status, open programs, and logs.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `message` | `string` |  | - | Optional message describing the issue being debugged |

---

## 32. `find-cross-references`

**Find Cross References** (查找交叉引用)

Find all references to or from a memory location, symbol, or function. Returns incoming and/or outgoing references with optional decompilation context.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `includeContext` | `boolean` |  | `False` | Include decompilation context snippets for code references |
| `contextLines` | `integer` |  | `2` | Number of lines before and after to include in context snippets |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program to get references from |
| `offset` | `integer` |  | `0` | Starting offset for pagination (0-based) |
| `includeFlow` | `boolean` |  | `True` | Include flow references (calls, jumps, branches) |
| `limit` | `integer` |  | `100` | Maximum number of references to return per direction |
| `location` | `string` | ✓ | - | Address or symbol name to get references for (e.g., '0x00400123', 'main', 'FUN_00401000') |
| `includeData` | `boolean` |  | `True` | Include data references (reads, writes) |
| `direction` | `string` |  | `both` | Direction of references to retrieve: 'to' (incoming), 'from' (outgoing), or 'both' (default) |

---

## 33. `get-data-type-archives`

**Get Data Type Archives** (获取数据类型归档)

Get data type archives for a specific program

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to get data type archives for |

---

## 34. `get-data-types`

**Get Data Types** (获取数据类型)

Get data types from a data type archive

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `startIndex` | `integer` |  | `0` | Starting index for pagination (0-based) |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to get data types from |
| `archiveName` | `string` | ✓ | - | Name of the data type archive |
| `categoryPath` | `string` |  | `/` | Path to category to list data types from (e.g., '/Structure'). Use '/' for root category. |
| `maxCount` | `integer` |  | `100` | Maximum number of data types to return |
| `includeSubcategories` | `boolean` |  | `False` | Whether to include data types from subcategories |

---

## 35. `get-data-type-by-string`

**Get Data Type by String** (通过字符串获取数据类型)

Get a data type by its string representation

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to search for data types in |
| `dataTypeString` | `string` | ✓ | - | String representation of the data type (e.g., 'char**', 'int[10]') |
| `archiveName` | `string` |  | `` | Optional name of the data type archive to search in. If not provided, all archives will be searched. |

---

## 36. `parse-c-structure`

**Parse C Structure** (解析C结构体)

Parse and create or replace a structure from a C-style definition. If a structure with the same name already exists, it will be replaced with the new definition (fields are completely rebuilt). Use get-structure-info to see the current layout before modifying.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path of the program |
| `cDefinition` | `string` | ✓ | - | C-style structure definition |
| `category` | `string` |  | - | Category path (default: /) |

---

## 37. `validate-c-structure`

**Validate C Structure** (验证C结构体)

Validate C-style structure definition without creating it

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `cDefinition` | `string` | ✓ | - | C-style structure definition to validate |

---

## 38. `get-structure-info`

**Get Structure Info** (获取结构体信息)

Get detailed information about a structure or union, including a C representation of its layout

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path of the program |
| `structureName` | `string` | ✓ | - | Name of the structure |

---

## 39. `list-structures`

**List Structures** (列出结构体)

List structures and unions in a program with optional filtering and pagination

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `startIndex` | `integer` |  | `0` | Starting index for pagination (0-based) |
| `programPath` | `string` | ✓ | - | Path of the program |
| `includeBuiltIn` | `boolean` |  | - | Include built-in types (default: false) |
| `category` | `string` |  | - | Filter by category path |
| `nameFilter` | `string` |  | - | Filter by name (substring match) |
| `maxCount` | `integer` |  | `100` | Maximum number of structures to return |

---

## 40. `apply-structure`

**Apply Structure** (应用结构体)

Apply a structure at a specific address

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `clearExisting` | `boolean` |  | - | Clear existing data |
| `programPath` | `string` | ✓ | - | Path of the program |
| `structureName` | `string` | ✓ | - | Name of the structure |
| `addressOrSymbol` | `string` | ✓ | - | Address or symbol name to apply structure |

---

## 41. `delete-structure`

**Delete Structure** (删除结构体)

Delete a structure from the program. Checks for references (function signatures, variables, memory) before deletion. Use force=true to delete anyway despite references.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path of the program |
| `structureName` | `string` | ✓ | - | Name of the structure to delete |
| `force` | `boolean` |  | - | Force deletion even if structure is referenced (default: false) |

---

## 42. `parse-c-header`

**Parse C Header** (解析C头文件)

Parse an entire C header file and create all structures

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `headerContent` | `string` | ✓ | - | C header file content |
| `programPath` | `string` | ✓ | - | Path of the program |
| `category` | `string` |  | - | Category path (default: /) |

---

## 43. `set-comment`

**Set Comment** (设置注释)

Set or update a comment at a specific address. Use this to keep notes or annotations for yourself and the human.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path to the program in the Ghidra Project |
| `addressOrSymbol` | `string` | ✓ | - | Address or symbol name where to set the comment |
| `commentType` | `string` |  | `eol` | Type of comment: 'pre', 'eol', 'post', 'plate', or 'repeatable' |
| `comment` | `string` | ✓ | - | The comment text to set |

---

## 44. `get-comments`

**Get Comments** (获取注释)

Get comments at a specific address or within an address range

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path to the program in the Ghidra Project |
| `addressOrSymbol` | `string` |  | - | Address or symbol name to get comments from (optional if using addressRange) |
| `addressRange` | `object` |  | - | Address range to get comments from (optional if using address) |
| `commentTypes` | `array` |  | - | Types of comments to retrieve (optional, defaults to all types) |

---

## 45. `remove-comment`

**Remove Comment** (删除注释)

Remove a specific comment at an address

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path to the program in the Ghidra Project |
| `addressOrSymbol` | `string` | ✓ | - | Address or symbol name where to remove the comment |
| `commentType` | `string` | ✓ | - | Type of comment to remove: 'pre', 'eol', 'post', 'plate', or 'repeatable' |

---

## 46. `search-comments`

**Search Comments** (搜索注释)

Search for comments containing specific text

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `searchText` | `string` | ✓ | - | Text to search for in comments |
| `programPath` | `string` | ✓ | - | Path to the program in the Ghidra Project |
| `caseSensitive` | `boolean` |  | `False` | Whether search is case sensitive |
| `maxResults` | `integer` |  | `100` | Maximum number of results to return |
| `commentTypes` | `array` |  | - | Types of comments to search (optional, defaults to all types) |

---

## 47. `set-bookmark`

**Set Bookmark** (设置书签)

Set or update a bookmark at a specific address. Used to keep track of important locations in the program.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path to the program in the Ghidra Project |
| `addressOrSymbol` | `string` | ✓ | - | Address or symbol name where to set the bookmark |
| `comment` | `string` | ✓ | - | Bookmark comment text |
| `type` | `string` | ✓ | - | Bookmark type (e.g. 'Note', 'Warning', 'TODO', 'Bug', 'Analysis') |
| `category` | `string` |  | - | Bookmark category for organizing bookmarks (optional) |

---

## 48. `get-bookmarks`

**Get Bookmarks** (获取书签)

Get bookmarks at a specific address or within an address range

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path to the program in the Ghidra Project |
| `maxResults` | `integer` |  | `200` | Maximum number of bookmarks to return (default 200) |
| `addressOrSymbol` | `string` |  | - | Address or symbol name to get bookmarks from (optional if using addressRange) |
| `addressRange` | `object` |  | - | Address range to get bookmarks from (optional if using address) |
| `type` | `string` |  | - | Filter by bookmark type (optional) |
| `category` | `string` |  | - | Filter by bookmark category (optional) |

---

## 49. `remove-bookmark`

**Remove Bookmark** (删除书签)

Remove a specific bookmark

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path to the program in the Ghidra Project |
| `addressOrSymbol` | `string` | ✓ | - | Address or symbol name of the bookmark |
| `type` | `string` | ✓ | - | Bookmark type |
| `category` | `string` |  | - | Bookmark category (optional) |

---

## 50. `search-bookmarks`

**Search Bookmarks** (搜索书签)

Search for bookmarks by text, type, category, or address range

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `searchText` | `string` |  | - | Text to search for in bookmark comments (optional) |
| `types` | `array` |  | - | Filter by bookmark types (optional) |
| `programPath` | `string` | ✓ | - | Path to the program in the Ghidra Project |
| `maxResults` | `integer` |  | `100` | Maximum number of results to return |
| `addressRange` | `object` |  | - | Limit search to address range (optional) |
| `categories` | `array` |  | - | Filter by bookmark categories (optional) |

---

## 51. `list-bookmark-categories`

**List Bookmark Categories** (列出书签类别)

List all categories for a given bookmark type

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path to the program in the Ghidra Project |
| `type` | `string` | ✓ | - | Bookmark type to get categories for |

---

## 52. `list-imports`

**List Imports** (列出导入函数)

List all imported functions from external libraries. Useful for understanding what external APIs a binary uses.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `startIndex` | `integer` |  | `0` | Starting index for pagination (default: 0) |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `groupByLibrary` | `boolean` |  | `True` | Group imports by library name (default: true) |
| `maxResults` | `integer` |  | `500` | Maximum number of imports to return (default: 500) |
| `libraryFilter` | `string` |  | - | Optional: filter by library name (case-insensitive partial match) |

---

## 53. `list-exports`

**List Exports** (列出导出符号)

List all exported symbols from the binary. Shows functions and data that the binary exports for use by other modules.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `startIndex` | `integer` |  | `0` | Starting index for pagination (default: 0) |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `maxResults` | `integer` |  | `500` | Maximum number of exports to return (default: 500) |

---

## 54. `find-import-references`

**Find Import References** (查找导入引用)

Find all locations where a specific imported function is called. Also finds references through thunks (IAT stubs).

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `libraryName` | `string` |  | - | Optional: specific library name to narrow search (case-insensitive) |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `maxResults` | `integer` |  | `100` | Maximum number of references to return (default: 100) |
| `importName` | `string` | ✓ | - | Name of the imported function to find references for (case-insensitive) |

---

## 55. `resolve-thunk`

**Resolve Thunk** (解析Thunk)

Follow a thunk chain to find the actual target function. Thunks are wrapper functions that jump to another location.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `address` | `string` | ✓ | - | Address of the thunk or jump stub to resolve |

---

## 56. `trace-data-flow-backward`

**Trace Data Flow Backward** (反向追踪数据流)

Trace where a value at an address comes from. Follows the data dependency chain backward to find origins (constants, parameters, memory loads, etc.).

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `address` | `string` | ✓ | - | Address within a function to trace backward from |

---

## 57. `trace-data-flow-forward`

**Trace Data Flow Forward** (正向追踪数据流)

Trace where a value at an address flows to. Follows the data dependency chain forward to find uses (stores, function calls, returns, etc.).

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `address` | `string` | ✓ | - | Address within a function to trace forward from |

---

## 58. `find-variable-accesses`

**Find Variable Accesses** (查找变量访问)

Find all reads and writes to a variable within a function. Useful for understanding how a variable is used throughout a function.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `variableName` | `string` | ✓ | - | Name of the variable to find accesses for |
| `functionAddress` | `string` | ✓ | - | Address of the function to analyze |

---

## 59. `get-call-graph`

**Get Call Graph** (获取调用图)

Get the call graph around a function, showing both callers (functions that call this one) and callees (functions this one calls) up to the specified depth. Useful for understanding a function's context in the overall program flow.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `depth` | `integer` |  | `1` | How many levels of callers/callees to include (default: 1, max: 10) |
| `functionAddress` | `string` | ✓ | - | Address or name of the function to analyze |

---

## 60. `get-call-tree`

**Get Call Tree** (获取调用树)

Get a hierarchical call tree starting from a function. Can traverse upward (callers - who calls this function) or downward (callees - what functions this calls). Detects and marks cycles.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `maxDepth` | `integer` |  | `3` | Maximum depth to traverse (default: 3, max: 10) |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `functionAddress` | `string` | ✓ | - | Address or name of the function to analyze |
| `direction` | `string` |  | `callees` | Direction to traverse: 'callers' (who calls this) or 'callees' (what this calls) |

---

## 61. `find-common-callers`

**Find Common Callers** (查找公共调用者)

Find functions that call ALL of the specified target functions. Useful for finding dispatch points, main loops, or common entry points that orchestrate multiple related functions.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `functionAddresses` | `array` | ✓ | - | List of function addresses or names to find common callers for |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |

---

## 62. `find-constant-uses`

**Find Constant Uses** (查找常量使用)

Find all locations where a specific constant value is used as an immediate operand in instructions. Useful for finding magic numbers, error codes, buffer sizes, or other significant values.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `maxResults` | `integer` |  | `500` | Maximum number of results to return (default: 500) |
| `value` | `string` | ✓ | - | The constant value to search for. Supports decimal (123), hex (0x7b), negative (-1), or named consta |

---

## 63. `find-constants-in-range`

**Find Constants in Range** (查找范围内的常量)

Find all constant values within a specified range. Useful for finding error codes (e.g., 400-599 for HTTP errors), enum values, or constants that fall within expected bounds.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `minValue` | `string` | ✓ | - | Minimum value (inclusive). Supports decimal or hex (0x) format. |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `maxValue` | `string` | ✓ | - | Maximum value (inclusive). Supports decimal or hex (0x) format. |
| `maxResults` | `integer` |  | `500` | Maximum number of results to return (default: 500) |

---

## 64. `list-common-constants`

**List Common Constants** (列出常用常量)

Find the most frequently used constant values in the program. Helps identify important magic numbers, sizes, flags, or other significant values. By default filters out small values (0-255) which are often noise.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `minValue` | `string` |  | - | Optional minimum value to consider (filters out small constants) |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `includeSmallValues` | `boolean` |  | `False` | Include small values (0-255) which are often noise (default: false) |
| `topN` | `integer` |  | `50` | Number of most common constants to return (default: 50) |

---

## 65. `analyze-vtable`

**Analyze Vtable** (分析虚函数表)

Analyze a virtual function table (vtable) at the given address. Returns the list of function pointers with their slot indices and offsets. Useful for understanding C++ class hierarchies and virtual method dispatch.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `vtableAddress` | `string` | ✓ | - | Address of the vtable to analyze |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `maxEntries` | `integer` |  | `200` | Maximum number of vtable entries to read (default: 200) |

---

## 66. `find-vtable-callers`

**Find Vtable Callers** (查找虚函数表调用者)

Find all indirect calls that could be calling a function through its vtable slot. Given a function that appears in a vtable, finds all indirect call instructions with the matching offset. If vtableAddress is not provided, will first search for vtables containing the function. Essential for finding callers of virtual methods. Note: Offset extraction patterns are optimized for x86/x64 instruction formats.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `vtableAddress` | `string` |  | - | Address of the vtable containing the function (optional - will search if not provided) |
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `maxResults` | `integer` |  | `500` | Maximum number of results to return (default: 500) |
| `functionAddress` | `string` | ✓ | - | Address or name of the function that is called via vtable |

---

## 67. `find-vtables-containing-function`

**Find Vtables Containing Function** (查找包含函数的虚函数表)

Find all vtables that contain a pointer to the given function. Returns the vtable addresses and slot indices where the function appears. Useful for discovering which classes implement a virtual method.

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| `programPath` | `string` | ✓ | - | Path in the Ghidra Project to the program |
| `functionAddress` | `string` | ✓ | - | Address or name of the function to search for in vtables |

---

