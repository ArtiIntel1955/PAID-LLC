const sqlite3 = require('sqlite3').verbose();
const path = require('path');

// Initialize database
const dbPath = path.join(__dirname, 'purchases.db');
const db = new sqlite3.Database(dbPath);

// Create purchases table if it doesn't exist
db.serialize(() => {
  db.run(`
    CREATE TABLE IF NOT EXISTS purchases (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      customerId TEXT NOT NULL,
      customerEmail TEXT NOT NULL,
      productId TEXT NOT NULL,
      productName TEXT NOT NULL,
      sessionId TEXT UNIQUE NOT NULL,
      amount INTEGER,
      currency TEXT DEFAULT 'usd',
      downloadToken TEXT UNIQUE NOT NULL,
      downloadCount INTEGER DEFAULT 0,
      maxDownloads INTEGER DEFAULT 5,
      expiresAt DATETIME,
      createdAt DATETIME DEFAULT CURRENT_TIMESTAMP,
      updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  // Create indexes for better performance
  db.run(`CREATE INDEX IF NOT EXISTS idx_customer_email ON purchases(customerEmail)`);
  db.run(`CREATE INDEX IF NOT EXISTS idx_download_token ON purchases(downloadToken)`);
  db.run(`CREATE INDEX IF NOT EXISTS idx_session_id ON purchases(sessionId)`);
});

/**
 * Add a new purchase record
 */
function addPurchase(purchaseData) {
  return new Promise((resolve, reject) => {
    // Set expiration date (30 days from purchase)
    const expiresAt = new Date();
    expiresAt.setDate(expiresAt.getDate() + 30);

    const stmt = db.prepare(`
      INSERT INTO purchases 
      (customerId, customerEmail, productId, productName, sessionId, amount, currency, downloadToken, expiresAt)
      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    `);

    stmt.run([
      purchaseData.customerId,
      purchaseData.customerEmail,
      purchaseData.productId,
      purchaseData.productName,
      purchaseData.sessionId,
      purchaseData.amount,
      purchaseData.currency,
      purchaseData.downloadToken,
      expiresAt.toISOString()
    ], function(err) {
      if (err) {
        console.error('Error adding purchase:', err);
        reject(err);
      } else {
        console.log(`Purchase added with ID: ${this.lastID}`);
        resolve(this.lastID);
      }
    });

    stmt.finalize();
  });
}

/**
 * Verify if a download token is valid and hasn't expired
 */
function verifyDownloadToken(token) {
  return new Promise((resolve, reject) => {
    const sql = `
      SELECT downloadCount, maxDownloads, expiresAt, downloadToken
      FROM purchases 
      WHERE downloadToken = ? AND expiresAt > datetime('now')
    `;

    db.get(sql, [token], (err, row) => {
      if (err) {
        console.error('Error verifying token:', err);
        reject(err);
      } else if (!row) {
        // Token doesn't exist or has expired
        resolve(false);
      } else {
        // Check if download limit has been reached
        if (row.downloadCount >= row.maxDownloads) {
          console.log(`Download limit reached for token: ${token}`);
          resolve(false);
        } else {
          resolve(true);
        }
      }
    });
  });
}

/**
 * Get purchase details by token
 */
function getPurchaseByToken(token) {
  return new Promise((resolve, reject) => {
    const sql = `
      SELECT *
      FROM purchases 
      WHERE downloadToken = ? AND expiresAt > datetime('now')
    `;

    db.get(sql, [token], async (err, row) => {
      if (err) {
        console.error('Error getting purchase:', err);
        reject(err);
      } else if (!row) {
        resolve(null);
      } else {
        // Increment download count
        await incrementDownloadCount(token);
        resolve(row);
      }
    });
  });
}

/**
 * Increment download count for a purchase
 */
async function incrementDownloadCount(token) {
  return new Promise((resolve, reject) => {
    const stmt = db.prepare(`
      UPDATE purchases 
      SET downloadCount = downloadCount + 1, updatedAt = datetime('now')
      WHERE downloadToken = ?
    `);

    stmt.run([token], function(err) {
      if (err) {
        console.error('Error incrementing download count:', err);
        reject(err);
      } else {
        console.log(`Download count incremented for token: ${token}`);
        resolve(this.changes);
      }
    });

    stmt.finalize();
  });
}

/**
 * Get download token by session ID
 */
function getDownloadTokenBySessionId(sessionId) {
  return new Promise((resolve, reject) => {
    const sql = `
      SELECT downloadToken, customerEmail, productName
      FROM purchases 
      WHERE sessionId = ? AND expiresAt > datetime('now')
    `;

    db.get(sql, [sessionId], (err, row) => {
      if (err) {
        console.error('Error getting download token by session ID:', err);
        reject(err);
      } else if (!row) {
        resolve(null);
      } else {
        resolve({
          token: row.downloadToken,
          customerEmail: row.customerEmail,
          productName: row.productName
        });
      }
    });
  });
}

/**
 * Clean up expired records (run periodically)
 */
function cleanupExpiredRecords() {
  return new Promise((resolve, reject) => {
    const stmt = db.prepare(`
      DELETE FROM purchases 
      WHERE expiresAt < datetime('now')
    `);

    stmt.run(function(err) {
      if (err) {
        console.error('Error cleaning up records:', err);
        reject(err);
      } else {
        console.log(`Cleaned up ${this.changes} expired records`);
        resolve(this.changes);
      }
    });

    stmt.finalize();
  });
}

// Cleanup expired records every 24 hours
setInterval(async () => {
  try {
    await cleanupExpiredRecords();
  } catch (error) {
    console.error('Cleanup error:', error);
  }
}, 24 * 60 * 60 * 1000); // 24 hours

module.exports = {
  addPurchase,
  verifyDownloadToken,
  getPurchaseByToken,
  getDownloadTokenBySessionId,
  cleanupExpiredRecords
};