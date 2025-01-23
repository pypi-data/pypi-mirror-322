import pytest
from unittest.mock import Mock
from crimson_solana_toolkit.programs import (
    MemoProgram,
    TokenProgram,
    NFTProgram,
    DeFiProgram,
    GovernanceProgram,
    StakingProgram
)
from solana.transaction import TransactionInstruction
import base58

def test_memo_program_create_instruction():
    """Test creating a memo instruction."""
    memo_text = "Test memo"
    instruction = MemoProgram.create_instruction(memo_text)
    
    assert isinstance(instruction, TransactionInstruction)
    assert instruction.program_id == base58.b58decode(MemoProgram.PROGRAM_ID)
    assert instruction.data == bytes(memo_text, "utf-8")
    assert instruction.keys == []

def test_token_program_create_mint_instruction():
    """Test creating a token mint instruction."""
    payer = "payer_address"
    mint_authority = "authority_address"
    decimals = 6
    
    instruction = TokenProgram.create_mint_instruction(
        payer=payer,
        mint_authority=mint_authority,
        decimals=decimals
    )
    
    assert isinstance(instruction, TransactionInstruction)
    assert len(instruction.keys) == 4
    assert instruction.data == bytes([0] + [decimals])

def test_staking_program_create_stake_account():
    """Test creating a stake account instruction."""
    from_pubkey = "from_address"
    stake_pubkey = "stake_address"
    authorized_pubkey = "auth_address"
    lockup_epoch = 100
    lamports = 1000000000
    
    instruction = StakingProgram.create_stake_account_instruction(
        from_pubkey=from_pubkey,
        stake_pubkey=stake_pubkey,
        authorized_pubkey=authorized_pubkey,
        lockup_epoch=lockup_epoch,
        lamports=lamports
    )
    
    assert isinstance(instruction, TransactionInstruction)

def test_defi_program_initialization():
    """Test DeFi program initialization."""
    program_id = "program_address"
    provider = Mock()
    
    defi = DeFiProgram(program_id, provider)
    assert defi.program_id == program_id
    assert defi.provider == provider

def test_governance_program_constants():
    """Test governance program constants."""
    assert GovernanceProgram.PROGRAM_ID == "GovER5Lthms3bLBqWub97yVrMmEogzX7xNjdXpPPCVZw"

def test_nft_program_constants():
    """Test NFT program constants."""
    assert NFTProgram.PROGRAM_ID == "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
