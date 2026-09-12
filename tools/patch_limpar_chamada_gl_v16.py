from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

old_button = '''<button type="button" class="btn-small-sec" onclick="glLimparMarcacoes()">🔄 Limpar marcações</button>'''
new_button = '''<button type="button" class="btn-small-sec" onclick="glLimparMarcacoes()">🗑️ Limpar chamada</button>'''
if s.count(old_button) != 1:
    raise SystemExit(f'Botão esperado 1 vez, encontrado {s.count(old_button)}')
s = s.replace(old_button, new_button, 1)

old_func = '''    function glLimparMarcacoes() {
      if (!window.isAdmin) return;
      Object.values(glRascunho).forEach(item => {
        item.status = '';
        item.justificado = 'nao';
        item.motivo = '';
      });
      glRenderChamada();
    }
'''

new_func = '''    async function glLimparMarcacoes() {
      if (!window.isAdmin) return;
      const data = document.getElementById('gl-data')?.value || '';
      if (!data) return alert('Selecione a data da chamada.');

      const temChamadaSalva = !!(window.glRegistros && window.glRegistros[data]);
      if (temChamadaSalva) {
        const confirmar = confirm(`Apagar a chamada do Grupo de Louvor de ${glFormatarData(data)}?\\n\\nEsta ação removerá a chamada salva desta data, mas não apagará os integrantes cadastrados.`);
        if (!confirmar) return;
        try {
          await window.dbRemove(window.dbRef(window.db, `registros_louvor/${data}`));
          delete window.glRegistros[data];
          glMontarRascunho();
          glMostrarMensagem(`✅ Chamada de ${glFormatarData(data)} apagada.`);
          glAtualizarKpis();
          glRenderHistorico();
          return;
        } catch (erro) {
          console.error(erro);
          glMostrarMensagem('Não foi possível apagar a chamada. Verifique a conexão e as permissões do Firebase.', true);
          return;
        }
      }

      Object.values(glRascunho).forEach(item => {
        item.status = '';
        item.justificado = 'nao';
        item.motivo = '';
      });
      glRenderChamada();
      glMostrarMensagem('Marcações não salvas foram limpas.');
    }
'''

if s.count(old_func) != 1:
    raise SystemExit(f'Função esperada 1 vez, encontrado {s.count(old_func)}')
s = s.replace(old_func, new_func, 1)

p.write_text(s, encoding='utf-8')
