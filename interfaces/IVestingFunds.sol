// interfaces/IVestingFunds.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

interface IVestingFunds {
    function getTotalLockedBalance(address _address) external view returns(uint256);
    function startCliff() external;
    function getReleaseBalance(address _address) external view returns(uint256);
    function release() external;
}
