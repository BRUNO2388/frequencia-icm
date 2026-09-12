from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

# 1) Estilos das sub-abas internas do Grupo de Louvor.
css_anchor = "  .gl-access-note { margin-bottom:12px; padding:10px 12px; border-radius:10px; background:var(--danger-bg); border:1px solid var(--danger-border); color:var(--danger-text); font-size:.78rem; line-height:1.4; }\n"
css_new = css_anchor + """  .gl-subnav { display:grid; grid-template-columns:repeat(3,1fr); gap:6px; margin:0 0 12px; padding:5px; border:1px solid var(--border-color); border-radius:12px; background:var(--card-bg); }\n  .gl-subtab-btn { border:1px solid transparent; background:transparent; color:var(--text-secondary); border-radius:9px; padding:9px 7px; font-size:.76rem; font-weight:900; cursor:pointer; transition:all .18s ease; }\n  .gl-subtab-btn:hover { border-color:var(--border-color); color:var(--text-main); background:var(--bg-container); }\n  .gl-subtab-btn.active { background:var(--primary); border-color:var(--primary); color:#fff; box-shadow:0 2px 8px var(--shadow); }\n  .gl-view { display:none; }\n  .gl-view.active { display:block; }\n"""
if s.count(css_anchor) != 1:
    raise SystemExit(f'Âncora CSS do GL inesperada: {s.count(css_anchor)}')
s = s.replace(css_anchor, css_new, 1)

# 2) Menu interno + tela Chamada como padrão.
start_anchor = """      <div id=\"gl-aviso-acesso\" class=\"gl-access-note\" hidden></div>\n\n      <section class=\"gl-section\">\n        <div class=\"gl-section-head\">\n          <div>\n            <h3>📝 Chamada do GL</h3>"""
start_new = """      <div id=\"gl-aviso-acesso\" class=\"gl-access-note\" hidden></div>\n\n      <div class=\"gl-subnav\" role=\"tablist\" aria-label=\"Áreas do Grupo de Louvor\">\n        <button type=\"button\" class=\"gl-subtab-btn active\" data-gl-view=\"chamada\" onclick=\"glAlternarTela('chamada')\">📝 Chamada</button>\n        <button type=\"button\" class=\"gl-subtab-btn\" data-gl-view=\"integrantes\" onclick=\"glAlternarTela('integrantes')\">👥 Integrantes</button>\n        <button type=\"button\" class=\"gl-subtab-btn\" data-gl-view=\"historico\" onclick=\"glAlternarTela('historico')\">📊 Histórico</button>\n      </div>\n\n      <div id=\"gl-view-chamada\" class=\"gl-view active\">\n      <section class=\"gl-section\">\n        <div class=\"gl-section-head\">\n          <div>\n            <h3>📝 Chamada do GL</h3>"""
if s.count(start_anchor) != 1:
    raise SystemExit(f'Início do módulo GL inesperado: {s.count(start_anchor)}')
s = s.replace(start_anchor, start_new, 1)

# 3) Fecha Chamada e abre Integrantes.
call_to_members = """        <div id=\"gl-msg\" class=\"gl-message\" aria-live=\"polite\"></div>\n      </section>\n\n      <section class=\"gl-section\">\n        <div class=\"gl-section-head\">\n          <div>\n            <h3>👥 Integrantes do GL</h3>"""
call_to_members_new = """        <div id=\"gl-msg\" class=\"gl-message\" aria-live=\"polite\"></div>\n      </section>\n      </div>\n\n      <div id=\"gl-view-integrantes\" class=\"gl-view\">\n      <section class=\"gl-section\">\n        <div class=\"gl-section-head\">\n          <div>\n            <h3>👥 Integrantes do GL</h3>"""
if s.count(call_to_members) != 1:
    raise SystemExit(f'Transição Chamada→Integrantes inesperada: {s.count(call_to_members)}')
s = s.replace(call_to_members, call_to_members_new, 1)

