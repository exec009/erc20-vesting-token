from brownie import accounts, network, Token, Contract

def main():
    cn = Contract('0x1111222233334444555566667777888899990000')
    Token.publish_source(cn)
