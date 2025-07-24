import os
import re
import time
import argparse
import hashlib
import shutil
import datetime
import csv
import logging
from enum import Enum
from typing import List, Dict, Tuple


class NumFormat(Enum):
    NUMERIC = 1
    ROMAN = 2
    ALPHA = 3


class SortBy(Enum):
    NAME = 1
    MTIME = 2
    CTIME = 3
    SIZE = 4


def parse_arguments():
    parser = argparse.ArgumentParser(description="文件名格式化工具", formatter_class=argparse.RawTextHelpFormatter)

    # 基础参数
    parser.add_argument("target", nargs="?", help="目标目录路径")
    parser.add_argument("--dry-run", action="store_true", help="仅预览不执行")

    # 操作范围
    parser.add_argument("-r", "--recursive", action="store_true", help="递归处理子目录")
    parser.add_argument("-e", "--extensions", help="文件扩展名过滤(逗号分隔，如: jpg,png)")
    parser.add_argument("--regex", help="文件名正则表达式过滤")

    # 重命名规则
    parser.add_argument("--prefix", help="文件名前缀")
    parser.add_argument("--suffix", help="文件名后缀")
    parser.add_argument("--template", help="重命名模板\n可用变量: {date}, {original_name}, {file_size}, {hash}, {num}")
    parser.add_argument("--date-format", default="%y%m%d", help="日期格式(默认: %%y%%m%%d)")
    parser.add_argument("--size-unit", choices=["B", "KB", "MB", "GB"], default="B", help="文件大小单位")
    parser.add_argument("--hash-algo", choices=["md5", "sha1", "sha256"], default="sha256", help="哈希算法")
    parser.add_argument("--hash-length", type=int, default=6, help="哈希值长度")
    parser.add_argument("--num-type", choices=["num", "roman", "alpha"], default="num", help="序号类型")
    parser.add_argument("--num-digits", type=int, default=0, help="序号位数(0为自动)")
    parser.add_argument("--sort-by", choices=["name", "mtime", "ctime", "size"], default="name", help="排序依据")
    parser.add_argument("--sort-order", choices=["asc", "desc"], default="asc", help="排序顺序")

    # 输出位置
    parser.add_argument("-o", "--output-dir", help="输出目录(默认覆盖原文件)")

    # 文件属性
    parser.add_argument("--no-preserve", action="store_true", help="不保留原始文件属性")

    # 逆向操作
    parser.add_argument("--reverse", action="store_true", help="逆向重命名操作")
    parser.add_argument("--log-file", help="用于逆向操作的日志文件")

    return parser.parse_args()


def get_files(target: str, recursive: bool, extensions: str = None, regex: str = None) -> List[str]:
    files = []
    if recursive:
        for root, _, filenames in os.walk(target):
            for f in filenames:
                files.append(os.path.join(root, f))
    else:
        files = [os.path.join(target, f) for f in os.listdir(target)
                 if os.path.isfile(os.path.join(target, f))]

    if extensions:
        ext_list = [ext.lower().strip(".") for ext in extensions.split(",")]
        files = [f for f in files
                 if os.path.splitext(f)[1][1:].lower() in ext_list]

    if regex:
        pattern = re.compile(regex)
        files = [f for f in files if pattern.search(os.path.basename(f))]
    return files


def sort_files(files: List[str], sort_by: str, sort_order: str) -> List[str]:
    key_func = {
        "name": lambda f: os.path.basename(f),
        "mtime": lambda f: os.path.getmtime(f),
        "ctime": lambda f: os.path.getctime(f),
        "size": lambda f: os.path.getsize(f)
    }[sort_by]

    reverse = (sort_order == "desc")
    return sorted(files, key=key_func, reverse=reverse)


