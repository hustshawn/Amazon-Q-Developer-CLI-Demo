const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const healthcheck = require('./healthcheck');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(bodyParser.urlencoded({ extended: false }));
app.use(bodyParser.json()); // Add JSON parser for AJAX requests
app.use(express.static(path.join(__dirname, 'public')));
app.set('view engine', 'ejs');

// Add cache control headers to prevent browser caching
app.use((req, res, next) => {
  res.set('Cache-Control', 'no-store');
  next();
});

// Health check endpoint
app.use('/health', healthcheck);

// In-memory storage for todos
let todos = [
  { id: 1, text: 'Learn Node.js', completed: false },
  { id: 2, text: 'Build a todo app', completed: false }
];

// Routes
// Home page - display todos
app.get('/', (req, res) => {
  res.render('index', { todos });
});

// Add a new todo
app.post('/todos', (req, res) => {
  const newTodo = {
    id: Date.now(),
    text: req.body.todoText,
    completed: false
  };

  todos.push(newTodo);
  
  // Check if the request expects JSON (AJAX request)
  if (req.xhr || req.headers.accept.indexOf('json') > -1) {
    // Return JSON response for AJAX requests
    res.json({ success: true, todo: newTodo });
  } else {
    // Redirect for traditional form submissions (fallback)
    res.redirect('/');
  }
});

// Toggle todo completion status
app.post('/todos/:id/toggle', (req, res) => {
  const id = parseInt(req.params.id);

  todos = todos.map(todo => {
    if (todo.id === id) {
      return { ...todo, completed: !todo.completed };
    }
    return todo;
  });

  // Check if the request expects JSON (AJAX request)
  if (req.xhr || req.headers.accept.indexOf('json') > -1) {
    // Return JSON response for AJAX requests
    res.json({ success: true });
  } else {
    // Redirect for traditional form submissions (fallback)
    res.redirect('/');
  }
});

// Delete a todo
app.post('/todos/:id/delete', (req, res) => {
  const id = parseInt(req.params.id);
  todos = todos.filter(todo => todo.id !== id);

  // Check if the request expects JSON (AJAX request)
  if (req.xhr || req.headers.accept.indexOf('json') > -1) {
    // Return JSON response for AJAX requests
    res.json({ success: true });
  } else {
    // Redirect for traditional form submissions (fallback)
    res.redirect('/');
  }
});

// Start server
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Server running on http://0.0.0.0:${PORT}`);
  console.log('Environment:', process.env.NODE_ENV);
  console.log('Available routes:');
  console.log('- / (GET): Home page');
  console.log('- /health (GET): Health check endpoint');
  console.log('- /todos (POST): Add new todo');
  console.log('- /todos/:id/toggle (POST): Toggle todo completion');
  console.log('- /todos/:id/delete (POST): Delete todo');
});
