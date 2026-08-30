from pathlib import Path

path = Path('index.html')
text = path.read_text(encoding='utf-8')
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
if old not in text:
    raise SystemExit('Trecho esperado não encontrado; nenhuma alteração aplicada.')
path.write_text(text.replace(old, new, 1), encoding='utf-8')
