// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ProofStorage {
    mapping(uint256 => string) public proofs;

    // Store Proof for Customer
    function storeProof(uint256 customerId, string memory proof) public {
        proofs[customerId] = proof;
    }

    // Retrieve Proof for Customer
    function getProof(uint256 customerId) public view returns (string memory) {
        return proofs[customerId];
    }
}
