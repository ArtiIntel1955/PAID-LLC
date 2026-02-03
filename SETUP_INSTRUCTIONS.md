# PAID-LLC Download System Setup Instructions

## Prerequisites
- Node.js (v14 or higher)
- Stripe account
- GitHub account (for syncing)

## Step 1: Sync with GitHub

1. Open command prompt/terminal in your workspace directory:
```bash
cd C:\Users\MyAIE\.openclaw\workspace
```

2. Initialize Git repository:
```bash
git init
```

3. Copy the `.gitignore` content:
```bash
echo "node_modules/
.env
*.log
.DS_Store
Thumbs.db
.vscode/
.idea/
dist/
build/" > .gitignore
```

4. Add all files and commit:
```bash
git add .
git commit -m "Initial commit: PAID-LLC products and download system"
```

5. Create a new repository on GitHub (go to https://github.com/new)
6. Link and push your local repository:
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git
git branch -M main
git push -u origin main
```

## Step 2: Set Up Stripe

1. Go to [Stripe Dashboard](https://dashboard.stripe.com/)
2. Navigate to Developers > Webhooks
3. Click "Add endpoint"
4. Enter your webhook URL: `https://yourdomain.com/webhook/stripe` (or `http://localhost:3000/webhook/stripe` for testing)
5. Select "Events to listen to" > "checkout.session.completed"
6. Click "Add endpoint"
7. Copy the "Signing secret" (starts with whsec_)

## Step 3: Install Dependencies

1. Navigate to the download_system directory:
```bash
cd download_system
```

2. Install dependencies:
```bash
npm install
```

## Step 4: Configure Environment Variables

1. Create a `.env` file in the `download_system` directory:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your values:
   - `STRIPE_SECRET_KEY`: Your Stripe secret key (starts with sk_live_ or sk_test_)
   - `STRIPE_WEBHOOK_SECRET`: The webhook signing secret from step 2
   - `SERVER_URL`: Your server URL (for production) or `http://localhost:3000` (for testing)

## Step 5: Test the System

1. Start the server:
```bash
npm start
```

2. The server will run on `http://localhost:3000`

## Step 6: Create Stripe Checkout Sessions

To create a checkout session, you'll need to implement this in your frontend or API:

```javascript
const stripe = require('stripe')(process.env.STRIPE_SECRET_KEY);

// Example of creating a checkout session
const session = await stripe.checkout.sessions.create({
  payment_method_types: ['card'],
  line_items: [{
    price_data: {
      currency: 'usd',
      product_data: {
        name: 'AI Implementation Guide',
        description: 'Complete Business Transformation Solution',
      },
      unit_amount: 12999, // $129.99 in cents
    },
    quantity: 1,
  }],
  metadata: {
    productId: 'ai_guide_001',
    productName: 'AI Implementation Guide'
  },
  mode: 'payment',
  success_url: 'https://yourwebsite.com/success',
  cancel_url: 'https://yourwebsite.com/cancel',
});
```

## Step 7: How Downloads Work

1. Customer completes purchase via Stripe
2. Stripe sends webhook to `/webhook/stripe` with payment confirmation
3. System stores purchase in database with a unique download token
4. Customer receives email with download link containing the token
5. Customer accesses `/download/TOKEN` to download their product
6. System verifies token validity and increments download counter
7. File is served as attachment to the customer

## Security Features

- Download tokens expire after 30 days
- Maximum of 5 downloads per token
- Rate limiting to prevent abuse
- Webhook signature verification
- Token-based authentication
- SQLite database for purchase records

## Production Deployment

For production, you'll need to:

1. Use a proper domain name instead of localhost
2. Set up SSL/TLS certificates
3. Use a production database (PostgreSQL/MongoDB) instead of SQLite
4. Set up reverse proxy (nginx/Apache) 
5. Configure environment variables securely
6. Set up monitoring and logging

## Troubleshooting

If downloads aren't working:
1. Check that webhook is properly configured in Stripe
2. Verify that `.env` file contains correct keys
3. Confirm that product PDF files exist in the correct paths
4. Check server logs for error messages

For webhook issues:
1. Use Stripe CLI for local testing: `stripe listen --forward-to localhost:3000/webhook/stripe`
2. Check webhook logs in Stripe Dashboard
3. Verify signing secret matches between Stripe and your .env file