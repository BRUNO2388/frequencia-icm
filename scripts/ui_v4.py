from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

def rep(old, new, count=1):
    global s
    if old not in s:
        raise SystemExit('Trecho esperado nao encontrado: ' + old[:160])
    s = s.replace(old, new, count)

css = r'''

  /* ===== EXPERIÊNCIA V4: PAINEL, CALENDÁRIO E CHAMADA ===== */
  .dashboard-hero {
    background: linear-gradient(135deg, var(--primary) 0%, var(--secondary) 100%);
    color: #fff;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 14px;
    box-shadow: 0 5px 18px var(--shadow);
  }
  .dashboard-hero small { opacity: .86; font-weight: 700; }
  .dashboard-hero h3 { font-size: 1.2rem; margin: 5px 0 2px; }
  .dashboard-status { display:inline-flex; align-items:center; gap:6px; margin-top:8px; padding:5px 10px; border-radius:20px; background:rgba(255,255,255,.16); font-size:.78rem; font-weight:800; }
  .dashboard-grid { display:grid; grid-template-columns:repeat(3,1fr); gap:8px; margin:12px 0; }
  .dashboard-card { background:var(--card-bg); border:1px solid var(--border-color); border-radius:12px; padding:13px 8px; text-align:center; }
  .dashboard-card .value { display:block; color:var(--primary); font-size:1.45rem; line-height:1; font-weight:900; }
  .dashboard-card .label { display:block; color:var(--text-secondary); font-size:.7rem; text-transform:uppercase; margin-top:5px; font-weight:800; }
  .dashboard-actions { display:grid; grid-template-columns:1fr 1fr; gap:8px; }
  .dashboard-actions .btn-main { margin-top:0; }

  .culto-status-banner { display:flex; justify-content:space-between; align-items:center; gap:10px; padding:10px 12px; border:1px solid var(--border-color); background:var(--card-bg); border-radius:10px; margin-bottom:12px; font-size:.82rem; font-weight:800; }
  .culto-status-banner.finalizado { background:var(--success-bg); border-color:var(--success-border); color:var(--success-text); }
  .culto-status-banner.andamento { background:var(--warning-bg); border-color:var(--warning-border); color:var(--warning-text); }
  .finalizar-btn { width:auto !important; min-width:170px; margin:0 !important; }

  .filter-chips { display:flex; gap:6px; overflow-x:auto; padding:2px 0 10px; scrollbar-width:thin; }
  .filter-chip { flex:0 0 auto; border:1px solid var(--border-color); background:var(--card-bg); color:var(--text-main); border-radius:18px; padding:6px 11px; font-size:.75rem; font-weight:800; cursor:pointer; }
  .filter-chip.active { background:var(--primary); border-color:var(--primary); color:#fff; }
  .status-badge-btn.ausente { background:var(--danger-bg); color:var(--danger-text); border-color:var(--danger-border); }
  .member-select-item { transition:transform .15s ease, box-shadow .15s ease; }
  .member-select-item:hover { transform:translateY(-1px); box-shadow:0 3px 10px var(--shadow); }

  .calendar-card { border:1px solid var(--border-color); background:var(--card-bg); border-radius:12px; padding:12px; margin:12px 0 16px; }
  .calendar-head { display:flex; align-items:center; justify-content:space-between; gap:8px; margin-bottom:10px; }
  .calendar-title { font-weight:900; color:var(--secondary); text-transform:capitalize; }
  .calendar-nav-btn { border:1px solid var(--border-color); background:var(--bg-container); color:var(--text-main); border-radius:8px; width:36px; height:32px; cursor:pointer; font-weight:900; }
  .calendar-week, .calendar-grid { display:grid; grid-template-columns:repeat(7,1fr); gap:4px; }
  .calendar-week span { text-align:center; color:var(--text-muted); font-size:.68rem; font-weight:800; padding:3px 0; }
  .calendar-day { min-height:42px; border:1px solid transparent; background:var(--bg-container); color:var(--text-main); border-radius:8px; cursor:pointer; font-size:.78rem; position:relative; }
  .calendar-day:hover { border-color:var(--primary); }
  .calendar-day.has-culto { border-color:var(--primary); font-weight:900; }
  .calendar-day.has-culto::after { content:''; width:6px; height:6px; background:var(--primary); border-radius:50%; position:absolute; bottom:5px; left:50%; transform:translateX(-50%); }
  .calendar-day.finished { background:var(--success-bg); color:var(--success-text); }
  .calendar-day.today { box-shadow:inset 0 0 0 2px var(--secondary); }
  .calendar-day.empty { visibility:hidden; }

  @media (max-width: 600px) {
    .dashboard-grid { grid-template-columns:repeat(3,1fr); }
    .dashboard-card { padding:11px 5px; }
    .dashboard-card .value { font-size:1.2rem; }
    .dashboard-actions { grid-template-columns:1fr; }
    .culto-status-banner { align-items:flex-start; flex-direction:column; }
    .finalizar-btn { width:100% !important; }
    .calendar-day { min-height:38px; padding:4px 1px; }
  }
'''
rep('  .auth-overlay { position: fixed;', css + '\n  .auth-overlay { position: fixed;')

