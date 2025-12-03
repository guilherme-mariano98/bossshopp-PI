# 🚀 Deploy Rápido - BOSS SHOPP no Render

## ⚡ Passos Rápidos (5 minutos)

### 1. Enviar para GitHub
```bash
cd "PI3 (2) (1)/PI3 (2)/PI3 (1)/PI3/PI2"
git add .
git commit -m "Deploy Render"
git push
```

### 2. Acessar Render
👉 https://render.com
- Faça login com GitHub
- Autorize o acesso

### 3. Criar Web Service
1. Clique **"New +"** → **"Web Service"**
2. Selecione: **guilherme-mariano98/bossshopp-PI**
3. Configure:

```
Name: bossshopp
Region: Frankfurt
Branch: main (ou master)
Root Directory: (deixe vazio)
Runtime: Python 3

Build Command:
cd backend && chmod +x build.sh && ./build.sh

Start Command:
cd backend && gunicorn boss_shopp.wsgi:application --bind 0.0.0.0:$PORT

Instance Type: Free
```

4. **Advanced** → Adicionar variáveis:
   - `PYTHON_VERSION` = `3.11.9`
   - `DEBUG` = `false`

5. Clique **"Create Web Service"**

### 4. Aguardar Deploy
⏱️ 5-10 minutos

### 5. Acessar Site
```
https://bossshopp.onrender.com
```

## 🎯 Pronto!

Seu site está online! 🌍

---

⚠️ **Importante:** 
- Plano gratuito "dorme" após 15 min sem uso
- Primeiro acesso pode levar 30-60 segundos
- Dados SQLite são perdidos a cada deploy (use PostgreSQL para persistência)

📖 **Guia Completo:** Veja `DEPLOY_RENDER.md`
