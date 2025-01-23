from typing import Dict, Any, List, Optional, Union
from datetime import datetime
import pandas as pd
import numpy as np
from solana.rpc.api import Client
import plotly.graph_objects as go
import plotly.express as px
import networkx as nx

class BlockchainAnalytics:
    """Tools for analyzing Solana blockchain data."""
    
    def __init__(self, client: Client):
        self.client = client
        
    def analyze_transaction_history(self,
                                  address: str,
                                  limit: int = 100) -> Dict[str, Any]:
        """Analyze transaction history for an address."""
        # Get transaction history
        response = self.client.get_signatures_for_address(
            address,
            limit=limit
        )
        
        transactions = response["result"]
        
        # Process transactions
        df = pd.DataFrame(transactions)
        
        analysis = {
            "total_transactions": len(df),
            "successful_transactions": len(df[df["err"].isna()]),
            "failed_transactions": len(df[df["err"].notna()]),
            "total_sol_transferred": df["sol_change"].sum() if "sol_change" in df else None,
            "average_sol_per_tx": df["sol_change"].mean() if "sol_change" in df else None,
            "time_analysis": {
                "first_tx": df["blockTime"].min(),
                "last_tx": df["blockTime"].max(),
                "avg_tx_per_day": len(df) / ((df["blockTime"].max() - df["blockTime"].min()) / 86400)
            }
        }
        
        return analysis
    
    def create_transaction_graph(self,
                               transactions: List[Dict[str, Any]],
                               min_amount: Optional[float] = None) -> Dict[str, Any]:
        """Create a transaction relationship graph."""
        G = nx.DiGraph()
        
        for tx in transactions:
            if "instructions" not in tx:
                continue
                
            for ix in tx["instructions"]:
                if "program" not in ix or ix["program"] != "system":
                    continue
                    
                if "parsed" not in ix or "type" not in ix["parsed"]:
                    continue
                    
                if ix["parsed"]["type"] != "transfer":
                    continue
                    
                amount = float(ix["parsed"]["info"]["lamports"]) / 1e9
                if min_amount and amount < min_amount:
                    continue
                    
                from_addr = ix["parsed"]["info"]["source"]
                to_addr = ix["parsed"]["info"]["destination"]
                
                G.add_edge(from_addr, to_addr, amount=amount)
        
        # Calculate network metrics
        metrics = {
            "total_nodes": G.number_of_nodes(),
            "total_edges": G.number_of_edges(),
            "average_degree": sum(dict(G.degree()).values()) / G.number_of_nodes(),
            "density": nx.density(G),
            "most_central_nodes": sorted(
                nx.degree_centrality(G).items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
        }
        
        return {
            "graph": G,
            "metrics": metrics
        }
    
    def plot_transaction_volume(self,
                              transactions: List[Dict[str, Any]],
                              interval: str = "1D") -> Dict[str, Any]:
        """Create time series plot of transaction volume."""
        df = pd.DataFrame(transactions)
        df["datetime"] = pd.to_datetime(df["blockTime"], unit="s")
        
        # Resample data
        volume = df.resample(interval, on="datetime").size()
        
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=volume.index,
                y=volume.values,
                mode="lines",
                name="Transaction Volume"
            )
        )
        
        fig.update_layout(
            title="Transaction Volume Over Time",
            xaxis_title="Date",
            yaxis_title="Number of Transactions"
        )
        
        return {
            "figure": fig,
            "data": volume.to_dict()
        }
    
    def analyze_token_transfers(self,
                              mint_address: str,
                              limit: int = 100) -> Dict[str, Any]:
        """Analyze transfers for a specific token."""
        response = self.client.get_token_largest_accounts(mint_address)
        holders = response["result"]["value"]
        
        # Get token supply
        supply_response = self.client.get_token_supply(mint_address)
        total_supply = int(supply_response["result"]["value"]["amount"])
        
        analysis = {
            "total_supply": total_supply,
            "number_of_holders": len(holders),
            "largest_holders": [
                {
                    "address": h["address"],
                    "balance": int(h["amount"]),
                    "percentage": (int(h["amount"]) / total_supply) * 100
                }
                for h in holders[:5]
            ],
            "concentration_metrics": {
                "gini_coefficient": self._calculate_gini([
                    int(h["amount"]) for h in holders
                ]),
                "top_10_percentage": sum(
                    int(h["amount"]) for h in holders[:10]
                ) / total_supply * 100
            }
        }
        
        return analysis
    
    def _calculate_gini(self, amounts: List[float]) -> float:
        """Calculate Gini coefficient for token distribution."""
        amounts = np.array(amounts)
        if np.amin(amounts) < 0:
            amounts -= np.amin(amounts)
        amounts += 0.0000001
        array = np.array(amounts)
        array = array.flatten()
        if np.amin(array) < 0:
            array -= np.amin(array)
        array += 0.0000001
        array = np.sort(array)
        index = np.arange(1, array.shape[0] + 1)
        n = array.shape[0]
        return ((np.sum((2 * index - n - 1) * array)) / (n * np.sum(array)))

