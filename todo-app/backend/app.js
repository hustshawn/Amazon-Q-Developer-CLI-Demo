const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const path = require('path');
const healthcheck = require('./routes/healthcheck');
const todosRoutes = require('./routes/todos');

const app = express();
const PORT = process.env.PORT || 3001;

// Middleware
app.use(cors());
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

// Add cache control headers to prevent browser caching
app.use((req, res, next) => {
  res.set('Cache-Control', 'no-store');
  next();
});

// Routes
app.use('/health', healthcheck);
app.use('/api/todos', todosRoutes);

// Serve static files from the React frontend app in production
if (process.env.NODE_ENV === 'production') {
  // Serve any static files
  app.use(express.static(path.join(__dirname, '../frontend/build')));
  
  // Handle React routing, return all requests to React app
  app.get('*', function(req, res) {
    res.sendFile(path.join(__dirname, '../frontend/build', 'index.html'));
  });
}

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on http://0.0.0.0:${PORT}`);
  console.log('Environment:', process.env.NODE_ENV || 'development');
  console.log('Available routes:');
  console.log('- /health (GET): Health check endpoint');
  console.log('- /api/todos (GET): Get all todos');
  console.log('- /api/todos (POST): Add new todo');
  console.log('- /api/todos/:id/toggle (PUT): Toggle todo completion');
  console.log('- /api/todos/:id (DELETE): Delete todo');
});

module.exports = app;
