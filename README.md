# sales-bot

This bot gets sales and listings for FTM NFTs from Paintswap and NFTKey.

Get started:

1. Set up an ubuntu vps on a site like Digital Ocean or Vultr.

2. Open the cli. Make sure python is installed with python3 --version

3. Git clone this repositiory

4. From the cli on the ubuntu vps you set up, navigate into the repository you've git cloned

5. Add your discord token (including your the "")
   with: echo "your-discord-token" > token.txt

6. Install dependancies with: pip3 install -r requirements.txt

7. Edit the main.py file to include your contract address and the discord channel id's you'd like the bot to post in (you can edit it in the cli using "nano main.py". Make your changes and save/exit with ctrl+x). You need to edit the "address", "sellchannel", and "listingchannel" variables.

8. Start the bot with "python3 main.py". Your server must remaining running for the bot to work continuously.
