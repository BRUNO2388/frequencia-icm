/**
 * Security Fix Library - Frequência ICM PINHOS
 * Biblioteca de segurança pronta para usar
 * 
 * Instruções:
 * 1. Inclua este arquivo ANTES de qualquer outro script no HTML
 * 2. Use as classes e funções conforme documentado
 * 3. Teste com DevTools para validar proteção
 */

// ============================================================
// CLASSE: ARMAZENAMENTO SEGURO
// ============================================================

class SecureStorage {
  constructor(prefix = 'icm_') {
    this.prefix = prefix;
  }

  /**
   * Sanitiza dados para prevenir XSS
   * @param {string} data - Dados a sanitizar
   * @returns {string} Dados sanitizados
   */
  sanitize(data) {
    if (typeof data === 'string') {
      return data
        .replace(/[<>\"'&]/g, (char) => {
          const map = { 
            '<': '&lt;', 
            '>': '&gt;', 
            '"': '&quot;', 
            "'": '&#39;', 
            '&': '&amp;' 
          };
          return map[char];
        })
        .trim();
    }
    return data;
  }

  /**
   * Sanitiza recursivamente objetos
   * @param {object} obj - Objeto a sanitizar
   * @returns {object} Objeto sanitizado
   */
  sanitizeObject(obj) {
    if (typeof obj !== 'object' || obj === null) {
      return this.sanitize(obj.toString());
    }

    if (Array.isArray(obj)) {
      return obj.map(item => this.sanitizeObject(item));
    }

    const sanitized = {};
    for (const key in obj) {
      if (obj.hasOwnProperty(key)) {
        sanitized[key] = this.sanitizeObject(obj[key]);
      }
    }
    return sanitized;
  }

  /**
   * Salva dados com validação e sanitização
   * @param {string} key - Chave
   * @param {*} value - Valor (string, object, array)
   * @returns {boolean} Sucesso
   */
  set(key, value) {
    try {
      const sanitized = typeof value === 'object' 
        ? JSON.stringify(this.sanitizeObject(value))
        : this.sanitize(value);
      
      localStorage.setItem(this.prefix + key, sanitized);
      SecureLogger.log(`Dados salvos: ${key}`, 'info');
      return true;
    } catch (error) {
      SecureLogger.error(`Erro ao salvar ${key}`, error.message);
      return false;
    }
  }

  /**
   * Recupera dados com segurança
   * @param {string} key - Chave
   * @returns {*} Valor armazenado ou null
   */
  get(key) {
    try {
      const value = localStorage.getItem(this.prefix + key);
      if (!value) return null;
      
      try {
        return JSON.parse(value);
      } catch {
        return value;
      }
    } catch (error) {
      SecureLogger.error(`Erro ao recuperar ${key}`, error.message);
      return null;
    }
  }

  /**
   * Remove dados
   * @param {string} key - Chave
   * @returns {boolean} Sucesso
   */
  remove(key) {
    try {
      localStorage.removeItem(this.prefix + key);
      SecureLogger.log(`Dados removidos: ${key}`, 'info');
      return true;
    } catch (error) {
      SecureLogger.error(`Erro ao remover ${key}`, error.message);
      return false;
    }
  }

  /**
   * Limpa todos os dados da aplicação
   * @returns {boolean} Sucesso
   */
  clear() {
    try {
      const keys = Object.keys(localStorage)
        .filter(key => key.startsWith(this.prefix));
      
      keys.forEach(key => localStorage.removeItem(key));
      SecureLogger.log(`${keys.length} itens removidos`, 'info');
      return true;
    } catch (error) {
      SecureLogger.error('Erro ao limpar dados', error.message);
      return false;
    }
  }

  /**
   * Lista todas as chaves armazenadas
   * @returns {array} Array de chaves
   */
  keys() {
    return Object.keys(localStorage)
      .filter(key => key.startsWith(this.prefix))
      .map(key => key.replace(this.prefix, ''));
  }
}

// ============================================================
// CLASSE: LOGGER SEGURO
// ============================================================

class SecureLogger {
  /**
   * Log genérico
   * @param {string} mensagem - Mensagem
   * @param {string} tipo - 'info', 'warn', 'error'
   */
  static log(mensagem, tipo = 'info') {
    const timestamp = new Date().toISOString();
    const logEntry = {
      timestamp,
      tipo,
      mensagem,
      url: window.location.href.split('?')[0]
    };

    // Apenas console em desenvolvimento (detecta localhost)
    if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
      console[tipo === 'error' ? 'error' : tipo === 'warn' ? 'warn' : 'log'](logEntry);
    }

