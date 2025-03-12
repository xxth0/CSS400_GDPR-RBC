const CustomerStorageFull = artifacts.require("CustomerStorageFull");
const ProofStorage = artifacts.require("ProofStorage");

module.exports = function (deployer) {
    deployer.deploy(CustomerStorageFull);
    deployer.deploy(ProofStorage);
};