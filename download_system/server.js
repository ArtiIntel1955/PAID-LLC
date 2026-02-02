const express = require('express');
const cors = require('cors');
const path = require('path');
const fs = require('fs');
const rateLimit = require('express-rate-limit');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 3000;

// Rate limiting
const limiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 100 // limit each IP to 100 requests per windowMs
});

app.use(limiter);
app.use(cors());
app.use(express.json());

// Import database and auth modules
const { 
  addPurchase, 
  verifyDownloadToken, 
  getPurchaseByToken 
} = require('./database');
const { authenticateToken } = require('./auth');

// Serve static files (optional for frontend)
app.use('/static', express.static(path.join(__dirname, 'public')));
app.use(express.static(path.join(__dirname, 'public'))); // Serve index.html at root

// Create checkout session
app.post('/create-checkout-session', async (req, res) => {
  try {
    const { productId, productName, price } = req.body;
    
    // Validate input
    if (!productId || !productName || !price) {
      return res.status(400).json({ error: 'Missing required fields' });
    }
    
    const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
    
    const session = await stripe.checkout.sessions.create({
      payment_method_types: ['card'],
      line_items: [{
        price_data: {
          currency: 'usd',
          product_data: {
            name: productName,
            description: `Digital product: ${productName}`,
          },
          unit_amount: price, // Amount in cents
        },
        quantity: 1,
      }],
      metadata: {
        productId: productId,
        productName: productName
      },
      mode: 'payment',
      success_url: `${process.env.SERVER_URL || 'http://localhost:3000'}/success?session_id={CHECKOUT_SESSION_ID}`,
      cancel_url: `${process.env.SERVER_URL || 'http://localhost:3000'}/cancel`,
    });
    
    res.json({ id: session.id });
  } catch (error) {
    console.error('Error creating checkout session:', error);
    res.status(500).json({ error: error.message });
  }
});

// Get download token by session ID (for success page)
app.get('/api/download-token/:sessionId', async (req, res) => {
  try {
    const { sessionId } = req.params;
    
    const { getDownloadTokenBySessionId } = require('./database');
    const result = await getDownloadTokenBySessionId(sessionId);
    
    if (result) {
      res.json({ 
        token: result.token,
        customerEmail: result.customerEmail,
        productName: result.productName
      });
    } else {
      res.status(404).json({ error: 'Download token not found for this session' });
    }
  } catch (error) {
    console.error('Error getting download token:', error);
    res.status(500).json({ error: error.message });
  }
});

// Stripe webhook endpoint (will be called by Stripe)
app.post('/webhook/stripe', express.raw({type: 'application/json'}), async (req, res) => {
  const sig = req.headers['stripe-signature'];
  const endpointSecret = process.env.STRIPE_WEBHOOK_SECRET;

  let event;

  try {
    const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);
    event = stripe.webhooks.constructEvent(req.body, sig, endpointSecret);
  } catch (err) {
    console.error(`Webhook signature verification failed: ${err.message}`);
    return res.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Handle the event
  switch (event.type) {
    case 'checkout.session.completed':
      const session = event.data.object;
      
      // Extract customer information
      const customerId = session.customer;
      const customerEmail = session.customer_details.email;
      const productId = session.metadata.productId || session.id;
      const productName = session.metadata.productName || 'Unknown Product';
      
      // Create download token
      const downloadToken = generateDownloadToken();
      
      // Store purchase in database
      await addPurchase({
        customerId,
        customerEmail,
        productId,
        productName,
        sessionId: session.id,
        amount: session.amount_total,
        currency: session.currency,
        downloadToken,
        createdAt: new Date()
      });

      console.log(`Purchase recorded for ${customerEmail}, product: ${productName}`);
      break;
    default:
      console.log(`Unhandled event type ${event.type}`);
  }

  res.json({ received: true });
});

// Generate download token
function generateDownloadToken() {
  const crypto = require('crypto');
  return crypto.randomBytes(32).toString('hex');
}

