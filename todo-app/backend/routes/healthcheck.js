// Enhanced health check endpoint for ECS
const express = require('express');
const router = express.Router();

router.get('/', (req, res) => {
  console.log('Health check requested at:', new Date().toISOString());
  
  // Always return success for health checks
  res.status(200).json({
    status: 'ok',
    timestamp: new Date().toISOString(),
    message: 'Todo app is healthy',
    environment: process.env.NODE_ENV || 'development'
  });
});

module.exports = router;
