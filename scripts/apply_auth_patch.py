from pathlib import Path
import re

path = Path('index.html')
s = path.read_text(encoding='utf-8')


def replace_once(old, new, label):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f'{label}: esperado 1 ocorrência, encontrado {count}')
    s = s.replace(old, new, 1)

# 1) Estilos da tela de autenticação e visibilidade das áreas administrativas.
css_anchor = """    .report-table { min-width: 100%; }
  }
</style>"""
css_new = """    .report-table { min-width: 100%; }
  }

  .auth-overlay { position: fixed; inset: 0; z-index: 20000; background: var(--bg-body); display:flex; align-items:center; justify-content:center; padding:20px; }
  .auth-card { width:100%; max-width:380px; background:var(--bg-container); border:1px solid var(--border-color); border-radius:14px; padding:24px; box-shadow:0 8px 30px var(--shadow); }
  .auth-card h2 { margin-top:0; }
  .auth-error { color:var(--danger-text); font-size:.85rem; margin-top:10px; min-height:20px; text-align:center; }
  .user-bar { width:100%; max-width:680px; display:none; justify-content:space-between; align-items:center; gap:10px; margin-bottom:10px; font-size:.82rem; color:var(--text-secondary); }
  .admin-only { display:none; }
  .admin-only.admin-visible { display:block; }
</style>"""
replace_once(css_anchor, css_new, 'CSS auth')

# 2) Tela de login e barra do usuário.
body_anchor = """<body>

  <!-- STATUS DA CONEXÃO DE INTERNET -->"""
body_new = """<body>
  <div id="auth-overlay" class="auth-overlay">
    <div class="auth-card">
      <h2>🔐 Acesso ao Frequência ICM</h2>
      <label>Usuário</label>
      <input id="login-usuario" type="text" autocomplete="username" placeholder="Usuário ou e-mail">
      <label>Senha</label>
      <input id="login-senha" type="password" autocomplete="current-password" placeholder="Senha" onkeydown="if(event.key==='Enter') entrarNoApp()">
      <button class="btn-main" onclick="entrarNoApp()">Entrar</button>
      <div id="login-erro" class="auth-error"></div>
    </div>
  </div>
  <div id="user-bar" class="user-bar no-print"><span id="user-info"></span><button class="btn-small-sec" onclick="sairDoApp()">Sair</button></div>


  <!-- STATUS DA CONEXÃO DE INTERNET -->"""
replace_once(body_anchor, body_new, 'HTML login')

# 3) Abas restritas.
replace_once(
    '<button class="tab-btn" onclick="alternarAba(\'mensal\')">🔒 Relatório Mensal</button>',
    '<button class="tab-btn admin-only" onclick="alternarAba(\'mensal\')">🔒 Relatório Mensal</button>',
    'aba mensal'
)
replace_once(
    '<button class="tab-btn" onclick="alternarAba(\'membros\')">🔒 Cadastrar Membros</button>',
    '<button class="tab-btn admin-only" onclick="alternarAba(\'membros\')">🔒 Cadastrar Membros</button>',
    'aba membros'
)

# 4) A senha administrativa deixa de ser gerenciada no Realtime Database.
replace_once(
    '<button class="btn-main btn-pdf" style="margin-top: 10px;" onclick="alterarSenhaAdministrador()">🔑 Alterar Senha do Administrador</button>',
    '<button class="btn-main btn-pdf" style="margin-top: 10px;" onclick="alterarSenhaAdministrador()">🔐 Senha gerenciada no Firebase</button>',
    'botão senha admin'
)

# 5) Firebase Authentication.
replace_once(
    '    import { getDatabase, ref, set, remove, onValue } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js";\n',
    '    import { getDatabase, ref, set, remove, onValue } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js";\n    import { getAuth, signInWithEmailAndPassword, signOut, onAuthStateChanged } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";\n',
    'import auth'
)
replace_once(
    '    const app = initializeApp(firebaseConfig);\n    const db = getDatabase(app);\n',
    '    const app = initializeApp(firebaseConfig);\n    const db = getDatabase(app);\n    const auth = getAuth(app);\n',
    'init auth'
)
replace_once(
    '    window.dbRemove = remove;\n',
    '    window.dbRemove = remove;\n    window.firebaseAuth = auth;\n    window.firebaseSignIn = signInWithEmailAndPassword;\n    window.firebaseSignOut = signOut;\n',
    'expor auth'
)

