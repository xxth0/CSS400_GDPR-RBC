const CustomerStorageFull = artifacts.require("CustomerStorageFull");


module.exports = function (deployer) {
    deployer.deploy(CustomerStorageFull);
};
