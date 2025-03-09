// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CustomerStorageOffChain {
    struct CustomerHash {
        bytes32 chameleonHash;
        address uploader;
    }

    mapping(uint256 => CustomerHash) public customerHashes;
    uint256 public customerCount;

    event CustomerHashStored(uint256 indexed customerIndex, bytes32 chameleonHash);

    constructor() {
        customerCount = 0;
    }

    function storeCustomerHash(bytes32 chameleonHash) public {
        customerHashes[customerCount] = CustomerHash(
            chameleonHash,
            msg.sender
        );

        emit CustomerHashStored(customerCount, chameleonHash);
        customerCount++;
    }

    function getCustomerHash(uint256 customerIndex) 
        public 
        view 
        returns (
            bytes32 chameleonHash,
            address uploader
        ) 
    {
        require(customerIndex < customerCount, "Customer does not exist");

        CustomerHash storage customer = customerHashes[customerIndex];
        return (
            customer.chameleonHash,
            customer.uploader
        );
    }
}