# Cache offline só é carregado depois que o Firebase confirma uma sessão autenticada.
replace_once(
    '    request.onsuccess = (e) => {\n      localDB = e.target.result;\n      carregarDadosLocais();\n    };',
    '    request.onsuccess = (e) => {\n      localDB = e.target.result;\n      if (window.usuarioAtual) carregarDadosLocais();\n    };',
    'indexeddb auth gate'
)
replace_once(
    '          atualizarSelectMembrosFiltro();\n          gerarRelatorioMensal();',
    '          atualizarSelectMembrosFiltro();\n          if (window.isAdmin) gerarRelatorioMensal();',
    'relatório mensal cache'
)
replace_once(
    '      if (!localDB || !navigator.onLine) return;',
    '      if (!localDB || !navigator.onLine || !window.usuarioAtual) return;',
    'fila auth gate'
)

# Listener do Realtime Database é iniciado apenas após login.
pattern = re.compile(
    r"    onValue\(ref\(db, 'cultos_app'\), \(snapshot\) => \{\n(?P<body>.*?)\n    \}\);\n\n    function atualizarStatusConexaoUI\(\) \{",
    re.S,
)
m = pattern.search(s)
if not m:
    raise SystemExit('listener Firebase original não encontrado')
listener_body = m.group('body')
listener_body = listener_body.replace('      gerarRelatorioMensal();', '      if (window.isAdmin) gerarRelatorioMensal();')
auth_listener = """    let unsubscribeCultos = null;
    function iniciarSincronizacaoFirebase() {
      if (unsubscribeCultos) return;
      unsubscribeCultos = onValue(ref(db, 'cultos_app'), (snapshot) => {
""" + listener_body + """
      });
    }

    onAuthStateChanged(auth, (user) => {
      window.usuarioAtual = user || null;
      window.isAdmin = !!user && (user.email || '').toLowerCase() === 'icmpinhos@gmail.com';
      const overlay = document.getElementById('auth-overlay');
      const bar = document.getElementById('user-bar');
      if (user) {
        overlay.style.display = 'none';
        bar.style.display = 'flex';
        document.getElementById('user-info').textContent = window.isAdmin ? '👑 Administrador' : '👤 Membro';
        document.querySelectorAll('.admin-only').forEach(el => el.classList.toggle('admin-visible', window.isAdmin));
        carregarDadosLocais();
        iniciarSincronizacaoFirebase();
      } else {
        overlay.style.display = 'flex';
        bar.style.display = 'none';
        document.querySelectorAll('.admin-only').forEach(el => el.classList.remove('admin-visible'));
        if (unsubscribeCultos) { unsubscribeCultos(); unsubscribeCultos = null; }
      }
    });

    function atualizarStatusConexaoUI() {"""
s = s[:m.start()] + auth_listener + s[m.end():]

# 6) Estado do usuário e funções de login/logout.
classic_anchor = """    window.hashSenhaAdmin = null;
    let chartInstancia = null;

    /**
     * Função auxiliar para gerar Hash simples do texto digitado
"""
classic_new = """    window.hashSenhaAdmin = null;
    let chartInstancia = null;

    window.isAdmin = false;
    window.usuarioAtual = null;

    async function entrarNoApp() {
      const usuario = document.getElementById('login-usuario').value.trim();
      const senha = document.getElementById('login-senha').value;
      const erro = document.getElementById('login-erro');
      erro.textContent = '';
      if (!usuario || !senha) { erro.textContent = 'Informe usuário e senha.'; return; }
      const usuarioNormalizado = usuario.toLowerCase();
      const email = usuarioNormalizado === 'admin'
        ? 'icmpinhos@gmail.com'
        : (usuario.includes('@') ? usuario : `${usuarioNormalizado}@frequencia-icm.app`);
      try {
        await window.firebaseSignIn(window.firebaseAuth, email, senha);
        document.getElementById('login-senha').value = '';
      } catch (e) {
        erro.textContent = 'Usuário ou senha inválidos.';
      }
    }

    async function sairDoApp() {
      await window.firebaseSignOut(window.firebaseAuth);
      alternarAba('chamada');
    }

    /**
     * Função auxiliar para gerar Hash simples do texto digitado
"""
replace_once(classic_anchor, classic_new, 'funções login')