    // Armazena localmente (máximo 50 entradas)
    try {
      let logs = JSON.parse(localStorage.getItem('icm_logs') || '[]');
      logs.push(logEntry);
      logs = logs.slice(-50);
      localStorage.setItem('icm_logs', JSON.stringify(logs));
    } catch (e) {
      // Falha silenciosa
    }
  }

  /**
   * Log de erro com mensagem genérica ao usuário
   * @param {string} mensagem - Mensagem técnica
   * @param {string} detalhe - Detalhes do erro
   */
  static error(mensagem, detalhe = null) {
    this.log(`ERRO: ${mensagem}${detalhe ? ' - ' + detalhe : ''}`, 'error');
    // Não expõe detalhes ao usuário
    alert('❌ Ocorreu um erro. Tente novamente mais tarde.');
  }

  /**
   * Log de aviso
   * @param {string} mensagem - Mensagem
   */
  static warn(mensagem) {
    this.log(`AVISO: ${mensagem}`, 'warn');
  }

  /**
   * Recupera logs armazenados
   * @param {number} limite - Número máximo de logs (padrão: 20)
   * @returns {array} Array de logs
   */
  static getLogs(limite = 20) {
    try {
      let logs = JSON.parse(localStorage.getItem('icm_logs') || '[]');
      return logs.slice(-limite);
    } catch (error) {
      return [];
    }
  }

  /**
   * Limpa todos os logs
   */
  static clearLogs() {
    try {
      localStorage.removeItem('icm_logs');
      this.log('Logs removidos', 'info');
    } catch (error) {
      // Falha silenciosa
    }
  }
}

// ============================================================
// VALIDADORES
// ============================================================

class Validadores {
  /**
   * Valida nome de membro
   * @param {string} nome - Nome a validar
   * @returns {string} Nome validado
   * @throws {Error} Se inválido
   */
  static validarNomeMembro(nome) {
    nome = nome.trim();

    if (nome.length < 2 || nome.length > 100) {
      throw new Error('Nome deve ter entre 2 e 100 caracteres');
    }

    // Permite apenas letras, números, espaços, hífens e apóstrofos
    if (!/^[a-záéíóúàâêôãõçñA-ZÁÉÍÓÚÀÂÊÔÃÕÇÑ\s\-']+$/.test(nome)) {
      throw new Error('Nome contém caracteres inválidos');
    }

    return nome;
  }

  /**
   * Valida email
   * @param {string} email - Email a validar
   * @returns {string} Email validado
   * @throws {Error} Se inválido
   */
  static validarEmail(email) {
    email = email.trim().toLowerCase();
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!regex.test(email)) {
      throw new Error('Email inválido');
    }

    return email;
  }

  /**
   * Valida comentário/texto
   * @param {string} texto - Texto a validar
   * @param {number} minCaracteres - Mínimo de caracteres
   * @param {number} maxCaracteres - Máximo de caracteres
   * @returns {string} Texto validado
   * @throws {Error} Se inválido
   */
  static validarTexto(texto, minCaracteres = 1, maxCaracteres = 500) {
    texto = texto.trim();

    if (texto.length < minCaracteres || texto.length > maxCaracteres) {
      throw new Error(`Texto deve ter entre ${minCaracteres} e ${maxCaracteres} caracteres`);
    }

    return texto;
  }

  /**
   * Valida data
   * @param {string} data - Data em formato YYYY-MM-DD
   * @returns {string} Data validada
   * @throws {Error} Se inválido
   */
  static validarData(data) {
    const regex = /^\d{4}-\d{2}-\d{2}$/;

    if (!regex.test(data)) {
      throw new Error('Data deve estar no formato YYYY-MM-DD');
    }

    const date = new Date(data);
    if (isNaN(date.getTime())) {
      throw new Error('Data inválida');
    }

    return data;
  }

  /**
   * Valida número
   * @param {*} numero - Número a validar
   * @param {number} minimo - Valor mínimo
   * @param {number} maximo - Valor máximo
   * @returns {number} Número validado
   * @throws {Error} Se inválido
   */
  static validarNumero(numero, minimo = 0, maximo = Infinity) {
    numero = Number(numero);

    if (isNaN(numero) || numero < minimo || numero > maximo) {
      throw new Error(`Número deve estar entre ${minimo} e ${maximo}`);
    }

    return numero;
  }
}

