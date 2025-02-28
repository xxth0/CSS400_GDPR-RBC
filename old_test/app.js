import Web3 from 'web3';
import bcrypt from 'bcrypt';
import express from 'express';
import 'dotenv/config';
import path from 'path';

const app = express();
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Connect to Ganache
const web3 = new Web3('http://127.0.0.1:7545');

// Import contract JSON
const contractData = await import('./build/contracts/eKYC.json', { assert: { type: 'json' } });
const contractABI = contractData.default.abi;
const contractAddress = process.env.CONTRACT_ADDRESS;

// Initialize the contract
const contract = new web3.eth.Contract(contractABI, contractAddress);

// Register user endpoint
app.post('/register', async (req, res) => {
    const { password } = req.body;
    const account = (await web3.eth.getAccounts())[0];

    try {
        const hashedPassword = await bcrypt.hash(password, 10); // Hash the password with a random salt
        await contract.methods.registerUser(hashedPassword).send({ from: account, gas: 3000000 });
        res.send({ success: true, message: 'User registered' });
    } catch (error) {
        console.error("Registration error:", error);
        res.status(500).send({ success: false, message: 'Registration failed' });
    }
});

// Verify user endpoint
app.post('/verify', async (req, res) => {
    const { password } = req.body;
    const account = (await web3.eth.getAccounts())[0];

    try {
        // Retrieve the stored hashed password from the contract
        const storedHashedPassword = await contract.methods.getUserPassword(account).call();


        // Compare the entered password with the stored hash
        const isVerified = await bcrypt.compare(password, storedHashedPassword);
        res.send({ success: isVerified, message: isVerified ? 'Login Successful' : 'Login Failed' });
    } catch (error) {
        console.error("Verification error:", error);
        res.status(500).send({ success: false, message: 'Verification failed' });
    }
});

// Serve the HTML file
app.get('/', (req, res) => {
    res.sendFile(path.join(process.cwd(), 'index.html'));
});

// Start server on port 3000
const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server running on http://localhost:${PORT}`);
});
