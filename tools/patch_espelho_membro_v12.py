from pathlib import Path

p = Path('index.html')
s = p.read_text(encoding='utf-8')

marker = "    function iniciarSincronizacaoFirebase() {\n"
helper = """    window.publicarEspelhoCultoSelecionado = function publicarEspelhoCultoSelecionado() {\n      if (!window.isAdmin) return;\n      const hojeLocal = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo' }).format(new Date());\n      const dataSelecionada = document.getElementById('culto-data')?.value || '';\n      const tipoSelecionado = document.getElementById('culto-tipo')?.value || '';\n      if (dataSelecionada !== hojeLocal || !tipoSelecionado) return;\n\n      const chaveAtual = `${dataSelecionada}_${tipoSelecionado.replace(/\\s+/g, '_')}`;\n      const registroAtual = window.registrosCultos[chaveAtual] || {};\n      const espelho = {\n        chave: chaveAtual,\n        data: hojeLocal,\n        tipo: tipoSelecionado,\n        registro: registroAtual\n      };\n\n      window.cultoAtual = espelho;\n      set(ref(db, 'cultos_app/atual'), espelho)\n        .catch((erro) => console.warn('Não foi possível atualizar o espelho do culto atual.', erro));\n    };\n\n"""
if helper not in s:
    if marker not in s:
        raise SystemExit('Marcador iniciarSincronizacaoFirebase não encontrado')
    s = s.replace(marker, helper + marker, 1)

old_admin = """          // O modo Membro lê cultos_app/atual. Sempre que o Admin carregar o\n          // registro oficial do culto selecionado de hoje, publica um retrato\n          // completo dele para eliminar dados antigos ou parciais do espelho.\n          const hojeLocal = new Intl.DateTimeFormat('en-CA', { timeZone: 'America/Sao_Paulo' }).format(new Date());\n          const dataSelecionada = document.getElementById('culto-data')?.value || '';\n          const tipoSelecionado = document.getElementById('culto-tipo')?.value || '';\n          if (dataSelecionada === hojeLocal && tipoSelecionado) {\n            const chaveAtual = `${dataSelecionada}_${tipoSelecionado.replace(/\\s+/g, '_')}`;\n            const registroAtual = window.registrosCultos[chaveAtual];\n            if (registroAtual) {\n              set(ref(db, 'cultos_app/atual'), {\n                chave: chaveAtual,\n                data: hojeLocal,\n                tipo: tipoSelecionado,\n                registro: registroAtual\n              }).catch((erro) => console.warn('Não foi possível atualizar o espelho do culto atual.', erro));\n            }\n          }\n"""
new_admin = """          // Publica sempre o culto selecionado de hoje, mesmo quando ainda não\n          // existe registro. Nesse caso o Membro recebe um espelho vazio (0/0/0)\n          // em vez de continuar vendo o último culto finalizado.\n          window.publicarEspelhoCultoSelecionado();\n"""
if old_admin in s:
    s = s.replace(old_admin, new_admin, 1)
elif new_admin not in s:
    raise SystemExit('Bloco antigo do espelho Admin não encontrado')

old_member = """            } else {\n              // Membro altera somente o campo necessário no espelho atual.\n              gravarOuEnfileirar('cultos_app/atual/chave', chaveCulto, false);\n              gravarOuEnfileirar('cultos_app/atual/data', hojeISO, false);\n              gravarOuEnfileirar('cultos_app/atual/tipo', tipoCulto, false);\n              if (restante) gravarOuEnfileirar(`cultos_app/atual/registro/${restante}`, valor, isRemove);\n              else gravarOuEnfileirar('cultos_app/atual/registro', valor, isRemove);\n            }\n"""
new_member = """            } else {\n              // Se o Membro estiver mudando para outro culto do mesmo dia, substitui\n              // o espelho inteiro antes da primeira alteração. Isso impede que campos\n              // do culto anterior (presenças, visitantes ou finalizado) sejam herdados.\n              const mesmoCultoNoEspelho = window.cultoAtual?.chave === chaveCulto && window.cultoAtual?.data === hojeISO;\n              if (!mesmoCultoNoEspelho) {\n                gravarOuEnfileirar('cultos_app/atual', {\n                  chave: chaveCulto,\n                  data: hojeISO,\n                  tipo: tipoCulto,\n                  registro: registroCompleto\n                }, false);\n              } else {\n                gravarOuEnfileirar('cultos_app/atual/chave', chaveCulto, false);\n                gravarOuEnfileirar('cultos_app/atual/data', hojeISO, false);\n                gravarOuEnfileirar('cultos_app/atual/tipo', tipoCulto, false);\n                if (restante) gravarOuEnfileirar(`cultos_app/atual/registro/${restante}`, valor, isRemove);\n                else gravarOuEnfileirar('cultos_app/atual/registro', valor, isRemove);\n              }\n            }\n"""
if old_member in s:
    s = s.replace(old_member, new_member, 1)
elif new_member not in s:
    raise SystemExit('Bloco antigo do espelho Membro não encontrado')

old_load = """    function carregarChamadaCulto() {\n      const chaveCulto = getChaveCulto();\n      const registroHoje = window.registrosCultos[chaveCulto] || {};\n"""
new_load = """    function carregarChamadaCulto() {\n      const chaveCulto = getChaveCulto();\n      if (window.isAdmin && typeof window.publicarEspelhoCultoSelecionado === 'function') {\n        window.publicarEspelhoCultoSelecionado();\n      }\n      const registroHoje = window.registrosCultos[chaveCulto] || {};\n"""
if old_load in s:
    s = s.replace(old_load, new_load, 1)
elif new_load not in s:
    raise SystemExit('Início de carregarChamadaCulto não encontrado')

required = [
    'window.publicarEspelhoCultoSelecionado = function publicarEspelhoCultoSelecionado()',
    'registroAtual = window.registrosCultos[chaveAtual] || {}',
    'window.publicarEspelhoCultoSelecionado();',
    'const mesmoCultoNoEspelho = window.cultoAtual?.chave === chaveCulto',
]
for item in required:
    if item not in s:
        raise SystemExit(f'Validação falhou: {item}')

p.write_text(s, encoding='utf-8')
print('Patch aplicado com sucesso')
