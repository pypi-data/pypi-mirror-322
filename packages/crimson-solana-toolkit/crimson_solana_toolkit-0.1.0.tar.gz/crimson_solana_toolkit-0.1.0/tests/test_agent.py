import pytest
from unittest.mock import Mock, patch
from solana_agent import SolanaAgent
from solana.keypair import Keypair
from solana.rpc.api import Client
from solana.transaction import Transaction

@pytest.fixture
def mock_client():
    return Mock(spec=Client)

@pytest.fixture
def agent(mock_client):
    with patch('solana_agent.agent.Client', return_value=mock_client):
        return SolanaAgent(network="devnet")

def test_agent_initialization():
    """Test agent initialization with default parameters."""
    agent = SolanaAgent()
    assert agent.network == "devnet"
    assert agent.rpc_url == "https://api.devnet.solana.com"
    assert isinstance(agent.keypair, Keypair)

def test_agent_custom_network():
    """Test agent initialization with custom network."""
    agent = SolanaAgent(network="mainnet")
    assert agent.network == "mainnet"
    assert agent.rpc_url == "https://api.mainnet-beta.solana.com"

def test_get_balance(agent, mock_client):
    """Test getting account balance."""
    mock_client.get_balance.return_value = {
        "result": {"value": 1000000000}  # 1 SOL in lamports
    }
    
    balance = agent.get_balance()
    assert balance == 1.0  # Should convert lamports to SOL
    mock_client.get_balance.assert_called_once()

def test_create_transaction(agent):
    """Test creating a transfer transaction."""
    to_address = "destination_address"
    amount = 1.0
    
    tx = agent.create_transaction(to_address, amount)
    assert isinstance(tx, Transaction)

def test_send_transaction(agent, mock_client):
    """Test sending a transaction."""
    mock_client.send_transaction.return_value = {
        "result": "transaction_signature"
    }
    
    tx = Transaction()
    result = agent.send_transaction(tx)
    
    assert result["signature"] == "transaction_signature"
    assert result["status"] == "submitted"
    mock_client.send_transaction.assert_called_once()

def test_create_token_account(agent, mock_client):
    """Test creating a token account."""
    mint_address = "mint_address"
    mock_account = "new_token_account"
    
    with patch('solana_agent.agent.Token') as mock_token:
        mock_token_instance = Mock()
        mock_token_instance.create_account.return_value = mock_account
        mock_token.return_value = mock_token_instance
        
        result = agent.create_token_account(mint_address)
        
        assert result["address"] == str(mock_account)
        assert result["mint"] == mint_address
        mock_token_instance.create_account.assert_called_once()

def test_get_token_balance(agent, mock_client):
    """Test getting token account balance."""
    token_account = "token_account"
    mock_client.get_token_account_balance.return_value = {
        "result": {"value": {"amount": "1000000000", "decimals": 9}}
    }
    
    balance = agent.get_token_balance(token_account)
    assert balance == 1.0  # Should convert to decimal based on decimals
    mock_client.get_token_account_balance.assert_called_once_with(token_account)

def test_airdrop(agent, mock_client):
    """Test requesting an airdrop."""
    mock_client.request_airdrop.return_value = {
        "result": "airdrop_signature"
    }
    
    result = agent.airdrop(amount=1.0)
    assert result["signature"] == "airdrop_signature"
    assert result["status"] == "submitted"
    
    # Should fail on mainnet
    agent.network = "mainnet"
    with pytest.raises(ValueError, match="Airdrop not available on mainnet"):
        agent.airdrop()

def test_monitor_address(agent, mock_client):
    """Test monitoring an address."""
    address = "test_address"
    callback = lambda x: x
    filter_type = "dataSize"
    
    mock_client.account_subscribe.return_value = 123  # subscription id
    
    sub_id = agent.monitor_address(address, callback, filter_type)
    assert sub_id == 123
    mock_client.account_subscribe.assert_called_once()

def test_estimate_transaction_fee(agent, mock_client):
    """Test estimating transaction fee."""
    mock_client.get_fee_for_message.return_value = {
        "result": 5000
    }
    
    tx = Transaction()
    fee = agent.estimate_transaction_fee(tx)
    assert fee == 5000
    mock_client.get_fee_for_message.assert_called_once()

def test_get_account_info(agent, mock_client):
    """Test getting account information."""
    address = "test_address"
    mock_client.get_account_info.return_value = {
        "result": {"value": {"data": "test_data"}}
    }
    
    info = agent.get_account_info(address)
    assert info["data"] == "test_data"
    mock_client.get_account_info.assert_called_once_with(
        address,
        encoding="jsonParsed"
    )
