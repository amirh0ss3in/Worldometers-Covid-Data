"""
MIT License

Copyright (c) 2021 amirh0ss3in

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
© 2021 GitHub, Inc.

"""


#########################################################

# A package to get the COVID-19 data using Worldometers #

#########################################################


"""
Developed by Amirhossein Rezaei

"""

import requests
from bs4 import BeautifulSoup as bs
import numpy as np 
import matplotlib.pyplot as plt 
import matplotlib
from datetime import datetime

# Returns the list of available countries from href
def countries():
    url = "https://www.worldometers.info/coronavirus/"
    r = requests.get(url)
    htmlcontent = r.content
    soup = str(bs(htmlcontent, "html.parser"))
    c = []
    for i in range(1,223):
        n = soup.find(f'<td style="font-size:12px;color: grey;text-align:center;vertical-align:middle;">{i}</td>')
        n2 = soup[n:].find('href="country/')
        m = soup[n+n2:].find('">')
        c.append(soup[n+n2+14:n+n2+m-1])
    return c

# Returns the dates of X-axis
def dates(country):
    url = f"https://www.worldometers.info/coronavirus/country/{country}/"
    r = requests.get(url)
    htmlcontent = r.content
    soup = str(bs(htmlcontent, "html.parser"))
    n = soup.find("xAxis: {")
    n2 = soup[n:].find("categories: [")
    m = soup[n+n2+13:].find(']')    
    data = np.array(soup[n+n2+13:n+n2+13+m].split('","'))
    data[0] = data[0].replace('"','')
    data[-1] = data[-1].replace('"','')
    data = np.array([datetime.strptime(i.replace(',',''), '%b %d %Y') for i in data])
    return data

# Plotting Function
def plot(data ,country, caption):
    fontsize = 10
    csfont = {'fontname':'Times New Roman'}
    ds = matplotlib.dates.date2num(dates(country))
    plt.plot_date(ds, data,'.-')
    plt.xlabel(f'{len(data)} Days since the beginning of the COVID-19 Pandemic in {str(country).upper()}',fontsize=fontsize, fontweight='bold',**csfont)
    plt.ylabel(f'{caption}',fontsize=fontsize, fontweight='bold',**csfont)
    plt.tight_layout()
    plt.show()

# Daily New Cases
def DNC(country,Plot = False):
    url = f"https://www.worldometers.info/coronavirus/country/{country}/"
    r = requests.get(url)
    htmlcontent = r.content
    soup = str(bs(htmlcontent, "html.parser"))
    n = soup.find("name: 'Daily Cases',")
    n2 = soup[n:].find("data:")
    m = soup[n:].find(']')
    data = np.array(soup[n+n2+7:n+m].replace('null','0').split(','),dtype=int)
    if Plot == True:
        plot(data, country, caption='Daily new Cases')
    return data

# Daily New Deaths
def DND(country,Plot = False):
    url = f"https://www.worldometers.info/coronavirus/country/{country}/"
    r = requests.get(url)
    htmlcontent = r.content
    soup = str(bs(htmlcontent, "html.parser"))
    n = soup.find("name: 'Daily Deaths',")
    n2 = soup[n:].find("data:")
    m = soup[n:].find(']')
    data = np.array(soup[n+n2+7:n+m].replace('null','0').split(','),dtype=int)
    if Plot == True:
        plot(data, country, caption='Daily new Deaths')
    return data

# Total Cases
def TC(country,Plot = False):
    data = np.cumsum(DNC(country))
    if Plot == True:
        plot(data,country,caption='Total Cases')
    return data    

# Total Deaths
def TD(country,Plot = False):
    data = np.cumsum(DND(country))
    if Plot == True:
        plot(data,country,caption='Total Deaths')
    return data
    
def main():
    
    # Plot the 'Daily New Cases'
    DNC('iran',True)

    # Plot the 'Daily New Deaths'
    DND('iran',True)

    # Plot the 'Total Cases'
    TC('iran',True)

    # Plot the 'Total deaths' 
    TD('iran',True)

    # Print the 'Daily New Cases' array of the first three countries from the available countries 
    for i in range(3):
        print('Country:',countries()[i],'\nDaily New Cases',DNC(countries()[i]))

    pass

if __name__ == '__main__':
    main()