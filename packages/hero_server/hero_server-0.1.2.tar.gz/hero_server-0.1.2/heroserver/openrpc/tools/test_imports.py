from heroserver.openrpc.tools import get_pydantic_type

# Simple test schema
test_schema = {"type": "string", "format": "email"}
result = get_pydantic_type(test_schema)
print(f"Test passed: {result == 'Email'}")
