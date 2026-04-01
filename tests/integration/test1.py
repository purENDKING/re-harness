from adapters.static_reva.client import ReVaClient, ReVaToolError
from adapters.static_reva.adapter import get_static_analyzer

# static_analyzer = get_static_analyzer(use_real=True)

client = ReVaClient()
print(client.ping())

# try:
#     print(static_analyzer.decompile("main", limit=200))
# except ReVaToolError as e:
#     print("tool:", e.tool_name)
#     print("args:", e.arguments)
#     print("error:")
#     print(e)
#     raise
