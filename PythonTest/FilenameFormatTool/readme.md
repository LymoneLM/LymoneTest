# 文件名格式化工具

## 程序设计

### 需求分析

使用Python编写一个文件名格式化工具脚本，可以批量重命名指定文件夹下的文件；处理前可预览，确认后执行。

### 功能设计

1. **基础形态**：纯命令行工具，所有功能通过附加参数实现。
2. **操作范围**：
   - 可选择是否递归处理目标目录下的所有子目录文件。
   - 可选择仅对特定后缀名的一种或多种文件进行操作。
   - 支持使用正则表达式筛选目标目录下需要操作的文件名。
3. **重命名规则定制**：
   - 可单独指定重命名后文件名的前缀或后缀（不影响文件后缀名）。
   - 也可以使用重命名模版，支持在重命名模板中使用变量：
     - `{date}`：插入当日日期（默认格式YYMMDD，支持自定义日期格式化）。
     - `{original_name}`：插入文件原始名称。
     - `{file_size}`：插入文件大小（支持参数修改单位）。
     - `{hash}`：插入文件哈希值（默认算法SHA256，取前六位；支持参数修改算法和位数）。
   - 支持指定编号方式（数字序号、罗马序号、字母序，默认数字序号）。
     - 可以使用{num}变量在模版中指定编号位置。
     - 使用参数修改不同的序号形式。
     - 数字序号支持手动指定位数或智能统计识别位数。
     - 支持指定文件排序依据（按文件名、修改时间、创建时间等）。
4. **输出位置**：
   - 可指定输出目录（默认在原始目录操作）。
   - 若指定了其他输出目录，则保留原始文件（相当于复制+重命名）。
5. **预览与安全执行**：
   - 正式重命名操作前，必须展示预览（格式为`原始文件名 -> 新文件名`）。
   - 提供独立的干运行模式参数（`--dry-run`），仅显示预览而不执行任何实际修改操作。
6. **冲突处理**：
   - 重命名时若目标位置文件已存在，需在命令行中依次提示用户选择：覆盖 / 跳过。
   - 可提示用户现有文件的大小和哈希值（与待重命名文件比较）以辅助决策。
7. **日志记录**：
   - 在工作目录自动生成按时间命名的日志文件。
   - 日志记录：目标目录、输出目录、有序的文件原始名称与重命名后名称对照表。
8. **逆向重命名**：
   - 提供参数支持通过工作目录的日志文件逆向操作（恢复原始文件名）。
   - 执行此指令时必须指定输出目录（即当初重命名时的输出目录）。
   - 需处理日志文件损坏或不可用的情况并报错。
9. **文件属性保留**：
   - 默认保留原始文件的属性（元数据）。
   - 提供参数选择是否保留原始属性：若不保留，则将文件的创建时间、修改时间更新为当前操作时间，并清空其他属性数据。

## 使用示例

### -help

> usage: fft.py [-h] [--dry-run] [-r] [-e EXTENSIONS] [--regex REGEX] [--prefix PREFIX] [--suffix SUFFIX]
>               [--template TEMPLATE] [--date-format DATE_FORMAT] [--size-unit {B,KB,MB,GB}]
>               [--hash-algo {md5,sha1,sha256}] [--hash-length HASH_LENGTH] [--num-type {num,roman,alpha}]   
>               [--num-digits NUM_DIGITS] [--sort-by {name,mtime,ctime,size}] [--sort-order {asc,desc}]      
>               [-o OUTPUT_DIR] [--no-preserve] [--reverse] [--log-file LOG_FILE]
>               [target]
>
> 文件名格式化工具
>
> positional arguments:
>   target                目标目录路径
>
> options:
>   -h, --help            show this help message and exit
>   --dry-run             仅预览不执行
>   -r, --recursive       递归处理子目录
>   -e, --extensions EXTENSIONS
>                         文件扩展名过滤(逗号分隔，如: jpg,png)
>   --regex REGEX         文件名正则表达式过滤
>   --prefix PREFIX       文件名前缀
>   --suffix SUFFIX       文件名后缀
>   --template TEMPLATE   重命名模板
>                         可用变量: {date}, {original_name}, {file_size}, {hash}, {num}
>   --date-format DATE_FORMAT
>                         日期格式(默认: %y%m%d)
>   --size-unit {B,KB,MB,GB}
>                         文件大小单位
>   --hash-algo {md5,sha1,sha256}
>                         哈希算法
>   --hash-length HASH_LENGTH
>                         哈希值长度
>   --num-type {num,roman,alpha}
>                         序号类型
>   --num-digits NUM_DIGITS
>                         序号位数(0为自动)
>   --sort-by {name,mtime,ctime,size}
>                         排序依据
>   --sort-order {asc,desc}
>                         排序顺序
>   -o, --output-dir OUTPUT_DIR
>                         输出目录(默认覆盖原文件)
>   --no-preserve         不保留原始文件属性
>   --reverse             逆向重命名操作
>   --log-file LOG_FILE   用于逆向操作的日志文件

### 参考命令

#### 1.基本重命名

```bash
python fft.py /path/to/files --prefix "vacation_" --suffix "_2023"
```

#### 2.模板重命名

```bash
python fft.py /path/to/photos --template "{date}_{num}_{original_name}" --date-format "%Y%m%d" --num-type alpha
```

#### 3.正则筛选创建时间排序重命名

```bash
python fft.py /path/to/data -r -e jpg,png --regex "IMG_\d+" --output-dir /sorted_photos --sort-by ctime --sort-order desc
```

#### 4.纯预览模式

```bash
python fft.py /path/to/files --template "{hash}_{original_name}" --hash-algo md5 --hash-length 8 --dry-run
```

#### 5.逆向操作

```bash
python fft.py --reverse --log-file rename_20230531_123456.log --output-dir /original_files
```