from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/webhooks/stripe', methods=['POST'])
def receive_stripe_webhook():
    """Receives a webhook payload from Stripe.
    """
    
    # Try to parse a webhook payload, get upset if we couldn't
    # parse any JSON in the body:
    stripe_payload = None
    try:
        stripe_payload = request.json
    except Exception:
        return jsonify(message="Could not parse webhook payload"), 400

    event = stripe_payload.get('type')
    if not event:
        return jsonify(message="Could not determine event type"), 400
    if event == 'charge.succeeded':
        # Pull fields out of payload:
        data_object = stripe_payload.get('data').get('object')
        customer_id = data_object.get('customer')
        amount = data_object.get('amount')
        # Here we just log the transaction, but at this point we can do
        # anything! (Provision accounts, push to a database, etc.)
        print(f'Customer {customer_id} made a purchase of {amount} cents!')       

    return jsonify(message="Webhook received"), 200