rep('''  <div id="badge-contador-flutuante" class="floating-counter">
    <span>👥 Presentes Hoje:</span>
    <span id="floating-presenca-count">0</span>
  </div>''', '''  <div id="badge-contador-flutuante" class="floating-counter">
    <span>👥 <span id="floating-membros-count">0</span> membros</span>
    <span>• <span id="floating-visitantes-count">0</span> visitantes</span>
    <strong>• Total <span id="floating-presenca-count">0</span></strong>
  </div>''')

rep('''    <div class="nav-tabs no-print">
      <button class="tab-btn active" onclick="alternarAba('chamada')">📝 Chamada</button>
      <button class="tab-btn" onclick="alternarAba('relatorio')">📄 Relatório Culto</button>
      <button class="tab-btn admin-only" onclick="alternarAba('mensal')">🔒 Relatório Mensal</button>
      <button class="tab-btn admin-only" onclick="alternarAba('membros')">🔒 Cadastrar Membros</button>
    </div>

    <!-- ABA 1: CHAMADA DO CULTO -->
    <div id="tab-chamada" class="tab-content active no-print">''', '''    <div class="nav-tabs no-print">
      <button class="tab-btn active" data-tab="painel" onclick="alternarAba('painel')">🏠 Painel</button>
      <button class="tab-btn" data-tab="chamada" onclick="alternarAba('chamada')">📝 Chamada</button>
      <button class="tab-btn" data-tab="relatorio" onclick="alternarAba('relatorio')">📄 Relatório Culto</button>
      <button class="tab-btn admin-only" data-tab="mensal" onclick="alternarAba('mensal')">🔒 Relatório Mensal</button>
      <button class="tab-btn admin-only" data-tab="membros" onclick="alternarAba('membros')">🔒 Cadastrar Membros</button>
    </div>

    <!-- PAINEL INICIAL -->
    <div id="tab-painel" class="tab-content active no-print">
      <div class="dashboard-hero">
        <small>FREQUÊNCIA ICM PINHOS</small>
        <h3 id="dash-culto-titulo">Culto de hoje</h3>
        <div id="dash-culto-data" style="font-size:.82rem; opacity:.9;"></div>
        <div id="dash-status" class="dashboard-status">⏳ Aguardando dados</div>
      </div>
      <div class="dashboard-grid">
        <div class="dashboard-card"><span id="dash-membros" class="value">0</span><span class="label">Membros</span></div>
        <div class="dashboard-card"><span id="dash-visitantes" class="value">0</span><span class="label">Visitantes</span></div>
        <div class="dashboard-card"><span id="dash-total" class="value">0</span><span class="label">Total</span></div>
      </div>
      <div class="dashboard-actions">
        <button class="btn-main" onclick="alternarAba('chamada')">📝 Abrir chamada</button>
        <button class="btn-main btn-img" onclick="alternarAba('relatorio')">📄 Ver relatório do culto</button>
        <button class="btn-main admin-only" onclick="alternarAba('mensal')">📊 Relatório mensal</button>
        <button class="btn-main admin-only" onclick="alternarAba('membros')">👥 Gerenciar membros</button>
      </div>
      <div id="dash-admin-resumo" class="admin-only" style="margin-top:14px;"></div>
    </div>

    <!-- ABA 1: CHAMADA DO CULTO -->
    <div id="tab-chamada" class="tab-content no-print">''')

