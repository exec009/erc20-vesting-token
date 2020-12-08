// contracts/Token.sol
// SPDX-License-Identifier: MIT
pragma solidity >=0.8.2 <0.9.0;

import "../node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "../node_modules/@openzeppelin/contracts/access/Ownable.sol";
import "./VestingFunds.sol";
import "../interfaces/IToken.sol";

struct BalanceLock {
    uint256 amount;
    uint256 time;
}

contract Token is VestingFunds, IToken {
    uint256 public stakingRate;
    mapping(address => BalanceLock) public _lockedBalance;
    constructor(uint256 initialSupply, uint256 _stakingRate) VestingFunds("VestingToken", "VTK") {
        _mint(msg.sender, initialSupply);
        stakingRate = _stakingRate;
        distribute();
    }
    function setStakingRate(uint256 rate) external override onlyOwner {
        stakingRate = rate;
    }
    function lockBalance(uint256 amount) external override {
        require(balanceOf(_msgSender()) >= amount, "Token: locking amount exceeds balance");
        require(_lockedBalance[_msgSender()].amount == 0, "Token: amount already locked");
        _lockedBalance[_msgSender()] = BalanceLock(amount, block.timestamp);
    }
    function getStakingReward(address adrs) external view override returns(uint256) {
        BalanceLock memory lock = _lockedBalance[adrs];
        return calculateStake(lock.amount, lock.time);
    }
    function getLockedBalance(address adrs) external view override returns(uint256) {
        return _lockedBalance[adrs].amount;
    }
    function getLockedTime(address adrs) external view override returns(uint256) {
        return _lockedBalance[adrs].time;
    }
    function unlockBalance() external override {
        BalanceLock memory lock = _lockedBalance[_msgSender()];
        require(lock.amount > 0, "Token: No Balance is locked");
        uint256 stakingReward = calculateStake(lock.amount, lock.time);
        delete _lockedBalance[_msgSender()];
        if (stakingReward > 0)
            _mint(_msgSender(), stakingReward);
    }
    function test_lockBalance(uint256 amount, uint256 time) external {
        require(balanceOf(_msgSender()) >= amount, "Token: locking amount exceeds balance");
        require(_lockedBalance[_msgSender()].amount == 0, "Token: amount already locked");
        _lockedBalance[_msgSender()] = BalanceLock(amount, time);
    }
    function _beforeTokenTransfer(address from, address to, uint256 amount) internal view override {
        require(from == address(0) || balanceOf(from) >= amount, "ERC20: transfer amount exceeds balance");
    }
    function balanceOf(address account) public view override returns (uint256) {
        return super.balanceOf(account) - _lockedBalance[account].amount;
    }
    function calculateStake(uint256 amount, uint256 time) internal view returns(uint256) {
        return (((block.timestamp - time) / 86400) * stakingRate * amount) / 100000;
    }
}
