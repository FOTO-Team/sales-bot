import asyncio
import json
from web3 import Web3
import logging

logging.basicConfig(filename="std.log",format='%(asctime)s %(message)s',filemode='w')

logger=logging.getLogger()

logger.setLevel(logging.INFO)

# websockets url for Fantom-network
url = 'wss://ws.fantom.network/'

# opening abi file
abi_file = open('files/abi/abi.json')
abi = json.load(abi_file)
fotoAbi = json.load(open("files/abi/fotoabi.json"))
nftkeyabi = json.load(open("files/abi/nftkeyabi.json"))

#ps
address = '0x6125fD14b6790d5F66509B7aa53274c93dAE70B9'
fotoAddress = "0x93C7B19df2DeA70C7FA3f355F079d6ed077998A7"
nftkeyaddress = "0x1A7d6ed890b6C284271AD27E7AbE8Fb5211D0739"


class ListenEvents:
    def __init__(self):
        # connecting with the contract
        self.w3 = Web3(Web3.WebsocketProvider(url))
        #ps
        self.contract = self.w3.eth.contract(address=address, abi=abi)
        # FOTO
        self.foto = self.w3.eth.contract(address=fotoAddress,abi=fotoAbi)
        # NFTKEY
        self.nftkey = self.w3.eth.contract(address=nftkeyaddress,abi=nftkeyabi)

    def listingevent(self):
        try:
            self.listing = (self.contract.events.NewSale.getLogs(fromBlock='latest'))
            if self.listing:
                logger.info(self.listing)
                #print(self.listing[0])
                return self.listing[0]
        except Exception as e:
            print(e)

    def soldevent(self):
        try:
            self.onsold = (self.contract.events.Sold.getLogs(fromBlock='latest'))
            if self.onsold:
                logger.info(self.onsold)
                #print(self.onsold[0])
                return self.onsold[0]
        except Exception as e:
            print(e)
            
    def nftkeylistingevent(self):
        try:
            self.nftkeylisting = self.nftkey.events.TokenListed.getLogs(fromBlock="latest",argument_filters={'erc721Address': '0x93C7B19df2DeA70C7FA3f355F079d6ed077998A7'})
            if self.nftkeylisting:
                return self.nftkeylisting[0]
        except Exception as e:
            print(e)
            
    def nftkeysaleevent(self):
        try:
            self.nftkeysale = self.nftkey.events.TokenBought.getLogs(fromBlock="latest",argument_filters={'erc721Address': '0x93C7B19df2DeA70C7FA3f355F079d6ed077998A7'})
            if self.nftkeysale:
                return self.nftkeysale[0]
        except Exception as e:
            print(e)
    		
    def getfotoURI(self,tokenId):
        try:
            tokenURI = self.foto.functions.tokenURI(tokenId).call()
            if tokenURI:
                return tokenURI
        except Exception as e:
            print(e)
            
    def totalminted(self):
        try:
            minted = self.foto.events.FoxesOfTheOperaMinted.getLogs(fromBlock='latest')
            if minted:
        	    return minted[0].args.totalMinted
        except Exception as e:
            print(e)
        	
        
