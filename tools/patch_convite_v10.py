from pathlib import Path

p = Path('index.html')
t = p.read_text(encoding='utf-8')

css_anchor = "  .dashboard-actions .btn-main { margin-top:0; }\n"
css_add = """  .dashboard-actions .btn-main { margin-top:0; }
  .btn-convite { grid-column:1 / -1; background:#476f5e !important; }
  .invite-admin-box { margin-top:12px; padding:14px; border:1px solid var(--border-color); border-radius:14px; background:var(--card-bg); box-shadow:0 4px 14px var(--shadow); }
  .invite-admin-head { display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:8px; }
  .invite-admin-head strong { color:var(--secondary); font-size:.95rem; }
  .invite-admin-preview { margin-top:10px; padding:10px 12px; border-radius:10px; background:var(--bg-container); border:1px dashed var(--border-color); color:var(--text-secondary); font-size:.8rem; line-height:1.4; }
  .invite-share-actions { display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:8px; }
  .invite-share-actions .btn-main { margin-top:0; }
"""
assert css_anchor in t, 'ancora CSS dashboard nao encontrada'
t = t.replace(css_anchor, css_add, 1)

mobile_anchor = "    .dashboard-actions { grid-template-columns:1fr; }\n"
mobile_add = """    .dashboard-actions { grid-template-columns:1fr; }
    .btn-convite { grid-column:auto; }
    .invite-share-actions { grid-template-columns:1fr; }
"""
assert mobile_anchor in t, 'ancora CSS mobile nao encontrada'
t = t.replace(mobile_anchor, mobile_add, 1)

button_anchor = "        <button class=\"btn-main admin-only\" onclick=\"alternarAba('membros')\">👥 Gerenciar membros</button>\n"
button_add = button_anchor + "        <button class=\"btn-main admin-only btn-convite\" onclick=\"alternarGeradorConvite()\">📣 Convite do culto</button>\n"
assert button_anchor in t, 'botao de membros nao encontrado'
t = t.replace(button_anchor, button_add, 1)

box_anchor = "      </div>\n      <div id=\"dash-admin-resumo\" class=\"admin-only\" style=\"margin-top:14px;\"></div>"
box_add = """      </div>
      <div id="convite-admin-box" class="invite-admin-box" hidden>
        <div class="invite-admin-head">
          <strong>📣 Gerar convite público</strong>
          <button type="button" class="btn-small-sec" onclick="alternarGeradorConvite()">Fechar</button>
        </div>
        <div class="grid-2">
          <div>
            <label for="convite-data">Data do culto</label>
            <input id="convite-data" type="date" onchange="atualizarOpcoesConvite()">
          </div>
          <div>
            <label for="convite-evento">Programação</label>
            <select id="convite-evento" onchange="atualizarPreviewConvite()"></select>
          </div>
        </div>
        <label for="convite-frase">Mensagem do convite</label>
        <select id="convite-frase" onchange="atualizarPreviewConvite()">
          <option value="1">Contamos com sua presença!</option>
          <option value="2">Venha cultuar conosco. Será uma alegria receber você!</option>
          <option value="3">Esperamos por você. Venha participar conosco!</option>
        </select>
        <div id="convite-admin-preview" class="invite-admin-preview">Escolha a data e a programação para gerar o link.</div>
        <div class="invite-share-actions">
          <button type="button" class="btn-main btn-wsp" onclick="compartilharConviteWhatsApp()">💬 Compartilhar no WhatsApp</button>
          <button type="button" class="btn-main btn-img" onclick="copiarLinkConvite()">🔗 Copiar link</button>
        </div>
      </div>
      <div id="dash-admin-resumo" class="admin-only" style="margin-top:14px;"></div>"""
assert box_anchor in t, 'local do box de convite nao encontrado'
t = t.replace(box_anchor, box_add, 1)

