import os
import subprocess
import pandas as pd
import numpy as np
import datetime


class itch():
  
  def __init__(self, file, msg):
    self.file = file
    self.date = file.split('.')[0]
    self.msg = msg
    
    
  def get_record(self):
    csvfile = str(self.date)+'-'+str(self.msg)+'.csv'
    if not os.path.exists(os.path.join('.', 'output', csvfile)): 
      subprocess.check_output(['clang -O2 ./itch5parser/parse_itch5.c -o ./itch5parser/parse_itch5'], shell=True) 
      subprocess.check_output(['./itch5parser/parse_itch5 ./'+str(self.file)+' ./output '+str(self.msg)], shell=True)
      
    dataframe = pd.read_csv(os.path.join('.', 'output', csvfile), header=None)
    print('./output/'+csvfile+' has been saved locally.')
    
    return dataframe
           
  def cal_vwap(self, df):
    if self.msg == 'P':
      df.columns = ['message type', 'stock locate', 'tracking number','timestamp', 'order reference number', 'buy/sell indicator', 'shares', 'stock', 'price', 'match number']
      df['amount'] = df['price'] * df['shares']
      df['hour'] = df['timestamp'].apply(lambda x: datetime.datetime.fromtimestamp(x)).dt.hour
      cols = ['amount', 'shares']
      df[cols] = df[cols].astype(float)
      df = df.groupby([df['hour'], df['stock']])['amount', 'shares'].sum()
      df['vwap'] = (df['amount'] / df['shares']).round(2)
      df = df.reset_index()
      df = df[['hour', 'stock', 'vwap']]
      return df
    else:
      return ("Oops! The message type is not 'P'.")
  
  
  def write_vwap_bystock(self, df):
    if self.msg == 'P':
      if not os.path.exists(os.path.join('.', 'output','bystock')):
        os.makedirs(os.path.join('.', 'output','bystock'))
      
      for stock in df.stock.unique():
        df1 = df.loc[df['stock'] == stock]
        df1.sort_values('hour', inplace = True)
        df1.to_csv(os.path.join('.', 'output', 'bystock', stock + '.txt'), sep=' ', index=False)
    else:
      return ("Oops! The message type is not 'P'.")
    
      
      
  def write_vwap_byhour(self, df):
    if self.msg == 'P':
      if not os.path.exists(os.path.join('.', 'output','byhour')):
        os.makedirs(os.path.join('.', 'output','byhour'))
        
      df['hour'] = df['hour'].astype(str)
      
      for hour in df.hour.unique():
        df1 = df.loc[df['hour'] == hour]
        df1.sort_values('stock', inplace = True)
        df1.to_csv(os.path.join('.', 'output', 'byhour', hour + '.txt'), sep=' ', index=False)
    else:
      return ("Oops! The message type is not 'P'.")
        
if __name__ == '__main__': 
  itch = itch('01302019.NASDAQ_ITCH50', 'P') ## get the trade message -- message type : p
  df = itch.get_record()  ## get data of the specific message
  df_vwap = itch.cal_vwap(df) ## calculate vwap
  itch.write_vwap_bystock(df_vwap) ## save vwap by stock
  itch.write_vwap_byhour(df_vwap) ## save vwap by hour
