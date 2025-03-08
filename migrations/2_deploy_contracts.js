const Redact = artifacts.require("5-Redact");

module.exports = function (deployer) {
    // Deploy 5th SC: Redact
    deployer.deploy(Redact);
};
