import pytest
from unittest.mock import Mock, patch
import pandas as pd
import numpy as np
from solana.rpc.api import Client
from crimson_solana_toolkit.tools import (
    BlockchainAnalytics,
    TokenAnalytics,
    NFTAnalytics,
    DeFiAnalytics,
    GovernanceAnalytics
)

@pytest.fixture
def mock_client():
    return Mock(spec=Client)

@pytest.fixture
def blockchain_analytics(mock_client):
    return BlockchainAnalytics(mock_client)

@pytest.fixture
def token_analytics(mock_client):
    return TokenAnalytics(mock_client)

@pytest.fixture
def nft_analytics(mock_client):
    return NFTAnalytics(mock_client)

@pytest.fixture
def sample_transactions():
    return [
        {
            "signature": "tx1",
            "blockTime": 1000000000,
            "err": None,
            "instructions": [
                {
                    "program": "system",
                    "parsed": {
                        "type": "transfer",
                        "info": {
                            "source": "addr1",
                            "destination": "addr2",
                            "lamports": 1000000000
                        }
                    }
                }
            ]
        },
        {
            "signature": "tx2",
            "blockTime": 1000000100,
            "err": "error",
            "instructions": []
        }
    ]

def test_analyze_transaction_history(blockchain_analytics, mock_client, sample_transactions):
    """Test transaction history analysis."""
    mock_client.get_signatures_for_address.return_value = {
        "result": sample_transactions
    }
    
    analysis = blockchain_analytics.analyze_transaction_history("test_address")
    
    assert analysis["total_transactions"] == 2
    assert analysis["successful_transactions"] == 1
    assert analysis["failed_transactions"] == 1
    mock_client.get_signatures_for_address.assert_called_once()

def test_create_transaction_graph(blockchain_analytics, sample_transactions):
    """Test transaction graph creation."""
    result = blockchain_analytics.create_transaction_graph(sample_transactions)
    
    assert "graph" in result
    assert "metrics" in result
    metrics = result["metrics"]
    assert metrics["total_nodes"] == 2  # addr1 and addr2
    assert metrics["total_edges"] == 1  # one transfer

def test_analyze_token_transfers(blockchain_analytics, mock_client):
    """Test token transfer analysis."""
    mock_client.get_token_largest_accounts.return_value = {
        "result": {
            "value": [
                {"address": "holder1", "amount": "1000000"},
                {"address": "holder2", "amount": "500000"}
            ]
        }
    }
    mock_client.get_token_supply.return_value = {
        "result": {
            "value": {
                "amount": "2000000"
            }
        }
    }
    
    analysis = blockchain_analytics.analyze_token_transfers("mint_address")
    
    assert analysis["total_supply"] == 2000000
    assert analysis["number_of_holders"] == 2
    assert len(analysis["largest_holders"]) == 2
    mock_client.get_token_largest_accounts.assert_called_once()
    mock_client.get_token_supply.assert_called_once()

def test_token_activity_analysis(token_analytics, mock_client):
    """Test token activity analysis."""
    mock_client.get_token_supply.return_value = {
        "result": {
            "value": {
                "amount": "1000000",
                "decimals": 6
            }
        }
    }
    mock_client.get_signatures_for_address.return_value = {
        "result": []
    }
    
    analysis = token_analytics.analyze_token_activity("mint_address")
    
    assert "token_info" in analysis
    assert "activity_metrics" in analysis
    assert "time_series" in analysis
    mock_client.get_token_supply.assert_called_once()
    mock_client.get_signatures_for_address.assert_called_once()

def test_nft_collection_analysis(nft_analytics, mock_client):
    """Test NFT collection analysis."""
    mock_client.get_account_info.return_value = {
        "result": {
            "value": {"data": "metadata"}
        }
    }
    mock_client.get_signatures_for_address.return_value = {
        "result": [
            {
                "signature": "tx1",
                "blockTime": 1000000000,
                "signer": "user1"
            }
        ]
    }
    
    analysis = nft_analytics.analyze_collection("collection_address")
    
    assert "collection_info" in analysis
    assert "activity_metrics" in analysis
    assert analysis["activity_metrics"]["total_transactions"] == 1
    mock_client.get_account_info.assert_called_once()
    mock_client.get_signatures_for_address.assert_called_once()

def test_calculate_gini(blockchain_analytics):
    """Test Gini coefficient calculation."""
    amounts = [100, 200, 300, 400]
    gini = blockchain_analytics._calculate_gini(amounts)
    
    assert 0 <= gini <= 1  # Gini coefficient should be between 0 and 1
    
    # Test with equal distribution
    equal_amounts = [100, 100, 100, 100]
    equal_gini = blockchain_analytics._calculate_gini(equal_amounts)
    assert equal_gini < gini  # Equal distribution should have lower Gini

def test_token_distribution_plot(token_analytics):
    """Test token distribution plot creation."""
    holders = [
        {"address": "holder1", "amount": 1000},
        {"address": "holder2", "amount": 500}
    ]
    
    result = token_analytics.create_token_distribution_plot(holders)
    
    assert "figure" in result
    assert "data" in result
    assert len(result["data"]) == 2

@pytest.mark.parametrize("amounts,expected_range", [
    ([1000, 1000, 1000], (0, 0.1)),  # Equal distribution
    ([1000, 0, 0], (0.9, 1)),  # Maximum inequality
    ([1000, 500, 250], (0.3, 0.7))  # Moderate inequality
])
def test_gini_coefficient_ranges(blockchain_analytics, amounts, expected_range):
    """Test Gini coefficient calculation for different distributions."""
    gini = blockchain_analytics._calculate_gini(amounts)
    min_expected, max_expected = expected_range
    assert min_expected <= gini <= max_expected
