import os
import re
import difflib

CHAPTERS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'book', 'chapters')

def is_obvious_artifact(line):
    stripped = line.strip()
    if not stripped:
        return False
    if re.match(r'^\d{4}-\d{2}-\d{2}\s*-\s+', stripped):
        return True
    if '༻' in stripped or re.match(r'^[\u0F00-\u0FFF]+$', stripped):
        return True
    if re.match(r'^[（(].*图片来源.*[）)]$', stripped):
        return True
    if re.match(r'^[（(].*作品[）)]$', stripped):
        return True
    if re.match(r'^[（(].*图片来源.*[）)]$', stripped):
        return True
    return False

def is_metadata_line(line, title_text):
    stripped = line.strip()
    if not stripped:
        return True
    if len(stripped) == 1 and not stripped.isdigit():
        return True
    if stripped == title_text:
        return True
    if stripped == '原创':
        return True
    if re.match(r'^\d{4}-\d{2}-\d{2}$', stripped):
        return True
    if stripped == '咪蒙':
        return True
    if re.match(r'^\d{4}-\d{2}-\d{2}\s+咪蒙', stripped):
        return True
    if re.match(r'^\s*咪蒙\s*咪蒙\s*$', stripped):
        return True
    if re.match(r'^\s*\d{4}-\d{2}-\d{2}\s*咪蒙\s*咪蒙\s*$', stripped):
        return True
    return False

def is_content_start(line):
    stripped = line.strip()
    if not stripped:
        return False
    if stripped.startswith('"') or stripped.startswith('"') or stripped.startswith('「'):
        return True
    if re.match(r'^\d{1,2}$', stripped):
        return True
    if len(stripped) > 5 and any(c in stripped for c in '。！？，'):
        return True
    return False

def is_section_number(line):
    stripped = line.strip()
    return bool(re.match(r'^\d{1,2}$', stripped))

def clean_paragraph(para, title_text):
    while True:
        stripped = para.strip()
        if not stripped:
            return ""
        changed = False
        if stripped.startswith('咪蒙'):
            stripped = stripped[2:]
            changed = True
        if stripped.startswith('原创'):
            stripped = stripped[2:]
            changed = True
        if title_text and stripped.startswith(title_text):
            stripped = stripped[len(title_text):]
            changed = True
        m = re.match(r'^\d{4}-\d{2}-\d{2}', stripped)
        if m:
            stripped = stripped[m.end():]
            changed = True
        m = re.search(r'\d{4}-\d{2}-\d{2}$', stripped)
        if m:
            stripped = stripped[:m.start()]
            changed = True
        para = stripped.strip()
        if not changed:
            break
    return para

def find_correct_title(lines, title_text):
    for line in lines[1:20]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped == title_text:
            continue
        if is_metadata_line(stripped, title_text):
            continue
        if re.match(r'^\d{4}-\d{2}-\d{2}', stripped):
            continue
        if stripped == '原创' or stripped == '咪蒙':
            continue
        ratio = difflib.SequenceMatcher(None, title_text, stripped).ratio()
        if 0.6 < ratio < 1.0 and len(stripped) > 5:
            return stripped
        if ratio == 1.0:
            return None
        break
    return None

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    lines = content.split('\n')

    if not lines or len(lines) < 3:
        return False

    title_line = lines[0]
    title_text = title_line.lstrip('# ').strip()

    correct_title = find_correct_title(lines, title_text)
    if correct_title:
        title_text = correct_title
        title_line = f'# {correct_title}'

    cleaned_lines = []
    for line in lines[1:]:
        if not is_obvious_artifact(line):
            cleaned_lines.append(line.strip())

    content_lines = []
    in_metadata = True
    for line in cleaned_lines:
        if in_metadata:
            if is_metadata_line(line, title_text):
                continue
            else:
                in_metadata = False
                content_lines.append(line)
        else:
            content_lines.append(line)

    paragraphs = []
    current_para = []

    for line in content_lines:
        if line:
            if is_section_number(line) and current_para:
                paragraphs.append(''.join(current_para))
                current_para = [line]
            elif current_para and is_section_number(current_para[-1]):
                paragraphs.append(''.join(current_para))
                current_para = [line]
            else:
                current_para.append(line)
        else:
            if current_para:
                paragraphs.append(''.join(current_para))
                current_para = []

    if current_para:
        paragraphs.append(''.join(current_para))

    paragraphs = [p for p in paragraphs if p.strip()]
    paragraphs = [clean_paragraph(p, title_text) for p in paragraphs]
    paragraphs = [p for p in paragraphs if p.strip()]

    if not paragraphs:
        return False

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(title_line + '\n')
        for para in paragraphs:
            f.write('\n' + para + '\n')

    return True

def main():
    total = 0
    success = 0
    for i in range(1, 747):
        filename = f'ch{i:03d}.md'
        filepath = os.path.join(CHAPTERS_DIR, filename)
        if os.path.exists(filepath):
            total += 1
            if clean_file(filepath):
                success += 1
            if i % 100 == 0:
                print(f'已处理 {i}/746...')

    print(f'\n完成！成功处理 {success}/{total} 个文件')

if __name__ == '__main__':
    main()