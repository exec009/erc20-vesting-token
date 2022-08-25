from brownie import accounts, Wei, network, Token

def main():
    acct = accounts.load('deployer-account')
    supply = Wei(1000000000) * Wei(1e18)
    Token.deploy(supply, 1*1000, 9999999999, {'from': acct})
