from datetime import datetime
from brownie import Token, Wei, accounts, reverts

supply = Wei(1000000000) * Wei(1e18)
availableMarketingBalance = Wei(10000000) * Wei(1e18)
marketingAddress = "0xcccc3333cccc3333cccc3333cccc3333cccc3333"

def deploy():
    return accounts[0].deploy(Token, supply, 1 * 1000, 9999999999)

def toWei(amount):
    return Wei(amount) * Wei(1e18)

def transfer(token):
    token.transfer(accounts[1], supply/2)
    assert token.balanceOf(accounts[0]) == supply/2
    assert token.balanceOf(accounts[1]) == (supply/2)

def transferWhiteListed(token):
    token.transfer(accounts[1], supply/2)
    assert token.balanceOf(accounts[0]) == supply/2
    assert token.balanceOf(accounts[1]) == supply/2

def splitAmount(token, v1):
    token.transfer(accounts[1], v1/2)
    assert token.balanceOf(accounts[0]) == v1/2
    assert token.balanceOf(accounts[1]) == v1/2

def tokenSupplyTest(token):
    assert token.totalSupply() == supply

def cliffTimeChangeMonth(token, monthNumber):
    token.changeCliffTime(int(datetime.now().timestamp()) - (monthNumber * 86400 * 30))

def cliffTimeChangeTime(token, time):
    token.changeCliffTime(time)

def getTime():
    return int(datetime.now().timestamp())

def supplyTest(token, now, value):
    a = 0
    try:
        assert token.totalSupply() == value
    except:
        a = 1
    if(a == 1):
        assert token.test_totalSupply(now) == value

class VestingAddress:
    def __init__(self, address, initialBalance, totalBalance, cliff, vestingDuration, amountPerMonth) -> None:
        self.address = address
        self.initialBalance = Wei(initialBalance) * Wei(1e18)
        self.totalBalance = Wei(totalBalance) * Wei(1e18)
        self.vesting = VestingPeriod(cliff, vestingDuration, amountPerMonth, initialBalance)
        assert amountPerMonth == round((totalBalance - initialBalance) / vestingDuration), "amountPerMonth: " + str(amountPerMonth) + "\t" + str(round((totalBalance - initialBalance) / vestingDuration))

class VestingPeriod:
    def __init__(self, cliff, vestingDuration, amountPerMonth, initialBalance):
        self.cliff = cliff
        self.vestingDuration = vestingDuration
        self.amountPerMonth = amountPerMonth
        self.maxVestingBalance = self.amountPerMonth * vestingDuration
        self.maxBalance = self.maxVestingBalance + initialBalance
    def getReleaseBalance(self, monthNumber):
        balance = 0 if self.cliff > 0 else self.amountPerMonth
        for x in range(min([monthNumber, self.vestingDuration + self.cliff])):
            month = x
            if (month >= self.cliff):
                balance += self.amountPerMonth
        return Wei(balance) * Wei(1e18)
    def fiveSecondDiff(self):
        return Wei((self.amountPerMonth/(86400 * 30)) * 5) * Wei(1e18)
    def isVestingStarted(self, monthNumber):
        return self.cliff < monthNumber

def startCliff(token):
    token.startCliff({'from': accounts[0]})

class Addresses:
    privateSale = VestingAddress("0xaaaa1111aaaa1111aaaa1111aaaa1111aaaa1111", 0, 150000000, cliff=3, vestingDuration=24, amountPerMonth=6250000)
    liquidityAndMM = VestingAddress("0xbbbb2222bbbb2222bbbb2222bbbb2222bbbb2222", 20000000, 200000000, cliff=0, vestingDuration=24, amountPerMonth=7500000)
    marketing = VestingAddress("0xcccc3333cccc3333cccc3333cccc3333cccc3333", 10000000, 100000000, cliff=0, vestingDuration=12, amountPerMonth=7500000)
    partnersAdvisors = VestingAddress("0xdddd4444dddd4444dddd4444dddd4444dddd4444", 0, 100000000, cliff=6, vestingDuration=36, amountPerMonth=2777778)
    reserves = VestingAddress("0xeeee5555eeee5555eeee5555eeee5555eeee5555", 45000000, 450000000, cliff=6, vestingDuration=48, amountPerMonth=8437500)

    All = {
        "privateSale": privateSale,
        "liquidityAndMM": liquidityAndMM,
        "marketing": marketing,
        "partnersAdvisors": partnersAdvisors,
        "reserves": reserves,
    }

def canChangeCliff(token):
    return hasattr(token, 'changeCliffTime')
