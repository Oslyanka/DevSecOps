const express = require('express');
const path = require('path');
const app = express();
const PORT = 8080;

app.use(express.urlencoded({ extended: true }));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public', 'index.html'));
});

// VULNERABILIDADE PROPOSITAL: sem validação/escape de input
app.post('/login', (req, res) => {
  const { username, password } = req.body || {};
  res.status(200).send(`
    <h1>Login recebido</h1>
    <p>Usuário: ${username || ''}</p>
    <p>Senha: ${password || ''}</p>
    <p>Obs: Este endpoint é propositalmente inseguro para fins educacionais.</p>
    <a href="/">Voltar</a>
  `);
});

app.get('/debug/info', (req, res) => {
  res.json({
    env: process.env.NODE_ENV || 'development',
    note: 'Endpoint propositalmente exposto para fins de demonstração'
  });
});

app.listen(PORT, () => {
  console.log(`ClickSeguro app rodando em http://localhost:${PORT}`);
});
