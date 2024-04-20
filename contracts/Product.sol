// SPDX-License-Identifier: MIT
pragma solidity >=0.4.22 <0.9.0;

contract Product {
    string public users;
    string public product;
    string public order;
    string public history;

    function addUsers(string memory u) public {
        users = u;	
    }

    function getUsers() public view returns (string memory) {
        return users;
    }

    function addproduct(string memory ba) public {
        product = ba;	
    }

    function getproduct() public view returns (string memory) {
        return product;
    }

    function addorder(string memory ca) public {
        order = ca;
    }

    function getorder() public view returns (string memory) {
        return order;
    }

    function addhistory(string memory ra) public {
        history = ra;
    }

    function gethistory() public view returns (string memory) {
        return history;
    }

    constructor() public {
        users = "empty";
	product = "empty";
    order = "empty";
    history = "empty";
    
    }
}