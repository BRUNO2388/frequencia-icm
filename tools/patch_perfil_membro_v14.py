from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
original = text

def replace_once(old, new, label):
    global text
    count = text.count(old)
    if count != 1:
        raise SystemExit(f'{label}: esperado 1 trecho, encontrado {count}')
    text = text.replace(old, new, 1)

# 1) Filtros de classe continuam navegaveis mesmo com culto finalizado.
old = "document.querySelectorAll('#tab-chamada input:not(#culto-data), #tab-chamada button:not(#btn-finalizar-culto):not(.calendar-nav-btn):not(.calendar-day), #tab-chamada select:not(#culto-tipo)').forEach(el => {"
new = "document.querySelectorAll('#tab-chamada input:not(#culto-data), #tab-chamada button:not(#btn-finalizar-culto):not(.calendar-nav-btn):not(.calendar-day):not(.filter-chip), #tab-chamada select:not(#culto-tipo)').forEach(el => {"
replace_once(old, new, 'filtros finalizacao')

# 2) Acoes em massa ficam apenas para Admin; evita marcar toda a igreja por engano no perfil Membro.
old = '''      <div style="display:flex; justify-content:space-between; margin-bottom:12px; gap: 6px;">
        <button class="btn-small-sec" onclick="marcarTodos('presente')">✅ Marcar Todos Presentes</button>
        <button class="btn-small-sec" onclick="marcarTodos('ausente')">🔄 Limpar Chamada</button>
      </div>'''
new = '''      <div class="admin-only" style="display:flex; justify-content:space-between; margin-bottom:12px; gap: 6px;">
        <button class="btn-small-sec" onclick="marcarTodos('presente')">✅ Marcar Todos Presentes</button>
        <button class="btn-small-sec" onclick="marcarTodos('ausente')">🔄 Limpar Chamada</button>
      </div>'''
replace_once(old, new, 'acoes em massa admin')

# A classe admin-only usa display:block quando visivel; restaura flex neste bloco especificamente.
marker_css = "  .admin-only.admin-visible { display:block; }\n"
if marker_css not in text:
    raise SystemExit('CSS admin-only nao encontrado')
text = text.replace(marker_css, marker_css + "  #tab-chamada .admin-only.admin-visible[style*=\"display:flex\"] { display:flex !important; }\n", 1)

# 3) Nao exibe cache antigo do Membro enquanto online. O dado corrente deve vir do Firebase.
old = '''        window.registrosCultos = {};
        carregarDadosLocais();
        iniciarSincronizacaoFirebase();
        window.processarFilaSincronizacao();'''
new = '''        window.registrosCultos = {};
        window.cultoAtual = {};
        if (window.isAdmin || !navigator.onLine) {
          carregarDadosLocais();
        } else if (localDB) {
          // Online, o Membro começa limpo e aguarda o espelho atual do servidor.
          // Evita mostrar presenças de um culto anterior salvas no IndexedDB.
          const txCacheMembro = localDB.transaction("appData", "readwrite");
          txCacheMembro.objectStore("appData").delete("cultos_app_member");
        }
        iniciarSincronizacaoFirebase();
        window.processarFilaSincronizacao();'''
replace_once(old, new, 'cache membro online')

# 4) O espelho cultos_app/atual e efemero: jamais deve ficar em fila offline.
old = '''        if (navigator.onLine && window.dbSet) {
          const operacao = remover
            ? window.dbRemove(window.dbRef(window.db, destino))
            : window.dbSet(window.dbRef(window.db, destino), valorDestino);
          Promise.resolve(operacao).catch(() => {
            window.adicionarFilaSincronizacao(destino, remover ? 'REMOVE' : 'SET', valorDestino);
          });
        } else {
          window.adicionarFilaSincronizacao(destino, remover ? 'REMOVE' : 'SET', valorDestino);
        }'''