js_anchor = "    function alternarAba(nomeAba) {\n"
js_add = r'''    const FRASES_CONVITE_CULTO = {
      '1': 'Contamos com sua presença!',
      '2': 'Venha cultuar conosco. Será uma alegria receber você!',
      '3': 'Esperamos por você. Venha participar conosco!'
    };

    function hojeISOConvite() {
      const partes = new Intl.DateTimeFormat('en-US', {
        timeZone: 'America/Sao_Paulo', year: 'numeric', month: '2-digit', day: '2-digit'
      }).formatToParts(new Date());
      const mapa = Object.fromEntries(partes.map(p => [p.type, p.value]));
      return `${mapa.year}-${mapa.month}-${mapa.day}`;
    }

    function opcoesConvitePorData(iso) {
      if (!/^\d{4}-\d{2}-\d{2}$/.test(iso || '')) return [];
      const diaSemana = new Date(`${iso}T12:00:00-03:00`).getUTCDay();
      if (diaSemana >= 1 && diaSemana <= 4) return [{ tipo: 'culto', nome: 'Culto da Noite', hora: '19:30' }];
      if (diaSemana === 6) return [{ tipo: 'culto', nome: 'Culto da Noite', hora: '19:00' }];
      if (diaSemana === 0) return [
        { tipo: 'ebd', nome: 'EBD', hora: '10:00' },
        { tipo: 'culto', nome: 'Culto da Noite', hora: '19:00' }
      ];
      return [];
    }

    function formatarDataConvite(iso) {
      return new Intl.DateTimeFormat('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })
        .format(new Date(`${iso}T12:00:00-03:00`));
    }

    function alternarGeradorConvite() {
      if (!window.isAdmin) {
        alert('🔒 Área restrita ao administrador.');
        return;
      }
      const box = document.getElementById('convite-admin-box');
      if (!box) return;
      box.hidden = !box.hidden;
      if (!box.hidden) {
        const dataInput = document.getElementById('convite-data');
        const hoje = hojeISOConvite();
        if (!dataInput.value) dataInput.value = hoje;
        dataInput.min = hoje;
        atualizarOpcoesConvite();
        setTimeout(() => box.scrollIntoView({ behavior: 'smooth', block: 'nearest' }), 50);
      }
    }

    function atualizarOpcoesConvite() {
      const data = document.getElementById('convite-data')?.value || '';
      const select = document.getElementById('convite-evento');
      if (!select) return;
      select.innerHTML = '';
      const opcoes = opcoesConvitePorData(data);
      if (!opcoes.length) {
        const option = document.createElement('option');
        option.value = '';
        option.textContent = 'Sem culto programado nesta data';
        select.appendChild(option);
        select.disabled = true;
      } else {
        select.disabled = false;
        opcoes.forEach(item => {
          const option = document.createElement('option');
          option.value = item.tipo;
          option.textContent = `${item.nome} — ${item.hora}`;
          select.appendChild(option);
        });
      }
      atualizarPreviewConvite();
    }

    function dadosConviteSelecionado() {
      const data = document.getElementById('convite-data')?.value || '';
      const tipo = document.getElementById('convite-evento')?.value || '';
      const fraseId = document.getElementById('convite-frase')?.value || '1';
      const evento = opcoesConvitePorData(data).find(item => item.tipo === tipo);
      if (!data || !evento) throw new Error('Escolha uma data com culto programado.');
      return { data, tipo, fraseId, evento };
    }

    function montarLinkConvite() {
      const { data, tipo, fraseId } = dadosConviteSelecionado();
      const url = new URL('convite.html', window.location.href);
      url.search = '';
      url.hash = '';
      url.searchParams.set('d', data);
      url.searchParams.set('tipo', tipo);
      url.searchParams.set('f', fraseId);
      return url.toString();
    }

    function atualizarPreviewConvite() {
      const preview = document.getElementById('convite-admin-preview');
      if (!preview) return;
      try {
        const { data, fraseId, evento } = dadosConviteSelecionado();
        preview.textContent = `${evento.nome} • ${formatarDataConvite(data)} às ${evento.hora} — ${FRASES_CONVITE_CULTO[fraseId] || FRASES_CONVITE_CULTO['1']} O link abrirá uma contagem regressiva pública.`;
      } catch (e) {
        preview.textContent = 'Escolha uma data com culto programado para gerar o link.';
      }
    }

    function compartilharConviteWhatsApp() {
      if (!window.isAdmin) return;
      try {
        const { data, fraseId, evento } = dadosConviteSelecionado();
        const link = montarLinkConvite();
        const frase = FRASES_CONVITE_CULTO[fraseId] || FRASES_CONVITE_CULTO['1'];
        const texto = `🙏 *ICM Pinhos*\n\n${evento.nome} — ${formatarDataConvite(data)} às ${evento.hora}\n${frase}\n\n⏳ Acompanhe a contagem regressiva para o início do culto:\n${link}`;
        window.open(`https://wa.me/?text=${encodeURIComponent(texto)}`, '_blank', 'noopener');
      } catch (e) {
        alert(e.message || 'Não foi possível gerar o convite.');
      }
    }

    async function copiarLinkConvite() {
      if (!window.isAdmin) return;
      try {
        const link = montarLinkConvite();
        if (navigator.clipboard && window.isSecureContext) {
          await navigator.clipboard.writeText(link);
          alert('✅ Link do convite copiado.');
        } else {
          window.prompt('Copie o link do convite:', link);
        }
      } catch (e) {
        alert(e.message || 'Não foi possível gerar o convite.');
      }
    }

    function alternarAba(nomeAba) {
'''
assert js_anchor in t, 'ancora JS alternarAba nao encontrada'
t = t.replace(js_anchor, js_add, 1)

assert t.count('id="convite-admin-box"') == 1
assert t.count('onclick="alternarGeradorConvite()"') >= 2
assert 'convite.html' in t
assert 'compartilharConviteWhatsApp' in t

p.write_text(t, encoding='utf-8')
