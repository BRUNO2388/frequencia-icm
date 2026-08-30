from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')

repls = []
repls.append((
'''    import { getDatabase, ref, set, remove, onValue } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js";''',
'''    import { getDatabase, ref, set, remove, onValue, get } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-database.js";'''
))

repls.append((
'''    let unsubMembros = null;
    let unsubRegistros = null;
    let unsubAtual = null;

    function pararSincronizacaoFirebase() {
      [unsubMembros, unsubRegistros, unsubAtual].forEach(fn => { if (fn) fn(); });
      unsubMembros = unsubRegistros = unsubAtual = null;
    }''',
'''    let unsubMembros = null;
    let unsubRegistros = null;
    let unsubAtual = null;
    let unsubPendentes = null;

    function pararSincronizacaoFirebase() {
      [unsubMembros, unsubRegistros, unsubAtual, unsubPendentes].forEach(fn => { if (fn) fn(); });
      unsubMembros = unsubRegistros = unsubAtual = unsubPendentes = null;
    }'''
))

repls.append((
'''      if (window.isAdmin) {
        unsubRegistros = onValue(ref(db, 'cultos_app/registros'), (snapshot) => {
          window.registrosCultos = snapshot.val() || {};
          carregarChamadaCulto();
          gerarRelatorioMensal();
          salvarCacheAtual();
        });
      } else {''',
'''      if (window.isAdmin) {
        unsubRegistros = onValue(ref(db, 'cultos_app/registros'), (snapshot) => {
          window.registrosCultos = snapshot.val() || {};
          carregarChamadaCulto();
          gerarRelatorioMensal();
          salvarCacheAtual();
        });

        // Membro grava em "pendentes". O Admin promove somente cultos ainda inexistentes
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
        });
      } else {'''
))

repls.append((
'''      const gravarOuEnfileirar = (destino, valorDestino, remover = false) => {
        if (navigator.onLine && window.dbSet) {''',
'''      const gravarOuEnfileirar = (destino, valorDestino, remover = false) => {
        // Histórico oficial é imutável para membro: gravações de chamada feitas por membro
        // são redirecionadas para a área pendente até um Admin consolidá-las.
        if (!window.isAdmin && destino.startsWith('cultos_app/registros/')) {
          destino = destino.replace('cultos_app/registros/', 'cultos_app/pendentes/');
        }
        if (navigator.onLine && window.dbSet) {'''
))

repls.append((
'''            const exigeAdmin = item.caminho.startsWith('cultos_app/membros/') || item.caminho.startsWith('cultos_app/config/');
            if (exigeAdmin && !window.isAdmin) continue;
            try {
              if (item.acao === 'SET') await set(ref(db, item.caminho), item.valor);
              else if (item.acao === 'REMOVE') await remove(ref(db, item.caminho));''',
'''            const exigeAdmin = item.caminho.startsWith('cultos_app/membros/') || item.caminho.startsWith('cultos_app/config/');
            if (exigeAdmin && !window.isAdmin) continue;
            let caminhoEfetivo = item.caminho;
            if (!window.isAdmin && caminhoEfetivo.startsWith('cultos_app/registros/')) {
              caminhoEfetivo = caminhoEfetivo.replace('cultos_app/registros/', 'cultos_app/pendentes/');
            }
            try {
              if (item.acao === 'SET') await set(ref(db, caminhoEfetivo), item.valor);
              else if (item.acao === 'REMOVE') await remove(ref(db, caminhoEfetivo));'''
))

for old, new in repls:
    if new in text:
        continue
    if old not in text:
        raise SystemExit('Trecho esperado não encontrado:\n' + old[:180])
    text = text.replace(old, new, 1)

path.write_text(text, encoding='utf-8')
