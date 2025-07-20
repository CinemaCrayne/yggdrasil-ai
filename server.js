const express = require('express');
const path = require('path');

const app = express();
const port = process.env.PORT || 3000;

// Serve static files from `.well-known`
app.use('/.well-known', express.static(path.join(__dirname, '.well-known')));

app.get('/', (req, res) => res.send('Yggdrasil AI plugin is live!'));

app.listen(port, () => {
  console.log(`Server running on port ${port}`);
});
