const eKYC = artifacts.require("eKYC");

module.exports = function (deployer) {
    deployer.deploy(eKYC);
};
