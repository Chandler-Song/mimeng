import pypdf

pdf_path = r'c:\Users\Administrator\IDEProjects\mimeng\咪蒙.pdf'
pdf = pypdf.PdfReader(pdf_path)

first_item = pdf.outline[2]
print(f'Title: {first_item.title}')
print(f'Type: {type(first_item)}')
print(f'Attributes: {dir(first_item)}')
print(f'Has dest: {hasattr(first_item, "dest")}')
print(f'Has destination: {hasattr(first_item, "destination")}')

if hasattr(first_item, 'destination'):
    print(f'Destination: {first_item.destination}')
    print(f'Page number: {pdf.get_destination_page_number(first_item.destination)}')