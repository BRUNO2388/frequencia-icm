from pathlib import Path
import json

index_path = Path('index.html')
rules_path = Path('database.rules.json')
s = index_path.read_text(encoding='utf-8')


def replace_once(old, new, label):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: esperado 1 ocorrência, encontrado {count}')
    s = s.replace(old, new, 1)


# 1) Aba administrativa na navegação.
replace_once(
'''      <button class="tab-btn" data-tab="relatorio" onclick="alternarAba('relatorio')">📄 Relatório Culto</button>
      <button class="tab-btn admin-only" data-tab="mensal" onclick="alternarAba('mensal')">🔒 Relatório Mensal</button>''',
'''      <button class="tab-btn" data-tab="relatorio" onclick="alternarAba('relatorio')">📄 Relatório Culto</button>
      <button class="tab-btn admin-only" data-tab="louvor" onclick="alternarAba('louvor')">🎵 Grupo de Louvor</button>
      <button class="tab-btn admin-only" data-tab="mensal" onclick="alternarAba('mensal')">🔒 Relatório Mensal</button>''',
'navegação Grupo de Louvor'
)

# 2) Atalho no painel do administrador.
replace_once(
'''        <button class="btn-main admin-only" onclick="alternarAba('membros')">👥 Gerenciar membros</button>
        <button class="btn-main admin-only btn-convite" onclick="alternarGeradorConvite()">📣 Convite do culto</button>''',
'''        <button class="btn-main admin-only" onclick="alternarAba('membros')">👥 Gerenciar membros</button>
        <button class="btn-main admin-only" onclick="alternarAba('louvor')">🎵 Grupo de Louvor</button>
        <button class="btn-main admin-only btn-convite" onclick="alternarGeradorConvite()">📣 Convite do culto</button>''',
'atalho Grupo de Louvor'
)

# 3) Interface do módulo. Usa diretamente membros_louvor e registros_louvor
#    para preservar cadastro e histórico existentes sem migração destrutiva.
gl_html = r'''
    <!-- MÓDULO ADMINISTRATIVO: GRUPO DE LOUVOR -->
    <div id="tab-louvor" class="tab-content no-print">
      <div class="gl-hero">
        <div>
          <small>MÓDULO ADMINISTRATIVO</small>
          <h2>🎵 Grupo de Louvor</h2>
          <p>Chamada, integrantes e histórico do GL no mesmo aplicativo. O módulo usa o cadastro e os registros já existentes do app Louvor.</p>
        </div>
        <div class="gl-kpis">
          <div class="gl-kpi"><strong id="gl-kpi-integrantes">0</strong><span>Integrantes</span></div>
          <div class="gl-kpi"><strong id="gl-kpi-chamadas">0</strong><span>Chamadas</span></div>
          <div class="gl-kpi"><strong id="gl-kpi-mes">0</strong><span>No mês</span></div>
        </div>
      </div>

      <div id="gl-aviso-acesso" class="gl-access-note" hidden></div>

      <section class="gl-section">
        <div class="gl-section-head">
          <div>
            <h3>📝 Chamada do GL</h3>
            <p>Marque cada integrante como presente, atrasado ou ausente.</p>
          </div>
          <div class="gl-date-box">
            <label for="gl-data">Data</label>
            <input type="date" id="gl-data" onchange="glMontarRascunho()">
          </div>
        </div>

        <div class="gl-bulk-actions">
          <button type="button" class="btn-small-sec" onclick="glMarcarTodos('presente')">✅ Todos presentes</button>
          <button type="button" class="btn-small-sec" onclick="glLimparMarcacoes()">🔄 Limpar marcações</button>
        </div>
        <div id="gl-progresso" class="gl-progress">0/0 marcados</div>
        <div id="gl-lista-chamada" class="gl-call-list">
          <div class="gl-muted">Carregando integrantes...</div>
        </div>
        <button type="button" id="gl-btn-salvar" class="btn-main gl-save-btn" onclick="glSalvarChamada()">💾 Salvar chamada do GL</button>
        <div id="gl-msg" class="gl-message" aria-live="polite"></div>
      </section>

      <section class="gl-section">
        <div class="gl-section-head">
          <div>
            <h3>👥 Integrantes do GL</h3>
            <p>O cadastro abaixo é o mesmo que já existia no aplicativo Louvor.</p>
          </div>
          <button type="button" class="btn-small-sec" onclick="glBaixarBackup()">⬇️ Backup do GL</button>
        </div>
        <div class="gl-add-member">
          <input type="text" id="gl-novo-nome" maxlength="120" placeholder="Nome do integrante">
          <button type="button" class="btn-main" onclick="glCadastrarIntegrante()">➕ Cadastrar</button>
        </div>
        <input type="search" id="gl-busca-integrante" placeholder="🔍 Buscar integrante..." oninput="glRenderIntegrantes()">
        <div class="gl-list-head"><span>Integrantes cadastrados</span><strong id="gl-total-integrantes">0</strong></div>
        <div id="gl-lista-integrantes" class="gl-manage-list">
          <div class="gl-muted">Carregando cadastro existente...</div>
        </div>
      </section>

      <section class="gl-section">
        <div class="gl-section-head">
          <div>
            <h3>📊 Histórico de frequência</h3>
            <p>Consulta das chamadas já salvas, inclusive as feitas no aplicativo Louvor anterior.</p>
          </div>
          <div class="gl-date-box">
            <label for="gl-mes">Mês</label>
            <input type="month" id="gl-mes" onchange="glRenderHistorico()">
          </div>
        </div>
        <div id="gl-resumo-historico" class="gl-history-summary"></div>
        <div class="table-responsive">
          <table class="report-table gl-history-table">
            <thead>
              <tr><th>Data</th><th>Presentes</th><th>Atrasados</th><th>Ausentes</th><th>Justificados</th><th></th></tr>
            </thead>
            <tbody id="gl-historico-body">
              <tr><td colspan="6" style="text-align:center;">Carregando histórico...</td></tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>

'''
replace_once(
'    <!-- ABA 3: RELATÓRIO MENSAL -->',
gl_html + '    <!-- ABA 3: RELATÓRIO MENSAL -->',
'interface Grupo de Louvor'
)

