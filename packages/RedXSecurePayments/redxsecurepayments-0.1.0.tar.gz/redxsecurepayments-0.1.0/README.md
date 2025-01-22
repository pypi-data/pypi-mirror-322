# RedXSecurePayments

A Python package for processing payments using Stripe. This library helps you create payment links that you can share with your customers to receive payments.

## Quick Installation

```bash
pip install git+https://github.com/RedXSecurePayments/RedXSecurePayments.git
```

Or add to your requirements.txt:
```
git+https://github.com/RedXSecurePayments/RedXSecurePayments.git
```

## Basic Usage

```python
from RedXSecurePayments import RedXSecureBuy

# Create a payment link
result = RedXSecureBuy(
    bank_name="Your Store Name",
    currency_type="usd",
    currency_amount=49.99,
    enable_multiple_payments=True,
    enable_custom_amount=True,
    enable_payment_history=True
)

if result['success']:
    print(f"Payment URL: {result['payment_url']}")
    print(f"Amount: ${result['amount']} {result['currency'].upper()}")
    print(f"Session ID: {result['session_id']}")
else:
    print(f"Error: {result['error']}")

# Check payment status later
from RedXSecurePayments import get_payment_status
status = get_payment_status(result['session_id'])
if status['success']:
    print(f"Payment Status: {status['status']}")
```

## Important: Set Your Stripe API Key

Before using the package, set your Stripe API key as an environment variable:

```bash
export STRIPE_SECRET_KEY='your_stripe_secret_key'
```

Or in your Python code (not recommended for production):
```python
import os
os.environ['STRIPE_SECRET_KEY'] = 'your_stripe_secret_key'
```

## Usage

First, make sure to set up your Stripe account and get your API keys from the Stripe Dashboard.


Then use the library to create payment sessions:

```python
from RedXSecurePayments import RedXSecureBuy

# Create a payment session
result = RedXSecureBuy(
    bank_name="Your Bank Name",  # Your bank name for identification
    currency_type="usd",         # Currency code
    currency_amount=10.0,        # Amount to charge
    enable_multiple_payments=True,  # Allow customers to make multiple payments
    enable_custom_amount=True,      # Let customers modify the payment amount
    enable_payment_history=True     # Track payment history
)

if result['success']:
    # Share this URL with your customer
    payment_url = result['payment_url']
    print(f"Share this payment link with your customer: {payment_url}")

    # You can also check the payment status later using the session ID
    session_id = result['session_id']
else:
    print(f"Error: {result['error']}")

# Check payment status
from RedXSecurePayments import get_payment_status

status = get_payment_status(session_id)
if status['success']:
    print(f"Payment status: {status['status']}")
    print(f"Amount: {status['amount_total']} {status['currency']}")
```

## Features
- Generate payment links to receive payments
- Support for multiple currencies
- Configurable payment options:
  - Multiple payment support
  - Custom amount support
  - Payment history tracking
- Payment status checking
- Secure payment processing through Stripe

## Important Notes
- You need a Stripe account to use this library
- Set your success_url and cancel_url in the RedXSecureBuy function to your actual website URLs
- Always keep your Stripe secret key secure and never share it
- Test thoroughly in Stripe's test mode before going live

## Testing the Payment System

When testing payments, use these Stripe test card numbers:

- Success payment: 4242 4242 4242 4242
- Failed payment: 4000 0000 0000 0002

For any test card:
- Use any future date for expiry
- Any 3-digit CVC
- Any postal code

Remember: Test mode is completely separate from live mode. No real charges will be made while testing.