new = '''        const espelhoAtualEfemero = destino === 'cultos_app/atual' || destino.startsWith('cultos_app/atual/');
        if (navigator.onLine && window.dbSet) {
          const operacao = remover
            ? window.dbRemove(window.dbRef(window.db, destino))
            : window.dbSet(window.dbRef(window.db, destino), valorDestino);
          Promise.resolve(operacao).catch(() => {
            // O histórico/pendentes podem esperar pela internet; o espelho atual não.
            if (!espelhoAtualEfemero) window.adicionarFilaSincronizacao(destino, remover ? 'REMOVE' : 'SET', valorDestino);
          });
        } else if (!espelhoAtualEfemero) {
          window.adicionarFilaSincronizacao(destino, remover ? 'REMOVE' : 'SET', valorDestino);
        }'''
replace_once(old, new, 'fila do espelho atual')

# 5) Purga entradas antigas do espelho atual e impede Membro de reenviar fila de outro dia.
old = '''          for (let i = 0; i < itens.length; i++) {
            const item = itens[i];
            const chave = chaves[i];
            const exigeAdmin = item.caminho.startsWith('cultos_app/membros/') || item.caminho.startsWith('cultos_app/config/');
            if (exigeAdmin && !window.isAdmin) continue;
            let caminhoEfetivo = item.caminho;
            if (!window.isAdmin && caminhoEfetivo.startsWith('cultos_app/registros/')) {
              caminhoEfetivo = caminhoEfetivo.replace('cultos_app/registros/', 'cultos_app/pendentes/');
            }
            try {'''
new = '''          for (let i = 0; i < itens.length; i++) {
            const item = itens[i];
            const chave = chaves[i];

            // Nunca reaplica o espelho de uma sessão anterior: ele é somente tempo real.
            if (item.caminho === 'cultos_app/atual' || item.caminho.startsWith('cultos_app/atual/')) {
              const txDeleteAtual = localDB.transaction("syncQueue", "readwrite");
              txDeleteAtual.objectStore("syncQueue").delete(chave);
              continue;
            }

            const exigeAdmin = item.caminho.startsWith('cultos_app/membros/') || item.caminho.startsWith('cultos_app/config/');
            if (exigeAdmin && !window.isAdmin) continue;
            let caminhoEfetivo = item.caminho;
            if (!window.isAdmin && caminhoEfetivo.startsWith('cultos_app/registros/')) {
              const hojeMembro = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo' }).format(new Date());
              const cultoIdFila = caminhoEfetivo.split('/')[2] || '';
              if (!cultoIdFila.startsWith(`${hojeMembro}_`)) {
                const txDeleteAntigo = localDB.transaction("syncQueue", "readwrite");
                txDeleteAntigo.objectStore("syncQueue").delete(chave);
                continue;
              }
              caminhoEfetivo = caminhoEfetivo.replace('cultos_app/registros/', 'cultos_app/pendentes/');
            }
            try {'''
replace_once(old, new, 'limpeza fila antiga')

# 6) Membro so aceita espelho cuja chave tambem pertence ao dia atual.
old = '''          if (atual.chave && atual.registro && atual.data === new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo' }).format(new Date())) {
            window.registrosCultos[atual.chave] = atual.registro;'''
new = '''          const hojeMembro = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo' }).format(new Date());
          if (atual.chave && atual.registro && atual.data === hojeMembro && atual.chave.startsWith(`${hojeMembro}_`)) {
            window.registrosCultos[atual.chave] = atual.registro;'''
replace_once(old, new, 'validacao espelho membro')

