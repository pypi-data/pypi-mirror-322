from typing import Dict, Any, Optional, List
from solana.rpc.api import Client
from solana.rpc.types import TxOpts
from solana.transaction import Transaction
from solana.system_program import TransferParams, transfer
from solana.keypair import Keypair
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID
from anchorpy import Program, Provider, Wallet
import base58
import json

class SolanaAgent:
    """Main agent class for Solana blockchain interactions."""
    
    NETWORKS = {
        "mainnet": "https://api.mainnet-beta.solana.com",
        "devnet": "https://api.devnet.solana.com",
        "testnet": "https://api.testnet.solana.com",
        "localnet": "http://localhost:8899",
    }

    def __init__(self,
                 network: str = "devnet",
                 private_key: Optional[str] = None,
                 rpc_url: Optional[str] = None):
        """
        Initialize SolanaAgent.

        Args:
            network: Network to connect to (mainnet, devnet, testnet, localnet)
            private_key: Base58 encoded private key (optional)
            rpc_url: Custom RPC URL (optional)
        """
        self.network = network
        self.rpc_url = rpc_url or self.NETWORKS[network]
        self.client = Client(self.rpc_url)
        
        # Initialize keypair
        if private_key:
            self.keypair = Keypair.from_secret_key(
                base58.b58decode(private_key)
            )
        else:
            self.keypair = Keypair()
            
        # Initialize provider for Anchor programs
        self.provider = Provider(
            self.client,
            Wallet(self.keypair),
            TxOpts(skip_preflight=True)
        )

    def get_balance(self, address: Optional[str] = None) -> float:
        """Get SOL balance for an address."""
        address = address or str(self.keypair.public_key)
        response = self.client.get_balance(address)
        return float(response["result"]["value"]) / 1e9  # Convert lamports to SOL

    def create_transaction(self,
                         to_address: str,
                         amount: float,
                         memo: Optional[str] = None) -> Transaction:
        """Create a SOL transfer transaction."""
        # Convert SOL to lamports
        lamports = int(amount * 1e9)
        
        # Create transfer instruction
        transfer_ix = transfer(
            TransferParams(
                from_pubkey=self.keypair.public_key,
                to_pubkey=to_address,
                lamports=lamports
            )
        )
        
        # Create and sign transaction
        transaction = Transaction().add(transfer_ix)
        
        # Add memo if provided
        if memo:
            # Import here to avoid circular dependency
            from .programs import MemoProgram
            memo_ix = MemoProgram.create_instruction(memo)
            transaction.add(memo_ix)
            
        return transaction

    def send_transaction(self, transaction: Transaction) -> Dict[str, Any]:
        """Sign and send a transaction."""
        # Sign transaction
        transaction.sign(self.keypair)
        
        # Send transaction
        result = self.client.send_transaction(
            transaction,
            self.keypair,
            opts=TxOpts(skip_preflight=True)
        )
        
        return {
            "signature": result["result"],
            "status": "submitted"
        }

    def create_token_account(self,
                           mint_address: str,
                           owner: Optional[str] = None) -> Dict[str, Any]:
        """Create a new token account."""
        owner = owner or str(self.keypair.public_key)
        
        # Create token client
        token = Token(
            self.client,
            mint_address,
            TOKEN_PROGRAM_ID,
            self.keypair
        )
        
        # Create account
        account = token.create_account(owner)
        
        return {
            "address": str(account),
            "mint": mint_address,
            "owner": owner
        }

    def get_token_balance(self,
                         token_account: str,
                         mint_decimals: int = 9) -> float:
        """Get token balance for a token account."""
        response = self.client.get_token_account_balance(token_account)
        amount = float(response["result"]["value"]["amount"])
        return amount / (10 ** mint_decimals)

    def deploy_program(self,
                      program_path: str,
                      program_id: Optional[str] = None) -> Dict[str, Any]:
        """Deploy a Solana program."""
        # Read program binary
        with open(program_path, "rb") as f:
            program_data = f.read()
            
        # Deploy program
        response = self.client.deploy_program(
            self.keypair,
            program_data,
            program_id
        )
        
        return {
            "program_id": response["result"],
            "status": "deployed"
        }

    def load_program(self,
                    program_id: str,
                    idl_path: Optional[str] = None) -> Program:
        """Load an Anchor program."""
        if idl_path:
            with open(idl_path) as f:
                idl = json.load(f)
        else:
            # Fetch IDL from chain
            idl = Program.fetch_idl(program_id, self.provider)
            
        return Program(idl, program_id, self.provider)

    def get_transaction_data(self, signature: str) -> Dict[str, Any]:
        """Get detailed transaction data."""
        response = self.client.get_transaction(
            signature,
            encoding="jsonParsed"
        )
        return response["result"]

    def get_account_info(self, address: str) -> Dict[str, Any]:
        """Get detailed account information."""
        response = self.client.get_account_info(
            address,
            encoding="jsonParsed"
        )
        return response["result"]["value"]

    def monitor_address(self,
                       address: str,
                       callback: callable,
                       filter_type: Optional[str] = None):
        """Monitor an address for transactions."""
        sub_id = self.client.account_subscribe(
            address,
            callback,
            encoding="jsonParsed",
            commitment="confirmed",
            filters=[{"type": filter_type}] if filter_type else None
        )
        return sub_id

    def estimate_transaction_fee(self, transaction: Transaction) -> int:
        """Estimate transaction fee in lamports."""
        response = self.client.get_fee_for_message(
            transaction.serialize_message()
        )
        return response["result"]

    def airdrop(self, address: Optional[str] = None, amount: float = 1.0) -> Dict[str, Any]:
        """Request airdrop of SOL (devnet/testnet only)."""
        if self.network == "mainnet":
            raise ValueError("Airdrop not available on mainnet")
            
        address = address or str(self.keypair.public_key)
        lamports = int(amount * 1e9)
        
        response = self.client.request_airdrop(
            address,
            lamports,
            commitment="confirmed"
        )
        
        return {
            "signature": response["result"],
            "status": "submitted"
        }

    def __repr__(self):
        return (f"<SolanaAgent(network={self.network}, "
                f"address={str(self.keypair.public_key)})>")