// ============================================================
// GERENCIADOR DE EXPORTAÇÕES SEGURO
// ============================================================

class ExportacaoSegura {
  /**
   * Pede confirmação antes de exportar dados sensíveis
   * @param {string} tipo - Tipo de exportação: 'pdf', 'csv', 'imagem'
   * @returns {boolean} Confirmação do usuário
   */
  static pedirConfirmacao(tipo) {
    const mensagens = {
      pdf: '📄 PDF - Será criado um arquivo PDF com os dados de frequência.',
      csv: '📊 CSV - Será criado um arquivo de planilha com os dados.',
      imagem: '🖼️ IMAGEM - Será capturada uma imagem da tela atual.'
    };

    const confirmacao = confirm(
      `⚠️ AVISO DE SEGURANÇA\n\n` +
      `${mensagens[tipo] || 'Operação de exportação'}\n\n` +
      `Certifique-se de que:\n` +
      `✓ Você tem direito de compartilhar esses dados\n` +
      `✓ Enviará APENAS para pessoas autorizadas\n` +
      `✓ Não salvará em locais públicos ou compartilhados\n\n` +
      `Deseja continuar?`
    );

    if (confirmacao) {
      SecureLogger.log(`Exportação aprovada: ${tipo}`, 'info');
    } else {
      SecureLogger.warn(`Exportação cancelada: ${tipo}`);
    }

    return confirmacao;
  }

  /**
   * Remove dados sensíveis antes de exportar
   * @param {array} dados - Dados a exportar
   * @param {array} camposRemover - Campos a remover (ex: ['email', 'telefone'])
   * @returns {array} Dados filtrados
   */
  static removerDadosSensiveis(dados, camposRemover = []) {
    if (!Array.isArray(dados)) return dados;

    return dados.map(item => {
      const copia = { ...item };
      camposRemover.forEach(campo => {
        delete copia[campo];
      });
      return copia;
    });
  }

  /**
   * Marca dados de exportação com timestamp
   * @param {*} dados - Dados a marcar
   * @returns {object} Dados com metadados
   */
  static adicionarMetadados(dados) {
    return {
      exportadoEm: new Date().toISOString(),
      navegador: navigator.userAgent.split('/')[0],
      url: window.location.href.split('?')[0],
      dados: dados
    };
  }
}

// ============================================================
// GERENCIADOR DE CONEXÃO
// ============================================================

class StatusConexao {
  /**
   * Verifica status de conexão
   * @returns {boolean} True se online
   */
  static isOnline() {
    return navigator.onLine;
  }

  /**
   * Adiciona listeners de conexão
   * @param {function} onOnline - Callback quando conecta
   * @param {function} onOffline - Callback quando desconecta
   */
  static monitorar(onOnline, onOffline) {
    window.addEventListener('online', () => {
      SecureLogger.log('Conexão estabelecida', 'info');
      if (onOnline) onOnline();
    });

    window.addEventListener('offline', () => {
      SecureLogger.warn('Sem conexão com internet');
      if (onOffline) onOffline();
    });
  }

  /**
   * Atualiza indicador visual de conexão
   * @param {string} selectorBarra - Seletor CSS da barra de status
   */
  static atualizarIndicador(selectorBarra) {
    const barra = document.querySelector(selectorBarra);
    if (!barra) return;

    const atualizar = () => {
      if (this.isOnline()) {
        barra.className = 'net-status-bar online';
        barra.textContent = '🟢 Conectado';
      } else {
        barra.className = 'net-status-bar offline';
        barra.textContent = '🟡 Sem conexão - Modo offline';
      }
    };

    atualizar();
    this.monitorar(atualizar, atualizar);
  }
}

// ============================================================
// INICIALIZAÇÃO
// ============================================================

// Cria instância global do storage
window.secureStorage = new SecureStorage();

// Log de inicialização
document.addEventListener('DOMContentLoaded', () => {
  SecureLogger.log('Security Fix Library carregada com sucesso', 'info');
});

// Monitora erros globais não capturados
window.addEventListener('error', (event) => {
  SecureLogger.error('Erro não tratado', event.message);
});

window.addEventListener('unhandledrejection', (event) => {
  SecureLogger.error('Promise rejeitada', event.reason);
});