def format_number(n: int, num_type: str, num_digits: int = 0) -> str:
    if num_type == "num":
        return f"{n:0{num_digits}d}" if num_digits > 0 else str(n)

    if num_type == "roman":
        # 简化版罗马数字转换(支持1-1000)
        val = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        sym = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
        roman = ""
        i = 0
        num = n
        while num > 0:
            for _ in range(num // val[i]):
                roman += sym[i]
                num -= val[i]
            i += 1
        return roman

    # 字母序号(A-Z, AA-AZ, BA-BZ, ...)
    if num_type == "alpha":
        letters = ""
        num = n
        while num > 0:
            num, remainder = divmod(num - 1, 26)
            letters = chr(65 + remainder) + letters
        return letters

    return str(n)


def calculate_hash(file_path: str, algorithm: str, length: int) -> str:
    hash_func = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256
    }[algorithm]()

    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)

    return hash_func.hexdigest()[:length]


def format_size(size: int, unit: str) -> str:
    if unit == "B":
        return str(size)
    if unit == "KB":
        return f"{size / 1024:.2f}"
    if unit == "MB":
        return f"{size / (1024 * 1024):.2f}"
    if unit == "GB":
        return f"{size / (1024 * 1024 * 1024):.2f}"
    return str(size)


def generate_new_filename(
        file_path: str,
        template: str,
        prefix: str,
        suffix: str,
        date_format: str,
        size_unit: str,
        hash_algo: str,
        hash_length: int,
        num: int,
        num_type: str,
        num_digits: int
) -> Tuple[str, Dict[str, str]]:
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    file_size = os.path.getsize(file_path)

    variables = {
        "date": datetime.datetime.now().strftime(date_format),
        "original_name": name,
        "file_size": format_size(file_size, size_unit),
        "hash": calculate_hash(file_path, hash_algo, hash_length),
        "num": format_number(num, num_type, num_digits)
    }

    if template:
        new_name = template.format(**variables)
    else:
        new_name = name
        if prefix:
            new_name = prefix + new_name
        if suffix:
            new_name += suffix

    return new_name + ext, variables


def handle_conflict(src: str, dst: str, preserve_attrs: bool):
    print(f"目标文件已存在: {dst}")
    print(
        f"源文件: {src} | 大小: {os.path.getsize(src)} | 修改时间: {datetime.datetime.fromtimestamp(os.path.getmtime(src))}")
    print(
        f"目标文件: {dst} | 大小: {os.path.getsize(dst)} | 修改时间: {datetime.datetime.fromtimestamp(os.path.getmtime(dst))}")

    if preserve_attrs:
        src_hash = calculate_hash(src, "sha256", 12)
        dst_hash = calculate_hash(dst, "sha256", 12)
        print(f"源文件哈希(SHA256-12): {src_hash}")
        print(f"目标文件哈希(SHA256-12): {dst_hash}")

    while True:
        choice = input("覆盖(overwrite)/跳过(skip)/全部覆盖(all)/全部跳过(none)? [o/s/a/n] ").lower()
        if choice == "o":
            return True
        if choice == "s":
            return False
        if choice == "a":
            return "all"
        if choice == "n":
            return "none"


def process_files(files: List[str], args) -> List[Tuple[str, str]]:
    operations = []
    num_digits = args.num_digits
    if num_digits == 0 and args.num_type == "num":
        num_digits = len(str(len(files)))

    global_override = None

    for i, file_path in enumerate(files, start=1):
        new_name, variables = generate_new_filename(
            file_path=file_path,
            template=args.template,
            prefix=args.prefix,
            suffix=args.suffix,
            date_format=args.date_format,
            size_unit=args.size_unit,
            hash_algo=args.hash_algo,
            hash_length=args.hash_length,
            num=i,
            num_type=args.num_type,
            num_digits=num_digits
        )

        if args.output_dir:
            dst_path = os.path.join(args.output_dir, new_name)
        else:
            dst_path = os.path.join(os.path.dirname(file_path), new_name)

        operations.append((file_path, dst_path))

        if os.path.exists(dst_path) and file_path != dst_path:
            if global_override == "all":
                continue
            if global_override == "none":
                operations.pop()
                continue

            print(f"\n发现冲突: {os.path.basename(file_path)} -> {new_name}")
            result = handle_conflict(file_path, dst_path, not args.no_preserve)

            if result == "all":
                global_override = "all"
            elif result == "none":
                global_override = "none"
                operations.pop()
            elif not result:
                operations.pop()

    return operations