# 7) Toda gravação exige login; cadastro/configuração exigem admin também no cliente.
replace_once(
    '    function executarGravacao(caminho, valor, isRemove = false) {\n      if (navigator.onLine && window.dbSet) {',
    """    function executarGravacao(caminho, valor, isRemove = false) {
      if (!window.usuarioAtual) { alert("Faça login para salvar alterações."); return; }
      const caminhoRestritoAdmin = caminho.startsWith('cultos_app/membros/') || caminho.startsWith('cultos_app/config/');
      if (caminhoRestritoAdmin && !window.isAdmin) {
        alert('🔒 Esta alteração é restrita ao administrador.');
        return;
      }
      if (navigator.onLine && window.dbSet) {""",
    'gravação auth gate'
)

# 8) Áreas administrativas não usam mais prompt/senha local.
aba_pattern = re.compile(
    r"    function alternarAba\(nomeAba\) \{\n.*?(?=      document\.querySelectorAll\('\.tab-btn'\))",
    re.S,
)
m = aba_pattern.search(s)
if not m:
    raise SystemExit('alternarAba original não encontrado')
aba_new = """    function alternarAba(nomeAba) {
      if ((nomeAba === 'membros' || nomeAba === 'mensal') && !window.isAdmin) {
        alert('🔒 Área restrita ao administrador.');
        return;
      }

"""
s = s[:m.start()] + aba_new + s[m.end():]

senha_pattern = re.compile(
    r"    function alterarSenhaAdministrador\(\) \{\n.*?\n    \}\n\n    function alternarFiltroMembro\(\) \{",
    re.S,
)
m = senha_pattern.search(s)
if not m:
    raise SystemExit('alterarSenhaAdministrador original não encontrado')
s = s[:m.start()] + """    function alterarSenhaAdministrador() {
      alert("A senha administrativa agora é gerenciada pelo Firebase Authentication.");
    }

    function alternarFiltroMembro() {""" + s[m.end():]

# 9) Guardas explícitas nos comandos de cadastro.
replace_once(
    '    function cadastrarMembro() {\n      const nome =',
    '    function cadastrarMembro() {\n      if (!window.isAdmin) { alert("Acesso restrito ao administrador."); return; }\n      const nome =',
    'guardar cadastrar'
)
replace_once(
    '    function editarMembro(id, nomeAtual, catAtual, grupoAtual) {\n      const novoNome =',
    '    function editarMembro(id, nomeAtual, catAtual, grupoAtual) {\n      if (!window.isAdmin) { alert("Acesso restrito ao administrador."); return; }\n      const novoNome =',
    'guardar editar'
)
replace_once(
    '    function removerMembro(id, nome) {\n      if (confirm(',
    '    function removerMembro(id, nome) {\n      if (!window.isAdmin) { alert("Acesso restrito ao administrador."); return; }\n      if (confirm(',
    'guardar remover'
)

# Sanidade mínima antes de gravar.
required_markers = [
    'firebase-auth.js',
    'onAuthStateChanged(auth',
    "usuarioNormalizado === 'admin'",
    '.admin-only.admin-visible',
    'caminhoRestritoAdmin',
]
for marker in required_markers:
    if marker not in s:
        raise SystemExit(f'marcador ausente após patch: {marker}')

path.write_text(s, encoding='utf-8')
print('Patch de autenticação aplicado com sucesso.')
