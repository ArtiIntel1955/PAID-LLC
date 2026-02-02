# Stripe Integration Guide for PAID LLC Online Store

## Overview
This document provides step-by-step instructions to fully integrate Stripe payment processing into your online store, making it ready for real transactions.

## Prerequisites

### 1. Stripe Account Setup
1. Go to [https://stripe.com](https://stripe.com) and sign up for an account
2. Complete the account verification process
3. Navigate to Developers > API Keys in your Stripe Dashboard
4. Copy your Publishable key (starts with pk_) and Secret key (starts with sk_)

### 2. Required Information
- Business details (legal name, address, tax ID)
- Bank account information for payouts
- Valid email address

## Step-by-Step Integration

### Step 1: Update Your Store with Real Stripe Keys

1. Open `online_store_stripe.html` in your code editor
2. Find this line in the JavaScript section:
   ```javascript
   const stripe = Stripe('pk_test_YOUR_STRIPE_PUBLISHABLE_KEY_HERE');
   ```
3. Replace `'pk_test_YOUR_STRIPE_PUBLISHABLE_KEY_HERE'` with your actual publishable key from Stripe Dashboard
4. Save the file

### Step 2: Backend Server Setup

Stripe requires server-side processing for security. You'll need to set up a simple server to handle payment processing:

#### Option A: Node.js Server (Recommended)
Create a new file called `server.js`:

```javascript
const express = require('express');
const cors = require('cors');
const stripe = require('stripe')('sk_test_YOUR_SECRET_KEY_HERE'); // Replace with your secret key
const app = express();

app.use(cors());
app.use(express.json());

// Create a payment intent
app.post('/create-payment-intent', async (req, res) => {
  const { amount, currency = 'usd', items } = req.body;

  try {
    const paymentIntent = await stripe.paymentIntents.create({
      amount: Math.round(amount * 100), // Amount in cents
      currency: currency,
      metadata: {
        order_id: Date.now().toString(),
        items: JSON.stringify(items)
      }
    });

    res.send({
      clientSecret: paymentIntent.client_secret
    });
  } catch (error) {
    res.status(400).send({
      error: {
        message: error.message
      }
    });
  }
});

// Webhook endpoint to handle payment confirmation
app.post('/webhook', express.raw({type: 'application/json'}), (request, response) => {
  const sig = request.headers['stripe-signature'];
  const endpointSecret = 'whsec_YOUR_WEBHOOK_SECRET'; // Get this from Stripe Dashboard

  let event;

  try {
    event = stripe.webhooks.constructEvent(request.body, sig, endpointSecret);
  } catch (err) {
    console.log(`Webhook signature verification failed.`, err.message);
    return response.status(400).send(`Webhook Error: ${err.message}`);
  }

  // Handle the event
  switch (event.type) {
    case 'payment_intent.succeeded':
      const paymentIntent = event.data.object;
      console.log('Payment succeeded!', paymentIntent.id);
      // Fulfill the order here
      break;
    default:
      console.log(`Unhandled event type ${event.type}`);
  }

  response.json({received: true});
});

app.listen(3000, () => console.log('Server running on port 3000'));
```

#### Option B: PHP Server
Create a file called `process_payment.php`:

```php
<?php
require_once 'vendor/autoload.php';

\Stripe\Stripe::setApiKey('sk_test_YOUR_SECRET_KEY_HERE'); // Replace with your secret key

header('Content-Type: application/json');

$input = json_decode(file_get_contents('php://input'), true);

try {
    $payment_intent = \Stripe\PaymentIntent::create([
        'amount' => $input['amount'] * 100, // Amount in cents
        'currency' => $input['currency'] ?? 'usd',
        'metadata' => [
            'order_id' => time(),
            'items' => json_encode($input['items'])
        ]
    ]);

    echo json_encode(['clientSecret' => $payment_intent->client_secret]);
} catch (Exception $e) {
    http_response_code(400);
    echo json_encode(['error' => $e->getMessage()]);
}
?>
```

### Step 3: Update Frontend for Server Communication

Modify the payment processing function in your HTML file to communicate with your server:

```javascript
async function processPayment() {
    const email = document.getElementById('email').value;
    const name = document.getElementById('name').value;
    const totalAmount = cart.reduce((sum, item) => sum + item.price, 0);
    
    // Validate email
    if (!isValidEmail(email)) {
        document.getElementById('email-error').textContent = 'Please enter a valid email address';
        return;
    }
    
    // Disable the submit button
    const submitButton = document.getElementById('submit-button');
    const buttonText = document.getElementById('button-text');
    submitButton.disabled = true;
    buttonText.textContent = 'Processing...';

    try {
        // 1. Create payment intent on your server
        const response = await fetch('/create-payment-intent', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                amount: totalAmount,
                currency: 'usd',
                items: cart
            }),
        });

        const { clientSecret } = await response.json();

        // 2. Confirm payment with Stripe
        const { error, paymentIntent } = await stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: cardElement,
                billing_details: {
                    name: name,
                    email: email,
                },
            }
        });

        if (error) {
            console.error('Payment failed:', error);
            document.getElementById('card-errors').textContent = error.message;
            submitButton.disabled = false;
            buttonText.textContent = 'Pay Now';
        } else if (paymentIntent.status === 'succeeded') {
            // Payment succeeded - handle order fulfillment
            console.log('Payment succeeded:', paymentIntent.id);
            
            // Show success message
            document.getElementById('payment-success').style.display = 'block';
            
            // Reset cart
            cart = [];
            cartCount = 0;
            updateCartDisplay();
            
            // Send order confirmation email
            setTimeout(() => {
                closeCheckout();
                alert(`Thank you for your purchase, ${name}! You will receive an email with download links for your products shortly.`);
                
                // Reset form
                document.getElementById('email').value = '';
                document.getElementById('name').value = '';
                document.getElementById('company').value = '';
                document.getElementById('payment-success').style.display = 'none';
                submitButton.disabled = false;
                buttonText.textContent = 'Pay Now';
            }, 2000);
        }
    } catch (err) {
        console.error('Error processing payment:', err);
        document.getElementById('card-errors').textContent = 'An error occurred processing your payment. Please try again.';
        submitButton.disabled = false;
        buttonText.textContent = 'Pay Now';
    }
}
```

### Step 4: Set Up Webhooks for Payment Confirmation

1. In your Stripe Dashboard, go to Developers > Webhooks
2. Click "Add endpoint"
3. Enter your webhook URL (e.g., `https://yourdomain.com/webhook`)
4. Select events to listen to: `payment_intent.succeeded`, `payment_intent.payment_failed`
5. Copy the signing secret and add it to your server configuration

### Step 5: Product Fulfillment System

Create an order fulfillment system to deliver purchased products:

```javascript
// Example function to handle successful payments
function fulfillOrder(paymentIntentId, customerEmail, items) {
    // Send email with download links
    const downloadLinks = items.map(item => {
        return `https://yourdomain.com/downloads/${item.name.toLowerCase().replace(/\s+/g, '-')}.zip`;
    }).join('\n');
    
    // Send email to customer with download links
    sendEmail(customerEmail, {
        subject: 'Your PAID LLC Purchase - Download Links',
        body: `Thank you for your purchase!\n\nDownload your products:\n${downloadLinks}\n\nQuestions? Reply to this email.`
    });
    
    // Log the order
    logOrder(paymentIntentId, customerEmail, items);
}
```

### Step 6: Security Considerations

1. **Never expose secret keys in frontend code**
2. **Always validate amounts on the server side**
3. **Implement rate limiting to prevent abuse**
4. **Log all transactions for auditing**
5. **Use HTTPS for all payment-related pages**

### Step 7: Testing Before Going Live

1. Test with Stripe test cards:
   - Successful payment: 4242 4242 4242 4242
   - Declined payment: 4000 0000 0000 0002
   - Invalid CVC: 4000 0000 0000 0127

2. Test the complete flow:
   - Add items to cart
   - Enter payment details
   - Process payment
   - Receive confirmation
   - Access downloads

### Step 8: Going Live

1. Switch to live mode in Stripe Dashboard
2. Replace test keys with live keys
3. Update your domain settings
4. Monitor transactions closely during the first week

## Required Legal Pages

Before going live, ensure you have these legal pages:

1. **Privacy Policy** - How you collect and use customer data
2. **Terms of Service** - Rules governing purchases
3. **Refund Policy** - Conditions for returns
4. **Cookie Policy** - Information about cookies used

## Additional Features to Consider

1. **Subscription Options** - For recurring revenue
2. **Discount Codes** - Promotional offers
3. **Bulk Purchasing** - Volume discounts
4. **Gift Purchases** - Send products to others
5. **Progressive Web App** - Mobile-friendly experience

## Support & Troubleshooting

### Common Issues:
- Payment fails due to incorrect API keys
- CORS errors (solve with proper server setup)
- Webhook delivery failures
- Incorrect tax calculations

### Resources:
- Stripe Documentation: [https://stripe.com/docs](https://stripe.com/docs)
- Stripe Support: [https://support.stripe.com](https://support.stripe.com)
- Community forums for troubleshooting

## Going Forward

Once your payment system is operational, consider:

1. **Analytics** - Track conversion rates and sales
2. **Customer accounts** - Allow repeat customers to access purchases
3. **Inventory management** - Track digital product licenses
4. **Marketing automation** - Follow-up emails and upsells
5. **International expansion** - Multi-currency and localization

Your online store is now ready to accept real payments and deliver digital products to customers. Remember to thoroughly test the entire process before announcing to customers.