/**
 * Sistema de Autenticação Seguro - Frequência ICM PINHOS
 * Implementa login com proteção de dados
 */

// ============================================================
// CLASSE: GERENCIADOR DE AUTENTICAÇÃO
// ============================================================

class AuthManager {
  constructor() {
    this.sessionKey = 'icm_session_token';
    this.sessionDuration = 24 * 60 * 60 * 1000; // 24 horas em ms
    this.isAuthenticated = this.checkSession();
    this.showAuthModalIfNeeded();
  }

  /**
   * Hash simples para senha (proteção básica para client-side)
   */
  hashPassword(password) {
    let hash = 0;
    for (let i = 0; i < password.length; i++) {
      const char = password.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Converte para 32-bit integer
    }
    return Math.abs(hash).toString(16);
  }

  /**
   * Retorna o HASH esperado referente à senha "Icm.123"
   */
  getExpectedPasswordHash() {
    return 'b1ecfe18';
  }

  /**
   * Verifica se existe sessão ativa
   */
  checkSession() {
    try {
      const session = localStorage.getItem(this.sessionKey);
      if (!session) return false;

      const sessionData = JSON.parse(session);
      const now = new Date().getTime();

      // Verifica se sessão expirou
      if (now > sessionData.expiresAt) {
        this.logout();
        return false;
      }

      return true;
    } catch (error) {
      console.error('Erro ao verificar sessão:', error);
      return false;
    }
  }

  /**
   * Realiza login com validação do hash
   */
  login(password) {
    try {
      const expectedHash = this.getExpectedPasswordHash();
      const inputPasswordHash = this.hashPassword(password);

      if (inputPasswordHash !== expectedHash) {
        return {
          success: false,
          message: '❌ Senha incorreta!'
        };
      }

      // Cria sessão
      const sessionData = {
        token: this.generateToken(),
        loginTime: new Date().getTime(),
        expiresAt: new Date().getTime() + this.sessionDuration,
        userAgent: navigator.userAgent
      };

      localStorage.setItem(
        this.sessionKey,
        JSON.stringify(sessionData)
      );

      this.isAuthenticated = true;
      if (typeof SecureLogger !== 'undefined') {
        SecureLogger.log('Autenticação realizada com sucesso', 'info');
      }

      return {
        success: true,
        message: '✅ Bem-vindo ao app de frequência!'
      };
    } catch (error) {
      if (typeof SecureLogger !== 'undefined') {
        SecureLogger.error('Erro no login', error.message);
      }
      return {
        success: false,
        message: '❌ Erro ao fazer login. Tente novamente.'
      };
    }
  }

  /**
   * Gera token aleatório para sessão
   */
  generateToken() {
    return 'token_' + Math.random().toString(36).substr(2, 9) +
           '_' + new Date().getTime();
  }

  /**
   * Realiza logout
   */
  logout() {
    try {
      localStorage.removeItem(this.sessionKey);
      this.isAuthenticated = false;
      if (typeof SecureLogger !== 'undefined') {
        SecureLogger.log('Logout realizado', 'info');
      }
      window.location.reload();
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
    }
  }

  /**
   * Exibe modal de autenticação se necessário
   */
  showAuthModalIfNeeded() {
    if (!this.isAuthenticated) {
      this.showAuthModal();
    }
  }

