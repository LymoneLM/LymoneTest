# 服务于本仓库的一些小工具

##  merge2ipynb.py

#### **功能说明**

可以将一个目录内的Python程序整理为一个`.ipynb`文件

#### 使用方法

通过命令行运行：

```bash
python merge2ipynb.py -i 输入目录路径 -o 输出文件路径.ipynb
```

示例：

```bash
python merge2ipynb.py -i ./Practice2 -o practice2.ipynb
```

## code2md.py

#### **功能说明**

   - 接受一个文件夹路径作为参数
   - 递归遍历所有子目录
   - 自动识别.cpp和.py文件
   - 生成与文件夹同名的Markdown文件

#### 可选参数

   - `--head` ：在文档开头插入指定Markdown内容
   - `--tail` ：在文档末尾插入指定Markdown内容
   - `--output` ：选择输出文件夹（默认为`脚本根目录/ouput`）

#### 使用方法

基本用法：

```
python code2md.py ./my_project
```
带参数：

```
python code2md.py ./my_project --head intro.md --tail notes.md --output ./output
```