# pyKobana Library

A Python library to access Kobana API through HTTP requests.

## Installation

```bash
pip install pyKobana
```

## Usage

```python
from pyKobana import Kobana

# Initialize the Kobana client
kobana = Kobana("dev", "YOUR_API_TOKEN")

# Get wallets
wallets = kobana.get_wallets()
print(wallets)
```

## Methods

### `Kobana.get_wallets()`

Fetches the list of wallets.

**Returns:**
- `list`: A list of wallet objects.

### `Kobana.get_wallet(wallet_id)`

Fetches details of a specific wallet.

**Parameters:**
- `wallet_id` (str): The ID of the wallet to fetch.

**Returns:**
- `dict`: A dictionary containing wallet details.

### `Kobana.create_wallet(data)`

Creates a new wallet.

**Parameters:**
- `data` (dict): A dictionary containing wallet creation data.

**Returns:**
- `dict`: A dictionary containing the created wallet details.

### `Kobana.update_wallet(wallet_id, data)`

Updates an existing wallet.

**Parameters:**
- `wallet_id` (str): The ID of the wallet to update.
- `data` (dict): A dictionary containing wallet update data.

**Returns:**
- `dict`: A dictionary containing the updated wallet details.

### `Kobana.delete_wallet(wallet_id)`

Deletes a wallet.

**Parameters:**
- `wallet_id` (str): The ID of the wallet to delete.

**Returns:**
- `None`

## Example

```python
from pyKobana import Kobana

# Initialize the Kobana client
kobana = Kobana("dev", "YOUR_API_TOKEN")

# Create a new wallet
new_wallet = kobana.create_wallet({"name": "New Wallet"})
print(new_wallet)

# Get details of a specific wallet
wallet = kobana.get_wallet(new_wallet["id"])
print(wallet)

# Update the wallet
updated_wallet = kobana.update_wallet(new_wallet["id"], {"name": "Updated Wallet"})
print(updated_wallet)

# Delete the wallet
kobana.delete_wallet(new_wallet["id"])
print("Wallet deleted")
```
