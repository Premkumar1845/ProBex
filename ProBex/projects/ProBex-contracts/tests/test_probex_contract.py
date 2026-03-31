import pytest
from algokit_utils import (
    AlgoAmount,
    CommonAppCallParams,
    PaymentParams,
    SigningAccount,
)
from algokit_utils.config import config

from smart_contracts.artifacts.probex_contract.probex_contract_client import (
    ProbexContractClient,
    ProbexContractFactory,
)
from tests.conftest import _fund


# ──────────── helpers ────────────

def _deploy_fresh(algorand, dispenser, fund_algo: int = 10):
    """Create a fresh contract with a unique creator each time."""
    config.configure(debug=False)
    owner = _fund(algorand, dispenser, algo=100)
    factory = algorand.client.get_typed_app_factory(
        ProbexContractFactory,
        default_sender=owner.address,
        default_signer=owner.signer,
    )
    client, _ = factory.send.create.bare()
    algorand.send.payment(
        PaymentParams(
            sender=dispenser.address,
            receiver=client.app_address,
            amount=AlgoAmount(algo=fund_algo),
        )
    )
    return client, owner


def _place_bet(
    *,
    algorand,
    client: ProbexContractClient,
    bettor: SigningAccount,
    outcome: str,
    amount_micro: int,
) -> None:
    pay_txn = algorand.create_transaction.payment(
        PaymentParams(
            sender=bettor.address,
            receiver=client.app_address,
            amount=AlgoAmount(micro_algo=amount_micro),
        )
    )
    client.send.opt_in.bet(
        args=(outcome, pay_txn),
        params=CommonAppCallParams(
            sender=bettor.address,
            signer=bettor.signer,
        ),
    )


def _balance(algorand, addr: str) -> int:
    return algorand.client.algod.account_info(addr)["amount"]


def _resolve(client: ProbexContractClient, creator: SigningAccount, outcome: str) -> None:
    client.send.resolve_market(
        args=(outcome,),
        params=CommonAppCallParams(
            sender=creator.address,
            signer=creator.signer,
        ),
    )


def _claim(client: ProbexContractClient, bettor: SigningAccount) -> None:
    client.send.claim_winnings(
        params=CommonAppCallParams(
            sender=bettor.address,
            signer=bettor.signer,
            extra_fee=AlgoAmount(micro_algo=1000),
        ),
    )


# ──────────── Test 1: Basic parimutuel (2 ALGO yes, 1 ALGO no → yes wins) ────────────

def test_basic_parimutuel_yes_wins(algorand, dispenser):
    client, owner = _deploy_fresh(algorand, dispenser)

    a = _fund(algorand, dispenser)
    b = _fund(algorand, dispenser)

    _place_bet(algorand=algorand, client=client, bettor=a, outcome="yes", amount_micro=2_000_000)
    _place_bet(algorand=algorand, client=client, bettor=b, outcome="no", amount_micro=1_000_000)

    _resolve(client, owner, "yes")

    app_before = _balance(algorand, client.app_address)
    _claim(client, a)
    app_after = _balance(algorand, client.app_address)

    # total pool = 3 ALGO, yes pool = 2 ALGO → payout = (2 * 3) / 2 = 3 ALGO
    assert app_before - app_after == 3_000_000


# ──────────── Test 2: NO side wins ────────────

def test_no_side_wins(algorand, dispenser):
    client, owner = _deploy_fresh(algorand, dispenser)

    a = _fund(algorand, dispenser)
    b = _fund(algorand, dispenser)

    _place_bet(algorand=algorand, client=client, bettor=a, outcome="yes", amount_micro=1_000_000)
    _place_bet(algorand=algorand, client=client, bettor=b, outcome="no", amount_micro=2_000_000)

    _resolve(client, owner, "no")

    app_before = _balance(algorand, client.app_address)
    _claim(client, b)
    app_after = _balance(algorand, client.app_address)

    # total pool = 3 ALGO, no pool = 2 ALGO → payout = (2 * 3) / 2 = 3 ALGO
    assert app_before - app_after == 3_000_000


# ──────────── Test 3: Multiple winners split proportionally ────────────

