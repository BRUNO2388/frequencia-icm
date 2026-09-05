from pathlib import Path

p = Path("index.html")
s = p.read_text(encoding="utf-8")

def replace_once(old, new, label):
    global s
    count = s.count(old)
    if count != 1:
        raise SystemExit(f"{label}: esperado 1 ocorrência, encontrado {count}")
    s = s.replace(old, new, 1)

replace_once(
'''    window.adicionarFilaSincronizacao = function(caminho, acao, valor) {
      if (!localDB) return;
      const tx = localDB.transaction("syncQueue", "readwrite");
      tx.objectStore("syncQueue").add({ caminho, acao, valor, timestamp: Date.now() });
      atualizarStatusConexaoUI();
    };''',
'''    window.adicionarFilaSincronizacao = function(caminho, acao, valor) {
      if (!localDB) return;
      const tx = localDB.transaction("syncQueue", "readwrite");
      tx.objectStore("syncQueue").add({
        caminho,
        acao,
        valor,
        timestamp: Date.now(),
        origem: window.isAdmin ? 'admin' : 'membro'
      });
      atualizarStatusConexaoUI();
    };''',
'origem da fila offline'
)

replace_once(
'''            const exigeAdmin = item.caminho.startsWith('cultos_app/membros/') || item.caminho.startsWith('cultos_app/config/');
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
            }''',
'''            const exigeAdmin = item.caminho.startsWith('cultos_app/membros/') || item.caminho.startsWith('cultos_app/config/');
            if (exigeAdmin && !window.isAdmin) continue;

            let caminhoEfetivo = item.caminho;
            const origemItem = item.origem || 'membro';

            if (caminhoEfetivo.startsWith('cultos_app/registros/')) {
              if (origemItem === 'admin') {
                // Alterações offline feitas pelo Admin só podem ir ao histórico oficial
                // quando um Admin estiver autenticado novamente.
                if (!window.isAdmin) continue;
              } else {
                // Alterações offline feitas pelo Membro nunca viram gravação direta no
                // histórico oficial, mesmo se quem processar a fila depois for um Admin.
                const hojeMembro = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo' }).format(new Date());
                const cultoIdFila = caminhoEfetivo.split('/')[2] || '';
                if (!cultoIdFila.startsWith(`${hojeMembro}_`)) {
                  const txDeleteAntigo = localDB.transaction("syncQueue", "readwrite");
                  txDeleteAntigo.objectStore("syncQueue").delete(chave);
                  continue;
                }
                caminhoEfetivo = caminhoEfetivo.replace('cultos_app/registros/', 'cultos_app/pendentes/');
              }
            }''',
'proteção da fila por perfil'
)

replace_once(
'''      } else {
        unsubAtual = onValue(ref(db, 'cultos_app/atual'), (snapshot) => {
          const atual = snapshot.val() || {};
          window.cultoAtual = atual;
          window.registrosCultos = {};
          const hojeMembro = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo' }).format(new Date());
          if (atual.chave && atual.registro && atual.data === hojeMembro && atual.chave.startsWith(`${hojeMembro}_`)) {
            window.registrosCultos[atual.chave] = atual.registro;
            if (atual.tipo) document.getElementById('culto-tipo').value = atual.tipo;
          }
          carregarChamadaCulto();
          salvarCacheAtual();
        });
      }''',
'''      } else {
        unsubAtual = onValue(ref(db, 'cultos_app/atual'), (snapshot) => {
          const atual = snapshot.val() || {};
          const hojeMembro = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo' }).format(new Date());
          const espelhoValido = !!(
            atual.chave &&
            atual.data === hojeMembro &&
            atual.chave.startsWith(`${hojeMembro}_`)
          );

          window.registrosCultos = {};

          if (espelhoValido) {
            // Firebase pode omitir "registro" quando ele é um objeto vazio.
            // Ainda assim o culto de hoje é válido e deve aparecer zerado.
            const registroAtual = atual.registro && typeof atual.registro === 'object'
              ? atual.registro
              : {};
            window.cultoAtual = { ...atual, registro: registroAtual };
            window.registrosCultos[atual.chave] = registroAtual;
            if (atual.tipo) document.getElementById('culto-tipo').value = atual.tipo;
          } else {
            // Nunca mantém como fallback um culto antigo ou inválido.
            window.cultoAtual = {};
          }

          carregarChamadaCulto();
          salvarCacheAtual();
        });
      }''',
'espelho seguro do perfil membro'
)

replace_once(
'''      const hojeISO = new Date().toISOString().split('T')[0];''',
'''      const hojeISO = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo' }).format(new Date());''',
'data correta do calendário'
)

replace_once(
'''      const chave = getChaveCulto();
      const registro = window.registrosCultos[chave] || window.cultoAtual?.registro || {};
      const presencas = registro.presencas || {};''',
'''      const chave = getChaveCulto();
      const espelhoDoCultoSelecionado = !!(
        window.cultoAtual?.chave === chave &&
        window.cultoAtual?.data === inputData.value
      );
      const registro = window.registrosCultos[chave]
        || (espelhoDoCultoSelecionado ? (window.cultoAtual?.registro || {}) : {});
      const presencas = registro.presencas || {};''',
'fallback seguro do dashboard'
)

replace_once(
'''      if (totalP === 0 && visitantesLista.length === 0) divPresenca.innerHTML = '<p style="text-align:center; color:#888; padding: 15px;">Nenhum membro ou visitante marcado como presente ainda.</p>';''',
'''      const filtroListaAtual = window.filtroChamadaAtual || 'PRESENTES';
      if (filtroListaAtual === 'PRESENTES' && totalP === 0) {
        divPresenca.innerHTML = '<p style="text-align:center; color:#888; padding: 15px;">Nenhum membro marcado como presente ainda.</p>';
      } else if (filtroListaAtual !== 'PRESENTES' && !divPresenca.innerHTML.trim()) {
        divPresenca.innerHTML = `<p style="text-align:center; color:#888; padding:15px;">Nenhum membro cadastrado em ${escapeHTML(filtroListaAtual)}.</p>`;
      }''',
'lista por categoria com chamada zerada'
)

p.write_text(s, encoding="utf-8")
