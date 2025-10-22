from .mongo import counters

def next_customer_id() -> str:
    doc = counters.find_one_and_update(
        {"_id": "customer"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    if "seq" not in doc:
        counters.update_one({"_id":"customer"}, {"$set":{"seq": 100000}})
        doc = counters.find_one_and_update(
            {"_id": "customer"}, {"$inc": {"seq": 1}}, return_document=True
        )
    return f"CUS{doc['seq']:06d}"
