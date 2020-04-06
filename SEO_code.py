import urllib.request
from bs4 import BeautifulSoup
import sqlite3
import xlsxwriter

fu=open("URL.txt","r")#open the file containing URL
urll=fu.read().split("\n")#split it at each line
fi=open("ignore.txt",'r')#open the file containing ignore text
igl=fi.read().split(" ")#split each word
igls=set(igl)
workbook=xlsxwriter.Workbook('Results.xlsx')#create a workbook


w={}
for url in urll:
    print (url)
    req=urllib.request.Request(url,data=None,headers={'User-Agent':'Mozilla/5.0(Macintosh;Intel Mac OS X 10_9_3)AppleWebKit/537.36(KHTML,like Gecko) Chrome/35.0.1916.47 Safari/537.36'})
    f=urllib.request.urlopen(req)    
    soup=BeautifulSoup(f,"html.parser") # page containing html content
    print(soup.title)#prints title tag 
    print(soup.title.string)
    print(soup.meta)#prints meta tag 
    print(soup.meta.string)
    
    #Create a new bs4 object from html data loaded
    for script in soup(["script","style"]):
        script.extract()#removes all javascript and stylecoding

    #get text
    text=soup.get_text()
    
    #break the text to lines and remove digits,white spaces to get keywords
    line=list(x.strip().lower() for x in text.split())
    aline=[]
    for i in line:
        if i.isalpha()==1:#checkif it's true
            aline.append(i)#append it to list
        else:
            continue

    alines=set(aline)#get unique word
    fls=alines-igls#set without ignore word
    fl=list(fls)#convert it into a list
    fl.sort()#sort the words

#Create an excel to represent the results in chart
    f=url.split("//")[-1].split("/")[0]#get the domain name
    worksheet=workbook.add_worksheet(f)#create worksheet  with name  as  domain name
    
#Write the words and counts into apropriate format and to excel file
    u={}
    row=0
    for i in fl:#f1 is sorted list of words 
        c=aline.count(i)#to count of each word in f1 against alines
        den=(c/len(aline))*100#density of each word
        worksheet.write(row,0,i)#row with words
        worksheet.write(row,1,den)#row with density
        row+=1
        
        v={i:[c,den,url]}
    #build dictionary for words frequency and density
        u.update(v) 
        
    w.update(u)
    
#Plot the chart
    chart=workbook.add_chart({'type':'column'})
    sn='='+f#sheet name
    add1='!$A$1:$A$%i'%row
    add2='!$B$1:$B$%i'%row
    c=sn+add1
    v=sn+add2
    
    chart.add_series({'categories':(c),'values':(v)})
##x axis name
    chart.set_x_axis({'name':'Keywords','name_font':{'size':14,'bold':True},'num_font':{}})
##y axis name
    chart.set_size({'width':1280,'height':580})
    chart.set_title({'name':'SEO optimization results'})
    chart.set_y_axis({'name':'Density','name_font':{'size':14,'bold':True},'num_font':{},'major_gridlines':{'visible':False}})
    worksheet.insert_chart('D2',chart)
    
workbook.close()
