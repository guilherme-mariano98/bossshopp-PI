# 🚀 Deploy do BOSS SHOPP no Render

## 📋 Pré-requisitos

1. Conta no GitHub (você já tem)
2. Conta no Render (gratuita) - https://render.com

## 🔧 Passo a Passo

### 1️⃣ Fazer Push para o GitHub

Primeiro, vamos enviar todas as alterações para o GitHub:

```bash
cd "PI3 (2) (1)/PI3 (2)/PI3 (1)/PI3/PI2"

git add .
git commit -m "Preparado para deploy no Render"
git push origin main
```

Se der erro, tente:
```bash
git push origin master
```

### 2️⃣ Criar Conta no Render

1. Acesse: https://render.com
2. Clique em **"Get Started"**
3. Faça login com sua conta do GitHub
4. Autorize o Render a acessar seus repositórios

### 3️⃣ Criar Novo Web Service

1. No dashboard do Render, clique em **"New +"**
2. Selecione **"Web Service"**
3. Conecte seu repositório: **guilherme-mariano98/bossshopp-PI**
4. Clique em **"Connect"**

### 4️⃣ Configurar o Web Service

Preencha os campos:

**Name:** `bossshopp` (ou qualquer nome que preferir)

**Region:** `Frankfurt (EU Central)` ou `Oregon (US West)`

**Branch:** `main` (ou `master` se for o caso)

**Root Directory:** `backend`

**Runtime:** `Python 3`

**Build Command:**
```bash
pip install -r requirements.txt && python manage.py collectstatic --no-input && python manage.py migrate && python populate_data.py
```

**Start Command:**
```bash
gunicorn boss_shopp.wsgi:application
```

**Instance Type:** `Free`

### 5️⃣ Variáveis de Ambiente

Clique em **"Advanced"** e adicione as seguintes variáveis:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `DEBUG` | `False` |
| `SECRET_KEY` | (Render vai gerar automaticamente) |

### 6️⃣ Criar Banco de Dados PostgreSQL (Opcional)

Se quiser usar PostgreSQL em vez de SQLite:

1. No dashboard, clique em **"New +"**
2. Selecione **"PostgreSQL"**
3. Preencha:
   - **Name:** `bossshopp-db`
   - **Database:** `bossshopp`
   - **User:** `bossshopp`
   - **Region:** (mesma do web service)
   - **Instance Type:** `Free`
4. Clique em **"Create Database"**
5. Copie a **Internal Database URL**
6. Volte ao Web Service e adicione a variável:
   - **Key:** `DATABASE_URL`
   - **Value:** (cole a URL copiada)

### 7️⃣ Deploy

1. Clique em **"Create Web Service"**
2. Aguarde o deploy (pode levar 5-10 minutos)
3. Quando terminar, você verá: ✅ **"Live"**

### 8️⃣ Acessar o Site

Seu site estará disponível em:
```
https://bossshopp.onrender.com
```

Ou o nome que você escolheu:
```
https://SEU-NOME.onrender.com
```

## 🔐 Criar Superusuário

Após o deploy, você precisa criar um usuário admin:

1. No dashboard do Render, vá até seu Web Service
2. Clique na aba **"Shell"**
3. Execute:
```bash
python manage.py createsuperuser
```

4. Preencha:
   - Username: `admin`
   - Email: `admin@bossshopp.com`
   - Password: (escolha uma senha segura)

## 📱 Acessar o Admin

```
https://SEU-SITE.onrender.com/admin
```

## ⚠️ Notas Importantes

### Plano Gratuito do Render:
- ✅ 750 horas/mês gratuitas
- ✅ SSL automático (HTTPS)
- ⚠️ O site "dorme" após 15 minutos de inatividade
- ⚠️ Primeiro acesso após dormir pode levar 30-60 segundos

### SQLite vs PostgreSQL:
- **SQLite:** Mais simples, mas dados são perdidos a cada deploy
- **PostgreSQL:** Recomendado para produção, dados persistem

## 🔄 Atualizações Automáticas

Toda vez que você fizer push para o GitHub, o Render vai:
1. Detectar as mudanças
2. Fazer rebuild automático
3. Atualizar o site

## 🐛 Troubleshooting

### Site não carrega:
1. Verifique os logs no dashboard do Render
2. Procure por erros em vermelho
3. Verifique se todas as variáveis de ambiente estão corretas

### Erro 500:
1. Verifique se `DEBUG=False`
2. Verifique se `ALLOWED_HOSTS` está configurado
3. Veja os logs para detalhes

### Arquivos estáticos não carregam:
1. Verifique se `collectstatic` rodou no build
2. Verifique se WhiteNoise está instalado
3. Limpe o cache do navegador

## 📞 Suporte

- Documentação Render: https://render.com/docs
- Documentação Django: https://docs.djangoproject.com

## 🎉 Pronto!

Seu e-commerce BOSS SHOPP está online e acessível para o mundo todo! 🌍

---

**Última Atualização:** 2025-12-03
