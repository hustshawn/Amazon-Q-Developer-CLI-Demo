import React from 'react';

function TodoItem({ todo, onToggle, onDelete }) {
  return (
    <li className={`todo-item ${todo.completed ? 'completed' : ''}`}>
      <span className="todo-text">{todo.text}</span>
      <div className="todo-actions">
        <button onClick={onToggle} className="btn-toggle">
          {todo.completed ? '↩️' : '✅'}
        </button>
        <button onClick={onDelete} className="btn-delete">
          🗑️
        </button>
      </div>
    </li>
  );
}

export default TodoItem;
