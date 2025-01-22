import os
import stripe
from flask import Flask, jsonify, request

app = Flask(__name__)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

def RedXSecureBuy(
    bank_name: str,
    currency_type: str = "usd",
    currency_amount: float = 10.0,
    enable_multiple_payments: bool = False,
    enable_custom_amount: bool = False,
    enable_payment_history: bool = False
):
    """
    Create a payment session that allows you to receive payments from customers.
    This function returns a payment URL that you can send to your customers.

    Args:
        bank_name (str): Your bank name for payment identification
        currency_type (str): Currency code (default: "usd")
        currency_amount (float): Amount to charge (default: 10.0)
        enable_multiple_payments (bool): Allow multiple payments if True (default: False)
        enable_custom_amount (bool): Allow custom payment amounts if True (default: False)
        enable_payment_history (bool): Enable payment history tracking if True (default: False)

    Returns:
        dict: Payment session information including the payment URL to share with customers
    """
    try:
        # Create a Stripe Checkout Session
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency_type.lower(),
                    'product_data': {
                        'name': f'Payment to {bank_name}',
                    },
                    'unit_amount': int(currency_amount * 100),
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:5000/payment/success',
            cancel_url='http://localhost:5000/payment/cancel',
            metadata={
                'bank_name': bank_name,
                'enable_multiple_payments': str(enable_multiple_payments),
                'enable_custom_amount': str(enable_custom_amount),
                'enable_payment_history': str(enable_payment_history)
            }
        )

        return {
            'success': True,
            'session_id': session.id,
            'payment_url': session.url,
            'amount': currency_amount,
            'currency': currency_type
        }

    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

def get_payment_status(session_id: str):
    """
    Check the status of a payment session.

    Args:
        session_id (str): The ID of the payment session

    Returns:
        dict: Payment status information
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {
            'success': True,
            'status': session.payment_status,
            'amount_total': session.amount_total / 100,  # Convert from cents
            'currency': session.currency
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }