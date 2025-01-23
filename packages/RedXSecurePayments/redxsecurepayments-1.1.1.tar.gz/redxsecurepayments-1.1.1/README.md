# RedXSecurePayments

A powerful Python package for processing secure payments using Stripe. Create payment links instantly and track payment status with ease.

## Installation

```bash
pip install RedXSecurePayments
```

## Quick Start

### Method 1: Using API Key Parameter (Recommended)
```python
from RedXSecurePayments import RedXSecureBuy

# Create a payment link using API key parameter
result = RedXSecureBuy(
    bank_name="Your Store",
    api_key="your_stripe_api_key",  # Your Stripe API key
    currency_amount=49.99,
    currency_type="usd"
)

if result['success']:
    print(f"Share this payment URL: {result['payment_url']}")
    print(f"Session ID: {result['session_id']}")
else:
    print(f"Error: {result['error']}")
```

### Method 2: Using Environment Variable
```python
from RedXSecurePayments import RedXSecureBuy
import os

# Set your Stripe API key as environment variable
os.environ['STRIPE_SECRET_KEY'] = 'your_stripe_api_key'

# Create a payment link using environment variable
result = RedXSecureBuy(
    bank_name="Your Store",
    currency_amount=49.99,
    currency_type="usd"
)

if result['success']:
    print(f"Share this payment URL: {result['payment_url']}")
    print(f"Session ID: {result['session_id']}")
else:
    print(f"Error: {result['error']}")
```

## Features

### 1. Create Payment Links
Create secure payment links with various options:
```python
result = RedXSecureBuy(
    bank_name="Your Store",
    api_key="your_stripe_api_key",  # Required (or use STRIPE_SECRET_KEY env var)
    currency_type="usd",        # Support for multiple currencies
    currency_amount=49.99,      # Amount to charge
    enable_multiple_payments=True,  # Allow multiple payments
    enable_custom_amount=True,      # Let customers modify amount
    enable_payment_history=True,    # Track payment history
    success_url="https://yoursite.com/success",  # Custom success URL
    cancel_url="https://yoursite.com/cancel"     # Custom cancel URL
)
```

### 2. Track Payment Status
Monitor payment status in real-time:
```python
from RedXSecurePayments import get_payment_status

# Using API key parameter
status = get_payment_status(
    session_id="session_id",
    api_key="your_stripe_api_key"  # Optional if STRIPE_SECRET_KEY env var is set
)

if status['success']:
    print(f"Payment Status: {status['status']}")
    print(f"Amount Paid: {status['amount_total']} {status['currency']}")
    if status['customer_email']:
        print(f"Customer Email: {status['customer_email']}")
```

### 3. Frontend Integration Example (React/TypeScript)
```typescript
import { useCreatePayment } from "./lib/payment";

function PaymentButton() {
  const createPayment = useCreatePayment();

  const handlePayment = async () => {
    try {
      const result = await createPayment.mutateAsync({
        amount: 49.99,
        currency: "usd",
        enableMultiplePayments: true,
        enableCustomAmount: true,
        enablePaymentHistory: true
      });

      // Redirect to payment URL
      if (result.url) {
        window.location.href = result.url;
      }
    } catch (error) {
      console.error("Payment creation failed:", error);
    }
  };

  return <button onClick={handlePayment}>Pay Now</button>;
}
```

### 4. Advanced Usage

#### Custom Success/Cancel URLs
```python
result = RedXSecureBuy(
    bank_name="Your Store",
    api_key="your_stripe_api_key",
    currency_amount=49.99,
    success_url="https://yoursite.com/success?session_id={CHECKOUT_SESSION_ID}",
    cancel_url="https://yoursite.com/cancel"
)
```

#### Payment Status Monitoring
```python
import time

def monitor_payment(session_id: str, api_key: str = None):
    while True:
        status = get_payment_status(session_id, api_key)
        if status['success']:
            if status['status'] == 'paid':
                print("Payment successful!")
                print(f"Amount: {status['amount_total']} {status['currency']}")
                break
            elif status['status'] == 'failed':
                print("Payment failed!")
                break
        time.sleep(5)  # Check every 5 seconds
```

## Testing

Use these test card numbers for development:
- Success: `4242 4242 4242 4242`
- Failure: `4000 0000 0000 0002`

For any test card:
- Any future expiration date
- Any 3-digit CVC
- Any postal code

## Important Notes

1. API Key Configuration:
   - Option 1: Pass API key directly to functions (recommended)
   ```python
   result = RedXSecureBuy(
       bank_name="Your Store",
       api_key="your_stripe_api_key",
       currency_amount=49.99
   )
   ```
   - Option 2: Set environment variable
   ```python
   import os
   os.environ['STRIPE_SECRET_KEY'] = 'your_stripe_api_key'
   result = RedXSecureBuy(bank_name="Your Store", currency_amount=49.99)
   ```

2. Error Handling
```python
result = RedXSecureBuy(...)
if not result['success']:
    error_message = result['error']
    # Handle error appropriately
```

3. Production vs Test Mode
- Use test API keys for development
- Switch to live API keys for production
- Test thoroughly before going live

## Security

- Never expose your Stripe secret key
- Always use HTTPS in production
- Keep your API keys secure
- Monitor payment activity regularly

## Support

For issues and feature requests, please visit our GitHub repository.

## License

MIT License - feel free to use in your projects!