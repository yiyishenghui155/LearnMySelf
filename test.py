import re
from pathlib import Path


def get_relative_line_in_patch(patch_content: str, target_line: int) -> int | None:
    """
    根据 GitHub patch 内容和文件中的绝对行号，计算出该行在 hunk 内的相对偏移量。
    如果该行不在任何 hunk 中，返回 None。
    """
    # 用正则匹配每个 hunk 的头
    hunk_pattern = re.compile(r"@@ -(\d+),?(\d*) \+(\d+),?(\d*) @@")

    for match in hunk_pattern.finditer(patch_content):
        old_start, old_count, new_start, new_count = match.groups()
        new_start = int(new_start)
        new_count = int(new_count) if new_count else 1

        # hunk 范围
        new_end = new_start + new_count - 1

        if new_start <= target_line <= new_end:
            # 找到所属 hunk，计算相对位置（从1开始）
            return target_line - new_start + 1

    return None

def main():
    file_path = Path( "D:\\bad_code_example.py")
    patch_content = open(file_path, 'r').read()
    # 添加行号前缀
    lines = patch_content.split('\n')
    numbered_lines = [f"{i + 1:3d} | {line}" for i, line in enumerate(lines)]
    numbered_content = '\n'.join(numbered_lines)
    print(f"{numbered_content}")

if __name__ == "__main__":
    main()
