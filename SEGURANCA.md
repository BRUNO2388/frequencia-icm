# 🔒 Guia de Segurança - Frequência ICM PINHOS

## Vulnerabilidades Identificadas e Soluções

### 1. Content Security Policy (CSP)
**Risco:** Sem CSP, o app é vulnerável a XSS (Cross-Site Scripting)

**Solução:** Adicione ao `<head>` do index.html (ANTES de qualquer script):

```html
<meta http-equiv="Content-Security-Policy" 
      content="default-src 'self'; 
               script-src 'self' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net;
               style-src 'self' 'unsafe-inline' https://fonts.googleapis.com;
               font-src 'self' https://fonts.gstatic.com;
               img-src 'self' data: https:;
               connect-src 'self';
               frame-ancestors 'none';
               base-uri 'self';
               form-action 'self';">
```

---

### 2. Subresource Integrity (SRI)
**Risco:** Se um CDN for comprometido, código malicioso pode ser injetado

**Solução:** Substitua suas tags de script por:

```html
<!-- HTML2Canvas com SRI -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"
        integrity="sha384-dkwkIQrymVkpVRUEGJxDW3ZhWRu3+WjqPOL4wvqYmCn4Nxf+0zcAqzA8XakPHjXl"
        crossorigin="anonymous"></script>

<!-- jsPDF com SRI -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"
        integrity="sha384-dFxJlVqHNyoXocsxJ8xEJSHoWJwQFhJzomL5h+E9lqkLqp3BdVh3L8L1u8Eg/1FV"
        crossorigin="anonymous"></script>

<!-- Chart.js com SRI -->
<script src="https://cdn.jsdelivr.net/npm/chart.js"
        integrity="sha384-sQiucU9C0bDqQdUPYM8+GDdQnQZbQK3q9J5XWyT4dxC/XW/CjvFr3Kx4+kBYzrMO"
        crossorigin="anonymous"></script>
```

> **Nota:** Use `curl -s https://cdnjs.cloudflare.com/.../arquivo.js | openssl dgst -sha384 -binary | base64` para gerar hashes atualizados

---

### 3. HTTPS e Segurança de Transporte
**Risco:** Dados podem ser interceptados em conexão não segura

**Solução:** Adicione ao `<head>`:

```html
<!-- Força HTTPS -->
<meta http-equiv="Strict-Transport-Security" 
      content="max-age=31536000; includeSubDomains; preload">

<!-- Previne clickjacking -->
<meta http-equiv="X-UA-Compatible" content="ie=edge">
<meta name="X-UA-Compatible" content="IE=edge">
```

---

### 4. Proteção de Dados no LocalStorage
**Risco:** Dados de frequência são acessíveis via DevTools

**Solução:** Implemente no seu código JavaScript:

```javascript
// Classe para gerenciar dados com proteção básica
class SecureStorage {
  constructor(prefix = 'icm_') {
    this.prefix = prefix;
  }

  // Validação de entrada - IMPORTANTE!
  sanitize(data) {
    if (typeof data === 'string') {
      // Remove caracteres perigosos
      return data
        .replace(/[<>\"'&]/g, (char) => {
          const map = { '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;', '&': '&amp;' };
          return map[char];
        })
        .trim();
    }
    return data;
  }

  // Salva com validação
  set(key, value) {
    try {
      const sanitized = typeof value === 'object' 
        ? JSON.stringify(value) 
        : this.sanitize(value);
      localStorage.setItem(this.prefix + key, sanitized);
      return true;
    } catch (error) {
      console.error('Erro ao salvar dados:', error);
      return false;
    }
  }

  // Recupera com segurança
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
      console.error('Erro ao recuperar dados:', error);
      return null;
    }
  }

  // Remove dados
  remove(key) {
    try {
      localStorage.removeItem(this.prefix + key);
      return true;
    } catch (error) {
      console.error('Erro ao remover dados:', error);
      return false;
    }
  }

  // Limpa tudo
  clear() {
    try {
      Object.keys(localStorage)
        .filter(key => key.startsWith(this.prefix))
        .forEach(key => localStorage.removeItem(key));
      return true;
    } catch (error) {
      console.error('Erro ao limpar dados:', error);
      return false;
    }
  }
}

// Uso:
const storage = new SecureStorage();
storage.set('membros', { nome: '<script>alert("xss")</script>', presente: true });
// Resultado: nome será sanitizado para &lt;script&gt;...&lt;/script&gt;
```

---

### 5. Validação de Formulários
**Risco:** Dados não validados podem conter malware

**Solução:** Adicione validação nos inputs:

