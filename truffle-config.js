module.exports = {
    networks: {
        development: {
            host: "127.0.0.1",   // Ganache runs locally
            port: 7545,          // Default Ganache GUI port
            network_id: "*",     // Match any network ID
        }
    },
    compilers: {
        solc: {
            version: "0.8.20",  // Specify Solidity version
        }
    }
};