rep('''      <div class="grid-2">
        <div>
          <label>Data:</label>
          <input type="date" id="culto-data" onchange="verificarDiaDaSemana(); carregarChamadaCulto();">''', '''      <div id="culto-status-banner" class="culto-status-banner andamento">
        <span id="culto-status-text">⏳ Culto em andamento</span>
        <button id="btn-finalizar-culto" class="btn-main finalizar-btn admin-only" onclick="alternarFinalizacaoCulto()">✅ Finalizar culto</button>
      </div>

      <div id="calendario-admin" class="calendar-card admin-only">
        <div class="calendar-head">
          <button class="calendar-nav-btn" onclick="mudarMesCalendario(-1)" aria-label="Mês anterior">‹</button>
          <div id="calendar-title" class="calendar-title"></div>
          <button class="calendar-nav-btn" onclick="mudarMesCalendario(1)" aria-label="Próximo mês">›</button>
        </div>
        <div class="calendar-week"><span>DOM</span><span>SEG</span><span>TER</span><span>QUA</span><span>QUI</span><span>SEX</span><span>SÁB</span></div>
        <div id="calendar-grid" class="calendar-grid"></div>
      </div>

      <div class="grid-2">
        <div>
          <label>Data:</label>
          <input type="date" id="culto-data" onchange="verificarDiaDaSemana(); sincronizarMesCalendario(); carregarChamadaCulto();">''')

rep('''      <div class="search-box">
        <input type="text" id="busca-membro" placeholder="🔍 Digite o nome para pesquisar e adicionar..." oninput="filtrarMembros(this.value)">
        <div id="search-results-box" class="search-results"></div>
      </div>
      
      <div style="display:flex; justify-content:space-between; margin-bottom:12px; gap: 6px;">''', '''      <div class="search-box">
        <input type="text" id="busca-membro" placeholder="🔍 Digite o nome para pesquisar..." oninput="filtrarMembros(this.value)">
        <div id="search-results-box" class="search-results"></div>
      </div>

      <div class="filter-chips" id="filtros-chamada">
        <button class="filter-chip active" data-filter="TODOS" onclick="setFiltroChamada('TODOS', this)">Todos</button>
        <button class="filter-chip" data-filter="PRESENTES" onclick="setFiltroChamada('PRESENTES', this)">✅ Presentes</button>
        <button class="filter-chip" data-filter="AUSENTES" onclick="setFiltroChamada('AUSENTES', this)">❌ Ausentes</button>
        <button class="filter-chip" data-filter="Varões" onclick="setFiltroChamada('Varões', this)">Varões</button>
        <button class="filter-chip" data-filter="Senhoras" onclick="setFiltroChamada('Senhoras', this)">Senhoras</button>
        <button class="filter-chip" data-filter="Jovens" onclick="setFiltroChamada('Jovens', this)">Jovens</button>
        <button class="filter-chip" data-filter="Adolescentes" onclick="setFiltroChamada('Adolescentes', this)">Adolescentes</button>
        <button class="filter-chip" data-filter="Crianças" onclick="setFiltroChamada('Crianças', this)">Crianças</button>
      </div>
      
      <div style="display:flex; justify-content:space-between; margin-bottom:12px; gap: 6px;">''')
