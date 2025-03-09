// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CustomerStorageFull {
    struct CustomerTX {
        bytes32 chameleonHash; // Precomputed hash
        bytes32 encryptedNatID;
        bytes32 encryptedConsent;
        bytes32 encryptedCID;
        bytes32 encrypted_h_FI_ID;
        bytes32 encrypted_sig_FI_ID;
        address uploader;
        bool isRedacted; // Indicates whether this record has been redacted
    }

    mapping(uint256 => CustomerTX) public customerRecords;
    uint256 public customerCount;

    event CustomerAdded(uint256 indexed customerIndex, bytes32 chameleonHash);
    event CustomerRedacted(uint256 indexed customerIndex);

    constructor() {
        customerCount = 0;
    }

    function addCustomer(
        bytes32 chameleonHash,
        bytes32 encryptedNatID,
        bytes32 encryptedConsent,
        bytes32 encryptedCID,
        bytes32 encrypted_h_FI_ID,
        bytes32 encrypted_sig_FI_ID
    ) public {
        customerRecords[customerCount] = CustomerTX(
            chameleonHash,
            encryptedNatID,
            encryptedConsent,
            encryptedCID,
            encrypted_h_FI_ID,
            encrypted_sig_FI_ID,
            msg.sender,
            false // Default: not redacted
        );

        emit CustomerAdded(customerCount, chameleonHash);
        customerCount++;
    }

    function redactCustomer(uint256 customerIndex) public {
        require(customerIndex < customerCount, "Customer does not exist");
        require(!customerRecords[customerIndex].isRedacted, "Already redacted");

        // Set values to null (on-chain redaction)
        customerRecords[customerIndex].chameleonHash = bytes32(0);
        customerRecords[customerIndex].encryptedNatID = bytes32(0);
        customerRecords[customerIndex].encryptedConsent = bytes32(0);
        customerRecords[customerIndex].encryptedCID = bytes32(0);
        customerRecords[customerIndex].encrypted_h_FI_ID = bytes32(0);
        customerRecords[customerIndex].encrypted_sig_FI_ID = bytes32(0);
        customerRecords[customerIndex].isRedacted = true;

        emit CustomerRedacted(customerIndex);
    }

    function getCustomer(uint256 customerIndex) 
        public 
        view 
        returns (
            bytes32 chameleonHash,
            bytes32 encryptedNatID,
            bytes32 encryptedConsent,
            bytes32 encryptedCID,
            bytes32 encrypted_h_FI_ID,
            bytes32 encrypted_sig_FI_ID,
            address uploader,
            bool isRedacted
        ) 
    {
        require(customerIndex < customerCount, "Customer does not exist");

        CustomerTX storage customer = customerRecords[customerIndex];
        return (
            customer.chameleonHash,
            customer.encryptedNatID,
            customer.encryptedConsent,
            customer.encryptedCID,
            customer.encrypted_h_FI_ID,
            customer.encrypted_sig_FI_ID,
            customer.uploader,
            customer.isRedacted
        );
    }
}