# 4) Fecha Integrantes e abre Histórico.
members_to_history = """        <div id=\"gl-lista-integrantes\" class=\"gl-manage-list\">\n          <div class=\"gl-muted\">Carregando cadastro existente...</div>\n        </div>\n      </section>\n\n      <section class=\"gl-section\">\n        <div class=\"gl-section-head\">\n          <div>\n            <h3>📊 Histórico de frequência</h3>"""
members_to_history_new = """        <div id=\"gl-lista-integrantes\" class=\"gl-manage-list\">\n          <div class=\"gl-muted\">Carregando cadastro existente...</div>\n        </div>\n      </section>\n      </div>\n\n      <div id=\"gl-view-historico\" class=\"gl-view\">\n      <section class=\"gl-section\">\n        <div class=\"gl-section-head\">\n          <div>\n            <h3>📊 Histórico de frequência</h3>"""
if s.count(members_to_history) != 1:
    raise SystemExit(f'Transição Integrantes→Histórico inesperada: {s.count(members_to_history)}')
s = s.replace(members_to_history, members_to_history_new, 1)

# 5) Fecha a tela Histórico antes de encerrar o módulo.
history_end = """        </div>\n      </section>\n    </div>\n\n    <!-- ABA 3: RELATÓRIO MENSAL -->"""
history_end_new = """        </div>\n      </section>\n      </div>\n    </div>\n\n    <!-- ABA 3: RELATÓRIO MENSAL -->"""
if s.count(history_end) != 1:
    raise SystemExit(f'Fim do Histórico inesperado: {s.count(history_end)}')
s = s.replace(history_end, history_end_new, 1)

# 6) Texto do topo mais enxuto.
s = s.replace(
    '          <p>Chamada, integrantes e histórico do GL no mesmo aplicativo. O módulo usa o cadastro e os registros já existentes do app Louvor.</p>',
    '          <p>Frequência e gestão do Grupo de Louvor.</p>',
    1
)

# 7) Controle das telas internas.
js_anchor = """    function iniciarGrupoLouvorAdmin() {\n      if (!window.isAdmin || !window.db || !window.dbRef || !window.dbOnValue) return;"""
js_new = """    function glAlternarTela(nome) {\n      if (!window.isAdmin) return;\n      const telas = ['chamada', 'integrantes', 'historico'];\n      if (!telas.includes(nome)) nome = 'chamada';\n\n      document.querySelectorAll('#tab-louvor .gl-subtab-btn').forEach(botao => {\n        botao.classList.toggle('active', botao.dataset.glView === nome);\n      });\n      document.querySelectorAll('#tab-louvor .gl-view').forEach(tela => {\n        tela.classList.toggle('active', tela.id === `gl-view-${nome}`);\n      });\n\n      if (nome === 'chamada') glRenderChamada();\n      else if (nome === 'integrantes') glRenderIntegrantes();\n      else if (nome === 'historico') glRenderHistorico();\n    }\n    window.glAlternarTela = glAlternarTela;\n\n    function iniciarGrupoLouvorAdmin() {\n      if (!window.isAdmin || !window.db || !window.dbRef || !window.dbOnValue) return;"""
if s.count(js_anchor) != 1:
    raise SystemExit(f'Âncora JS do GL inesperada: {s.count(js_anchor)}')
s = s.replace(js_anchor, js_new, 1)

# 8) Sempre entra no módulo pela Chamada.
aba_old = "      if (nomeAba === 'louvor' && window.isAdmin) glRenderTudo();"
aba_new = """      if (nomeAba === 'louvor' && window.isAdmin) {\n        glAlternarTela('chamada');\n        glRenderTudo();\n      }"""
if s.count(aba_old) != 1:
    raise SystemExit(f'Chamada do módulo em alternarAba inesperada: {s.count(aba_old)}')
s = s.replace(aba_old, aba_new, 1)

# 9) Abrir uma data pelo Histórico leva automaticamente para a tela Chamada.
hist_old = """      if (input) input.value = data;\n      glMontarRascunho();\n      document.getElementById('gl-data')?.scrollIntoView({ behavior: 'smooth', block: 'center' });"""
hist_new = """      if (input) input.value = data;\n      glMontarRascunho();\n      glAlternarTela('chamada');\n      document.getElementById('gl-data')?.scrollIntoView({ behavior: 'smooth', block: 'center' });"""
if s.count(hist_old) != 1:
    raise SystemExit(f'Função glAbrirDataHistorico inesperada: {s.count(hist_old)}')
s = s.replace(hist_old, hist_new, 1)

p.write_text(s, encoding='utf-8')
