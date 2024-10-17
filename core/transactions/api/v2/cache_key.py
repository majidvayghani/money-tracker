
def get_transaction_key(id, pk):
    """
        key pattern: transactions:u:<id>:trans:<pk>
        u<id> is user ID based on Authentication
        trans<pk> is transaction ID
    """
    return "transactions:u"f"{id}"f"{pk}"

