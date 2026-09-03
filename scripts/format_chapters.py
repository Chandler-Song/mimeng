# -*- coding: utf-8 -*-
"""
批量优化 book/chapters/ 下所有 md 文件的格式。
断句规则：在引号外的句末符号（。！？及省略号……）处断句，
每个句子单独一行，元素之间用空行分隔。
保留标题（#）和引用（>）原样。
"""
import os
import re
import glob

OPEN_Q = ['\u201c', '\u300c', '\u300e', '\u2018']   # " 「 『 '
CLOSE_Q = ['\u201d', '\u300d', '\u300f', '\u2019']  # " 』 」 '
END_MARKS = set('。！？!?')


def split_sentences(text):
    """将一段文本按句末符号断句，引号内不断句。"""
    text = text.strip()
    if not text:
        return []

    sentences = []
    current = ""
    quote_depth = 0

    i = 0
    n = len(text)

    while i < n:
        char = text[i]
        current += char

        if char in OPEN_Q:
            quote_depth += 1
            i += 1
            continue
        if char in CLOSE_Q:
            quote_depth = max(0, quote_depth - 1)
            i += 1
            continue

        # 省略号 ……（两个 \u2026）
        if char == '\u2026' and i + 1 < n and text[i + 1] == '\u2026':
            current += text[i + 1]
            i += 2
            if quote_depth == 0:
                # 吸收后面连续的闭合引号
                while i < n and text[i] in CLOSE_Q:
                    current += text[i]
                    i += 1
                sentences.append(current.strip())
                current = ""
            continue

        # 句末符号
        if char in END_MARKS:
            if quote_depth == 0:
                # 吸收后面连续的闭合引号
                j = i + 1
                while j < n and text[j] in CLOSE_Q:
                    j += 1
                if j > i + 1:
                    current += text[i + 1:j]
                    i = j
                else:
                    i += 1
                sentences.append(current.strip())
                current = ""
            else:
                i += 1
            continue

        i += 1

    if current.strip():
        sentences.append(current.strip())

    return [s for s in sentences if s]


def count_end_marks(text):
    """统计引号外的句末符号数量。"""
    depth = 0
    count = 0
    for ch in text:
        if ch in OPEN_Q:
            depth += 1
        elif ch in CLOSE_Q:
            depth = max(0, depth - 1)
        elif depth == 0 and ch in END_MARKS:
            count += 1
    return count


def process_file(filepath):
    """处理单个 md 文件，返回是否修改。
    只对引号外句末符号>=2且长度>60的行断句，保留已格式化的短行。"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')
    elements = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        # 保留标题
        if stripped.startswith('#'):
            elements.append(stripped)
            continue
        # 保留引用
        if stripped.startswith('>'):
            elements.append(stripped)
            continue
        # 判断是否需要断句：多个句末符号且较长
        if count_end_marks(stripped) >= 2 and len(stripped) > 60:
            sentences = split_sentences(stripped)
            elements.extend(sentences)
        else:
            elements.append(stripped)

    output = '\n\n'.join(elements) + '\n'

    if output != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(output)
        return True
    return False


def main():
    chapters_dir = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'book', 'chapters'
    )
    files = sorted(glob.glob(os.path.join(chapters_dir, 'ch*.md')))
    modified = 0
    for f in files:
        if process_file(f):
            modified += 1
    print(f'共 {len(files)} 个文件，修改 {modified} 个')


if __name__ == '__main__':
    main()