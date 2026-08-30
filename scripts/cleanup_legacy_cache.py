from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
original = text

old = '''    request.onsuccess = (e) => {
      localDB = e.target.result;
      if (window.usuarioAtual) carregarDadosLocais();
    };'''
new = '''    request.onsuccess = (e) => {
      localDB = e.target.result;
      const cleanupTx = localDB.transaction("appData", "readwrite");
      cleanupTx.objectStore("appData").delete("cultos_app");
      if (window.usuarioAtual) carregarDadosLocais();
    };'''
if old in text:
    text = text.replace(old, new, 1)

text = text.replace("new Date().toISOString().split('-')[0]", "new Date().toISOString().split('T')[0]")

if text == original:
    raise SystemExit('Nenhuma correção pendente encontrada.')
path.write_text(text, encoding='utf-8')
