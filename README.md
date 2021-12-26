# TPEX_StockBot
<p>
	<img src="https://img.shields.io/badge/-Python-61DAFB?logo=python&style=plastic">
	<img src="https://img.shields.io/github/license/WeiTaKuan/TPEX_StockBot">
	</p>

## Project description
This project fetch Taipei Exchange (TPEX) stock market data daily and use simple moving average strategy for scanning stock. After scanning, the potential stock list will be pushed to your Line Bot.

There are two packages in this project, which is StockScraping and StockScanning.
- StockScraping includes how to store historical stock price into mySQL database and run daily scraping task from TPEX open data.
- StockScanning provide a simple moving average method to scan different stock and push notification to your chat bot. Feel free to add your stratagies for filtering out next skyrocket stock

## License
Distrubuted under MIT License. See `LICENSE` for more information