rep('<h2>Lista de Presentes no Culto</h2>', '<h2>Lista de Membros</h2>')

rep("      await window.firebaseSignOut(window.firebaseAuth);\n      alternarAba('chamada');", "      await window.firebaseSignOut(window.firebaseAuth);\n      alternarAba('painel');")

rep('''    window.cultoAtual = {};
    window.processandoFila = false;''', '''    window.cultoAtual = {};
    window.processandoFila = false;
    window.filtroChamadaAtual = 'TODOS';
    window.mesCalendario = null;''')

rep('''    const hoje = new Date();
    inputData.value = hoje.toISOString().split('T')[0];''', '''    const hoje = new Date();
    window.mesCalendario = new Date(hoje.getFullYear(), hoje.getMonth(), 1);
    inputData.value = hoje.toISOString().split('T')[0];''')

old_alt = '''    function alternarAba(nomeAba) {
      if ((nomeAba === 'membros' || nomeAba === 'mensal') && !window.isAdmin) {
        alert('🔒 Área restrita ao administrador.');
        return;
      }

      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

      const floatingBadge = document.getElementById('badge-contador-flutuante');

      if(nomeAba === 'chamada') {
        document.querySelectorAll('.tab-btn')[0].classList.add('active');
        document.getElementById('tab-chamada').classList.add('active');
        if (floatingBadge) floatingBadge.style.display = 'flex';
      } else if(nomeAba === 'relatorio') {
        document.querySelectorAll('.tab-btn')[1].classList.add('active');
        document.getElementById('tab-relatorio').classList.add('active');
        if (floatingBadge) floatingBadge.style.display = 'none';
      } else if(nomeAba === 'mensal') {
        document.querySelectorAll('.tab-btn')[2].classList.add('active');
        document.getElementById('tab-mensal').classList.add('active');
        if (floatingBadge) floatingBadge.style.display = 'none';
        gerarRelatorioMensal();
      } else if(nomeAba === 'membros') {
        document.querySelectorAll('.tab-btn')[3].classList.add('active');
        document.getElementById('tab-membros').classList.add('active');
        if (floatingBadge) floatingBadge.style.display = 'none';
      }
    }'''
new_alt = '''    function alternarAba(nomeAba) {
      if ((nomeAba === 'membros' || nomeAba === 'mensal') && !window.isAdmin) {
        alert('🔒 Área restrita ao administrador.');
        return;
      }
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      const botao = document.querySelector(`.tab-btn[data-tab="${nomeAba}"]`);
      const conteudo = document.getElementById(`tab-${nomeAba}`);
      if (botao) botao.classList.add('active');
      if (conteudo) conteudo.classList.add('active');
      const floatingBadge = document.getElementById('badge-contador-flutuante');
      if (floatingBadge) floatingBadge.style.display = nomeAba === 'chamada' ? 'flex' : 'none';
      if (nomeAba === 'mensal') gerarRelatorioMensal();
      if (nomeAba === 'painel') atualizarDashboard();
      if (nomeAba === 'chamada' && window.isAdmin) renderizarCalendarioAdmin();
    }'''
rep(old_alt, new_alt)

