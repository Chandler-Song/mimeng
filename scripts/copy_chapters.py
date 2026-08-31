import shutil
from pathlib import Path

articles_dir = Path(r'c:\Users\Administrator\IDEProjects\mimeng\articles')
chapters_dir = Path(r'c:\Users\Administrator\IDEProjects\mimeng\book\chapters')

mapping = {
    '001_女友对你作你应该谢天谢地因为她爱你.md': 'ch01.md',
    '003_你为什么是外貌协会的.md': 'ch02.md',
    '005_如何对付爱搞暧昧的男人.md': 'ch03.md',
    '008_异地恋怎么才能成功呢.md': 'ch04.md',
    '020_所谓情商高就是懂得好好说话.md': 'ch05.md',
    '030_作为老板今天我又哭着下班了.md': 'ch06.md',
    '081_到底怎么才能赚到很多钱？.md': 'ch07.md',
    '130_你知道你为什么穷吗？因为你喜欢省钱！.md': 'ch08.md',
    '082_我上讨好世界，我只讨好自己.md': 'ch09.md',
    '083_亲人去世了，该怎么走出阴影？.md': 'ch10.md',
    '051_你明明配得上更好的生活.md': 'ch11.md',
    '053_你可以坚强但上必逞强.md': 'ch12.md',
}

count = 0
for src_name, dst_name in mapping.items():
    src = articles_dir / src_name
    dst = chapters_dir / dst_name
    if src.exists():
        shutil.copy2(src, dst)
        print(f'✅ {dst_name} <- {src_name}')
        count += 1
    else:
        print(f'❌ 未找到: {src_name}')

print(f'\n共复制 {count} 个章节文件')
