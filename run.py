import requests
import time
import json
 
# Replace the following variables with your own values
ip_list_file = "ip_list.txt"
discord_webhook_url = "https://discord.com/api/webhooks/your-webhook-url"
rpc_username = "your-rpc-username"
rpc_password = "your-rpc-password"
 
# Define the RPC request payload
payload = json.dumps({
    "jsonrpc": "1.0",
    "id":"curltext",
    "method": "getblockchaininfo",
    "params": []
})
 
# Define a function to send an alert to a Discord webhook
def send_alert(ip_address):
    message = f"Alert! Invalid RPC request from IP address: {ip_address}"
    payload = {
        "content": message
    }
    requests.post(discord_webhook_url, data=payload)
 
# Read the list of IP addresses from the file
with open(ip_list_file, "r") as f:
    ip_list = f.readlines()
ip_list = [ip.strip() for ip in ip_list]
 
# Loop through the IP addresses every 10 seconds.
while True:
    for ip_address in ip_list:
        # Define the RPC endpoint URL
        url = f"http://{ip_address}:8888"
 
        # Send the RPC request
        try:
            response = requests.post(url, data=payload, auth=(rpc_username, rpc_password), timeout=10)
            response_json = response.json()
            if "result" in response_json:
                print(f"Valid RPC request from IP address: {ip_address}")
            else:
                send_alert(ip_address)
        except:
            send_alert(ip_address)
 
    # Wait for 10 seconds before checking again
    time.sleep(10)
