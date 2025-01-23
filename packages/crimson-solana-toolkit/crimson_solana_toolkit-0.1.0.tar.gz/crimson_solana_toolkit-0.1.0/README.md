# Crimson Solana Toolkit

A comprehensive toolkit for interacting with the Solana blockchain, designed to work seamlessly with the Crimson Agent ecosystem. This toolkit provides advanced capabilities for blockchain operations, analytics, and AI-powered analysis through integration with CrimsonAgent.

## Features

### Core Blockchain Operations
- **Wallet Management**
  - Create and manage Solana wallets
  - Handle private key operations securely
  - Support for multiple network environments

- **Transaction Management**
  - Create and sign transactions
  - Estimate transaction fees
  - Monitor transaction status
  - Add memo data to transactions

- **Account Operations**
  - Query account balances
  - Monitor account activity
  - Retrieve detailed account information
  - Subscribe to account updates

### Program Utilities
- **Token Operations (SPL)**
  - Create token mints
  - Manage token accounts
  - Transfer tokens
  - Query token balances and metadata

- **NFT Support (Metaplex)**
  - Create NFT collections
  - Mint NFTs
  - Manage metadata
  - Track NFT transfers

- **DeFi Integration**
  - Create liquidity pools
  - Execute swaps
  - Provide/remove liquidity
  - Track pool metrics

- **Governance**
  - Create proposals
  - Cast votes
  - Track governance activities
  - Analyze voting patterns

### Analytics Tools
- **Blockchain Analytics**
  - Transaction history analysis
  - Network activity metrics
  - Token distribution analysis
  - Gini coefficient calculations

- **Token Analytics**
  - Holder distribution analysis
  - Transfer volume tracking
  - Price history analysis
  - Liquidity metrics

- **NFT Analytics**
  - Collection statistics
  - Trading volume analysis
  - Rarity calculations
  - Price trend analysis

- **DeFi Analytics**
  - Pool performance metrics
  - Volume analysis
  - Impermanent loss calculations
  - Yield tracking

## Installation

```bash
# Clone the repository
git clone https://github.com/crimson-labs/crimson-solana-toolkit.git
cd crimson-solana-toolkit

# Install the package
pip install -e .
```

## Quick Start

```python
from crimson_solana_toolkit import SolanaAgent
from crimson_agent import CrimsonAgent

# Initialize agents
solana = SolanaAgent(network="devnet")
crimson = CrimsonAgent(tools_enabled=True)

# Basic operations
balance = solana.get_balance()
print(f"Wallet balance: {balance} SOL")

# Create and send transaction
tx = solana.create_transaction(
    to_address="destination_address",
    amount=1.0,
    memo="Test transfer"
)
result = solana.send_transaction(tx)

# Analyze with CrimsonAgent
analysis = crimson.analyze_blockchain_data(
    solana.get_transaction_data(result["signature"])
)
```

## Advanced Usage

### Token Management
```python
from crimson_solana_toolkit.tools import TokenAnalytics

# Create token
token_account = solana.create_token_account(mint_address)

# Analyze token metrics
analytics = TokenAnalytics(solana.client)
activity = analytics.analyze_token_activity(mint_address)
```

### NFT Operations
```python
from crimson_solana_toolkit.programs import NFTProgram
from crimson_solana_toolkit.tools import NFTAnalytics

# Create NFT
NFTProgram.create_metadata_instruction(
    metadata_account="metadata_address",
    mint=mint_address,
    name="My NFT",
    symbol="MNFT",
    uri="https://example.com/metadata.json"
)

# Analyze NFT collection
analytics = NFTAnalytics(solana.client)
collection_data = analytics.analyze_collection(collection_address)
```

### DeFi Integration
```python
from crimson_solana_toolkit.programs import DeFiProgram
from crimson_solana_toolkit.tools import DeFiAnalytics

# Create liquidity pool
defi = DeFiProgram(program_id, solana.provider)
pool_ix = defi.create_pool({
    "token_a": "token_a_mint",
    "token_b": "token_b_mint",
    "fee_rate": 0.003
})

# Analyze pool metrics
analytics = DeFiAnalytics(solana.client)
pool_analysis = analytics.analyze_pool(pool_address)
```

## Testing

The toolkit includes comprehensive tests for all components:

```bash
# Run all tests
pytest tests/

# Run specific test categories
pytest tests/test_agent.py
pytest tests/test_programs.py
pytest tests/test_tools.py
```

## Examples

The `examples/` directory contains detailed examples:

- `basic_operations.py`: Core blockchain operations
- `token_operations.py`: Token creation and analysis
- `nft_and_defi.py`: NFT and DeFi protocol interactions

Run examples:
```bash
python examples/basic_operations.py
python examples/token_operations.py
python examples/nft_and_defi.py
```

## Integration with CrimsonAgent

The toolkit is designed to work seamlessly with CrimsonAgent for AI-powered blockchain analysis:

```python
# Analyze blockchain data
data = solana.get_account_info(address)
analysis = crimson.analyze_blockchain_data(data)

# Generate reports
report = crimson.generate_report(
    title="Blockchain Analysis Report",
    data=analysis
)
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Solana Foundation for blockchain infrastructure
- Metaplex for NFT standards
- CrimsonAgent team for AI integration capabilities
