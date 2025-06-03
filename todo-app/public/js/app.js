document.addEventListener('DOMContentLoaded', function () {
  const todoForm = document.getElementById('todoForm');
  const todoInput = document.getElementById('todoInput');
  const todoList = document.querySelector('.todo-list');

  // Function to handle form submission for adding new todos
  todoForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const todoText = todoInput.value.trim();
    if (!todoText) return;
    
    fetch('/todos', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({ todoText })
    })
    .then(response => response.json())
    .then(data => {
      if (data.success && data.todo) {
        // Remove empty state if it exists
        const emptyState = todoList.querySelector('.empty-state');
        if (emptyState) {
          emptyState.remove();
        }
        
        // Create new todo item
        const todoItem = document.createElement('li');
        todoItem.className = 'todo-item';
        todoItem.innerHTML = `
          <span class="todo-text">${data.todo.text}</span>
          <div class="todo-actions">
            <form action="/todos/${data.todo.id}/toggle" method="POST" class="inline-form">
              <button type="submit" class="btn-toggle">✅</button>
            </form>
            <form action="/todos/${data.todo.id}/delete" method="POST" class="inline-form">
              <button type="submit" class="btn-delete">🗑️</button>
            </form>
          </div>
        `;
        
        todoList.appendChild(todoItem);
        todoInput.value = '';
      }
    })
    .catch(error => {
      console.error('Error:', error);
    });
  });

  // Function to handle toggle action
  function handleToggle(id, button) {
    fetch(`/todos/${id}/toggle`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          const todoItem = button.closest('.todo-item');
          todoItem.classList.toggle('completed');
          button.textContent = todoItem.classList.contains('completed') ? '↩️' : '✅';
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  // Function to handle delete action
  function handleDelete(id, button) {
    fetch(`/todos/${id}/delete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      }
    })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          const todoItem = button.closest('.todo-item');
          todoItem.remove();

          // If no todos left, show empty state
          if (todoList.children.length === 0) {
            const emptyState = document.createElement('li');
            emptyState.className = 'empty-state';
            emptyState.textContent = 'No todos yet! Add one above.';
            todoList.appendChild(emptyState);
          }
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  // Add event delegation for toggle and delete buttons
  todoList.addEventListener('click', function (e) {
    const toggleBtn = e.target.closest('.btn-toggle');
    const deleteBtn = e.target.closest('.btn-delete');

    if (toggleBtn) {
      e.preventDefault();
      const form = toggleBtn.closest('form');
      const id = form.action.split('/').slice(-2)[0];
      handleToggle(id, toggleBtn);
    } else if (deleteBtn) {
      e.preventDefault();
      const form = deleteBtn.closest('form');
      const id = form.action.split('/').slice(-2)[0];
      handleDelete(id, deleteBtn);
    }
  });
});
