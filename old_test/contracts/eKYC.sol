// Solidity contract for storing user passwords
pragma solidity ^0.8.0;

contract eKYC {
    mapping(address => string) private userPasswords;

    // Register user with hashed password
    function registerUser(string memory hashedPassword) public {
        require(bytes(userPasswords[msg.sender]).length == 0, "User already registered");
        userPasswords[msg.sender] = hashedPassword;
    }

    // Verify user by checking hashed password
    function verifyUser(string memory hashedPassword) public view returns (bool) {
        require(bytes(userPasswords[msg.sender]).length != 0, "User not registered");
        return keccak256(abi.encodePacked(userPasswords[msg.sender])) == keccak256(abi.encodePacked(hashedPassword));
    }

    // Getter function to retrieve hashed password
    function getUserPassword(address user) public view returns (string memory) {
        require(bytes(userPasswords[user]).length != 0, "User not registered");
        return userPasswords[user];
    }
}
