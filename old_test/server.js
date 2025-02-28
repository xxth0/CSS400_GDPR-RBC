const express = require('express');
const path = require('path');
const bodyParser = require('body-parser');
const Web3 = require('web3');
require('dotenv').config();

const app = express();
const web3 = new Web3('http://localhost:7545'); // Connect to local blockchain

const contractABI = /* Contract ABI here */;
const contractAddress = 'YOUR_CONTRACT_ADDRESS_HERE'; // Update with deployed address
const contract = new web3.eth.Contract(contractABI, contractAddress);

app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

app.post('/authenticate', async (req, res) => {
    const { username, password } = req.body;

    try {
        const isAuthenticated = await contract.methods.verifyUser(username, password).call();
        res.json({ authenticated: isAuthenticated });
    } catch (error) {
        res.status(500).json({ error: 'Authentication failed' });
    }
});

app.listen(3000, () => {
    console.log('Server running on http://localhost:3000');
});