# 4) Estilos do módulo.
gl_css = r'''
  /* ===== MÓDULO GRUPO DE LOUVOR ===== */
  .gl-hero { display:grid; grid-template-columns:1.4fr 1fr; gap:14px; align-items:center; padding:18px; border-radius:14px; margin-bottom:14px; background:linear-gradient(135deg, var(--secondary) 0%, var(--primary) 100%); color:#fff; box-shadow:0 5px 18px var(--shadow); }
  .gl-hero small { font-size:.68rem; letter-spacing:.8px; font-weight:900; opacity:.82; }
  .gl-hero h2 { margin:4px 0 5px; color:#fff; border:0; padding:0; font-size:1.25rem; }
  .gl-hero p { margin:0; font-size:.78rem; line-height:1.45; opacity:.92; }
  .gl-kpis { display:grid; grid-template-columns:repeat(3,1fr); gap:7px; }
  .gl-kpi { background:rgba(255,255,255,.13); border:1px solid rgba(255,255,255,.22); border-radius:11px; padding:10px 6px; text-align:center; }
  .gl-kpi strong { display:block; font-size:1.25rem; line-height:1; }
  .gl-kpi span { display:block; margin-top:4px; font-size:.65rem; text-transform:uppercase; font-weight:800; opacity:.9; }
  .gl-section { border:1px solid var(--border-color); background:var(--card-bg); border-radius:14px; padding:14px; margin:12px 0; box-shadow:0 3px 12px var(--shadow); }
  .gl-section-head { display:flex; align-items:flex-end; justify-content:space-between; gap:12px; margin-bottom:12px; }
  .gl-section-head h3 { margin:0 0 3px; color:var(--secondary); font-size:1rem; }
  .gl-section-head p { margin:0; color:var(--text-secondary); font-size:.75rem; line-height:1.35; }
  .gl-date-box { width:150px; flex:0 0 150px; }
  .gl-date-box label { margin-top:0; }
  .gl-bulk-actions { display:flex; flex-wrap:wrap; gap:7px; margin-bottom:8px; }
  .gl-progress { font-size:.75rem; font-weight:900; color:var(--primary); margin:7px 0 10px; }
  .gl-call-list { display:grid; gap:7px; }
  .gl-call-item { display:flex; align-items:center; justify-content:space-between; gap:10px; border:1px solid var(--border-light); background:var(--bg-container); border-radius:10px; padding:9px 10px; }
  .gl-call-item.unmarked { border-style:dashed; }
  .gl-call-info { min-width:0; }
  .gl-call-name { display:block; font-size:.84rem; font-weight:900; color:var(--text-main); overflow-wrap:anywhere; }
  .gl-call-detail { display:block; margin-top:2px; font-size:.68rem; color:var(--text-secondary); }
  .gl-call-actions { display:flex; align-items:center; gap:4px; flex:0 0 auto; }
  .gl-status-btn { width:34px; height:32px; border-radius:8px; border:1px solid var(--border-color); background:var(--card-bg); color:var(--text-main); font-weight:900; cursor:pointer; }
  .gl-status-btn.present.active { background:var(--success-bg); color:var(--success-text); border-color:var(--success-border); }
  .gl-status-btn.late.active { background:var(--warning-bg); color:var(--warning-text); border-color:var(--warning-border); }
  .gl-status-btn.absent.active { background:var(--danger-bg); color:var(--danger-text); border-color:var(--danger-border); }
  .gl-status-btn.note { width:38px; }
  .gl-save-btn { margin-top:12px; }
  .gl-message { min-height:20px; margin-top:7px; text-align:center; font-size:.76rem; font-weight:800; color:var(--primary); }
  .gl-add-member { display:grid; grid-template-columns:1fr 150px; gap:8px; margin-bottom:8px; }
  .gl-add-member .btn-main { margin-top:0; }
  .gl-list-head { display:flex; justify-content:space-between; align-items:center; margin:10px 0 6px; color:var(--text-secondary); font-size:.72rem; font-weight:800; }
  .gl-list-head strong { min-width:28px; text-align:center; padding:3px 7px; border-radius:12px; background:var(--primary); color:#fff; }
  .gl-manage-list { display:grid; gap:6px; }
  .gl-manage-item { display:flex; justify-content:space-between; align-items:center; gap:10px; padding:9px 10px; border:1px solid var(--border-light); border-radius:9px; background:var(--bg-container); }
  .gl-manage-item strong { font-size:.82rem; overflow-wrap:anywhere; }
  .gl-manage-actions { display:flex; gap:5px; flex:0 0 auto; }
  .gl-history-summary { display:grid; grid-template-columns:repeat(3,1fr); gap:7px; margin:8px 0 4px; }
  .gl-history-card { padding:9px 7px; border:1px solid var(--border-color); background:var(--bg-container); border-radius:10px; text-align:center; }
  .gl-history-card strong { display:block; font-size:1.05rem; color:var(--primary); }
  .gl-history-card span { font-size:.65rem; color:var(--text-secondary); text-transform:uppercase; font-weight:800; }
  .gl-history-table td, .gl-history-table th { text-align:center; }
  .gl-muted { padding:12px; text-align:center; color:var(--text-secondary); font-size:.78rem; }
  .gl-access-note { margin-bottom:12px; padding:10px 12px; border-radius:10px; background:var(--danger-bg); border:1px solid var(--danger-border); color:var(--danger-text); font-size:.78rem; line-height:1.4; }

  @media (max-width: 600px) {
    .gl-hero { grid-template-columns:1fr; padding:14px; }
    .gl-section-head { align-items:stretch; flex-direction:column; }
    .gl-date-box { width:100%; flex-basis:auto; }
    .gl-add-member { grid-template-columns:1fr; }
    .gl-call-item { align-items:flex-start; flex-direction:column; }
    .gl-call-actions { width:100%; justify-content:flex-end; }
    .gl-history-summary { grid-template-columns:repeat(3,1fr); }
  }

'''
replace_once('  @media print {', gl_css + '  @media print {', 'CSS Grupo de Louvor')

