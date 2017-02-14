#! /usr/bin/env python

import requests
from bs4 import BeautifulSoup
from datetime import datetime
from dateutil.parser import parse

# This script makes a file on disk called: Swift_LCs.html


############################################################################################

import argparse

desc="""Script to scrape Swift LAT-monitored sources web site 
and make a new page with a table of objects, reverse sorted by
date, and showing the results of the last observation."""


parser = argparse.ArgumentParser(description=desc, 
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument('-o', '--outfile', 
                    type=str, 
                    default="Swift_LCs.html",  
                    help='name of output html file')

parser.add_argument('-c','--cts', 
                    action='store_true', 
                    help='get the cts/s for the previous observation (slow!)')

parser.add_argument('-l','--limit', 
                    type=int,
                    default=0,
                    help="limit to objects that have updated in last n days, 0 to turn off")


parser.add_argument('-q','--quiet', 
                    action='store_true', 
                    help="don't print out to screen")


cfg = parser.parse_args()

#if not cfg.verbose and not cfg.file and not cfg.mod_date:
#    parser.error("Please select options -v and/or -f or -m. Option -h for detailed help.")




############################################################################################


def process_cells(cells):
    if len(cells)>5:
        name=cells[1].getText().strip()
        if name=="Target":
            return
        link=URL+cells[1].find('a').get('href')
        datetmp=cells[5].getText().strip()
        date=parse(datetmp)
        

        if cfg.limit and (datetime.today() - date).days > cfg.limit:
            pass
        else:
            data.append((name, date.date(), link))



def get_last_cts(name):
    name=name.replace(" ","")
    LC_URL="http://www.swift.psu.edu/monitoring/data/"+name+"/lightcurve.txt"
    r=requests.get(LC_URL)
    last=r.text.split("\n")[-2].split() # split into lines, take 2nd last and split fields
    return(float(last[2]))  



def make_html_string(data, get_cts=True):
    "data is expected to be a list of tuples of format (Name, date, URL)"

    str="""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
            margin-left: auto;
            margin-right: auto;
        }
        th, td {
            padding: 5px;
            text-align: left;
        }
    </style>
    </head>
    """

    str+="""
    <h1 align="center"> Swift LAT-monitored sources</h1>
    <body>
    <p align="center"> Original site: <a href="{0}">{0}</a></p>
    <p align="center"> Time of last update of this page: UT {1:%Y-%m-%d %H:%M} </p>
    """.format(URL,datetime.utcnow())

    if(cfg.limit):
        str+="""   <p align="center"> Limited to objects with updates in last {} days </p>""".format(cfg.limit)
        


    str+="""
    <table style="width:50%">
    <tr>
        <th> Object </th>
        <th> Last Observation </th>
        <th> Last ct/s </th>
    </tr>
    """

    for d in data:
        link="""<a href="{}"> {} </a>""".format(d[2],d[0])
        
        if get_cts:
            last_cts="{:.2f}".format(get_last_cts(d[0]))
        else:
            last_cts="-"

        str+="""
        <tr> 
            <td> {} </td>
            <td> {} </td>
            <td> {} </td> 
        </tr>
        """.format(link, d[1], last_cts)
    
    str+="""
    </table>
    </body>
    </html>
    """

    return str





URL="http://www.swift.psu.edu/monitoring/"
page=requests.get(URL)
soup=BeautifulSoup(page.content,'lxml')
table=soup.findAll("table")


data=[]

for row in table[2].findAll("tr"):
    cells=row.findAll("td")
    process_cells(cells)

for row in table[3].findAll("tr"):
    cells=row.findAll("td")
    process_cells(cells)


data_sorted=sorted(data, key=lambda d: d[1], reverse=True) 

#for d in data_sorted:
#    print("{:20s} {}  {}".format(d[0], d[1], d[2]))


s=make_html_string(data_sorted,get_cts=cfg.cts)

with open(cfg.outfile,"w") as f:
    f.write(s)



