const jwt = require('jsonwebtoken');

/**
 * Middleware to authenticate download tokens
 * Checks if the token is valid and hasn't exceeded download limits
 */
async function authenticateToken(req, res, next) {
  // For the download endpoint, the token comes from the URL parameter
  // But we'll also allow token in header for flexibility
  
  const token = req.params.token || req.query.token || req.headers['authorization']?.split(' ')[1];
  
  if (!token) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    // In this case, we're not using JWT decoding but checking against database
    // The verification happens in the database module
    const { verifyDownloadToken } = require('./database');
    const isValid = await verifyDownloadToken(token);

    if (!isValid) {
      return res.status(401).json({ error: 'Invalid or expired token' });
    }

    // Token is valid, proceed to next middleware/route handler
    req.token = token;
    next();
  } catch (error) {
    console.error('Authentication error:', error);
    res.status(500).json({ error: 'Authentication failed' });
  }
}

/**
 * Generate a secure download URL with token
 */
function generateDownloadUrl(token, productId) {
  return `${process.env.SERVER_URL || 'http://localhost:3000'}/download/${token}`;
}

/**
 * Validate if a token exists and is active
 */
async function validateToken(token) {
  try {
    const { verifyDownloadToken } = require('./database');
    return await verifyDownloadToken(token);
  } catch (error) {
    console.error('Token validation error:', error);
    return false;
  }
}

module.exports = {
  authenticateToken,
  generateDownloadUrl,
  validateToken
};