// Download endpoint - requires valid token
app.get('/download/:token', authenticateToken, async (req, res) => {
  try {
    const token = req.params.token;
    
    // Verify token and get purchase info
    const isValid = await verifyDownloadToken(token);
    if (!isValid) {
      return res.status(401).json({ error: 'Invalid or expired download token' });
    }

    // Get purchase details
    const purchase = await getPurchaseByToken(token);
    if (!purchase) {
      return res.status(401).json({ error: 'Purchase not found' });
    }

    // Map product names to file paths
    const productToFileMap = {
      'AI Implementation Guide': '../projects/current/PAID-LLC/products/AI_IMPLEMENTATION_GUIDE/AI_Implementation_Guide.pdf',
      'Cybersecurity Essentials': '../projects/current/PAID-LLC/products/CYBERSECURITY_ESSENTIALS/Cybersecurity_Essentials.pdf',
      'Business Strategy Toolkit': '../projects/current/PAID-LLC/products/BUSINESS_STRATEGY_TOOLKIT/Business_Strategy_Toolkit.pdf',
      'Process Optimization Course': '../projects/current/PAID-LLC/products/PROCESS_OPTIMIZATION_COURSE/Process_Optimization_Course.pdf',
      'Digital Transformation Playbook': '../projects/current/PAID-LLC/products/DIGITAL_TRANSFORMATION_PLAYBOOK/Digital_Transformation_Playbook.pdf',
      'Analytics Dashboard Template': '../projects/current/PAID-LLC/products/ANALYTICS_DASHBOARD_TEMPLATE/Analytics_Dashboard_Template.pdf'
    };

    const filePath = productToFileMap[purchase.productName];
    
    if (!filePath) {
      return res.status(404).json({ error: 'Product file not found' });
    }

    // Check if file exists
    if (!fs.existsSync(filePath)) {
      console.error(`File not found: ${filePath}`);
      return res.status(404).json({ error: 'Product file not found' });
    }

    // Log download
    console.log(`Download initiated for ${purchase.customerEmail}, product: ${purchase.productName}`);

    // Set headers for file download
    res.setHeader('Content-Type', 'application/pdf');
    res.setHeader('Content-Disposition', `attachment; filename="${purchase.productName.replace(/\s+/g, '_')}.pdf"`);

    // Stream the file
    const fileStream = fs.createReadStream(filePath);
    fileStream.pipe(res);

    fileStream.on('error', (err) => {
      console.error('File stream error:', err);
      res.status(500).json({ error: 'Error reading file' });
    });

  } catch (error) {
    console.error('Download error:', error);
    res.status(500).json({ error: 'Download failed' });
  }
});

// Verification endpoint - to check if token is valid without downloading
app.get('/verify/:token', authenticateToken, async (req, res) => {
  try {
    const token = req.params.token;
    const isValid = await verifyDownloadToken(token);
    
    if (isValid) {
      const purchase = await getPurchaseByToken(token);
      res.json({ 
        valid: true, 
        purchase: {
          productName: purchase.productName,
          customerEmail: purchase.customerEmail
        }
      });
    } else {
      res.json({ valid: false });
    }
  } catch (error) {
    console.error('Verification error:', error);
    res.status(500).json({ error: 'Verification failed' });
  }
});

// Health check endpoint
app.get('/', (req, res) => {
  res.json({ status: 'Download server is running', timestamp: new Date().toISOString() });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({ error: 'Something went wrong!' });
});

// 404 handler
app.use('*', (req, res) => {
  res.status(404).json({ error: 'Route not found' });
});

app.listen(PORT, () => {
  console.log(`Download server running on port ${PORT}`);
  console.log(`Webhook endpoint: http://localhost:${PORT}/webhook/stripe`);
  console.log(`Download endpoint: http://localhost:${PORT}/download/:token`);
});

module.exports = app;