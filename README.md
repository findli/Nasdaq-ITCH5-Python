# Nasdaq-ITCH5-Python


## Parser
Considering the large amount of daily Nasdaq trading data, the speed is very essential. I improve the Python parsing speed for Nasdaq daily trading data (10 GB each) by wrapping a [C parser](https://github.com/shawfdong/itch5parser)  (with MIT license).

In addtion, I provide two functions to calculate and output the running volume-weighted average price (VWAP) for each stock at every trading hour.


## Dataset
Download raw ITCH 5.0 data from ```ftp://emi.nasdaq.com/ITCH/01302019.NASDAQ_ITCH50.gz```. Copy it into the folder.

The data format is defined by the document [Nasdaq TotalView-ITCH 5.0](http://www.nasdaqtrader.com/content/technicalsupport/specifications/dataproducts/NQTVITCHspecification.pdf).


## Run Code
Run the following command in the terminal.

```
python3 parser.py
```

Please make sure Python3 with packages  ```os```, ```subprocess```, ```numpy```, ```pandas```, and ```datetime``` have installed.


## Output
The code would generate two ouput folders: VWAP  ```bystock```  and  ```byhour``` .


