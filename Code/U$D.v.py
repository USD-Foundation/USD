# U$D Token Implementation

# Author: Samuel Troper

# Based upon code from:
    # Solidity-Compatible EIP20/ERC20 Token
    # Implements https://github.com/ethereum/EIPs/blob/master/EIPS/eip-20-token-standard.md
    # Author: Phil Daian

# Key notes:

    # U$D is programatically similar to ETH, in that 1 ETH = 10^18 Wei, and 1 Wei is atomistic.

    # 1 U$D = 10^18 Salmon (Named for Salmon P. Chase)

# Need to add external calls to governance contracts

# Events issued by the contract
Transfer: event({_from: indexed(address), _to: indexed(address), _value: uint256(Salmon)})
Approval: event({_owner: indexed(address), _spender: indexed(address), _value: uint256(Salmon)})

governance_address: address
backup_address: address
def __init__():
    governance_address = [[need to add]]
    backup_address = [[need to add]]
    restrict_inputs = False

def setGovernanceAddress(newAddress: address):
    assert msg.sender == governance_address or msg.sender == backup_address
    governance_address = newAddress

def setBackupAddress(newAddress: address):
    assert msg.sender == governance_address or msg.sender == backup_address
    backup_address = newAddress

#          amount [Token  ][Owner  ]
USDIssued: uint256[address][address]

# Maps approval based upon addresses of other ERC-20 tokens.
tokens {
    approved: bool
    number_comprising_one_Salmon: uint256
    weight: uint256
}[address]
# [[need to add update tokens]]

# A mapping which uses the first number_of_approved_tokens indices to provide
# what is functionally a variable sized array.
approvedTokenAddress: address[uint256]
number_of_approved_tokens: uint256
totalWeight: uint256

def inflate():
    # [[code]]

def deflate():
    # [[code]]

inflationTokens: uint256(salmon)
tokensDeflated: uint256(salmon)

#need to add approve functionality

flexNumerator: uint256
flexDenominator: uint256

# A boolean which restricts inputs. This is to prevent the token
# from "freezing" at initiation when it has no backing,
# which would lead to some errors.
restrict_inputs: bool

balances: uint256(Salmon)[address]
allowances: (uint256(Salmon)[address])[address]
num_issued: uint256(Salmon)

@public
def issue(tokenAddress: address):
    # [[NEED TO TRANSFER]]
    assert self.tokens[tokenAddress].approved
    _sender: address = msg.sender
    _allowance: #[[load allowances here]]
    _maxIssue: maxIssueAllowed[tokenAddress]
    amountToIssue: uint256(salmon) = min(_allowance/self.tokens[address].number_comprising_one_Salmon, _maxIssue)
    self.balances[_sender] = self.balances[_sender] + amountToIssue
    self.num_issued = self.num_issued + amountToIssue
    # Fire issue event as transfer from 0x0
    log.Transfer(0x0000000000000000000000000000000000000000, _sender, amountToIssue)

@public
def maxIssueAllowed(tokenAddress: address) -> uint256(salmon):
    #[[load amount owned]]
    salmonsSupported: uint256(salmon) = amountOwned/self.tokens[address].number_comprising_one_Salmon #[[check if this will stop the calculation with divide by zero]]
    maxPercentage: decimal = (1 + flexNumerator/flexDenominator) * self.tokens[address].weight/totalWeight
    currentPercentage: decimal = salmonsSupported/(self.num_issued-inflationTokens+tokensDeflated)
    return (maxPercentage-currentPercentage)*self.num_issued

def maxWithdrawalAllowed(tokenAddress: address) -> uint256:
    #[[load amount owned]]
    salmonsSupported: uint256(salmon) = amountOwned/self.tokens[address].number_comprising_one_Salmon #[[check if this will stop the calculation with divide by zero]]
    minPercentage: decimal = (1 - flexNumerator/flexDenominator) * self.tokens[address].weight/totalWeight
    currentPercentage: decimal = salmonsSupported/(self.num_issued-inflationTokens+tokensDeflated)
    return (currentPercentage-minPercentage)*self.num_issued

@public
def withdraw(_value : uint256(Salmon), tokenAddress:address) -> bool:
    assert self.tokens[tokenAddress].approved
    _sender: address = msg.sender
    _maxWithdrawal: uint256(salmon) = maxWithdrawalAllowed(tokenAddress)
    # Make sure sufficient funds are present implicitly through overflow protection
    amountToWitdraw: uint256(salmon) = min(_value, _maxWithdrawal)
    self.balances[_sender] = self.balances[_sender] - _value
    self.num_issued = self.num_issued - _value
    # [[NEED TO TRANSFER]]
    # Fire withdraw event as transfer to 0x0
    log.Transfer(_sender, 0x0000000000000000000000000000000000000000, _value)
    return True

@public
@constant
def totalSupply() -> uint256(Salmon):
    return self.num_issued

@public
@constant
def balanceOf(_owner : address) -> uint256(Salmon):
    return self.balances[_owner]

@public
def transfer(_to : address, _value : uint256(Salmon)) -> bool:
    _sender: address = msg.sender
    # Make sure sufficient funds are present implicitly through overflow protection
    self.balances[_sender] = self.balances[_sender] - _value
    self.balances[_to] = self.balances[_to] + _value
    # Fire transfer event
    log.Transfer(_sender, _to, _value)
    return True

@public
def transferFrom(_from : address, _to : address, _value : uint256(Salmon)) -> bool:
    _sender: address = msg.sender
    allowance: uint256(Salmon) = self.allowances[_from][_sender]
    # Make sure sufficient funds/allowance are present implicitly through overflow protection
    self.balances[_from] = self.balances[_from] - _value
    self.balances[_to] = self.balances[_to] + _value
    self.allowances[_from][_sender] = allowance - _value
    # Fire transfer event
    log.Transfer(_from, _to, _value)
    return True

@public
def approve(_spender : address, _value : uint256(Salmon)) -> bool:
    _sender: address = msg.sender
    self.allowances[_sender][_spender] = _value
    # Fire approval event
    log.Approval(_sender, _spender, _value)
    return True

@public
@constant
def allowance(_owner : address, _spender : address) -> uint256(Salmon):
    return self.allowances[_owner][_spender]
