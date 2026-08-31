import pypdf

pdf_path = r'c:\Users\Administrator\IDEProjects\mimeng\咪蒙.pdf'
pdf = pypdf.PdfReader(pdf_path)

print(f'Outline length: {len(pdf.outline)}')
print(f'Outline items:')

for i, item in enumerate(pdf.outline):
    print(f'\n{i}: {type(item)}')
    if isinstance(item, list):
        print(f'  List with {len(item)} items')
        for j, subitem in enumerate(item[:5]):  # 只显示前5个
            print(f'  {j}: {subitem.title}')
    else:
        print(f'  Title: {item.title}')
        print(f'  Attributes: {[a for a in dir(item) if not a.startswith("_")]}')