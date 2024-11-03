const Web3 = require('web3');
const web3 = new Web3('http://localhost:8545'); // Connect to local blockchain
const contractABI = /* Contract ABI here */;
const contractAddress = 'YOUR_CONTRACT_ADDRESS_HERE'; // Update with deployed address

const contract = new web3.eth.Contract(contractABI, contractAddress);

document.getElementById('auth-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Sample verification process (replace with proper hashing and contract call)
    const isAuthenticated = await contract.methods.verifyUser(username, password).call();

    if (isAuthenticated) {
        document.getElementById('consent-status').innerText = "Authenticated and consent verified!";
    } else {
        document.getElementById('consent-status').innerText = "Authentication failed.";
    }
});
