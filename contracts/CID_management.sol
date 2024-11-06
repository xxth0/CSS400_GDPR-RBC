// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract BankCustomers {
    struct Customer {
        string hashedName;
        string encryptedSSN;
        uint256 accountNumber;
        uint256 balance;
    }

    struct CustomerBatch {
        uint batchId;
        Customer[] customers;
    }

    CustomerBatch[] public customerBatches;
    uint public currentBatchId = 1;

    // Add customers in batches
    function addCustomerBatch(Customer[] memory _customers) public {
        require(_customers.length == 100, "Batch must contain exactly 100 customers");

        CustomerBatch memory newBatch;
        newBatch.batchId = currentBatchId;
        currentBatchId++;

        for (uint i = 0; i < _customers.length; i++) {
            newBatch.customers.push(_customers[i]);
        }

        customerBatches.push(newBatch);
    }

    // Get customer data by batch and index
    function getCustomer(uint batchId, uint index) public view returns (Customer memory) {
        require(batchId < customerBatches.length, "Batch does not exist");
        require(index < 100, "Customer index out of range");
        return customerBatches[batchId].customers[index];
    }
}
