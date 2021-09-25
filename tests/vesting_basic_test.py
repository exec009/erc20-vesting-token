from time import sleep
import pytest
from brownie import Token, Wei, accounts, reverts
import shared
from datetime import datetime

@pytest.fixture
def token():
    return shared.deploy()

def test_cliff(token):
    assert token.getReleaseBalance(shared.Addresses.privateSale.address) == 0
    _pass = False
    try:
        token.startCliff({'from': accounts[1]})
    except:
        _pass = True
    assert _pass, "called via non admin"

def test_vesting1(token):
    token.startCliff({'from': accounts[0]})
    assert token.getReleaseBalance(shared.Addresses.privateSale.address) == 0

def test_vesting2(token):
    test_vesting1(token)
    token.changeCliffTime(86400 * 60)
    for vestingType in shared.Addresses.All:
        vestingAddress = shared.Addresses.All[vestingType]
        assert token.getReleaseBalance(vestingAddress.address) == vestingAddress.totalBalance - vestingAddress.initialBalance, "Failed For " + vestingType
        assert token.balanceOf(vestingAddress.address) == vestingAddress.initialBalance, "Failed For " + vestingType
        token.release({'from': vestingAddress.address})
        assert token.balanceOf(vestingAddress.address) == vestingAddress.totalBalance, "Failed For " + vestingType
        assert token.getTotalLockedBalance(vestingAddress.address) == 0, "Failed For " + vestingType
        token.transfer(accounts[1], vestingAddress.totalBalance, { 'from': vestingAddress.address })
    assert token.balanceOf(accounts[1]) == shared.supply
    shared.tokenSupplyTest(token)

def test_vesting3(token):
    test_vesting1(token)
    token.changeCliffTime(86400 * 0)
    for vestingType in shared.Addresses.All:
        vestingAddress = shared.Addresses.All[vestingType]
        assert token.getReleaseBalance(vestingAddress.address) == vestingAddress.totalBalance - vestingAddress.initialBalance, "Failed For " + vestingType
        assert token.balanceOf(vestingAddress.address) == vestingAddress.initialBalance, "Failed For " + vestingType
        _pass = False
        try:
            token.release({'from': accounts[1]})
        except:
            _pass = True
        assert _pass, "Release called from invalid address " + vestingType
        token.release({'from': vestingAddress.address})
        assert token.balanceOf(vestingAddress.address) == vestingAddress.totalBalance, "Failed For " + vestingType
        assert token.getTotalLockedBalance(vestingAddress.address) == 0, "Failed For " + vestingType
        token.transfer(accounts[1], vestingAddress.totalBalance, { 'from': vestingAddress.address })
    assert token.balanceOf(accounts[1]) == shared.supply
    shared.tokenSupplyTest(token)
