from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old1 = '>🔒 Relatório Mensal</button>'
new1 = '>📊 Relatório Mensal</button>'
old2 = '>🔒 Cadastrar Membros</button>'
new2 = '>👥 Cadastrar Membros</button>'

if s.count(old1) != 1:
    raise SystemExit(f'Rótulo Relatório Mensal inesperado: {s.count(old1)}')
if s.count(old2) != 1:
    raise SystemExit(f'Rótulo Cadastrar Membros inesperado: {s.count(old2)}')

s = s.replace(old1, new1, 1)
s = s.replace(old2, new2, 1)

p.write_text(s, encoding='utf-8')