# 5) Protege a aba também por função, não apenas visualmente.
replace_once(
"      if ((nomeAba === 'membros' || nomeAba === 'mensal') && !window.isAdmin) {",
"      if ((nomeAba === 'membros' || nomeAba === 'mensal' || nomeAba === 'louvor') && !window.isAdmin) {",
'proteção da aba Grupo de Louvor'
)
replace_once(
"      if (nomeAba === 'chamada' && window.isAdmin) renderizarCalendarioAdmin();",
"      if (nomeAba === 'chamada' && window.isAdmin) renderizarCalendarioAdmin();\n      if (nomeAba === 'louvor' && window.isAdmin) glRenderTudo();",
'renderização ao abrir Grupo de Louvor'
)

# 6) Liga/desliga listeners do GL junto com a autenticação administrativa.
replace_once(
'''        iniciarSincronizacaoFirebase();
        window.processarFilaSincronizacao();
        alternarAba('painel');''',
'''        iniciarSincronizacaoFirebase();
        if (window.isAdmin) window.iniciarGrupoLouvorAdmin?.();
        else window.pararGrupoLouvorAdmin?.();
        window.processarFilaSincronizacao();
        alternarAba('painel');''',
'inicialização do Grupo de Louvor'
)
replace_once(
'''        document.querySelectorAll('.admin-only').forEach(el => el.classList.remove('admin-visible'));
        pararSincronizacaoFirebase();''',
'''        document.querySelectorAll('.admin-only').forEach(el => el.classList.remove('admin-visible'));
        window.pararGrupoLouvorAdmin?.();
        pararSincronizacaoFirebase();''',
'parada do Grupo de Louvor no logout'
)

