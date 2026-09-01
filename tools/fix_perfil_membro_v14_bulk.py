from pathlib import Path
p = Path('index.html')
s = p.read_text(encoding='utf-8')
old_css = '  #tab-chamada .admin-only.admin-visible[style*="display:flex"] { display:flex !important; }\n'
new_css = '  .chamada-bulk-actions { justify-content:space-between; margin-bottom:12px; gap:6px; }\n  .chamada-bulk-actions.admin-visible { display:flex; }\n'
if s.count(old_css) != 1:
    raise SystemExit(f'CSS anterior encontrado {s.count(old_css)} vez(es)')
s = s.replace(old_css, new_css, 1)
old_html = '      <div class="admin-only" style="display:flex; justify-content:space-between; margin-bottom:12px; gap: 6px;">'
new_html = '      <div class="admin-only chamada-bulk-actions">'
if s.count(old_html) != 1:
    raise SystemExit(f'Bloco bulk encontrado {s.count(old_html)} vez(es)')
s = s.replace(old_html, new_html, 1)
p.write_text(s, encoding='utf-8')
print('Ajuste bulk V14 aplicado.')
