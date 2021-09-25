import pytest
from brownie import Token, accounts, reverts
import shared
from datetime import datetime

@pytest.fixture
def token():
    tk = shared.deploy()
    shared.startCliff(tk)
    return tk

def test_vestingAdvance(token):
    for vestingType in shared.Addresses.All:
        shared.cliffTimeChangeMonth(token, 0)
        vestingAddress = shared.Addresses.All[vestingType]
        for x in range (vestingAddress.vesting.cliff + vestingAddress.vesting.vestingDuration):
            shared.cliffTimeChangeMonth(token, x)
            assert (token.getReleaseBalance(vestingAddress.address) - vestingAddress.vesting.getReleaseBalance(x) < (vestingAddress.vesting.fiveSecondDiff())), "Failed For " + vestingType

        for x in range (vestingAddress.vesting.cliff + vestingAddress.vesting.vestingDuration):
            x = x+1
            shared.cliffTimeChangeMonth(token, x)
            assert (token.getReleaseBalance(vestingAddress.address) - shared.toWei(vestingAddress.vesting.amountPerMonth) < (vestingAddress.vesting.fiveSecondDiff())), "Failed For " + vestingType
            if vestingAddress.vesting.getReleaseBalance(x) > 0:
                token.release({'from': vestingAddress.address})
            assert (token.balanceOf(vestingAddress.address) - (vestingAddress.initialBalance + vestingAddress.vesting.getReleaseBalance(x))) < vestingAddress.vesting.fiveSecondDiff(), "Failed For " + vestingType
        assert token.balanceOf(vestingAddress.address) == vestingAddress.totalBalance
        print(vestingType + ": done")


def test_firstMonthUnlockAfter2MonthsCliff(token):
    vestingAddress = shared.Addresses.privateSale
    currentTime = shared.getTime()
    march1st = currentTime - (86400 * 60)
    shared.cliffTimeChangeTime(token, march1st)
    assert token.getReleaseBalance(vestingAddress.address) - shared.toWei(117000000) < vestingAddress.vesting.fiveSecondDiff()
