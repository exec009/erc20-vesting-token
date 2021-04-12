import pytest
from brownie import Token, Wei, accounts, reverts
import shared
from datetime import datetime


@pytest.fixture
def token():
    return shared.deploy()

def test_balanceOf(token):
    assert token.balanceOf(shared.marketingAddress) == shared.availableMarketingBalance

def test_ownership(token):
    fail = True
    try:
        token.setStakingRate(1, {'from': accounts[1]})
        fail = False
    except:
        fail = True
    assert fail, "Ownership test failed"


def test_transfer(token):
    token.transfer(accounts[1], shared.availableMarketingBalance / 2, {'from': shared.marketingAddress})
    assert token.balanceOf(shared.marketingAddress) == shared.availableMarketingBalance / 2
    assert token.balanceOf(accounts[1]) == shared.availableMarketingBalance / 2

def test_lockUnlockBalance(token):
    tm = int(datetime.now().timestamp())
    token.lockBalance(shared.availableMarketingBalance / 2, { 'from': shared.marketingAddress })
    assert token.balanceOf(shared.marketingAddress) == shared.availableMarketingBalance / 2
    assert token.getLockedBalance(shared.marketingAddress) == shared.availableMarketingBalance / 2
    assert abs(token.getLockedTime(shared.marketingAddress) - tm) < 30
    assert token.getStakingReward(shared.marketingAddress) == 0
    token.unlockBalance({ 'from': shared.marketingAddress })
    assert token.balanceOf(shared.marketingAddress) == shared.availableMarketingBalance
    assert token.getLockedBalance(shared.marketingAddress) == 0
    assert token.getLockedTime(shared.marketingAddress) == 0

def test_lockUnlockBalanceWithTimeFactor1(token):
    lockUnlockBalanceWithTimeFactor(token, 1, 86400 * 5)

def test_lockUnlockBalanceWithTimeFactor2(token):
    lockUnlockBalanceWithTimeFactor(token, 10, 86400 * 10)

def test_lockUnlockBalanceWithTimeFactor3(token):
    lockUnlockBalanceWithTimeFactor(token, 5, 86400 * 365 * 2)

def lockUnlockBalanceWithTimeFactor(token, stakingRate, duration):
    if stakingRate != 1:
        token.setStakingRate(stakingRate * 1000)
    tm = int(datetime.now().timestamp())
    days = duration / 86400
    token.test_lockBalance(shared.availableMarketingBalance / 2, tm - duration, { 'from': shared.marketingAddress })
    assert token.balanceOf(shared.marketingAddress) == shared.availableMarketingBalance / 2
    assert token.getLockedBalance(shared.marketingAddress) == shared.availableMarketingBalance / 2
    assert token.getLockedTime(shared.marketingAddress) == tm - duration
    assert token.getStakingReward(shared.marketingAddress) == (Wei(days) * Wei(stakingRate) * Wei(shared.availableMarketingBalance / 2))/100
    token.unlockBalance({ 'from': shared.marketingAddress })
    assert token.balanceOf(shared.marketingAddress) == Wei(shared.availableMarketingBalance) + (Wei(days) * Wei(stakingRate) * Wei(shared.availableMarketingBalance / 2))/100
    assert token.getLockedBalance(shared.marketingAddress) == 0
    assert token.getLockedTime(shared.marketingAddress) == 0