# 7) Consolida alteracoes do Membro mesmo quando o registro oficial ja existe.
insert_before = '''    function iniciarSincronizacaoFirebase() {
'''
helper = '''    function mesclarRegistroPendente(registroOficial, registroPendente) {
      const oficial = registroOficial && typeof registroOficial === 'object' ? registroOficial : {};
      const pendente = registroPendente && typeof registroPendente === 'object' ? registroPendente : {};
      const resultado = { ...oficial };

      if (pendente.presencas && typeof pendente.presencas === 'object') {
        resultado.presencas = { ...(oficial.presencas || {}), ...pendente.presencas };
      }
      if (Object.prototype.hasOwnProperty.call(pendente, 'visitantesLista')) {
        resultado.visitantesLista = Array.isArray(pendente.visitantesLista) ? [...pendente.visitantesLista] : [];
      }
      if (pendente.visitantesData && typeof pendente.visitantesData === 'object') {
        resultado.visitantesData = { ...(oficial.visitantesData || {}), ...pendente.visitantesData };
      }
      if (pendente.eventoInfo && typeof pendente.eventoInfo === 'object') {
        resultado.eventoInfo = { ...(oficial.eventoInfo || {}), ...pendente.eventoInfo };
      }

      // finalizado continua sendo decisão exclusiva do Admin.
      if (Object.prototype.hasOwnProperty.call(oficial, 'finalizado')) resultado.finalizado = oficial.finalizado;
      else delete resultado.finalizado;
      return resultado;
    }

'''
if text.count(insert_before) != 1:
    raise SystemExit(f'local helper: esperado 1, encontrado {text.count(insert_before)}')
text = text.replace(insert_before, helper + insert_before, 1)

old = '''        // Membro grava em "pendentes". O Admin promove somente cultos ainda inexistentes
        // no histórico oficial. Assim um registro já consolidado nunca é sobrescrito por membro.
        unsubPendentes = onValue(ref(db, 'cultos_app/pendentes'), async (snapshot) => {
          const pendentes = snapshot.val() || {};
          for (const [chaveCulto, registroPendente] of Object.entries(pendentes)) {
            try {
              const destino = ref(db, `cultos_app/registros/${chaveCulto}`);
              const existente = await get(destino);
              if (!existente.exists()) {
                await set(destino, registroPendente);
              }
              await remove(ref(db, `cultos_app/pendentes/${chaveCulto}`));
            } catch (erro) {
              console.warn('Não foi possível consolidar o culto pendente.', chaveCulto, erro);
            }
          }
        });'''
new = '''        // Membro grava alterações parciais em "pendentes". O Admin mescla essas
        // alterações no registro oficial, inclusive quando o culto já existe.
        unsubPendentes = onValue(ref(db, 'cultos_app/pendentes'), async (snapshot) => {
          const pendentes = snapshot.val() || {};
          for (const [chaveCulto, registroPendente] of Object.entries(pendentes)) {
            try {
              const destino = ref(db, `cultos_app/registros/${chaveCulto}`);
              const existente = await get(destino);
              const registroOficial = existente.exists() ? (existente.val() || {}) : {};

              // Não permite que uma pendência antiga altere culto já finalizado.
              if (registroOficial.finalizado) {
                await remove(ref(db, `cultos_app/pendentes/${chaveCulto}`));
                continue;
              }

              const consolidado = mesclarRegistroPendente(registroOficial, registroPendente);
              await set(destino, consolidado);
              await remove(ref(db, `cultos_app/pendentes/${chaveCulto}`));
            } catch (erro) {
              console.warn('Não foi possível consolidar o culto pendente.', chaveCulto, erro);
            }
          }
        });'''
replace_once(old, new, 'consolidacao pendentes')

# 8) Copia lista de visitantes antes de aplicar fallback, evitando mutar o registro em memória.
old_vis = "      let visitantesLista = registroHoje.visitantesLista || [];"
count_vis = text.count(old_vis)
if count_vis != 2:
    raise SystemExit(f'visitantesLista: esperado 2, encontrado {count_vis}')
text = text.replace(old_vis, "      let visitantesLista = Array.isArray(registroHoje.visitantesLista) ? [...registroHoje.visitantesLista] : [];", 2)

if text == original:
    raise SystemExit('Nenhuma alteração aplicada')

path.write_text(text, encoding='utf-8')
print('Patch perfil Membro V14 aplicado com sucesso.')
