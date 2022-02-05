from datetime import datetime
import discord
from discord.ext import commands
import requests as req
from web3 import Web3
import base64
import ast

address = '0x93C7B19df2DeA70C7FA3f355F079d6ed077998A7'

'''mychannels
sellchannel = 934838447154298931
listingchannel = 936303447093956648'''
#prod channels
sellchannel = 933916357886623747
listingchannel = 936297568286175232
# bot prefix
intents = discord.Intents.default()
intents.members = True
intents.presences = True
intents.messages = True
intents.all()

bot = commands.Bot(command_prefix='!-!', intents=intents, status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.watching,name="Foxes"))


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_listing(p):
	try:
		channel = bot.get_channel(listingchannel)
		apidata = req.get(f'https://api.paintswap.finance/nft/{p.args.nfts[0]}/{p.args.tokenIds[0]}?numToFetch=1')
		api_data = apidata.json()
		#print(api_data)
		uri = api_data['nft']['uri']
		contractaddress = api_data['nft']['address']
		#print(uri)
		if uri.startswith('ipfs://'):
			replaced_uri = uri.replace('ipfs://', 'https://cf-ipfs.com/ipfs/')
			#print(replaced_uri)
		else:
			replaced_uri = uri
		if 'base64' not in uri:
			uri_data = req.get(replaced_uri)
			#print(uri_data)
			image_link = uri_data.json()['image']
			if image_link.startswith('ipfs://'):
				image: str = image_link.replace('ipfs://', 'https://cf-ipfs.com/ipfs/')
			else:
				image: str = image_link
		elif 'base64' in uri:
			image = None
		else:
			pass

		embed = discord.Embed(title=p.args.searchKeywords, color=discord.Colour.random(),url=f'https://paintswap.finance/marketplace/{p.args.marketplaceId}')
		embed.add_field(name='Price', value=f'`{Web3.fromWei(p.args.price,"ether")} FTM`')
		embed.set_footer(text=f"Listed on Paintswap • {datetime.utcnow().strftime('%I:%M %p')}", icon_url='https://cdn.discordapp.com/attachments/934838447154298931/935931569691037696/a_e314d937b5a1ab1dc394191d346144d8.png')
		if image is not None:
			embed.set_thumbnail(url=image)
		if contractaddress == address.lower():
			await channel.send(embed=embed)
			print("Sent Listing")
	except Exception as e:
		print(e)


@bot.event
async def on_sold(g):
	try:
		channel = bot.get_channel(sellchannel)
		apidata = req.get(f'https://api.paintswap.finance/nft/{g.args.nfts[0]}/{g.args.tokenIds[0]}?numToFetch=1')
		api_data = apidata.json()
		#print(api_data)
		uri = api_data['nft']['uri']
		contractaddress = api_data['nft']['address']
	#	print(uri)
		if uri.startswith('ipfs://'):
			replaced_uri = uri.replace('ipfs://', 'https://cf-ipfs.com/ipfs/')
	#		print(replaced_uri)
		else:
			replaced_uri = uri
		if 'base64' not in uri:
			uri_data = req.get(replaced_uri)
			name = uri_data.json()['name']
	#		print(uri_data)
			image_link = uri_data.json()['image']
			if image_link.startswith('ipfs://'):
				image: str = image_link.replace('ipfs://', 'https://cf-ipfs.com/ipfs/')
			else:
				image: str = image_link
		elif 'base64' in uri:
			name = (ast.literal_eval(base64.b64decode(uri[28:]).decode('utf-8'))["name"])
			image = None
		
		embed = discord.Embed(title=name, color=discord.Colour.random(),url=f'https://paintswap.finance/marketplace/{g.args.marketplaceId}')
		embed.add_field(name='Price', value=f'`{Web3.fromWei(g.args.price, "ether")} FTM`',inline=False)
		embed.add_field(name="Buyer",value=f'[{g.args.buyer[:6]}...{g.args.buyer[-5:]}](https://paintswap.finance/marketplace/user/{g.args.buyer})')
		embed.add_field(name="Seller",value=f'[{g.args.seller[:6]}...{g.args.seller[-5:]}](https://paintswap.finance/marketplace/user/{g.args.seller})')
		embed.set_footer(text=f"Sold on Paintswap • {datetime.utcnow().strftime('%I:%M %p')}",icon_url='https://cdn.discordapp.com/attachments/934838447154298931/935931569691037696/a_e314d937b5a1ab1dc394191d346144d8.png')
		if image is not None:
			embed.set_image(url=image)
		if contractaddress == address.lower():
			await channel.send(embed=embed)
			print("Sent Sold")
	except Exception as e:
		print(e)
		

@bot.event
async def on_nftkeylisting(nftkey,uri):
	channel = bot.get_channel(listingchannel)
	try:
		replaced = uri.replace("ipfs://","https://mypinata.cloud/ipfs/")
		data = req.get(replaced)
		image_link = data.json()["image"]
		image = image_link.replace("ipfs://","https://mypinata.cloud/ipfs/")
		embed = discord.Embed(title=f"Fox #{nftkey.args['tokenId']}", color=discord.Colour.random(),url=f'https://nftkey.app/collections/foxesoftheopera/token-details/?tokenId={nftkey.args.tokenId}')
		embed.add_field(name='Price', value=f'`{Web3.fromWei(nftkey.args.listing[1],"ether")} FTM`')
		embed.set_footer(text=f"Listed on NFT Key • {datetime.utcnow().strftime('%I:%M %p')}",icon_url="https://media.discordapp.net/attachments/621609685539225622/938406616112447528/icon-384x384.png")
		embed.set_thumbnail(url=image)
		print("sent nft key listing")
		await channel.send(embed=embed)
	except Exception as e:
		print(e)
		
@bot.event
async def on_nftkeysale(nftkey,uri):
	channel = bot.get_channel(sellchannel)
	try:
		replaced = uri.replace("ipfs://","https://mypinata.cloud/ipfs/")
		data = req.get(replaced)
		image_link = data.json()["image"]
		image = image_link.replace("ipfs://","https://mypinata.cloud/ipfs/")
		embed = discord.Embed(title=f"Fox #{nftkey.args['tokenId']}", color=discord.Colour.random(),url=f'https://nftkey.app/collections/foxesoftheopera/token-details/?tokenId={nftkey.args.tokenId}')
		embed.add_field(name='Price', value=f'`{Web3.fromWei(nftkey.args.listing[1],"ether")} FTM`')
		embed.set_footer(text=f"Sold on NFT Key • {datetime.utcnow().strftime('%I:%M %p')}",icon_url="https://media.discordapp.net/attachments/621609685539225622/938406616112447528/icon-384x384.png")
		embed.set_image(url=image)
		print("sent nft key sold")
		await channel.send(embed=embed)
	except Exception as e:
		print(e)
		

if __name__ == "__main__":
    bot.load_extension("files.listenertask")


bot.run("OTM2NTYxNDEyNTE4NTc2MTU5.YfO-yQ.rmHre8XCOV7nTUbljLMj-VYA0a4")
