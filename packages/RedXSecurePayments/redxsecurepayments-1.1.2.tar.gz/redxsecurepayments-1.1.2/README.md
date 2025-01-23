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
    currency_type="usd",
    enable_multiple_payments=True,  # Optional: Allow multiple payments
    enable_custom_amount=True,      # Optional: Let customers modify amount
    enable_payment_history=True     # Optional: Track payment history
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

## Payment Status Verification

You can check payment status using either method:

### Method 1: Using API Key Parameter (Recommended)
```python
from RedXSecurePayments import get_payment_status

status = get_payment_status(
    session_id="your_session_id",
    api_key="your_stripe_api_key"
)

if status['success']:
    print(f"Payment Status: {status['status']}")
    print(f"Amount: ${status['amount_total']} {status['currency']}")
    if status['customer_email']:
        print(f"Customer Email: {status['customer_email']}")
```

### Method 2: Using Environment Variable
```python
import os
from RedXSecurePayments import get_payment_status

os.environ['STRIPE_SECRET_KEY'] = 'your_stripe_api_key'

status = get_payment_status(session_id="your_session_id")

if status['success']:
    print(f"Payment Status: {status['status']}")
    print(f"Amount: ${status['amount_total']} {status['currency']}")
```

## Payment Status Monitoring Example
```python
import time
from RedXSecurePayments import get_payment_status

def monitor_payment(session_id: str, api_key: str = None):
    while True:
        status = get_payment_status(session_id, api_key)
        if status['success']:
            print(f"Status: {status['status']}")
            print(f"Amount: ${status['amount_total']} {status['currency']}")

            if status['status'] in ['paid', 'completed']:
                print("Payment successful!")
                break
            elif status['status'] == 'failed':
                print("Payment failed!")
                break

        time.sleep(5)  # Check every 5 seconds
```

## Features

- Direct API key support or environment variable configuration
- Real-time payment status tracking
- Support for multiple currencies
- Customizable payment options
- Detailed payment status information
- Error handling and status verification
- Payment history tracking
- Multiple payment support
- Custom amount support

## Testing

Use these test card numbers for development:
- Success: `4242 4242 4242 4242`
- Failure: `4000 0000 0000 0002`

For any test card:
- Any future expiration date
- Any 3-digit CVC
- Any postal code

## Error Handling

The package includes comprehensive error handling:

```python
from RedXSecurePayments import RedXSecureBuy, get_payment_status

# Creating payment
try:
    result = RedXSecureBuy(
        bank_name="Test Store",
        api_key="your_stripe_api_key",
        currency_amount=10.00
    )

    if not result['success']:
        print(f"Error creating payment: {result['error']}")
    else:
        session_id = result['session_id']

        # Checking status
        try:
            status = get_payment_status(
                session_id=session_id,
                api_key="your_stripe_api_key"
            )

            if status['success']:
                print(f"Payment Status: {status['status']}")
                print(f"Amount: ${status['amount_total']} {status['currency']}")
            else:
                print(f"Error checking status: {status['error']}")

        except Exception as e:
            print(f"Status check error: {str(e)}")

except Exception as e:
    print(f"Payment creation error: {str(e)}")
```

## Important Notes

1. API Key Configuration Options:
   - Option 1: Pass API key directly (recommended for better error tracking)
   - Option 2: Use environment variable 'STRIPE_SECRET_KEY'

2. Status Verification:
   - Always verify payment status before fulfilling orders
   - Use monitoring for real-time status updates
   - Handle all possible status values: 'unpaid', 'paid', 'failed', etc.

3. Security:
   - Never expose your Stripe secret key
   - Always use HTTPS in production
   - Keep your API keys secure
   - Monitor payment activity regularly

## Support

For issues and feature requests, please visit our GitHub repository.

## License

MIT License - feel free to use in your projects!