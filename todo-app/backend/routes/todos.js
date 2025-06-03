const express = require('express');
const router = express.Router();

// In-memory storage for todos
let todos = [
  { id: 1, text: 'Learn Node.js', completed: false },
  { id: 2, text: 'Build a todo app', completed: false }
];

// Get all todos
router.get('/', (req, res) => {
  res.json(todos);
});

// Add a new todo
router.post('/', (req, res) => {
  const newTodo = {
    id: Date.now(),
    text: req.body.text,
    completed: false
  };
  
  todos.push(newTodo);
  res.status(201).json(newTodo);
});

// Toggle todo completion status
router.put('/:id/toggle', (req, res) => {
  const id = parseInt(req.params.id);
  
  let updatedTodo = null;
  todos = todos.map(todo => {
    if (todo.id === id) {
      updatedTodo = { ...todo, completed: !todo.completed };
      return updatedTodo;
    }
    return todo;
  });
  
  if (updatedTodo) {
    res.json(updatedTodo);
  } else {
    res.status(404).json({ error: 'Todo not found' });
  }
});

// Delete a todo
router.delete('/:id', (req, res) => {
  const id = parseInt(req.params.id);
  const initialLength = todos.length;
  
  todos = todos.filter(todo => todo.id !== id);
  
  if (todos.length < initialLength) {
    res.status(204).end();
  } else {
    res.status(404).json({ error: 'Todo not found' });
  }
});

module.exports = router;
