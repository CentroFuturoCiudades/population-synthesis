#import conda libs
import pandas as pd
from glob import glob
import os
import requests
import numpy as np
from bs4 import BeautifulSoup

class Enigh:
    def __init__(self, filepath:str = '../data/ENIGH/2018/*.csv') -> None:
        self.filepath = filepath
        self.files = glob(filepath)

    def getDictionaryUrls(self) -> dict:
        """
        method to get all the links from the catalog of data dictonary of enigh
        and return a dictionary that map each file to each link
        """

        # URL of the catalog website
        url = "https://www.inegi.org.mx/rnm/index.php/catalog/511/data-dictionary"
        # Send an HTTP GET request to the website
        response = requests.get(url)
        # Parse the HTML code using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        urls =  []
        for tab in soup.find_all("tr",{"class":"data-file-row row-color1"}):
            try:
                urls.append(tab.find_all('a')[0].attrs["href"])
            except: 
                pass
        return {f:urls[list(map(lambda x: os.path.basename(f).split('.')[0] in x, urls)).index(True)] for f in self.files}

    def tansformData(self) -> None:
        """
        This method transform each file to the corresponding attribute value
        from the data dictionary link
        """
        #get the dictionary links for each file
        dictFiles = self.getDictionaryUrls()
        for k in dictFiles.keys():
            df = pd.read_csv(k)
            # Send an HTTP GET request to the website
            response = requests.get(dictFiles[k])
            # Parse the HTML code using BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            attDivs = soup.findAll('a', attrs={'class' : "var-id"})
            #get urls for each attribute
            urlsAtt = [attDivs[id].attrs["href"] for id in range(len(attDivs)) if id %2 == 0]
            #copy df file to str
            df_proc = df.copy().astype(str)
            for i in range (len(df.columns)-1):
                column = df_proc.columns[i+1]
                column_values = df_proc[column].unique()
                # Send an HTTP GET request to the website
                response = requests.get(urlsAtt[i+1])
                # Parse the HTML code using BeautifulSoup
                soup = BeautifulSoup(response.content, 'html.parser')
                try:
                    table = soup.find('table', class_='xsl-table')
                    items = list(table.find_all('td'))
                    items = [str(ix).replace("<td>", "").replace("</td>", "").strip() for ix in items]
                    digs = len(str(int(np.nanmax(pd.to_numeric(column_values, errors='coerce')))))
                    column_values_proc = [f'%0{digs}d'% int(x) for x in pd.to_numeric(column_values, errors='coerce') if not(np.isnan(x))]
                    mapping = {col : items[items.index(col_p)+1] 
                                    for col,col_p in zip(column_values, column_values_proc)}
                    df_proc[column] = df_proc[column].map(mapping)
                except:
                    pass
            df_proc.to_csv(k,index=False)