helpers = r'''
    function cultoEstaFinalizado() {
      return !!window.registrosCultos[getChaveCulto()]?.finalizado;
    }

    function bloquearSeFinalizado() {
      if (!cultoEstaFinalizado()) return false;
      alert('🔒 Este culto foi finalizado. O administrador precisa reabrir o culto antes de fazer alterações.');
      return true;
    }

    function aplicarEstadoFinalizacao(finalizado) {
      const banner = document.getElementById('culto-status-banner');
      const texto = document.getElementById('culto-status-text');
      const botao = document.getElementById('btn-finalizar-culto');
      if (banner) banner.className = `culto-status-banner ${finalizado ? 'finalizado' : 'andamento'}`;
      if (texto) texto.textContent = finalizado ? '✅ Culto finalizado — chamada protegida' : '⏳ Culto em andamento';
      if (botao) botao.textContent = finalizado ? '🔓 Reabrir culto' : '✅ Finalizar culto';
      document.querySelectorAll('#tab-chamada input:not(#culto-data), #tab-chamada button:not(#btn-finalizar-culto):not(.calendar-nav-btn):not(.calendar-day), #tab-chamada select:not(#culto-tipo)').forEach(el => {
        el.disabled = !!finalizado;
      });
    }

    function alternarFinalizacaoCulto() {
      if (!window.isAdmin) { alert('🔒 Apenas o administrador pode finalizar ou reabrir um culto.'); return; }
      const chave = getChaveCulto();
      const registro = window.registrosCultos[chave] || {};
      const finalizadoAtual = !!registro.finalizado;
      if (!finalizadoAtual && Object.keys(registro).length === 0) {
        alert('Faça a chamada ou preencha os dados do culto antes de finalizá-lo.');
        return;
      }
      const mensagem = finalizadoAtual
        ? 'Reabrir este culto para permitir alterações novamente?'
        : 'Finalizar este culto? A chamada ficará protegida contra alterações acidentais.';
      if (!confirm(mensagem)) return;
      if (!window.registrosCultos[chave]) window.registrosCultos[chave] = {};
      window.registrosCultos[chave].finalizado = !finalizadoAtual;
      executarGravacao(`cultos_app/registros/${chave}/finalizado`, !finalizadoAtual);
      carregarChamadaCulto();
    }

    function setFiltroChamada(filtro, botao) {
      window.filtroChamadaAtual = filtro;
      document.querySelectorAll('.filter-chip').forEach(b => b.classList.remove('active'));
      if (botao) botao.classList.add('active');
      carregarChamadaCulto();
    }

    function sincronizarMesCalendario() {
      if (!inputData.value) return;
      const [ano, mes] = inputData.value.split('-').map(Number);
      window.mesCalendario = new Date(ano, mes - 1, 1);
      renderizarCalendarioAdmin();
    }

    function mudarMesCalendario(delta) {
      if (!window.isAdmin) return;
      const base = window.mesCalendario || new Date();
      window.mesCalendario = new Date(base.getFullYear(), base.getMonth() + delta, 1);
      renderizarCalendarioAdmin();
    }

    function selecionarDiaCalendario(dataISO) {
      if (!window.isAdmin) return;
      inputData.value = dataISO;
      const chaves = Object.keys(window.registrosCultos).filter(k => k.startsWith(dataISO + '_')).sort();
      if (chaves.length) {
        const tipo = chaves[0].split('_').slice(1).join(' ');
        const select = document.getElementById('culto-tipo');
        if ([...select.options].some(o => o.value === tipo)) select.value = tipo;
      } else {
        verificarDiaDaSemana();
      }
      sincronizarMesCalendario();
      carregarChamadaCulto();
    }

    function renderizarCalendarioAdmin() {
      if (!window.isAdmin) return;
      const grid = document.getElementById('calendar-grid');
      const titulo = document.getElementById('calendar-title');
      if (!grid || !titulo) return;
      const base = window.mesCalendario || new Date();
      const ano = base.getFullYear();
      const mes = base.getMonth();
      titulo.textContent = base.toLocaleDateString('pt-BR', { month:'long', year:'numeric' });
      const primeiroDia = new Date(ano, mes, 1).getDay();
      const totalDias = new Date(ano, mes + 1, 0).getDate();
      const hojeISO = new Date().toISOString().split('T')[0];
      let html = '';
      for (let i = 0; i < primeiroDia; i++) html += '<button class="calendar-day empty" tabindex="-1"></button>';
      for (let dia = 1; dia <= totalDias; dia++) {
        const dataISO = `${ano}-${String(mes + 1).padStart(2,'0')}-${String(dia).padStart(2,'0')}`;
        const chaves = Object.keys(window.registrosCultos).filter(k => k.startsWith(dataISO + '_'));
        const temCulto = chaves.length > 0;
        const finalizado = temCulto && chaves.every(k => !!window.registrosCultos[k]?.finalizado);
        const classes = ['calendar-day', temCulto ? 'has-culto' : '', finalizado ? 'finished' : '', dataISO === hojeISO ? 'today' : ''].filter(Boolean).join(' ');
        html += `<button class="${classes}" onclick="selecionarDiaCalendario('${dataISO}')" title="${temCulto ? chaves.length + ' culto(s) registrado(s)' : 'Abrir esta data'}">${dia}</button>`;
      }
      grid.innerHTML = html;
    }

    function atualizarDashboard() {
      const titulo = document.getElementById('dash-culto-titulo');
      if (!titulo) return;
      const chave = getChaveCulto();
      const registro = window.registrosCultos[chave] || window.cultoAtual?.registro || {};
      const presencas = registro.presencas || {};
      const membros = Object.values(presencas).filter(v => v === 'presente').length;
      const visitantes = (registro.visitantesLista || []).length || (registro.visitantesData?.qtd || 0);
      const total = membros + visitantes;
      titulo.textContent = document.getElementById('culto-tipo').value || 'Culto';
      document.getElementById('dash-culto-data').textContent = inputData.value ? inputData.value.split('-').reverse().join('/') : '';
      document.getElementById('dash-membros').textContent = membros;
      document.getElementById('dash-visitantes').textContent = visitantes;
      document.getElementById('dash-total').textContent = total;
      const status = document.getElementById('dash-status');
      status.textContent = registro.finalizado ? '✅ Culto finalizado' : (Object.keys(registro).length ? '⏳ Culto em andamento' : '📝 Chamada ainda não iniciada');

      const resumo = document.getElementById('dash-admin-resumo');
      if (resumo && window.isAdmin) {
        const mesAtual = inputData.value.slice(0, 7);
        const cultosMes = Object.keys(window.registrosCultos).filter(k => k.startsWith(mesAtual));
        let soma = 0;
        cultosMes.forEach(k => {
          const r = window.registrosCultos[k] || {};
          soma += Object.values(r.presencas || {}).filter(v => v === 'presente').length + ((r.visitantesLista || []).length || (r.visitantesData?.qtd || 0));
        });
        const media = cultosMes.length ? Math.round(soma / cultosMes.length) : 0;
        resumo.innerHTML = `<div class="dashboard-grid"><div class="dashboard-card"><span class="value">${Object.keys(window.membrosCadastrados).length}</span><span class="label">Cadastrados</span></div><div class="dashboard-card"><span class="value">${cultosMes.length}</span><span class="label">Cultos no mês</span></div><div class="dashboard-card"><span class="value">${media}</span><span class="label">Média / culto</span></div></div>`;
      }
    }

'''
rep('    function alternarStatusMembro(membroId) {', helpers + '    function alternarStatusMembro(membroId) {')

