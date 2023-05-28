# ERC20 Token Vesting

An ERC20 token implementation with configurable vesting schedules and a staking mechanism, built with Solidity and the Brownie development framework.

## Overview

This project implements a full-featured ERC20 token with two core systems:

**Vesting**: Token allocations for different stakeholder categories are distributed with configurable cliff periods and linear vesting schedules. Categories include private sale, liquidity, marketing, partners/advisors, and reserves.

**Staking**: Token holders can lock their balance and earn rewards at a configurable daily rate over a defined staking period.

## Contracts

- `contracts/Token.sol` - Main token contract. Inherits VestingFunds and implements locking, staking reward calculation, and token distribution on deploy.
- `contracts/VestingFunds.sol` - Manages vesting schedules. Handles cliff periods, linear release calculations, and fund distribution to stakeholder addresses.
- `contracts/Addresses.sol` - Registry of stakeholder wallet addresses used during initial token distribution.
- `interfaces/IToken.sol` - Interface for token staking and balance locking functions.
- `interfaces/IVestingFunds.sol` - Interface for vesting release and query functions.

## Requirements

- Python 3.8+
- Brownie
- Node.js and npm

Install Node dependencies:

```
npm install
```

## Deployment

```
brownie run scripts/deploy.py --network <network-name>
```

## Verify Contract Source

```
brownie run scripts/verifySmartContract.py --network <network-name>
```

## Tests

```
brownie test
```

## Token Distribution

Total supply: 1,000,000,000 tokens

| Category         | Amount       | Initial Unlock | Cliff    | Vesting Duration |
|------------------|-------------|----------------|----------|-----------------|
| Private Sale     | 150,000,000 | 0%             | 3 months | 24 months       |
| Liquidity / MM   | 200,000,000 | 10%            | None     | 24 months       |
| Marketing        | 100,000,000 | 10%            | None     | 12 months       |
| Partners/Advisors| 100,000,000 | 0%             | 6 months | 36 months       |
| Reserves         | 450,000,000 | 10%            | 6 months | 48 months       |

## Staking

Token holders can lock any portion of their available balance to earn staking rewards. Rewards accrue daily at the configured staking rate and are minted to the holder when they unlock their balance. Staking rewards stop accruing after the staking end time set by the owner.

## License

MIT
