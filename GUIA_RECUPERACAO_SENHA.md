# 🔑 Guia Rápido - Recuperação de Senha

## 🚀 Como Usar

### Para Usuários

#### 1. Esqueceu a Senha?
1. Acesse a página de login: `http://localhost:8000/login.html`
2. Clique no link **"Esqueceu a senha?"**
3. Digite seu email cadastrado
4. Clique em **"Enviar Link de Recuperação"**

#### 2. Verifique o Email
- **Em Desenvolvimento:** O link aparece no console do servidor
- **Em Produção:** Você receberá um email com o link

#### 3. Redefina sua Senha
1. Clique no link recebido (ou copie do console)
2. Digite sua nova senha (mínimo 8 caracteres)
3. Confirme a nova senha
4. Clique em **"Redefinir Senha"**

#### 4. Faça Login
Use sua nova senha para acessar sua conta!

## 🎯 Acesso Rápido

### Páginas
- **Login:** http://localhost:8000/login.html
- **Esqueci Senha:** http://localhost:8000/forgot-password.html
- **Redefinir Senha:** http://localhost:8000/reset-password.html?token=SEU_TOKEN

### Endpoints API
```bash
# Solicitar recuperação
curl -X POST http://localhost:8000/api/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{"email": "seu@email.com"}'

# Redefinir senha
curl -X POST http://localhost:8000/api/password-reset-confirm/ \
  -H "Content-Type: application/json" \
  -d '{"token": "SEU_TOKEN", "password": "NovaSenha123"}'
```

## ✅ Requisitos de Senha

Sua nova senha deve ter:
- ✅ Mínimo de 8 caracteres
- ✅ Pelo menos uma letra MAIÚSCULA
- ✅ Pelo menos uma letra minúscula
- ✅ Pelo menos um número (0-9)

**Exemplos válidos:**
- `Senha123`
- `MinhaSenha2024`
- `BossShopp99`

**Exemplos inválidos:**
- `senha` (sem maiúscula e número)
- `SENHA123` (sem minúscula)
- `SenhaForte` (sem número)
- `Senha1` (menos de 8 caracteres)

## 🔍 Solução de Problemas

### "Link inválido ou expirado"
- O link expira em 1 hora
- Solicite um novo link em: http://localhost:8000/forgot-password.html

### "Email não recebido"
- **Em desenvolvimento:** Verifique o console do servidor
- **Em produção:** Verifique sua caixa de spam

### "Senha não atende aos requisitos"
- Verifique os indicadores visuais na página
- Certifique-se de ter maiúscula, minúscula e número

### "Token não encontrado"
- Certifique-se de copiar o link completo
- O token deve estar na URL: `?token=...`

## 📱 Demonstração Visual

### Página de Recuperação
```
┌─────────────────────────────────────┐
│         🔑 Esqueceu sua senha?      │
│                                     │
│  Digite seu email e enviaremos      │
│  instruções para redefinir          │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ 📧 Email                      │ │
│  │ usuario@email.com             │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  📤 Enviar Link de Recuperação│ │
│  └───────────────────────────────┘ │
│                                     │
│  ← Voltar para o login              │
└─────────────────────────────────────┘
```

### Página de Redefinição
```
┌─────────────────────────────────────┐
│         🔒 Redefinir Senha          │
│                                     │
│  Crie uma nova senha segura         │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ 🔐 Nova Senha                 │ │
│  │ ••••••••                      │ │
│  └───────────────────────────────┘ │
│                                     │
│  ┌───────────────────────────────┐ │
│  │ 🔐 Confirmar Senha            │ │
│  │ ••••••••                      │ │
│  └───────────────────────────────┘ │
│                                     │
│  Requisitos da senha:               │
│  ✅ Mínimo de 8 caracteres          │
│  ✅ Letra maiúscula                 │
│  ✅ Letra minúscula                 │
│  ✅ Número                          │
│                                     │
│  ┌───────────────────────────────┐ │
│  │  ✔️ Redefinir Senha           │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

## 🎨 Recursos Visuais

### Indicadores em Tempo Real
- 🔴 Vermelho: Requisito não atendido
- 🟢 Verde: Requisito atendido
- 👁️ Botão para mostrar/ocultar senha
- ⏱️ Feedback instantâneo

### Mensagens
- ✅ Sucesso: Verde com ícone de check
- ❌ Erro: Vermelho com ícone de alerta
- ℹ️ Info: Azul com ícone de informação

## 🔐 Segurança

### O que fazemos para proteger você:
- 🔒 Senhas criptografadas
- ⏰ Links expiram em 1 hora
- 🔑 Tokens únicos e aleatórios
- 🚫 Não revelamos se email existe
- ✅ Validação em múltiplas camadas

## 📞 Suporte

Problemas? Entre em contato:
- 📧 Email: suporte@bossshopp.com
- 💬 Chat: Disponível no site
- 📱 WhatsApp: (11) 99999-9999

---

**Última Atualização:** 03/12/2025  
**Versão:** 1.0
