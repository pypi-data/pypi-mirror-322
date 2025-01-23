from typing import Dict, Any, Optional, List
from solana.transaction import TransactionInstruction
from solana.system_program import CreateAccountParams, create_account
from solana.sysvar import SYSVAR_RENT_PUBKEY
from spl.token.constants import TOKEN_PROGRAM_ID
import base58

class MemoProgram:
    """Utility class for Solana's Memo Program."""
    
    PROGRAM_ID = "MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr"
    
    @staticmethod
    def create_instruction(memo_text: str) -> TransactionInstruction:
        """Create a memo instruction."""
        return TransactionInstruction(
            program_id=base58.b58decode(MemoProgram.PROGRAM_ID),
            data=bytes(memo_text, "utf-8"),
            keys=[]
        )

class TokenProgram:
    """Utility class for SPL Token Program operations."""
    
    @staticmethod
    def create_mint_instruction(
        payer: str,
        mint_authority: str,
        decimals: int = 9,
        freeze_authority: Optional[str] = None
    ) -> TransactionInstruction:
        """Create instruction for token mint account creation."""
        return TransactionInstruction(
            program_id=TOKEN_PROGRAM_ID,
            data=bytes([0] + [decimals]),  # Instruction index 0 = InitializeMint
            keys=[
                {"pubkey": payer, "is_signer": True, "is_writable": True},
                {"pubkey": mint_authority, "is_signer": False, "is_writable": False},
                {"pubkey": freeze_authority or mint_authority, "is_signer": False, "is_writable": False},
                {"pubkey": SYSVAR_RENT_PUBKEY, "is_signer": False, "is_writable": False}
            ]
        )

class NFTProgram:
    """Utility class for Metaplex NFT operations."""
    
    PROGRAM_ID = "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
    
    @staticmethod
    def create_metadata_instruction(
        metadata_account: str,
        mint: str,
        mint_authority: str,
        payer: str,
        update_authority: str,
        name: str,
        symbol: str,
        uri: str
    ) -> TransactionInstruction:
        """Create instruction for NFT metadata account creation."""
        # Implementation would include Metaplex metadata program interaction
        pass

class DeFiProgram:
    """Base class for DeFi program interactions."""
    
    def __init__(self, program_id: str, provider: Any):
        self.program_id = program_id
        self.provider = provider
        
    def create_pool(self, params: Dict[str, Any]) -> TransactionInstruction:
        """Create a liquidity pool instruction."""
        # Implementation would be specific to the DeFi protocol
        pass
        
    def swap(self, params: Dict[str, Any]) -> TransactionInstruction:
        """Create a swap instruction."""
        # Implementation would be specific to the DeFi protocol
        pass
        
    def provide_liquidity(self, params: Dict[str, Any]) -> TransactionInstruction:
        """Create a liquidity provision instruction."""
        # Implementation would be specific to the DeFi protocol
        pass

class GovernanceProgram:
    """Utility class for Solana Governance Program operations."""
    
    PROGRAM_ID = "GovER5Lthms3bLBqWub97yVrMmEogzX7xNjdXpPPCVZw"
    
    @staticmethod
    def create_proposal_instruction(
        governance: str,
        proposal_owner: str,
        name: str,
        description_link: str,
        vote_type: str,
        options: List[str],
        deny_vote_weight: Optional[int] = None
    ) -> TransactionInstruction:
        """Create instruction for governance proposal creation."""
        # Implementation would include Governance program interaction
        pass

class StakingProgram:
    """Utility class for Solana Staking operations."""
    
    @staticmethod
    def create_stake_account_instruction(
        from_pubkey: str,
        stake_pubkey: str,
        authorized_pubkey: str,
        lockup_epoch: int,
        lamports: int
    ) -> TransactionInstruction:
        """Create instruction for stake account creation."""
        return create_account(
            CreateAccountParams(
                from_pubkey=from_pubkey,
                new_account_pubkey=stake_pubkey,
                lamports=lamports,
                space=200,  # Size of stake account
                program_id=base58.b58decode("Stake11111111111111111111111111111111111111")
            )
        )
