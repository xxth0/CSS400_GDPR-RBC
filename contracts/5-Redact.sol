// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract CustomerStorage {
    struct CustomerTX {
        bytes32 chameleonHash; // Chameleon hash for redactable data
        bytes32 encryptedNatID;
        bytes32 encryptedConsent;
        bytes32 encryptedCID;
        bytes32 encrypted_h_FI_ID;
        bytes32 encrypted_sig_FI_ID;
        address uploader;
    }
    
    mapping(uint256 => CustomerTX) public customerRecords;
    uint256 public customerCount;
    
    event CustomerAdded(uint256 indexed customerIndex, bytes32 chameleonHash);
    event CustomerUpdated(uint256 indexed customerIndex, bytes32 newHash);

    function addCustomer(
        bytes32 encryptedNatID,
        bytes32 encryptedConsent,
        bytes32 encryptedCID,
        bytes32 encrypted_h_FI_ID,
        bytes32 encrypted_sig_FI_ID,
        bytes32 chameleonHash
    ) public {
        customerRecords[customerCount] = CustomerTX(
            chameleonHash,
            encryptedNatID,
            encryptedConsent,
            encryptedCID,
            encrypted_h_FI_ID,
            encrypted_sig_FI_ID,
            msg.sender
        );
        emit CustomerAdded(customerCount, chameleonHash);
        customerCount++;
    }
    
    function updateCustomerHash(uint256 customerIndex, bytes32 newChameleonHash) public {
        require(customerIndex < customerCount, "Customer does not exist");
        require(msg.sender == customerRecords[customerIndex].uploader, "Unauthorized");
        
        customerRecords[customerIndex].chameleonHash = newChameleonHash;
        emit CustomerUpdated(customerIndex, newChameleonHash);
    }
    
    function getCustomer(uint256 customerIndex) public view returns (CustomerTX memory) {
        require(customerIndex < customerCount, "Customer does not exist");
        return customerRecords[customerIndex];
    }
}