def execute_operations(
        operations: List[Tuple[str, str]],
        preserve_attrs: bool,
        dry_run: bool,
        logger: logging.Logger
):
    for src, dst in operations:
        if src == dst:
            continue

        logger.info(f"{src} -> {dst}")

        if dry_run:
            print(f"预览: {os.path.basename(src)} -> {os.path.basename(dst)}")
            continue

        os.makedirs(os.path.dirname(dst), exist_ok=True)

        if os.path.exists(dst):
            os.remove(dst)

        if preserve_attrs:
            shutil.copy2(src, dst)
        else:
            shutil.copy(src, dst)
            now = time.time()
            os.utime(dst, (now, now))


def reverse_operations(log_file: str, output_dir: str, dry_run: bool, preserve_attrs: bool):
    if not os.path.exists(log_file):
        print(f"错误: 日志文件不存在 - {log_file}")
        return

    operations = []
    with open(log_file, "r") as f:
        reader = csv.reader(f)
        next(reader)  # 跳过标题
        for row in reader:
            if len(row) >= 3:
                operations.append((row[2], row[1]))  # new_path -> original_path

    for new_path, original_path in operations:
        if not os.path.exists(new_path):
            print(f"警告: 文件不存在 - {new_path}")
            continue

        dst_path = os.path.join(output_dir, os.path.basename(original_path)) if output_dir else original_path

        if dry_run:
            print(f"预览: {os.path.basename(new_path)} -> {os.path.basename(dst_path)}")
            continue

        if os.path.exists(dst_path):
            print(f"冲突: 目标文件已存在 - {dst_path}")
            result = handle_conflict(new_path, dst_path, preserve_attrs)
            if not result:
                continue

        os.makedirs(os.path.dirname(dst_path), exist_ok=True)
        shutil.move(new_path, dst_path)


def setup_logger():
    log_dir = os.getcwd()
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, ".log", f"rename_{timestamp}.log")

    logger = logging.getLogger("file_renamer")
    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(logging.Formatter("%(asctime)s - %(message)s"))

    logger.addHandler(file_handler)
    logger.info("original_path,new_path,new_file_path")

    return logger, log_file


def main():
    args = parse_arguments()

    if args.reverse:
        if not args.log_file:
            print("错误: 逆向操作需要指定日志文件(--log-file)")
            return

        reverse_operations(
            log_file=args.log_file,
            output_dir=args.output_dir,
            dry_run=args.dry_run,
            preserve_attrs=not args.no_preserve
        )
        return

    if not args.target:
        print("错误: 必须指定目标目录")
        return

    if not os.path.isdir(args.target):
        print(f"错误: 目标目录不存在 - {args.target}")
        return

    logger, log_file = setup_logger()

    files = get_files(
        target=args.target,
        recursive=args.recursive,
        extensions=args.extensions,
        regex=args.regex
    )

    if not files:
        print("没有找到符合条件的文件")
        return

    sorted_files = sort_files(
        files=files,
        sort_by=args.sort_by,
        sort_order=args.sort_order
    )

    operations = process_files(sorted_files, args)

    if not operations:
        print("没有需要重命名的文件")
        return

    print("\n重命名预览:")
    for src, dst in operations:
        print(f"{os.path.basename(src)} -> {os.path.basename(dst)}")

    if not args.dry_run:
        confirm = input("\n确认执行重命名操作? (y/n): ").lower()
        if confirm != "y":
            print("操作已取消")
            return

    execute_operations(
        operations=operations,
        preserve_attrs=not args.no_preserve,
        dry_run=args.dry_run,
        logger=logger
    )

    print(f"\n操作完成! 日志文件: {log_file}")


if __name__ == "__main__":
    main()