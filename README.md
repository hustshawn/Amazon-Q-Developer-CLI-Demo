# Amazon Q Developer CLI Demo

A demonstration repository for showcasing Amazon Q Developer CLI capabilities.

## Overview

This repository contains demo applications to demonstrate the features and capabilities of the Amazon Q Developer CLI. It includes multiple sample projects that you can use to test and explore Amazon Q's functionality.

## Projects

- **pacman-nibbles**: A simple Pacman-inspired game combining elements of classic Pacman and Snake
- **snake-game**: A classic snake game implementation with multiple difficulty levels
- **todo-app**: A modern todo application with React frontend and Express backend

## Prerequisites

- Python 3.8 or higher (for game projects)
- pip (Python package installer)
- Node.js and npm (for todo-app)
- Docker and Docker Compose (optional, for todo-app)

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/amazon-q-developer-cli-demo.git
cd amazon-q-developer-cli-demo
```

Each project has its own dependencies. Please refer to the project-specific README files for detailed installation instructions.

## Usage

Each project in this repository can be run separately. Navigate to the project directory and follow the instructions in the project-specific README.

### Running the Pacman Nibbles Game

```bash
cd pacman-nibbles
# Install dependencies
pip install pygame
# Run the game
python pacman_nibbles.py
```

### Running the Snake Game

```bash
cd snake-game
# Install dependencies
pip install pygame
# Run the game
python snake_game.py
```

### Running the Todo App

#### Using Docker Compose (Recommended)

```bash
cd todo-app
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:3001/api/todos

#### Running Frontend and Backend Separately

Please refer to the todo-app's README.md for detailed instructions on running the frontend and backend separately.

## Development

### Python Game Projects Requirements

The game projects require:
- Python 3.8 or higher
- Pygame library

### Setting Up Python Development Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install pygame
```

### Todo App Development Requirements

The todo-app requires:
- Node.js 14 or higher
- npm 6 or higher
- Docker and Docker Compose (optional)

Please refer to the todo-app's README.md for detailed development setup instructions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
