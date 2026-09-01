from pathlib import Path
import re

path = Path('index.html')
text = path.read_text(encoding='utf-8')
original = text

# 1) Os chips deixam de depender de onclick inline. O clique será tratado
# por delegação de eventos, de forma igual para Admin e Membro.
pattern_onclick = re.compile(r' onclick="setFiltroChamada\(\'([^\']+)\', this\)"')
text, removidos = pattern_onclick.subn('', text)
if removidos != 8:
    raise SystemExit(f'Esperados 8 onclick de filtros; encontrados {removidos}')

text, tipos = re.subn(r'<button class="filter-chip', '<button type="button" class="filter-chip', text)
if tipos != 8:
    raise SystemExit(f'Esperados 8 chips para receber type=button; encontrados {tipos}')

old_filter = '''    function setFiltroChamada(filtro, botao) {
      window.filtroChamadaAtual = filtro;
      document.querySelectorAll('.filter-chip').forEach(b => b.classList.remove('active'));
      if (botao) botao.classList.add('active');
      carregarChamadaCulto();
    }
'''
new_filter = '''    function setFiltroChamada(filtro, botao) {
      const filtrosValidos = ['PRESENTES', ...CATEGORIAS];
      if (!filtrosValidos.includes(filtro)) return;

      window.filtroChamadaAtual = filtro;
      document.querySelectorAll('.filter-chip').forEach(b => b.classList.remove('active'));
      if (botao) botao.classList.add('active');

      // Ao navegar por categoria, fecha qualquer resultado da busca por nome
      // para que a lista da classe fique totalmente visível.
      const busca = document.getElementById('busca-membro');
      const resultados = document.getElementById('search-results-box');
      if (busca) busca.value = '';
      if (resultados) {
        resultados.innerHTML = '';
        resultados.style.display = 'none';
      }

      carregarChamadaCulto();
    }

    // Expõe explicitamente a função usada pela interface, inclusive para
    // sessões autenticadas como Membro.
    window.setFiltroChamada = setFiltroChamada;

    function prepararFiltrosChamada() {
      const filtros = document.getElementById('filtros-chamada');
      if (!filtros || filtros.dataset.filtrosV12 === '1') return;
      filtros.dataset.filtrosV12 = '1';

      filtros.addEventListener('click', (event) => {
        const botao = event.target.closest('.filter-chip');
        if (!botao || !filtros.contains(botao)) return;
        event.preventDefault();
        event.stopPropagation();
        setFiltroChamada(botao.dataset.filter || '', botao);
      });
    }

    prepararFiltrosChamada();
'''
if text.count(old_filter) != 1:
    raise SystemExit(f'Bloco setFiltroChamada esperado uma vez; encontrado {text.count(old_filter)}')
text = text.replace(old_filter, new_filter, 1)

# 2) Corrige as comparações de "hoje" do Membro para o fuso da igreja.
# Antes, toISOString() usava UTC e podia virar o dia às 21h no Brasil.
sp_today = "new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo' }).format(new Date())"

old = "atual.data === new Date().toISOString().split('T')[0]"
count = text.count(old)
if count != 1:
    raise SystemExit(f'Esperada 1 validação de atual.data; encontrada {count}')
text = text.replace(old, f"atual.data === {sp_today}")

old = "inputDataCulto.value = new Date().toISOString().split('T')[0];"
count = text.count(old)
if count != 1:
    raise SystemExit(f'Esperada 1 definição da data do membro; encontrada {count}')
text = text.replace(old, f"inputDataCulto.value = {sp_today};")

old = "if (!window.isAdmin && inputData.value !== new Date().toISOString().split('T')[0])"
count = text.count(old)
if count != 6:
    raise SystemExit(f'Esperadas 6 validações de ações do membro; encontradas {count}')
text = text.replace(old, f"if (!window.isAdmin && inputData.value !== {sp_today})")

if text == original:
    raise SystemExit('Nenhuma alteração aplicada')

path.write_text(text, encoding='utf-8')
print('Patch V12 aplicado com sucesso.')