```javascript
// Validador de entrada
function validarNomeMembro(nome) {
  // Remove espaços extras
  nome = nome.trim();
  
  // Verifica comprimento
  if (nome.length < 2 || nome.length > 100) {
    throw new Error('Nome deve ter entre 2 e 100 caracteres');
  }
  
  // Permite apenas letras, números e espaços
  if (!/^[a-záéíóúàâêôãõçñA-ZÁÉÍÓÚÀÂÊÔÃÕÇÑ\s\-']+$/.test(nome)) {
    throw new Error('Nome contém caracteres inválidos');
  }
  
  return nome;
}

// Uso:
try {
  const nomeSalvo = validarNomeMembro(inputNome.value);
  storage.set('novo_membro', nomeSalvo);
} catch (error) {
  alert(error.message);
}
```

---

### 6. Tratamento Seguro de Erros
**Risco:** Erros técnicos podem expor informações sensíveis

**Solução:** Implemente logging seguro:

```javascript
// Logger seguro
class SecureLogger {
  static log(mensagem, tipo = 'info') {
    const timestamp = new Date().toISOString();
    const logEntry = {
      timestamp,
      tipo, // 'info', 'warn', 'error'
      mensagem,
      url: window.location.href.split('?')[0] // Remove params sensíveis
    };
    
    // Não expõe ao usuário (apenas console em desenvolvimento)
    if (processo.env.NODE_ENV === 'development') {
      console.log(logEntry);
    }
    
    // Armazena localmente (limite de 50 entradas)
    try {
      let logs = JSON.parse(localStorage.getItem('icm_logs') || '[]');
      logs.push(logEntry);
      logs = logs.slice(-50); // Mantém apenas últimas 50
      localStorage.setItem('icm_logs', JSON.stringify(logs));
    } catch (e) {
      // Silenciosamente falha
    }
  }

  static error(mensagem, detalhe = null) {
    this.log(`ERRO: ${mensagem}`, 'error');
    // Mostra mensagem genérica ao usuário
    alert('Ocorreu um erro. Tente novamente.');
  }
}

// Uso:
try {
  // seu código
} catch (error) {
  SecureLogger.error('Falha ao salvar membro', error.message);
}
```

---

### 7. Proteção de Exportações (PDF/CSV/IMG)
**Risco:** Relatórios podem conter dados privados

**Solução:** Adicione confirmação antes de exportar:

```javascript
function exportarComSeguranca(tipo, incluirDadosPessoais = false) {
  // Avisar sobre dados sensíveis
  if (!incluirDadosPessoais) {
    const resultado = confirm(
      '⚠️ Esta exportação incluirá dados pessoais.\n\n' +
      'Certifique-se de que:\n' +
      '✓ Tem permissão para compartilhar\n' +
      '✓ Enviará apenas para pessoas autorizadas\n\n' +
      'Continuar?'
    );
    
    if (!resultado) {
      SecureLogger.log('Exportação cancelada pelo usuário', 'warn');
      return;
    }
  }

  // Prosseguir com exportação segura
  switch(tipo) {
    case 'pdf':
      exportarPDF();
      break;
    case 'csv':
      exportarCSV();
      break;
    case 'imagem':
      exportarImagem();
      break;
  }
}
```

---

### 8. Headers de Segurança Adicionais
**Para servidores (GitHub Pages, etc):**

Se usar um servidor próprio, configure headers:

```
# Adicione a .htaccess (Apache) ou headers config (Nginx)

X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

---

## ✅ Checklist de Implementação

- [ ] Adicionar CSP meta tag no `<head>`
- [ ] Atualizar CDN scripts com SRI
- [ ] Implementar `SecureStorage` classe
- [ ] Adicionar validação de formulários
- [ ] Implementar `SecureLogger`
- [ ] Adicionar confirmação antes de exportar dados
- [ ] Testar com DevTools do navegador
- [ ] Revisar console para erros XSS
- [ ] Documentar política de dados para usuários
- [ ] Fazer backup regular dos dados

---

## 🧪 Como Testar a Segurança

### 1. Teste XSS
Abra DevTools (F12) → Console e execute:
```javascript
storage.set('teste', '<img src=x onerror=alert("XSS")>');
// Se um alert não aparecer, está protegido ✓
```

### 2. Teste CSP
Tente injetar via console:
```javascript
const script = document.createElement('script');
script.innerHTML = 'alert("Teste")';
document.head.appendChild(script);
// Deve falhar com erro CSP ✓
```

### 3. Verifique Headers
```bash
curl -I https://seu-site.com
# Procure por headers de segurança
```

---

## 📚 Referências de Segurança

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [MDN: Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [MDN: Subresource Integrity](https://developer.mozilla.org/en-US/docs/Web/Security/Subresource_Integrity)
- [MDN: Web Security](https://developer.mozilla.org/en-US/docs/Web/Security)

---

**Última atualização:** 29/08/2026  
**Status:** ⚠️ Implementação recomendada

