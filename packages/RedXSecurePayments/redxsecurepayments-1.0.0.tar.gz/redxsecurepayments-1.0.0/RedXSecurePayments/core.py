import os
import stripe
from flask import Flask, jsonify, request
from typing import Dict, Union, Optional

app = Flask(__name__)

def RedXSecureBuy(
    bank_name: str,
    currency_type: str = "usd",
    currency_amount: float = 10.0,
    enable_multiple_payments: bool = False,
    enable_custom_amount: bool = False,
    enable_payment_history: bool = False,
    success_url: Optional[str] = None,
    cancel_url: Optional[str] = None
) -> Dict[str, Union[bool, str, float]]:
    """
    Create a payment session that allows you to receive payments from customers.

    Args:
        bank_name (str): Your business or store name
        currency_type (str): Currency code (e.g., "usd", "eur")
        currency_amount (float): Amount to charge
        enable_multiple_payments (bool): Allow multiple payments if True
        enable_custom_amount (bool): Allow custom payment amounts if True
        enable_payment_history (bool): Enable payment history tracking if True
        success_url (str, optional): URL to redirect after successful payment
        cancel_url (str, optional): URL to redirect after cancelled payment

    Returns:
        dict: Payment session information including:
            - success (bool): Whether the session was created successfully
            - session_id (str): Unique session identifier
            - payment_url (str): URL to share with customers
            - amount (float): Amount to be charged
            - currency (str): Currency code
            - error (str): Error message if success is False
    """
    if not os.getenv('STRIPE_SECRET_KEY'):
        return {
            'success': False,
            'error': 'STRIPE_SECRET_KEY environment variable not set'
        }

    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    try:
        # Create Stripe Checkout Session
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
            success_url=success_url or 'http://localhost:5000/payment/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=cancel_url or 'http://localhost:5000/payment/cancel',
            allow_promotion_codes=True,
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

def get_payment_status(session_id: str) -> Dict[str, Union[bool, str, float]]:
    """
    Check the status of a payment session.

    Args:
        session_id (str): The ID of the payment session to check

    Returns:
        dict: Payment status information including:
            - success (bool): Whether the status check was successful
            - status (str): Payment status ('paid', 'pending', or 'failed')
            - amount_total (float): Total amount paid
            - currency (str): Currency used
            - error (str): Error message if success is False
    """
    if not os.getenv('STRIPE_SECRET_KEY'):
        return {
            'success': False,
            'error': 'STRIPE_SECRET_KEY environment variable not set'
        }

    stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

    try:
        session = stripe.checkout.Session.retrieve(session_id)
        return {
            'success': True,
            'status': session.payment_status,
            'amount_total': session.amount_total / 100 if session.amount_total else 0,
            'currency': session.currency,
            'customer_email': session.customer_details.email if session.customer_details else None
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }