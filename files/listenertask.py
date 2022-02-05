import discord
from discord.ext import commands, tasks
from files import eventlistener
import asyncio

class botcmnds(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self.start_listener.start()
		self.b = eventlistener.ListenEvents()
	
	@tasks.loop()
	async def start_listener(self):
		p = await asyncio.to_thread(self.b.listingevent)
		if p is not None:
			await asyncio.sleep(5)
			#print("Listing dispatch")
			self.bot.dispatch("listing",p)
			
		q = await asyncio.to_thread(self.b.soldevent)
		if q is not None:
			await asyncio.sleep(5)
			#print("Sold dispatch")
			self.bot.dispatch("sold",q)
			
		nftkey = await asyncio.to_thread(self.b.nftkeylistingevent)
		if nftkey is not None:
			URI = self.b.getfotoURI(nftkey.args["tokenId"])
			await asyncio.sleep(5)
			#print("Listing on NFT key")
			self.bot.dispatch("nftkeylisting",nftkey,URI)
			
		nftkeysold = await asyncio.to_thread(self.b.nftkeysaleevent)
		if nftkeysold is not None:
			URI = self.b.getfotoURI(nftkeysold.args["tokenId"])
			#print("Sold on NFT key")
			self.bot.dispatch("nftkeysale",nftkeysold,URI)
			
		totalminted = self.b.totalminted()
		if totalminted:
			print(totalminted)
			await self.bot.change_presence(status=discord.Status.dnd,activity=discord.Activity(type=discord.ActivityType.watching,name=f'foxes {totalminted}/10000'))
	
	@start_listener.before_loop
	async def before_printer(self):
		print("Waiting...")
		await self.bot.wait_until_ready()
		
		
def setup(bot):
	bot.add_cog(botcmnds(bot))