  /**
   * Cria e exibe modal de login
   */
  showAuthModal() {
    // Remove modal anterior se existir
    const existingModal = document.getElementById('auth-modal');
    if (existingModal) existingModal.remove();

    const modal = document.createElement('div');
    modal.id = 'auth-modal';
    modal.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background: rgba(0, 0, 0, 0.7);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 99999;
      backdrop-filter: blur(4px);
    `;

    modal.innerHTML = `
      <div style="
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        max-width: 400px;
        width: 90%;
        animation: slideIn 0.3s ease-out;
      ">
        <div style="text-align: center; margin-bottom: 25px;">
          <h1 style="color: #2d6a4f; margin: 0 0 8px 0; font-size: 24px;">
            🔒 Frequência ICM
          </h1>
          <p style="color: #666; margin: 0; font-size: 14px;">
            Digite a senha para acessar
          </p>
        </div>

        <div id="auth-message" style="
          display: none;
          padding: 12px;
          border-radius: 8px;
          margin-bottom: 15px;
          font-size: 14px;
          font-weight: bold;
        "></div>

        <input
          type="password"
          id="auth-password-input"
          placeholder="Senha de acesso"
          autocorrect="off"
          autocapitalize="none"
          spellcheck="false"
          autocomplete="off"
          style="
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
            box-sizing: border-box;
            margin-bottom: 15px;
            transition: border-color 0.2s;
          "
          onkeypress="if(event.key === 'Enter') document.getElementById('auth-btn').click()"
          onfocus="this.style.borderColor='#2d6a4f'"
          onblur="this.style.borderColor='#ddd'"
        />

        <button
          id="auth-btn"
          style="
            width: 100%;
            padding: 12px;
            background: #2d6a4f;
            color: white;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: background 0.2s;
          "
          onmouseover="this.style.background='#1f513b'"
          onmouseout="this.style.background='#2d6a4f'"
          onclick="authManager.handleLogin()"
        >
          ACESSAR
        </button>

        <p style="
          text-align: center;
          margin-top: 15px;
          font-size: 12px;
          color: #999;
        ">
          ⚠️ Este app contém dados sensíveis
        </p>
      </div>

      <style>
        @keyframes slideIn {
          from {
            opacity: 0;
            transform: translateY(-20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      </style>
    `;

    document.body.appendChild(modal);

    // Focus no input automaticamente
    setTimeout(() => {
      document.getElementById('auth-password-input').focus();
    }, 100);
  }

  /**
   * Processa tentativa de login
   */
  handleLogin() {
    const passwordInput = document.getElementById('auth-password-input');
    // Remove qualquer espaço inserido automaticamente pelo teclado virtual
    const password = passwordInput.value.replace(/\s+/g, '');
    const messageDiv = document.getElementById('auth-message');

    if (!password) {
      messageDiv.style.display = 'block';
      messageDiv.style.background = '#ffebee';
      messageDiv.style.color = '#b71c1c';
      messageDiv.textContent = '⚠️ Digite a senha';
      return;
    }

    const result = this.login(password);

    if (result.success) {
      messageDiv.style.display = 'block';
      messageDiv.style.background = '#e8f5e9';
      messageDiv.style.color = '#1b5e20';
      messageDiv.textContent = result.message;

      setTimeout(() => {
        const modal = document.getElementById('auth-modal');
        if (modal) modal.remove();
        this.isAuthenticated = true;
        // Recarrega a página para inicializar os elementos da interface
        window.location.reload();
      }, 500);
    } else {
      messageDiv.style.display = 'block';
      messageDiv.style.background = '#ffebee';
      messageDiv.style.color = '#b71c1c';
      messageDiv.textContent = result.message;
      passwordInput.value = '';
      passwordInput.focus();
    }
  }

  /**
   * Adiciona botão de logout na interface
   */
  addLogoutButton() {
    if (this.isAuthenticated) {
      const logoutBtn = document.createElement('button');
      logoutBtn.textContent = '🚪 Sair';
      logoutBtn.style.cssText = `
        position: fixed;
        top: 15px;
        left: 15px;
        padding: 8px 15px;
        background: #ef5350;
        color: white;
        border: none;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: bold;
        cursor: pointer;
        z-index: 100;
        transition: all 0.2s ease;
      `;

      logoutBtn.onmouseover = function() {
        this.style.background = '#c62828';
        this.style.transform = 'translateY(-1px)';
      };

      logoutBtn.onmouseout = function() {
        this.style.background = '#ef5350';
        this.style.transform = 'translateY(0)';
      };

      logoutBtn.onclick = () => this.logout();

      document.body.appendChild(logoutBtn);
    }
  }

  /**
   * Verifica inatividade e faz logout automático
   */
  setupInactivityTimer() {
    let inactivityTimeout;

    const resetTimer = () => {
      clearTimeout(inactivityTimeout);
      
      inactivityTimeout = setTimeout(() => {
        if (this.isAuthenticated) {
          if (typeof SecureLogger !== 'undefined') {
            SecureLogger.warn('Sessão expirada por inatividade');
          }
          this.logout();
        }
      }, this.sessionDuration);
    };

    // Monitora atividade do usuário
    ['mousedown', 'keydown', 'scroll', 'touchstart', 'click'].forEach(event => {
      document.addEventListener(event, resetTimer, true);
    });

    resetTimer();
  }
}

// ============================================================
// INICIALIZAÇÃO
// ============================================================

let authManager;

document.addEventListener('DOMContentLoaded', () => {
  // Aguarda carregamento do security-fix.js
  if (typeof SecureLogger !== 'undefined') {
    authManager = new AuthManager();
    authManager.addLogoutButton();
    authManager.setupInactivityTimer();
  } else {
    setTimeout(() => {
      authManager = new AuthManager();
      authManager.addLogoutButton();
      authManager.setupInactivityTimer();
    }, 500);
  }
});