for fn in ['alternarStatusMembro(membroId)', 'adicionarPresencaRapida(membroId)', 'marcarTodos(status)', 'adicionarVisitante()', 'removerVisitante(index)', 'salvarCamposEvento()']:
    rep(f'    function {fn} {{\n', f'    function {fn} {{\n      if (bloquearSeFinalizado()) return;\n')

old_block = '''            if (status === 'presente') {
              totalP++;
              htmlPresencaCat += `
                <div class="member-select-item">
                  <div class="member-info"><span><strong>${escapeHTML(m.nome)}</strong></span><span class="member-tag">${escapeHTML(cat)} • ${escapeHTML(grupoStr)}</span></div>
                  <button class="status-badge-btn presente" onclick="alternarStatusMembro(decodeURIComponent('${idSeguroParaHTML(id)}'))">Presente</button>
                </div>
              `;
              tabelaFolhaCat += `<tr class="row-presente"><td style="width:50%;">${escapeHTML(m.nome)}</td><td style="width:25%;">${escapeHTML(cat)}</td><td style="width:25%;">${escapeHTML(grupoStr)}</td></tr>`;
            }'''
new_block = '''            if (status === 'presente') {
              totalP++;
              tabelaFolhaCat += `<tr class="row-presente"><td style="width:50%;">${escapeHTML(m.nome)}</td><td style="width:25%;">${escapeHTML(cat)}</td><td style="width:25%;">${escapeHTML(grupoStr)}</td></tr>`;
            }
            const filtro = window.filtroChamadaAtual || 'TODOS';
            const mostrar = filtro === 'TODOS' || (filtro === 'PRESENTES' && status === 'presente') || (filtro === 'AUSENTES' && status !== 'presente') || filtro === cat;
            if (mostrar) {
              htmlPresencaCat += `
                <div class="member-select-item">
                  <div class="member-info"><span><strong>${escapeHTML(m.nome)}</strong></span><span class="member-tag">${escapeHTML(cat)} • ${escapeHTML(grupoStr)}</span></div>
                  <button class="status-badge-btn ${status === 'presente' ? 'presente' : 'ausente'}" onclick="alternarStatusMembro(decodeURIComponent('${idSeguroParaHTML(id)}'))">${status === 'presente' ? '✅ Presente' : '❌ Ausente'}</button>
                </div>
              `;
            }'''
