import os
import re
import shutil
import json
from pathlib import Path

articles_dir = Path(r'c:\Users\Administrator\IDEProjects\mimeng\articles')
chapters_dir = Path(r'c:\Users\Administrator\IDEProjects\mimeng\book\chapters')
output_json = Path(r'c:\Users\Administrator\IDEProjects\mimeng\scripts\chapters_config.json')

files = list(articles_dir.glob('*.md'))
files = [f for f in files if f.name != 'progress.json']

def get_number(filepath):
    match = re.match(r'^(\d+)_', filepath.name)
    return int(match.group(1)) if match else 9999

files.sort(key=get_number)

print(f'找到 {len(files)} 个文章文件')

chapters_dir.mkdir(exist_ok=True)

chapters_config = []
parts_config = {}

part_size = 50
total_parts = (len(files) + part_size - 1) // part_size

for i, src in enumerate(files):
    num = get_number(src)
    dst_name = f'ch{num:03d}.md'
    dst = chapters_dir / dst_name
    shutil.copy2(src, dst)

    title = src.stem
    title = re.sub(r'^\d+_', '', title)
    if len(title) > 40:
        title = title[:40] + '...'

    part_idx = i // part_size
    part_start = part_idx * part_size + 1
    part_end = min((part_idx + 1) * part_size, len(files))
    part_name = f'第{part_idx + 1}篇 ({part_start}-{part_end})'

    chapters_config.append({
        'idx': i,
        'file': f'chapters/{dst_name}',
        'title': title,
        'part': part_name
    })

    if part_name not in parts_config:
        parts_config[part_name] = []
    parts_config[part_name].append({
        'idx': i,
        'file': f'chapters/{dst_name}',
        'title': title,
        'part': part_name
    })

config_data = {
    'chapters': chapters_config,
    'parts': parts_config,
    'total': len(files)
}

with open(output_json, 'w', encoding='utf-8') as f:
    json.dump(config_data, f, ensure_ascii=False, indent=2)

print(f'✅ 已复制 {len(files)} 个章节文件到 {chapters_dir}')
print(f'✅ 配置已保存到 {output_json}')
print(f'✅ 共分为 {total_parts} 篇，每篇约 {part_size} 章')
print(f'\n前5个章节:')
for ch in chapters_config[:5]:
    print(f"  {ch['idx']}: {ch['file']} - {ch['title']} ({ch['part']})")
print(f'\n后5个章节:')
for ch in chapters_config[-5:]:
    print(f"  {ch['idx']}: {ch['file']} - {ch['title']} ({ch['part']})")