// contracts/VestingFunds.sol
// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.2 <0.9.0;

import "../node_modules/@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "../node_modules/@openzeppelin/contracts/access/Ownable.sol";
import "../interfaces/IVestingFunds.sol";

struct VestingInfo {
    uint256 total;
    uint256 released;
    uint256 startDuration;
    uint256 duration;
}

contract VestingFunds is ERC20, Ownable, IVestingFunds {
    mapping(address => VestingInfo) public _vesting;
    bool public cliffStarted = false;
    uint256 public cliffStartTime = 0;
    constructor(string memory Name, string memory Symbol) ERC20(Name, Symbol) {
    }
    function getTotalLockedBalance(address _address) public view override returns(uint256) {
        VestingInfo memory _vest = _vesting[_address];
        return _vest.total - _vest.released;
    }
    function startCliff() external override onlyOwner {
        require(!cliffStarted, "Cliff already started");
        cliffStarted = true;
        cliffStartTime = block.timestamp;
    }
    function getReleaseBalance(address _address) public view override returns(uint256) {
        return _getReleaseBalance(_address);
    }
    function release() external override {
        _release(_msgSender());
    }
    function balanceOf(address account) virtual public view override returns(uint256) {
        VestingInfo memory _vest = _vesting[account];
        return (super.balanceOf(account) + _vest.released) - _vest.total;
    }
    function addVesting(address _address, uint256 amount, uint256 startDuration, uint256 duration) external onlyOwner {
        require(amount > 0, "Amount cannot be 0");
        require(_address != address(0), "VestingWallet: beneficiary is zero address");
        require(_vesting[_address].total == 0, "VestingWallet: vesting already added for that beneficiary");
        _vesting[_address] = VestingInfo(amount, 0, startDuration, duration);
    }
    function _release(address _address) private {
        require(cliffStarted, "Cliff not started");
        VestingInfo storage _vest = _vesting[_address];
        require(_vest.total > 0, "VestingWallet: No Balance is vested");
        require(block.timestamp >= getStartTime(_vest.startDuration), "Vesting not started");
        uint256 balance = _getReleaseBalance(_address);
        require(balance > 0, "Nothing to release");
        require(_vest.released + balance <= _vest.total, "Released cannot be more than total");
        _vest.released += balance;
    }
    function _getReleaseBalance(address _address) private view returns (uint256) {
        if(!cliffStarted) return 0;
        VestingInfo memory _vest = _vesting[_address];
        uint256 startTime = getStartTime(_vest.startDuration);
        if(_vest.total == 0 || startTime > block.timestamp)
            return 0;
        if (block.timestamp > (startTime + _vest.duration))
            return _vest.total - _vest.released;
        else {
            return ((_vest.total * (block.timestamp - startTime)) / _vest.duration) - _vest.released;
        }
    }
    function getStartTime(uint256 startDuration) private view returns(uint256) {
        return startDuration + cliffStartTime;
    }
}
