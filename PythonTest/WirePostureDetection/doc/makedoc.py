import ast
import os
import pathlib
import traceback


def extract_methods(file_path: str) -> dict:
    """提取单个文件中的函数和方法"""
    # 尝试多种可能的编码
    encodings = ['utf-8', 'gbk', 'latin-1', 'iso-8859-1']
    file_content = None

    for encoding in encodings:
        try:
            with open(file_path, "r", encoding=encoding) as f:
                file_content = f.read()
            break
        except UnicodeDecodeError:
            continue

    if file_content is None:
        print(f"警告: 无法解码文件 {file_path}，跳过")
        return {}

    try:
        tree = ast.parse(file_content)
    except SyntaxError as e:
        print(f"语法错误在 {file_path}:{e.lineno} - {e.msg}，跳过")
        return {}

    results = {}
    for node in ast.walk(tree):
        # 捕获函数和异步函数
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            docstring = ast.get_docstring(node) or "No docstring"
            params = [arg.arg for arg in node.args.args]
            results[node.name] = {
                "doc": docstring,
                "params": params,
                "lineno": node.lineno
            }
        # 捕获类中的方法
        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    docstring = ast.get_docstring(child) or "No docstring"
                    params = [arg.arg for arg in child.args.args]
                    method_name = f"{node.name}.{child.name}"
                    results[method_name] = {
                        "doc": docstring,
                        "params": params,
                        "lineno": child.lineno
                    }
    return results


def generate_docs(project_path: str, output_file: str):
    """生成项目文档"""
    output = ["# 项目API文档\n\n> 自动生成的函数/方法文档\n"]

    # 统计信息
    total_files = 0
    processed_files = 0
    error_files = []

    for root, _, files in os.walk(project_path):
        # 跳过虚拟环境等目录
        if any(dir in root for dir in ["venv", "__pycache__", ".git", ".idea", "dist", "build"]):
            continue

        for file in files:
            if not file.endswith(".py"):
                continue

            total_files += 1
            file_path = os.path.join(root, file)
            try:
                relative_path = pathlib.Path(file_path).relative_to(project_path)
                methods = extract_methods(file_path)

                if methods:
                    processed_files += 1
                    output.append(f"## 🗂️ 文件: `{relative_path}`\n")

                    # 创建表格
                    output.append("| 方法 | 参数 | 行号 | 描述 |")
                    output.append("|------|------|------|------|")

                    for name, info in methods.items():
                        param_str = ", ".join(info['params'])
                        output.append(f"| `{name}` | `{param_str}` | {info['lineno']} | {info['doc']} |")
                    output.append("\n")
            except Exception as e:
                error_files.append((file_path, str(e)))
                continue

    # 添加统计信息
    output.append(f"\n## 统计信息\n")
    output.append(f"- 扫描文件总数: {total_files}")
    output.append(f"- 成功处理文件: {processed_files}")
    output.append(f"- 失败文件数: {len(error_files)}")

    if error_files:
        output.append("\n## 错误文件列表\n")
        for file, error in error_files:
            output.append(f"- `{file}`: {error}")

    # 写入输出文件
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(output))

    print(f"文档已生成至: {output_file}")
    print(f"统计: {processed_files}/{total_files} 文件成功处理")


if __name__ == "__main__":
    project_path = "../"
    output_file = "API_DOC.md"

    print(f"开始扫描项目: {project_path}")
    generate_docs(project_path, output_file)