class TokenAnalytics:
    """Tools for analyzing token-related data."""
    
    def __init__(self, client: Client):
        self.client = client
        
    def analyze_token_activity(self,
                             mint_address: str,
                             days: int = 30) -> Dict[str, Any]:
        """Analyze token activity metrics."""
        # Get token metadata
        metadata = self.client.get_token_supply(mint_address)
        
        # Get recent transfers
        transfers = self.client.get_signatures_for_address(
            mint_address,
            limit=100
        )["result"]
        
        # Process transfer data
        df = pd.DataFrame(transfers)
        df["datetime"] = pd.to_datetime(df["blockTime"], unit="s")
        
        analysis = {
            "token_info": {
                "mint": mint_address,
                "total_supply": metadata["result"]["value"]["amount"],
                "decimals": metadata["result"]["value"]["decimals"]
            },
            "activity_metrics": {
                "total_transfers": len(transfers),
                "unique_senders": df["signer"].nunique() if "signer" in df else None,
                "average_transfer_size": df["amount"].mean() if "amount" in df else None,
                "transfer_frequency": len(transfers) / days
            },
            "time_series": {
                "daily_transfers": df.resample("D", on="datetime").size().to_dict(),
                "daily_volume": df.resample("D", on="datetime")["amount"].sum().to_dict() if "amount" in df else None
            }
        }
        
        return analysis
    
    def create_token_distribution_plot(self,
                                     holders: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create visualization of token distribution."""
        df = pd.DataFrame(holders)
        
        fig = px.pie(
            df,
            values="amount",
            names="address",
            title="Token Distribution"
        )
        
        return {
            "figure": fig,
            "data": df.to_dict("records")
        }

class NFTAnalytics:
    """Tools for analyzing NFT collections and activity."""
    
    def __init__(self, client: Client):
        self.client = client
        
    def analyze_collection(self,
                         collection_address: str) -> Dict[str, Any]:
        """Analyze an NFT collection."""
        # Get collection metadata
        metadata = self.client.get_account_info(collection_address)
        
        # Get recent activity
        activity = self.client.get_signatures_for_address(
            collection_address,
            limit=100
        )["result"]
        
        analysis = {
            "collection_info": {
                "address": collection_address,
                "metadata": metadata["result"]["value"] if metadata["result"] else None
            },
            "activity_metrics": {
                "total_transactions": len(activity),
                "unique_interactors": len(set(tx["signer"] for tx in activity if "signer" in tx)),
                "last_activity": max(tx["blockTime"] for tx in activity if "blockTime" in tx)
            }
        }
        
        return analysis
    
    def get_nft_price_history(self,
                             mint_address: str,
                             days: int = 30) -> Dict[str, Any]:
        """Get price history for an NFT."""
        # This would typically integrate with a marketplace API
        # Implementation would depend on the specific marketplace
        pass

class DeFiAnalytics:
    """Tools for analyzing DeFi protocols and liquidity pools."""
    
    def __init__(self, client: Client):
        self.client = client
        
    def analyze_pool(self,
                    pool_address: str) -> Dict[str, Any]:
        """Analyze a liquidity pool."""
        # Get pool data
        pool_data = self.client.get_account_info(pool_address)
        
        # Get recent swaps
        swaps = self.client.get_signatures_for_address(
            pool_address,
            limit=100
        )["result"]
        
        analysis = {
            "pool_info": {
                "address": pool_address,
                "data": pool_data["result"]["value"] if pool_data["result"] else None
            },
            "metrics": {
                "total_swaps": len(swaps),
                "unique_traders": len(set(tx["signer"] for tx in swaps if "signer" in tx)),
                "last_swap": max(tx["blockTime"] for tx in swaps if "blockTime" in tx)
            }
        }
        
        return analysis
    
    def calculate_pool_metrics(self,
                             pool_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate key metrics for a liquidity pool."""
        # Implementation would depend on the specific DEX protocol
        pass

class GovernanceAnalytics:
    """Tools for analyzing governance proposals and voting."""
    
    def __init__(self, client: Client):
        self.client = client
        
    def analyze_proposal(self,
                        proposal_address: str) -> Dict[str, Any]:
        """Analyze a governance proposal."""
        # Get proposal data
        proposal_data = self.client.get_account_info(proposal_address)
        
        # Get votes
        votes = self.client.get_signatures_for_address(
            proposal_address,
            limit=100
        )["result"]
        
        analysis = {
            "proposal_info": {
                "address": proposal_address,
                "data": proposal_data["result"]["value"] if proposal_data["result"] else None
            },
            "voting_metrics": {
                "total_votes": len(votes),
                "unique_voters": len(set(tx["signer"] for tx in votes if "signer" in tx)),
                "last_vote": max(tx["blockTime"] for tx in votes if "blockTime" in tx)
            }
        }
        
        return analysis
    
    def create_voting_distribution_plot(self,
                                      votes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Create visualization of vote distribution."""
        df = pd.DataFrame(votes)
        
        fig = px.bar(
            df,
            x="vote",
            title="Vote Distribution"
        )
        
        return {
            "figure": fig,
            "data": df.to_dict("records")
        }
