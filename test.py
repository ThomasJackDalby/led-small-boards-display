import requests
import sys
message = sys.argv[1]

response = requests.get("http://192.168.1.195/message", params={"message": message})
print(response)