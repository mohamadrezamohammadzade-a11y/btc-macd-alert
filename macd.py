response = requests.get(
    URL,
    params={
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "limit": LIMIT,
    },
    timeout=20,
)

print(response.status_code)
print(response.text)

response.raise_for_status()

data = response.json()
