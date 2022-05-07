from brownie import accounts, network, Token, Contract
from pprint import pprint


def main():
    cn = Contract('0x1111222233334444555566667777888899990000')
    print("Balance: ")
    print(cn.getLockedBalance('0x1111111122222222333333334444444455555555'))
    print(cn.balanceOf('0x1111111122222222333333334444444455555555'))
    print(cn.balanceOf('0x9999999988888888777777776666666655555555'))