# 7) Lógica do módulo, mantendo exatamente as raízes legadas do app Louvor.
gl_js = r'''
    /* ===== GRUPO DE LOUVOR — integração administrativa ===== */
    window.glIntegrantes = {};
    window.glRegistros = {};
    let glRascunho = {};
    let glUnsubIntegrantes = null;
    let glUnsubRegistros = null;

    function glHojeISO() {
      return new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo' }).format(new Date());
    }

    function glChaveNome(nome) {
      return String(nome || '').replace(/[.#$[\]\\/]/g, '_');
    }

    function glFormatarData(dataISO) {
      if (!dataISO) return '';
      const partes = dataISO.split('-');
      return partes.length === 3 ? `${partes[2]}/${partes[1]}/${partes[0]}` : dataISO;
    }

    function glGarantirCampos() {
      const hoje = glHojeISO();
      const campoData = document.getElementById('gl-data');
      const campoMes = document.getElementById('gl-mes');
      if (campoData && !campoData.value) campoData.value = hoje;
      if (campoMes && !campoMes.value) campoMes.value = hoje.slice(0, 7);
    }

    function glMostrarMensagem(texto, erro = false) {
      const el = document.getElementById('gl-msg');
      if (!el) return;
      el.textContent = texto || '';
      el.style.color = erro ? 'var(--danger-text)' : 'var(--primary)';
      clearTimeout(window.__glMsgTimer);
      if (texto) window.__glMsgTimer = setTimeout(() => { if (el.textContent === texto) el.textContent = ''; }, 3500);
    }

    function glMostrarErroAcesso(erro) {
      console.warn('Grupo de Louvor: falha de acesso ao Firebase.', erro);
      const aviso = document.getElementById('gl-aviso-acesso');
      if (aviso) {
        aviso.hidden = false;
        aviso.textContent = 'Não foi possível acessar os dados do Grupo de Louvor. O cadastro antigo não foi alterado. Confira a conexão e as regras do Firebase para membros_louvor e registros_louvor.';
      }
    }

    function glLimparErroAcesso() {
      const aviso = document.getElementById('gl-aviso-acesso');
      if (aviso) {
        aviso.hidden = true;
        aviso.textContent = '';
      }
    }

    function glListaIntegrantes() {
      return Object.entries(window.glIntegrantes || {})
        .filter(([, item]) => item && item.nome)
        .sort((a, b) => String(a[1].nome).localeCompare(String(b[1].nome), 'pt-BR'));
    }

    function iniciarGrupoLouvorAdmin() {
      if (!window.isAdmin || !window.db || !window.dbRef || !window.dbOnValue) return;
      pararGrupoLouvorAdmin();
      glGarantirCampos();
      glLimparErroAcesso();

      glUnsubIntegrantes = window.dbOnValue(
        window.dbRef(window.db, 'membros_louvor'),
        snapshot => {
          window.glIntegrantes = snapshot.val() || {};
          glLimparErroAcesso();
          glRenderTudo();
        },
        glMostrarErroAcesso
      );

      glUnsubRegistros = window.dbOnValue(
        window.dbRef(window.db, 'registros_louvor'),
        snapshot => {
          window.glRegistros = snapshot.val() || {};
          glLimparErroAcesso();
          glRenderTudo();
        },
        glMostrarErroAcesso
      );
    }

    function pararGrupoLouvorAdmin() {
      if (glUnsubIntegrantes) glUnsubIntegrantes();
      if (glUnsubRegistros) glUnsubRegistros();
      glUnsubIntegrantes = null;
      glUnsubRegistros = null;
      glRascunho = {};
      window.glIntegrantes = {};
      window.glRegistros = {};
    }

    window.iniciarGrupoLouvorAdmin = iniciarGrupoLouvorAdmin;
    window.pararGrupoLouvorAdmin = pararGrupoLouvorAdmin;

    function glAtualizarKpis() {
      const totalIntegrantes = glListaIntegrantes().length;
      const datas = Object.keys(window.glRegistros || {});
      const mes = document.getElementById('gl-mes')?.value || glHojeISO().slice(0, 7);
      const totalMes = datas.filter(data => data.startsWith(mes)).length;
      const a = document.getElementById('gl-kpi-integrantes');
      const b = document.getElementById('gl-kpi-chamadas');
      const c = document.getElementById('gl-kpi-mes');
      if (a) a.textContent = totalIntegrantes;
      if (b) b.textContent = datas.length;
      if (c) c.textContent = totalMes;
    }

    function glRenderTudo() {
      if (!window.isAdmin) return;
      glGarantirCampos();
      glAtualizarKpis();
      glMontarRascunho();
      glRenderIntegrantes();
      glRenderHistorico();
    }

    function glMontarRascunho() {
      if (!window.isAdmin) return;
      glGarantirCampos();
      const data = document.getElementById('gl-data')?.value || glHojeISO();
      const salvos = (window.glRegistros || {})[data] || {};
      const novo = {};

      glListaIntegrantes().forEach(([id, integrante]) => {
        const registro = salvos[id] || salvos[glChaveNome(integrante.nome)] || {};
        novo[id] = {
          id,
          nome: integrante.nome,
          status: registro.status || '',
          justificado: registro.justificado || 'nao',
          motivo: registro.motivo || '',
          cadastrado: true
        };
      });

      // Se uma chamada antiga contém alguém que já saiu do cadastro atual, mantém
      // a pessoa visível nessa data e nunca elimina o registro histórico.
      Object.entries(salvos).forEach(([id, registro]) => {
        if (novo[id] || !registro || !registro.nome) return;
        novo[id] = {
          id,
          nome: registro.nome,
          status: registro.status || '',
          justificado: registro.justificado || 'nao',
          motivo: registro.motivo || '',
          cadastrado: false
        };
      });

      glRascunho = novo;
      glRenderChamada();
    }

    function glRenderChamada() {
      const box = document.getElementById('gl-lista-chamada');
      const progress = document.getElementById('gl-progresso');
      if (!box || !progress) return;
      const itens = Object.values(glRascunho).sort((a, b) => String(a.nome).localeCompare(String(b.nome), 'pt-BR'));
      if (!itens.length) {
        box.innerHTML = '<div class="gl-muted">Nenhum integrante cadastrado no Grupo de Louvor.</div>';
        progress.textContent = '0/0 marcados';
        return;
      }

      box.innerHTML = itens.map(item => {
        const id = idSeguroParaHTML(item.id);
        const precisaNota = item.status === 'atrasado' || item.status === 'ausente';
        let detalhe = item.cadastrado ? '' : '<span class="gl-call-detail">Registro histórico • fora do cadastro atual</span>';
        if (precisaNota && (item.justificado === 'sim' || item.motivo)) {
          detalhe += `<span class="gl-call-detail">${item.justificado === 'sim' ? '✓ Justificado' : 'Não justificado'}${item.motivo ? ' • ' + escapeHTML(item.motivo) : ''}</span>`;
        }
        return `
          <div class="gl-call-item ${item.status ? '' : 'unmarked'}">
            <div class="gl-call-info">
              <span class="gl-call-name">${escapeHTML(item.nome)}</span>
              ${detalhe}
            </div>
            <div class="gl-call-actions">
              <button type="button" class="gl-status-btn present ${item.status === 'presente' ? 'active' : ''}" onclick="glMarcar(decodeURIComponent('${id}'),'presente')" title="Presente">✓</button>
              <button type="button" class="gl-status-btn late ${item.status === 'atrasado' ? 'active' : ''}" onclick="glMarcar(decodeURIComponent('${id}'),'atrasado')" title="Atrasado">A</button>
              <button type="button" class="gl-status-btn absent ${item.status === 'ausente' ? 'active' : ''}" onclick="glMarcar(decodeURIComponent('${id}'),'ausente')" title="Ausente">F</button>
              ${precisaNota ? `<button type="button" class="gl-status-btn note" onclick="glEditarJustificativa(decodeURIComponent('${id}'))" title="Justificativa">📝</button>` : ''}
            </div>
          </div>`;
      }).join('');

      const marcados = itens.filter(item => item.status).length;
      progress.textContent = `${marcados}/${itens.length} marcados`;
    }

    function glMarcar(id, status) {
      if (!window.isAdmin) return;
      const item = glRascunho[id];
      if (!item) return;
      item.status = item.status === status ? '' : status;
      if (!item.status || item.status === 'presente') {
        item.justificado = 'nao';
        item.motivo = '';
      }
      glRenderChamada();
    }

    function glEditarJustificativa(id) {
      if (!window.isAdmin) return;
      const item = glRascunho[id];
      if (!item || (item.status !== 'atrasado' && item.status !== 'ausente')) return;
      item.justificado = confirm(`${item.nome}: ${item.status === 'atrasado' ? 'o atraso' : 'a falta'} foi justificado?`) ? 'sim' : 'nao';
      const motivo = prompt('Motivo (opcional):', item.motivo || '');
      if (motivo !== null) item.motivo = motivo.trim();
      glRenderChamada();
    }

    function glMarcarTodos(status) {
      if (!window.isAdmin) return;
      Object.values(glRascunho).forEach(item => {
        item.status = status;
        item.justificado = 'nao';
        item.motivo = '';
      });
      glRenderChamada();
    }

    function glLimparMarcacoes() {
      if (!window.isAdmin) return;
      Object.values(glRascunho).forEach(item => {
        item.status = '';
        item.justificado = 'nao';
        item.motivo = '';
      });
      glRenderChamada();
    }

    async function glSalvarChamada() {
      if (!window.isAdmin) return alert('Acesso restrito ao administrador.');
      const data = document.getElementById('gl-data')?.value;
      if (!data) return alert('Selecione a data da chamada.');
      const itens = Object.values(glRascunho);
      if (!itens.length) return alert('Não há integrantes para registrar.');
      const faltando = itens.filter(item => !item.status);
      if (faltando.length) return alert(`Ainda faltam ${faltando.length} integrante(s) para marcar.`);

      const payload = {};
      itens.forEach(item => {
        payload[item.id || glChaveNome(item.nome)] = {
          nome: item.nome,
          status: item.status,
          justificado: item.justificado || 'nao',
          motivo: item.motivo || ''
        };
      });

      try {
        await window.dbSet(window.dbRef(window.db, `registros_louvor/${data}`), payload);
        window.glRegistros[data] = payload;
        glMostrarMensagem(`✅ Chamada de ${glFormatarData(data)} salva com sucesso.`);
        glAtualizarKpis();
        glRenderHistorico();
      } catch (erro) {
        console.error(erro);
        glMostrarMensagem('Não foi possível salvar a chamada. Verifique a conexão e as permissões do Firebase.', true);
      }
    }

    async function glCadastrarIntegrante() {
      if (!window.isAdmin) return;
      const input = document.getElementById('gl-novo-nome');
      const nome = input?.value.trim() || '';
      if (!nome) return alert('Digite o nome do integrante.');
      const id = glChaveNome(nome);
      if (window.glIntegrantes?.[id]) return alert('Já existe um integrante com esse nome.');
      try {
        await window.dbSet(window.dbRef(window.db, `membros_louvor/${id}`), { nome });
        window.glIntegrantes[id] = { nome };
        if (input) input.value = '';
        glMostrarMensagem('✅ Integrante cadastrado.');
        glRenderTudo();
      } catch (erro) {
        console.error(erro);
        glMostrarMensagem('Não foi possível cadastrar o integrante.', true);
      }
    }

    async function glEditarIntegrante(id) {
      if (!window.isAdmin) return;
      const atual = window.glIntegrantes?.[id];
      if (!atual) return;
      const novoNome = (prompt('Novo nome do integrante:', atual.nome || '') || '').trim();
      if (!novoNome || novoNome === atual.nome) return;
      const novoId = glChaveNome(novoNome);
      if (window.glIntegrantes?.[novoId] && novoId !== id) return alert('Já existe um integrante com esse nome.');
      try {
        await window.dbSet(window.dbRef(window.db, `membros_louvor/${novoId}`), { nome: novoNome });
        if (novoId !== id) await window.dbRemove(window.dbRef(window.db, `membros_louvor/${id}`));
        delete window.glIntegrantes[id];
        window.glIntegrantes[novoId] = { nome: novoNome };
        glMostrarMensagem('✅ Nome atualizado. O histórico antigo foi preservado.');
        glRenderTudo();
      } catch (erro) {
        console.error(erro);
        glMostrarMensagem('Não foi possível editar o integrante.', true);
      }
    }

    async function glRemoverIntegrante(id) {
      if (!window.isAdmin) return;
      const atual = window.glIntegrantes?.[id];
      if (!atual) return;
      if (!confirm(`Excluir ${atual.nome} do cadastro do GL? As chamadas antigas serão mantidas.`)) return;
      try {
        await window.dbRemove(window.dbRef(window.db, `membros_louvor/${id}`));
        delete window.glIntegrantes[id];
        glMostrarMensagem('Integrante removido do cadastro. O histórico foi mantido.');
        glRenderTudo();
      } catch (erro) {
        console.error(erro);
        glMostrarMensagem('Não foi possível remover o integrante.', true);
      }
    }

    function glRenderIntegrantes() {
      const box = document.getElementById('gl-lista-integrantes');
      const total = document.getElementById('gl-total-integrantes');
      if (!box || !total) return;
      const termo = (document.getElementById('gl-busca-integrante')?.value || '').trim().toLowerCase();
      const todos = glListaIntegrantes();
      const filtrados = termo ? todos.filter(([, item]) => String(item.nome).toLowerCase().includes(termo)) : todos;
      total.textContent = termo ? `${filtrados.length}/${todos.length}` : todos.length;
      if (!filtrados.length) {
        box.innerHTML = `<div class="gl-muted">${todos.length ? 'Nenhum integrante encontrado.' : 'Nenhum integrante cadastrado.'}</div>`;
        return;
      }
      box.innerHTML = filtrados.map(([id, item]) => {
        const seguro = idSeguroParaHTML(id);
        return `<div class="gl-manage-item"><strong>${escapeHTML(item.nome)}</strong><div class="gl-manage-actions"><button type="button" class="btn-small-sec" onclick="glEditarIntegrante(decodeURIComponent('${seguro}'))">✏️ Editar</button><button type="button" class="btn-small-sec" onclick="glRemoverIntegrante(decodeURIComponent('${seguro}'))">✕ Excluir</button></div></div>`;
      }).join('');
    }

    function glRenderHistorico() {
      const body = document.getElementById('gl-historico-body');
      const resumo = document.getElementById('gl-resumo-historico');
      if (!body || !resumo) return;
      glGarantirCampos();
      const mes = document.getElementById('gl-mes')?.value || glHojeISO().slice(0, 7);
      const datas = Object.keys(window.glRegistros || {}).filter(data => data.startsWith(mes)).sort().reverse();
      let somaPresentes = 0;
      let somaAtrasados = 0;
      let somaAusentes = 0;

      const linhas = datas.map(data => {
        const registros = Object.values(window.glRegistros[data] || {});
        const presentes = registros.filter(item => item?.status === 'presente').length;
        const atrasados = registros.filter(item => item?.status === 'atrasado').length;
        const ausentes = registros.filter(item => item?.status === 'ausente').length;
        const justificados = registros.filter(item => (item?.status === 'atrasado' || item?.status === 'ausente') && item?.justificado === 'sim').length;
        somaPresentes += presentes;
        somaAtrasados += atrasados;
        somaAusentes += ausentes;
        return `<tr><td>${glFormatarData(data)}</td><td>${presentes}</td><td>${atrasados}</td><td>${ausentes}</td><td>${justificados}</td><td><button type="button" class="btn-small-sec" onclick="glAbrirDataHistorico('${data}')">Abrir</button></td></tr>`;
      });

      body.innerHTML = linhas.length ? linhas.join('') : '<tr><td colspan="6" style="text-align:center; color:#888;">Nenhuma chamada salva neste mês.</td></tr>';
      resumo.innerHTML = `
        <div class="gl-history-card"><strong>${datas.length}</strong><span>Chamadas</span></div>
        <div class="gl-history-card"><strong>${somaPresentes + somaAtrasados}</strong><span>Participações</span></div>
        <div class="gl-history-card"><strong>${somaAusentes}</strong><span>Ausências</span></div>`;
      glAtualizarKpis();
    }

    function glAbrirDataHistorico(data) {
      if (!window.isAdmin) return;
      const input = document.getElementById('gl-data');
      if (input) input.value = data;
      glMontarRascunho();
      document.getElementById('gl-data')?.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    function glBaixarBackup() {
      if (!window.isAdmin) return;
      const backup = {
        app: 'Louvor_Pinhos_integrado',
        versao: 3,
        geradoEm: new Date().toISOString(),
        membros_louvor: window.glIntegrantes || {},
        registros_louvor: window.glRegistros || {}
      };
      const blob = new Blob([JSON.stringify(backup, null, 2)], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = `backup-grupo-louvor-${glHojeISO()}.json`;
      link.click();
      URL.revokeObjectURL(url);
      glMostrarMensagem('✅ Backup do Grupo de Louvor gerado.');
    }

'''
replace_once(
'    function exportarExcelCSV() {',
gl_js + '    function exportarExcelCSV() {',
'lógica Grupo de Louvor'
)

index_path.write_text(s, encoding='utf-8')

# 8) Regras de referência: GL somente para o administrador e com validação.
rules = json.loads(rules_path.read_text(encoding='utf-8'))
admin_rule = "auth != null && auth.token.email == 'icmpinhos@gmail.com'"
rules['rules']['registros_louvor'] = {
    '.read': admin_rule,
    '.write': admin_rule,
    '$data': {
        '$pessoa': {
            '.validate': "!newData.exists() || (newData.hasChildren(['nome','status']) && newData.child('nome').isString() && newData.child('nome').val().length > 0 && newData.child('nome').val().length <= 120 && (newData.child('status').val() == 'presente' || newData.child('status').val() == 'atrasado' || newData.child('status').val() == 'ausente'))"
        }
    }
}
rules['rules']['membros_louvor'] = {
    '.read': admin_rule,
    '.write': admin_rule,
    '$membro': {
        '.validate': "!newData.exists() || (newData.hasChild('nome') && newData.child('nome').isString() && newData.child('nome').val().length > 0 && newData.child('nome').val().length <= 120)"
    }
}
rules_path.write_text(json.dumps(rules, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
