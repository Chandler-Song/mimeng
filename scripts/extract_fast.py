import fitz  # PyMuPDF
from pathlib import Path
import time
import json
import re

pdf_path = Path(r'c:\Users\Administrator\IDEProjects\mimeng\咪蒙.pdf')
doc = fitz.open(pdf_path)

# 使用pypdf获取书签结构
import pypdf
pdf_reader = pypdf.PdfReader(pdf_path)
article_list = pdf_reader.outline[1]
total_articles = len(article_list)

print(f'开始提取 {total_articles} 篇文章（使用PyMuPDF加速）...')
print(f'PDF总页数: {len(doc)}')

# 创建输出目录
output_dir = Path(r'c:\Users\Administrator\IDEProjects\mimeng\articles')
output_dir.mkdir(exist_ok=True)

# 保存进度
progress_file = output_dir / 'progress.json'
progress = {'completed': 0, 'total': total_articles, 'last_article_index': -1}

if progress_file.exists():
    with open(progress_file, 'r', encoding='utf-8') as f:
        progress = json.load(f)
    print(f'检测到进度文件，已完成 {progress["completed"]}/{progress["total"]} 篇文章')

start_index = progress['last_article_index'] + 1
start_time = time.time()

def clean_title(title):
    """清理文件名中的非法字符"""
    safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)
    safe_title = safe_title.strip()
    return safe_title[:100]  # 限制文件名长度

for idx in range(start_index, total_articles):
    item = article_list[idx]
    title = item.title
    start_page = item.page - 1  # 转换为0-based索引
    
    # 确定结束页
    if idx < total_articles - 1:
        end_page = article_list[idx + 1].page - 1
    else:
        end_page = len(doc) - 1
    
    # 提取文章内容
    md_content = []
    md_content.append(f'# {title}\n\n')
    
    for page_idx in range(start_page, min(end_page + 1, len(doc))):
        page = doc[page_idx]
        text = page.get_text()
        if text:
            md_content.append(text)
            md_content.append('\n\n')
    
    md_text = ''.join(md_content)
    
    # 保存单篇文章
    safe_title = clean_title(title)
    if not safe_title:
        safe_title = f'article_{idx}'
    article_file = output_dir / f'{idx:03d}_{safe_title}.md'
    article_file.write_text(md_text, encoding='utf-8')
    
    # 更新进度
    progress['completed'] = idx + 1
    progress['last_article_index'] = idx
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump(progress, f, ensure_ascii=False, indent=2)
    
    # 显示进度
    elapsed = time.time() - start_time
    processed = idx - start_index + 1
    avg_time = elapsed / processed
    remaining = (total_articles - idx - 1) * avg_time
    print(f'[{idx + 1}/{total_articles}] {title[:50]}... | 耗时: {elapsed:.0f}s | 剩余: {remaining:.0f}s ({remaining/60:.1f}min)')

doc.close()

# 生成合并的完整文件
print('\n正在生成合并文件...')
all_md = []
all_md.append('# 咪蒙文章合集\n\n')
all_md.append(f'总共有 **{total_articles}** 篇文章\n\n')
all_md.append('---\n\n')

for idx in range(total_articles):
    safe_title = clean_title(article_list[idx].title)
    if not safe_title:
        safe_title = f'article_{idx}'
    article_file = output_dir / f'{idx:03d}_{safe_title}.md'
    
    if article_file.exists():
        content = article_file.read_text(encoding='utf-8')
        all_md.append(content)
        all_md.append('\n\n---\n\n')
        if (idx + 1) % 50 == 0:
            print(f'合并: {idx + 1}/{total_articles}')

final_md = ''.join(all_md)
output_file = Path(r'c:\Users\Administrator\IDEProjects\mimeng\咪蒙.md')
output_file.write_text(final_md, encoding='utf-8')

total_elapsed = time.time() - start_time
print(f'\n✅ 完成！')
print(f'总耗时: {total_elapsed:.0f}秒 ({total_elapsed/60:.1f}分钟)')
print(f'合并文件: {output_file}')
print(f'单篇文章目录: {output_dir}')
print(f'总文章数: {total_articles}')