def test_proportional_split_multiple_winners(algorand, dispenser):
    client, owner = _deploy_fresh(algorand, dispenser)

    a = _fund(algorand, dispenser)  # yes 3 ALGO
    b = _fund(algorand, dispenser)  # yes 1 ALGO
    c = _fund(algorand, dispenser)  # no  4 ALGO

    _place_bet(algorand=algorand, client=client, bettor=a, outcome="yes", amount_micro=3_000_000)
    _place_bet(algorand=algorand, client=client, bettor=b, outcome="yes", amount_micro=1_000_000)
    _place_bet(algorand=algorand, client=client, bettor=c, outcome="no", amount_micro=4_000_000)

    # Total pool: 8 ALGO, yes pool: 4 ALGO
    _resolve(client, owner, "yes")

    # a payout: (3 * 8) / 4 = 6 ALGO
    bal_a_before = _balance(algorand, a.address)
    _claim(client, a)
    bal_a_after = _balance(algorand, a.address)
    a_received = bal_a_after - bal_a_before + 2000  # add back the extra_fee
    assert a_received == 6_000_000

    # b payout: (1 * 8) / 4 = 2 ALGO
    bal_b_before = _balance(algorand, b.address)
    _claim(client, b)
    bal_b_after = _balance(algorand, b.address)
    b_received = bal_b_after - bal_b_before + 2000
    assert b_received == 2_000_000


# ──────────── Test 4: Loser cannot claim ────────────

def test_loser_cannot_claim(algorand, dispenser):
    client, owner = _deploy_fresh(algorand, dispenser)

    a = _fund(algorand, dispenser)
    b = _fund(algorand, dispenser)

    _place_bet(algorand=algorand, client=client, bettor=a, outcome="yes", amount_micro=1_000_000)
    _place_bet(algorand=algorand, client=client, bettor=b, outcome="no", amount_micro=1_000_000)

    _resolve(client, owner, "yes")

    with pytest.raises(Exception):
        _claim(client, b)


# ──────────── Test 5: Double claim rejected ────────────

def test_double_claim_rejected(algorand, dispenser):
    client, owner = _deploy_fresh(algorand, dispenser)

    a = _fund(algorand, dispenser)
    b = _fund(algorand, dispenser)

    _place_bet(algorand=algorand, client=client, bettor=a, outcome="yes", amount_micro=1_000_000)
    _place_bet(algorand=algorand, client=client, bettor=b, outcome="no", amount_micro=1_000_000)

    _resolve(client, owner, "yes")
    _claim(client, a)

    with pytest.raises(Exception):
        _claim(client, a)


# ──────────── Test 6: Cannot bet after resolve ────────────

def test_no_bet_after_resolve(algorand, dispenser):
    client, owner = _deploy_fresh(algorand, dispenser)

    a = _fund(algorand, dispenser)
    b = _fund(algorand, dispenser)

    _place_bet(algorand=algorand, client=client, bettor=a, outcome="yes", amount_micro=1_000_000)
    _resolve(client, owner, "yes")

    with pytest.raises(Exception):
        _place_bet(algorand=algorand, client=client, bettor=b, outcome="no", amount_micro=1_000_000)


# ──────────── Test 7: Only creator can resolve ────────────

def test_only_creator_can_resolve(algorand, dispenser):
    client, owner = _deploy_fresh(algorand, dispenser)

    a = _fund(algorand, dispenser)
    _place_bet(algorand=algorand, client=client, bettor=a, outcome="yes", amount_micro=1_000_000)

    with pytest.raises(Exception):
        _resolve(client, a, "yes")


# ──────────── Test 8: Cannot double bet (same user) ────────────

def test_double_bet_rejected(algorand, dispenser):
    client, owner = _deploy_fresh(algorand, dispenser)

    a = _fund(algorand, dispenser)
    _place_bet(algorand=algorand, client=client, bettor=a, outcome="yes", amount_micro=1_000_000)

    with pytest.raises(Exception):
        _place_bet(algorand=algorand, client=client, bettor=a, outcome="no", amount_micro=1_000_000)


# ──────────── Test 9: Invalid outcome rejected ────────────

def test_invalid_outcome_rejected(algorand, dispenser):
    client, owner = _deploy_fresh(algorand, dispenser)

    a = _fund(algorand, dispenser)
    with pytest.raises(Exception):
        _place_bet(algorand=algorand, client=client, bettor=a, outcome="maybe", amount_micro=1_000_000)


# ──────────── Test 10: Claim before resolve rejected ────────────

def test_claim_before_resolve_rejected(algorand, dispenser):
    client, owner = _deploy_fresh(algorand, dispenser)

    a = _fund(algorand, dispenser)
    _place_bet(algorand=algorand, client=client, bettor=a, outcome="yes", amount_micro=1_000_000)

    with pytest.raises(Exception):
        _claim(client, a)
