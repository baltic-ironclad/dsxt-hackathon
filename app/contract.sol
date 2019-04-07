pragma solidity >=0.4.22 <0.7.0;
contract Exchange{
    event TransferDollar(address indexed from, address indexed to, uint256 value);
    event TransferBitcoin(address indexed from, address indexed to, uint256 value);
    event Deal(address indexed from, address indexed to, uint256 val1, uint256 val2);
    mapping (address => uint256) public balanceDollars;
    mapping (address => uint256) public balanceBCS;
    mapping (address => uint256) public hash;
    
    function GiveHASH(uint256 a) public{
        hash[msg.sender] = a;
    }
    
    function transfer1(address _from, address _to, uint256 _value) internal{
        require(balanceDollars[_from]>=_value && balanceDollars[_to] + _value >= balanceDollars[_to]);
        balanceDollars[_from]-=_value;
        balanceDollars[_to] += _value;
        emit TransferDollar(_from, _to, _value);
    }
    function transfer2(address _from, address _to, uint256 _value) internal{
        require(balanceBCS[_from]>=_value && balanceBCS[_to] + _value >= balanceBCS[_to]);
        balanceBCS[_from]-=_value;
        balanceBCS[_to] += _value;
        emit TransferBitcoin(_from, _to, _value);
    }
    function exchange(address _from, address _with, uint256 val1, uint256 val2, uint256 hash1, uint256 hash2)public{
        require(hash1 == hash[_from] && hash2 == hash[_with], "Something went wrong");
        transfer1(_from, _with, val1);
        transfer2(_with, _from, val2);
        emit Deal(_from, _with, val1, val2);
    }
 }      
}      
