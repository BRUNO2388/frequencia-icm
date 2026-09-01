from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
original = text

# 1) Datas do painel/chamada sempre no fuso da igreja.
old_init = """    const inputData = document.getElementById('culto-data');
    const hoje = new Date();
    window.mesCalendario = new Date(hoje.getFullYear(), hoje.getMonth(), 1);
    inputData.value = hoje.toISOString().split('T')[0];
    document.getElementById('filtro-mes-ano').value = hoje.toISOString().slice(0, 7);
"""
new_init = """    const inputData = document.getElementById('culto-data');
    const hoje = new Date();
    const hojeISOIgreja = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo' }).format(hoje);
    window.mesCalendario = new Date(hoje.getFullYear(), hoje.getMonth(), 1);
    inputData.value = hojeISOIgreja;
    document.getElementById('filtro-mes-ano').value = hojeISOIgreja.slice(0, 7);
"""
if text.count(old_init) != 1:
    raise SystemExit(f'Inicializacao de data esperada 1 vez; encontrada {text.count(old_init)}')
text = text.replace(old_init, new_init, 1)

old_today = "          const hojeISO = new Date().toISOString().split('T')[0];"
new_today = "          const hojeISO = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo' }).format(new Date());"
if text.count(old_today) != 1:
    raise SystemExit(f'hojeISO UTC esperado 1 vez; encontrado {text.count(old_today)}')
text = text.replace(old_today, new_today, 1)

# 2) Quando o Admin carrega o registro oficial de hoje, repara o espelho público
# usado pelo usuário Membro. Isso corrige imediatamente um cultos_app/atual antigo.
old_listener = """        unsubRegistros = onValue(ref(db, 'cultos_app/registros'), (snapshot) => {
          window.registrosCultos = snapshot.val() || {};
          carregarChamadaCulto();
          gerarRelatorioMensal();
          salvarCacheAtual();
        });
"""
new_listener = """        unsubRegistros = onValue(ref(db, 'cultos_app/registros'), (snapshot) => {
          window.registrosCultos = snapshot.val() || {};

          // O modo Membro lê cultos_app/atual. Sempre que o Admin carregar o
          // registro oficial do culto selecionado de hoje, publica um retrato
          // completo dele para eliminar dados antigos ou parciais do espelho.
          const hojeLocal = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo' }).format(new Date());
          const dataSelecionada = document.getElementById('culto-data')?.value || '';
          const tipoSelecionado = document.getElementById('culto-tipo')?.value || '';
          if (dataSelecionada === hojeLocal && tipoSelecionado) {
            const chaveAtual = `${dataSelecionada}_${tipoSelecionado.replace(/\\s+/g, '_')}`;
            const registroAtual = window.registrosCultos[chaveAtual];
            if (registroAtual) {
              set(ref(db, 'cultos_app/atual'), {
                chave: chaveAtual,
                data: hojeLocal,
                tipo: tipoSelecionado,
                registro: registroAtual
              }).catch((erro) => console.warn('Não foi possível atualizar o espelho do culto atual.', erro));
            }
          }

          carregarChamadaCulto();
          gerarRelatorioMensal();
          salvarCacheAtual();
        });
"""
if text.count(old_listener) != 1:
    raise SystemExit(f'Listener de registros esperado 1 vez; encontrado {text.count(old_listener)}')
text = text.replace(old_listener, new_listener, 1)

# 3) Ao Admin alterar o culto de hoje, substitui o espelho inteiro de uma vez.
# Para Membro mantemos atualização por campo, evitando que um cliente com estado
# antigo sobrescreva o trabalho feito pelo Admin.
old_mirror = """          if (dataCulto === hojeISO) {
            const restante = partes.slice(3).join('/');
            const tipoCulto = document.getElementById('culto-tipo').value;
            gravarOuEnfileirar('cultos_app/atual/chave', chaveCulto, false);
            gravarOuEnfileirar('cultos_app/atual/data', hojeISO, false);
            gravarOuEnfileirar('cultos_app/atual/tipo', tipoCulto, false);
            if (restante) gravarOuEnfileirar(`cultos_app/atual/registro/${restante}`, valor, isRemove);
            else gravarOuEnfileirar('cultos_app/atual/registro', valor, isRemove);
            window.cultoAtual = {
              chave: chaveCulto,
              data: hojeISO,
              tipo: tipoCulto,
              registro: window.registrosCultos[chaveCulto] || {}
            };
          }
"""
new_mirror = """          if (dataCulto === hojeISO) {
            const restante = partes.slice(3).join('/');
            const tipoCulto = document.getElementById('culto-tipo').value;
            const registroCompleto = window.registrosCultos[chaveCulto] || {};

            if (window.isAdmin) {
              // Admin é a fonte oficial: substitui o espelho inteiro para não
              // deixar presenças/visitantes de um culto anterior misturados.
              gravarOuEnfileirar('cultos_app/atual', {
                chave: chaveCulto,
                data: hojeISO,
                tipo: tipoCulto,
                registro: registroCompleto
              }, false);
            } else {
              // Membro altera somente o campo necessário no espelho atual.
              gravarOuEnfileirar('cultos_app/atual/chave', chaveCulto, false);
              gravarOuEnfileirar('cultos_app/atual/data', hojeISO, false);
              gravarOuEnfileirar('cultos_app/atual/tipo', tipoCulto, false);
              if (restante) gravarOuEnfileirar(`cultos_app/atual/registro/${restante}`, valor, isRemove);
              else gravarOuEnfileirar('cultos_app/atual/registro', valor, isRemove);
            }

            window.cultoAtual = {
              chave: chaveCulto,
              data: hojeISO,
              tipo: tipoCulto,
              registro: registroCompleto
            };
          }
"""
if text.count(old_mirror) != 1:
    raise SystemExit(f'Bloco de espelho esperado 1 vez; encontrado {text.count(old_mirror)}')
text = text.replace(old_mirror, new_mirror, 1)

if text == original:
    raise SystemExit('Nenhuma alteracao aplicada')

path.write_text(text, encoding='utf-8')
print('Patch V13 aplicado com sucesso.')
