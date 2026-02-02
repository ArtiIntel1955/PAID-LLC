/**
 * Stripe Webhook Handler
 * 
 * This file contains functions to test and verify the webhook functionality
 * In production, Stripe will call the webhook endpoint directly
 */

const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

/**
 * Function to simulate webhook verification (for testing)
 */
function verifyWebhookSignature(payload, signature, secret) {
  const crypto = require('crypto');
  const expectedSignature = crypto
    .createHmac('sha256', secret)
    .update(payload, 'utf8')
    .digest('hex');
  
  const expectedSignatureWithPrefix = `v0=${expectedSignature}`;
  
  // Use constant-time comparison to prevent timing attacks
  return crypto.timingSafeEqual(
    Buffer.from(signature),
    Buffer.from(expectedSignatureWithPrefix)
  );
}

/**
 * Function to process a checkout.session.completed event
 */
async function processCheckoutCompleted(session) {
  console.log('Processing checkout session:', session.id);
  
  // Extract relevant information
  const purchaseData = {
    customerId: session.customer,
    customerEmail: session.customer_details?.email || session.customer_email,
    productId: session.metadata?.productId || session.id,
    productName: session.metadata?.productName || 'Unknown Product',
    sessionId: session.id,
    amount: session.amount_total,
    currency: session.currency,
    createdAt: new Date()
  };
  
  console.log('Purchase data extracted:', purchaseData);
  
  // Generate a secure download token
  const crypto = require('crypto');
  const downloadToken = crypto.randomBytes(32).toString('hex');
  purchaseData.downloadToken = downloadToken;
  
  // Store in database
  const { addPurchase } = require('./database');
  try {
    await addPurchase(purchaseData);
    console.log(`Purchase recorded successfully for ${purchaseData.customerEmail}`);
    
    // In a real implementation, you might want to send a confirmation email
    // await sendConfirmationEmail(purchaseData);
    
    return { success: true, downloadToken };
  } catch (error) {
    console.error('Error recording purchase:', error);
    throw error;
  }
}

/**
 * Function to retrieve webhook signing secret from Stripe
 * This would typically be done during setup
 */
async function retrieveWebhookDetails() {
  try {
    // Retrieve webhook endpoints from Stripe
    const endpoints = await stripe.webhookEndpoints.list();
    console.log('Configured webhook endpoints:');
    endpoints.data.forEach(endpoint => {
      console.log(`- ${endpoint.url}: ${endpoint.enabled_events.join(', ')}`);
    });
    
    return endpoints;
  } catch (error) {
    console.error('Error retrieving webhook details:', error);
    throw error;
  }
}

/**
 * Helper function to create a webhook endpoint in Stripe (during setup)
 */
async function createWebhookEndpoint() {
  try {
    const endpoint = await stripe.webhookEndpoints.create({
      url: `${process.env.SERVER_URL || 'http://localhost:3000'}/webhook/stripe`,
      enabled_events: [
        'checkout.session.completed',
      ],
      description: 'PAID-LLC Download System Webhook'
    });
    
    console.log(`Webhook endpoint created: ${endpoint.url}`);
    console.log(`Signing secret: ${endpoint.secret} (store this securely!)`);
    
    return endpoint;
  } catch (error) {
    console.error('Error creating webhook endpoint:', error);
    throw error;
  }
}

/**
 * Simulate receiving a webhook event (for testing)
 */
async function simulateWebhookEvent(eventType, eventData) {
  const event = {
    type: eventType,
    data: {
      object: eventData
    }
  };
  
  switch (eventType) {
    case 'checkout.session.completed':
      return await processCheckoutCompleted(eventData);
    default:
      console.log(`Unhandled event type: ${eventType}`);
      return { success: false, error: `Unhandled event type: ${eventType}` };
  }
}

module.exports = {
  verifyWebhookSignature,
  processCheckoutCompleted,
  retrieveWebhookDetails,
  createWebhookEndpoint,
  simulateWebhookEvent
};

// Example usage:
if (require.main === module) {
  // This would run if the file is executed directly
  console.log('Stripe webhook handler functions loaded.');
  console.log('Use these functions to set up and test your webhook.');
}