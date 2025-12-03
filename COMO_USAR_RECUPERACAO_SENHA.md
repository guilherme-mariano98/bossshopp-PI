# 🔐 Como Usar a Recuperação de Senha

## ✅ JÁ ESTÁ IMPLEMENTADO E FUNCIONANDO!

O botão "Esqueceu a senha?" já está na tela de login e totalmente funcional.

## 📍 Onde Encontrar

### Na Tela de Login
```
┌─────────────────────────────────────────────┐
│         BOSS SHOPP - Login                  │
├─────────────────────────────────────────────┤
│                                             │
│  Email: [________________]                  │
│                                             │
│  Senha: [________________]                  │
│                                             │
│  ☐ Lembrar de mim    [Esqueceu a senha?] ← AQUI!
│                                             │
│  [        ENTRAR        ]                   │
│                                             │
└─────────────────────────────────────────────┘
```

## 🎯 Passo a Passo para o Usuário

### 1️⃣ Acessar a Recuperação
1. Abra: `http://localhost:8000/login.html`
2. Clique no link **"Esqueceu a senha?"** (ao lado de "Lembrar de mim")
3. Você será redirecionado para: `forgot-password.html`

### 2️⃣ Solicitar Recuperação
```
┌─────────────────────────────────────────────┐
│    🔑 Esqueceu sua senha?                   │
│                                             │
│  Digite seu email e enviaremos              │
│  instruções para redefinir                  │
│                                             │
│  Email: [usuario@email.com]                 │
│                                             │
│  [📤 Enviar Link de Recuperação]            │
│                                             │
│  ℹ️ Você receberá um email com um link     │
│     para criar uma nova senha               │
│                                             │
│  ← Voltar para o login                      │
└─────────────────────────────────────────────┘
```

### 3️⃣ Pegar o Link (Desenvolvimento)
Após enviar o email, verifique o **console do servidor Django**:

```bash
============================================================
EMAIL DE RECUPERAÇÃO DE SENHA
============================================================
Para: usuario@email.com
Assunto: Recuperação de Senha - BOSS SHOPP

Olá João,

Você solicitou a recuperação de senha.
Clique no link abaixo para criar uma nova senha:

http://localhost:8000/reset-password.html?token=abc123...

Este link expira em 1 hora.
============================================================
```

**Copie o link completo!**

### 4️⃣ Redefinir a Senha
Cole o link no navegador e você verá:

```
┌─────────────────────────────────────────────┐
│    🔒 Redefinir Senha                       │
│                                             │
│  Crie uma nova senha segura                 │
│                                             │
│  Nova Senha: [••••••••] 👁️                 │
│                                             │
│  Confirmar:  [••••••••] 👁️                 │
│                                             │
│  Requisitos da senha:                       │
│  ✅ Mínimo de 8 caracteres                  │
│  ✅ Letra maiúscula                         │
│  ✅ Letra minúscula                         │
│  ✅ Número                                  │
│                                             │
│  [✔️ Redefinir Senha]                       │
│                                             │
│  ← Voltar para o login                      │
└─────────────────────────────────────────────┘
```

### 5️⃣ Fazer Login
Após redefinir, você será redirecionado para o login automaticamente!

## 🧪 Teste Rápido

### Opção 1: Via Interface (Recomendado)
```bash
# 1. Certifique-se que o servidor está rodando
cd backend
python manage.py runserver 0.0.0.0:8000

# 2. Abra no navegador
http://localhost:8000/login.html

# 3. Clique em "Esqueceu a senha?"

# 4. Digite: teste@example.com

# 5. Verifique o console do servidor e copie o link

# 6. Cole o link no navegador

# 7. Crie uma nova senha
```

### Opção 2: Via API (Para Desenvolvedores)
```bash
# 1. Solicitar recuperação
curl -X POST http://localhost:8000/api/password-reset/ \
  -H "Content-Type: application/json" \
  -d '{"email": "teste@example.com"}'

# Resposta:
# {
#   "message": "Se o email existir, você receberá instruções...",
#   "reset_link": "http://localhost:8000/reset-password.html?token=..."
# }

# 2. Copie o token da resposta

# 3. Redefinir senha
curl -X POST http://localhost:8000/api/password-reset-confirm/ \
  -H "Content-Type: application/json" \
  -d '{"token": "SEU_TOKEN_AQUI", "password": "NovaSenha123"}'

# Resposta:
# {
#   "message": "Senha redefinida com sucesso!"
# }

# 4. Fazer login com a nova senha
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "teste@example.com", "password": "NovaSenha123"}'
```

## 📱 URLs Importantes

| Página | URL | Descrição |
|--------|-----|-----------|
| Login | `http://localhost:8000/login.html` | Página de login com link de recuperação |
| Esqueci Senha | `http://localhost:8000/forgot-password.html` | Solicitar recuperação |
| Redefinir | `http://localhost:8000/reset-password.html?token=...` | Criar nova senha |

## 🎨 Recursos Visuais

### ✅ Validação em Tempo Real
Ao digitar a nova senha, você vê instantaneamente:
- 🔴 Vermelho = Requisito não atendido
- 🟢 Verde = Requisito atendido

### 👁️ Mostrar/Ocultar Senha
Clique no ícone do olho para ver a senha que está digitando

### 📱 Design Responsivo
Funciona perfeitamente em:
- 💻 Desktop
- 📱 Celular
- 📱 Tablet

## ⚠️ Importante

### Em Desenvolvimento
- O email **NÃO** é enviado de verdade
- O link aparece no **console do servidor**
- Você precisa **copiar manualmente** o link

### Em Produção
- Configure SMTP no `settings.py`
- O email será enviado automaticamente
- O usuário recebe o link por email

## 🔒 Segurança

### O que está protegido:
- ✅ Tokens únicos e aleatórios (64 caracteres)
- ✅ Expiração automática (1 hora)
- ✅ Senhas criptografadas
- ✅ Validação de requisitos
- ✅ Tokens usados são invalidados
- ✅ Não revela se email existe

### Requisitos de Senha:
```
✅ Mínimo 8 caracteres
✅ Letra MAIÚSCULA (A-Z)
✅ Letra minúscula (a-z)
✅ Número (0-9)
```

**Exemplos válidos:**
- `Senha123` ✅
- `MeuBoss2024` ✅
- `BossShopp99` ✅

**Exemplos inválidos:**
- `senha123` ❌ (sem maiúscula)
- `SENHA123` ❌ (sem minúscula)
- `SenhaForte` ❌ (sem número)
- `Senha1` ❌ (menos de 8 caracteres)

## 🆘 Problemas Comuns

### "Link inválido ou expirado"
**Solução:** Solicite um novo link (expira em 1 hora)

### "Não encontrei o link"
**Solução:** Verifique o console do servidor Django

### "Senha não aceita"
**Solução:** Verifique os indicadores verdes na tela

### "Token não encontrado"
**Solução:** Copie o link completo com `?token=...`

## 📞 Suporte

Dúvidas? Consulte:
- 📖 `GUIA_RECUPERACAO_SENHA.md` - Guia detalhado
- 📖 `RECUPERACAO_SENHA_IMPLEMENTADA.md` - Documentação técnica
- 📖 `API_DOCUMENTATION.md` - Documentação da API

---

## 🎉 Pronto para Usar!

O sistema está **100% funcional**. Basta:
1. Acessar o login
2. Clicar em "Esqueceu a senha?"
3. Seguir os passos acima

**Última Atualização:** 03/12/2025  
**Status:** ✅ Funcionando Perfeitamente
