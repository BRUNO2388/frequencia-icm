from pathlib import Path

p = Path('index.html')
t = p.read_text(encoding='utf-8')

old_userbar = "  .user-bar { width:100%; max-width:680px; display:none; justify-content:space-between; align-items:center; gap:10px; margin-bottom:10px; font-size:.82rem; color:var(--text-secondary); }"
new_userbar = """  .user-bar { width:100%; max-width:680px; display:none; justify-content:space-between; align-items:center; gap:8px; margin-bottom:10px; padding:6px 2px; font-size:.82rem; color:var(--text-secondary); position:sticky; top:6px; z-index:15000; background:var(--bg-body); border-radius:12px; }
  #user-info { flex:0 0 auto; font-weight:700; white-space:nowrap; }
  .user-bar > .btn-small-sec { flex:0 0 auto; }"""
assert old_userbar in t, 'CSS da barra do usuario nao encontrado'
t = t.replace(old_userbar, new_userbar, 1)

old_counter_css = """  .floating-counter {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: var(--primary);
    color: #ffffff;
    padding: 12px 18px;
    border-radius: 30px;
    font-weight: bold;
    font-size: 0.95rem;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
    z-index: 9999;
    display: flex;
    align-items: center;
    gap: 8px;
    border: 2px solid var(--bg-container);
  }"""
new_counter_css = """  .floating-counter {
    position: static;
    flex:1 1 auto;
    min-width:0;
    max-width:300px;
    background: var(--primary);
    color: #ffffff;
    padding: 7px 10px;
    border-radius: 22px;
    font-weight: 800;
    font-size: 0.78rem;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.18);
    display: flex;
    align-items: center;
    justify-content:center;
    gap: 5px;
    border: 1px solid var(--bg-container);
    white-space:nowrap;
  }"""
assert old_counter_css in t, 'CSS do contador flutuante nao encontrado'
t = t.replace(old_counter_css, new_counter_css, 1)

old_mobile = "    .floating-counter { bottom: 15px; right: 15px; padding: 10px 14px; font-size: 0.85rem; }"
new_mobile = """    .user-bar { gap:6px; padding:5px 0; font-size:.76rem; }
    .floating-counter { max-width:none; padding:6px 8px; gap:4px; font-size:.72rem; box-shadow:0 2px 6px rgba(0,0,0,.16); }
    .floating-counter .counter-word { display:none; }"""
assert old_mobile in t, 'CSS mobile do contador nao encontrado'
t = t.replace(old_mobile, new_mobile, 1)

old_bar_html = "  <div id=\"user-bar\" class=\"user-bar no-print\"><span id=\"user-info\"></span><button class=\"btn-small-sec\" onclick=\"sairDoApp()\">Sair</button></div>"
new_bar_html = """  <div id=\"user-bar\" class=\"user-bar no-print\">
    <span id=\"user-info\"></span>
    <div id=\"badge-contador-flutuante\" class=\"floating-counter\" title=\"Membros presentes • visitantes • total\">
      <span>👥 <span id=\"floating-membros-count\">0</span><span class=\"counter-word\"> membros</span></span>
      <span>• 🙋 <span id=\"floating-visitantes-count\">0</span><span class=\"counter-word\"> visitantes</span></span>
      <strong>• Total <span id=\"floating-presenca-count\">0</span></strong>
    </div>
    <button class=\"btn-small-sec\" onclick=\"sairDoApp()\">Sair</button>
  </div>"""
assert old_bar_html in t, 'HTML da barra do usuario nao encontrado'
t = t.replace(old_bar_html, new_bar_html, 1)

old_float_html = """  <!-- CONTADOR FLUTUANTE -->
  <div id=\"badge-contador-flutuante\" class=\"floating-counter\">
    <span>👥 <span id=\"floating-membros-count\">0</span> membros</span>
    <span>• <span id=\"floating-visitantes-count\">0</span> visitantes</span>
    <strong>• Total <span id=\"floating-presenca-count\">0</span></strong>
  </div>

"""
assert old_float_html in t, 'HTML antigo do contador nao encontrado'
t = t.replace(old_float_html, '', 1)

assert t.count('id="badge-contador-flutuante"') == 1
assert 'bottom: 20px;' not in t
assert "floatingBadge.style.display = nomeAba === 'chamada' ? 'flex' : 'none'" in t

p.write_text(t, encoding='utf-8')
