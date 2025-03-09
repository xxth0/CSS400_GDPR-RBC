module.exports = {
    networks: {
        development: {
            host: "127.0.0.1",
            port: 7545, // Ensure Ganache is running on this port
            network_id: "5777"
        }
    },
    compilers: {
        solc: {
            version: "0.8.0",
            settings: {
                optimizer: {
                    enabled: true,
                    runs: 200
                }
            }
        }
    }
};
