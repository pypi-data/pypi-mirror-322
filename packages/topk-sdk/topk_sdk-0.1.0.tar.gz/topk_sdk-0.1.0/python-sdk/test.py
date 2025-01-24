from topk_sdk import Client, collection, field, literal

client = Client(api_key="zojuke6ypd4czd4mcghqaaaa2adqqajre26qcaabaaapd4y", region="...")

client.upsert(
    "test",
    [
        {"_id": "one", "name": "one"},
        {"_id": "two"},
    ],
)

res = client.query(
    collection("test").select("name", a=field("a"))
    # .filter((field("a") + literal(1)) & field("b") | field("c"))
    # .filter(field("_id").eq(literal("one")))
    # .filter(field("b").neq(literal(13)))
    # .top_k(field("_id"), 10)
)

print(res)

# client.query(
#     collection("test")
#     .select("foo", a=field("a"))
#     .filter((field("a") + literal(1)) & field("b") | field("c"))
#     .filter(field("a").eq(literal(12)))
#     .filter(field("b").neq(literal(13)))
#     .top_k(field("a"), 10)
# )


# client.create_collection("test", {"a": "int32", "b": "int32", "c": "int32"})