rep(old_block, new_block)

rep("      const eventoInfo = registroHoje.eventoInfo || {};\n      let visitantesLista", "      const eventoInfo = registroHoje.eventoInfo || {};\n      const finalizado = !!registroHoje.finalizado;\n      let visitantesLista")

rep('''      const elemContador = document.getElementById('floating-presenca-count');
      if (elemContador) elemContador.innerText = `${totalGeralPresentes}`;''', '''      const elemContador = document.getElementById('floating-presenca-count');
      const elemMembros = document.getElementById('floating-membros-count');
      const elemVisitantes = document.getElementById('floating-visitantes-count');
      if (elemContador) elemContador.innerText = `${totalGeralPresentes}`;
      if (elemMembros) elemMembros.innerText = `${totalP}`;
      if (elemVisitantes) elemVisitantes.innerText = `${visitantesLista.length}`;''')

rep('''      divFolha.innerHTML = htmlFolha;
    }

    function renderizarGraficoMensal''', '''      divFolha.innerHTML = htmlFolha;
      aplicarEstadoFinalizacao(finalizado);
      atualizarDashboard();
      if (window.isAdmin) renderizarCalendarioAdmin();
    }

    function renderizarGraficoMensal''')

# Garantir que o painel e calendário atualizem quando não há membros ainda.
rep('''        divFolha.innerHTML = '<p style="text-align:center; color:#888;">Nenhum membro cadastrado.</p>';
        return;''', '''        divFolha.innerHTML = '<p style="text-align:center; color:#888;">Nenhum membro cadastrado.</p>';
        aplicarEstadoFinalizacao(finalizado);
        atualizarDashboard();
        if (window.isAdmin) renderizarCalendarioAdmin();
        return;''')

# Ao logar, iniciar no painel.
rep('''        window.registrosCultos = {};
        carregarDadosLocais();
        iniciarSincronizacaoFirebase();
        window.processarFilaSincronizacao();''', '''        window.registrosCultos = {};
        carregarDadosLocais();
        iniciarSincronizacaoFirebase();
        window.processarFilaSincronizacao();
        alternarAba('painel');''')

p.write_text(s, encoding='utf-8')
print('UI V4 aplicada com sucesso')
