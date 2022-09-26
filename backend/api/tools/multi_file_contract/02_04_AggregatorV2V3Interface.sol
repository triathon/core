// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./03_04_AggregatorInterface.sol";
import "./04_04_AggregatorV3Interface.sol";

interface AggregatorV2V3Interface is AggregatorInterface, AggregatorV3Interface {}