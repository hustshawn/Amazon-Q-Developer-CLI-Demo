import React, { useState, useEffect } from 'react';
import TodoForm from './components/TodoForm';
import TodoList from './components/TodoList';
import './App.css';

// Use environment variable with fallback for local development
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3001/api';

function App() {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      console.log('Fetching todos from:', `${API_URL}/todos`);
      const response = await fetch(`${API_URL}/todos`);
      if (!response.ok) {
        throw new Error('Failed to fetch todos');
      }
      const data = await response.json();
      console.log('Fetched todos:', data);
      setTodos(data);
      setError(null);
    } catch (err) {
      setError('Failed to load todos. Please try again later.');
      console.error('Error fetching todos:', err);
    } finally {
      setLoading(false);
    }
  };

  const addTodo = async (text) => {
    try {
      console.log('Adding todo:', text);
      const response = await fetch(`${API_URL}/todos`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      });
      
      if (!response.ok) {
        throw new Error('Failed to add todo');
      }
      
      const newTodo = await response.json();
      console.log('Added todo:', newTodo);
      setTodos([...todos, newTodo]);
    } catch (err) {
      setError('Failed to add todo. Please try again.');
      console.error('Error adding todo:', err);
    }
  };

  const toggleTodo = async (id) => {
    try {
      console.log('Toggling todo:', id);
      const response = await fetch(`${API_URL}/todos/${id}/toggle`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      
      if (!response.ok) {
        throw new Error('Failed to toggle todo');
      }
      
      const updatedTodo = await response.json();
      console.log('Toggled todo:', updatedTodo);
      setTodos(
        todos.map(todo => 
          todo.id === id ? { ...todo, completed: updatedTodo.completed } : todo
        )
      );
    } catch (err) {
      setError('Failed to update todo. Please try again.');
      console.error('Error toggling todo:', err);
    }
  };

  const deleteTodo = async (id) => {
    try {
      console.log('Deleting todo:', id);
      const response = await fetch(`${API_URL}/todos/${id}`, {
        method: 'DELETE',
      });
      
      if (!response.ok && response.status !== 204) {
        throw new Error('Failed to delete todo');
      }
      
      console.log('Deleted todo:', id);
      setTodos(todos.filter(todo => todo.id !== id));
    } catch (err) {
      setError('Failed to delete todo. Please try again.');
      console.error('Error deleting todo:', err);
    }
  };

  return (
    <div className="container">
      <h1>Todo App</h1>
      
      {error && <div className="error-message">{error}</div>}
      
      <TodoForm onAddTodo={addTodo} />
      
      {loading ? (
        <div className="loading">Loading...</div>
      ) : (
        <TodoList 
          todos={todos} 
          onToggleTodo={toggleTodo} 
          onDeleteTodo={deleteTodo} 
        />
      )}
    </div>
  );
}

export default App;
