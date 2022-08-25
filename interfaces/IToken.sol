// interfaces/IToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IToken {
    function setStakingRate(uint256 rate) external;
    function setStakingEndTime(uint256 time) external;
    function lockBalance(uint256 amount) external;
    function getStakingReward(address adrs) external view returns(uint256);
    function getLockedBalance(address adrs) external view returns(uint256);
    function getLockedTime(address adrs) external view returns(uint256);
    function unlockBalance() external;
}
