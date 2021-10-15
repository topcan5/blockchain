// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

contract SimpleStorage {
    // integer with size of 256 bits.
    // by default variable is internal.
    // uint256 public favoriteNumber;
    uint256 favoriteNumber;
    // bool flag = true;
    // string word = 'okok';
    // address adr2 = 0x5e3Dc05e0Ef44dF054599bB7E3A92b9942D19F66;
    struct People {
        uint256 favoriteNumber;
        string name;
    }
    
    // People public people = People({favoriteNumber: 5, name: 'ge song'});
    
    // array
    People[] public people;
    // like hashmap
    mapping(string => uint256) public nameToFavoriteNumber;
    
    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }
    
    // view and pure don't start a transaction.
    function retrieve() public view returns (uint256){
        return favoriteNumber;
    }
    
    // // pure: just do some math.
    // function retrieve2() public pure {
    //     favoriteNumber = 1 + favoriteNumber;
    // }
    
    // memory: just in this transaction
    // storage: live forever
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People(_favoriteNumber, _name));
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }
}