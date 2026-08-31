import pypdf

pdf_path = r'c:\Users\Administrator\IDEProjects\mimeng\咪蒙.pdf'
pdf = pypdf.PdfReader(pdf_path)

article_list = pdf.outline[1]

print(f'Article list length: {len(article_list)}')

# 检查前几个文章项
for i, item in enumerate(article_list[:5]):
    print(f'\n{i}: {item.title}')
    print(f'  Type: {type(item)}')
    print(f'  Attributes: {[a for a in dir(item) if not a.startswith("_")]}')

    # 尝试获取页面信息
    if hasattr(item, 'page'):
        print(f'  Page: {item.page}')
    if hasattr(item, 'dest_array'):
        print(f'  Dest array: {item.dest_array}')
    if hasattr(item, 'typ'):
        print(f'  Typ: {item.typ}')

    # 尝试获取页面号
    try:
        page_num = pdf.get_destination_page_number(item)
        print(f'  Page number: {page_num}')
    except Exception as e:
        print(f'  Error getting page number: {e}')