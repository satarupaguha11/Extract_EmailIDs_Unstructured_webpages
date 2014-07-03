from bs4 import BeautifulSoup
import urllib
import urllib2
import re


def extractFromEachPage(page):
    sock=urllib.urlopen(page)
    doc=sock.read()
    soup = BeautifulSoup(''.join(doc))


    allTags = soup.findAll(True)
    #finding name of the business
    title=soup.find('title').text
    

    #finding phone number
    flag=0
    for i in range(len(allTags)):
        if allTags[i].name=="span" and allTags[i].attrs.keys()==[u'id', u'itemprop'] and allTags[i].attrs.values()==[u'bizPhone', u'telephone']:
            phone=allTags[i].text
            flag=1
    if flag==0:
        phone="NULL"
    

    #finding home page URL
    flag=0
    for i in range(len(allTags)):
        if allTags[i].name=="div" and allTags[i].attrs.keys()==[u'id'] and allTags[i].attrs.values()==[u'bizUrl']:
            a=allTags[i].findChild().attrs.values()[0]
            b=a.split('http')
            k='http'+b[1]
            c=k.split('&')
            url=urllib.unquote(c[0])
            flag=1
    if flag==0:
        url="NULL"
        
      
          
    #finding contact page URL
    flag=0
    contact="NULL"
    email_id="NULL"
    try:
        if url!="NULL":
            #trying to open url using urllib. If it throws exception, then using urllib2
            try:
                sock2=urllib.urlopen(url)
                doc2=sock2.read()
                soup2=BeautifulSoup(doc2)
            except:
                
                try:
                    sock2=urllib2.urlopen(url)
                    doc2=sock2.read()
                    soup2=BeautifulSoup(''.join(doc2))
                except:
            
                    pass
            tags = soup2.findAll(True)
            flag=0
            for i in range(len(tags)):
                if tags[i].name=="a" or tags[i].name=="link":
                            #regular expression for finding tags containing different variations of the word contact
                            match1=re.search(r'Contact',str(tags[i]))
                            match2=re.search(r'contact',str(tags[i]))
                            match3=re.search(r'CONTACT',str(tags[i]))
                            
                            if match1 or match2 or match3:
                                
                                flag=1
                                string=tags[i].attrs.values()[0]
                                #checking if contact url starts with '..'
                                if string[0]=='.' and string[1]=='.':
                                    string=string[2:len(string)]
                                else:
                                    #checking if contact url starts with '.'
                                    if string[0]=='.' and string[1]!='.':
                                        string=string[1:len(string)]
                                #checking if contact url starts with '/'
                                if string.startswith('/',0,len(string)):
                                    if url.endswith('/'):
                                        url=url[0:len(url)-1]
                                    
                                    contact=url+string
                                    
                                    break
                                #checking if contact url starts with '#' or any other alphabet
                                if string[0]=='#' or string[0] in 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ':
                                    
                                    if re.search(r'www',url):
                                        portion=url.split('www.')
                                    else:
                                        portion=url.split('http://')
                                    temp=re.search(portion[1],string)
                                    
                                    if temp:
                                        
                                        contact=string
                                        
                                    else:
                                        #checking if contact url ends with '/'
                                        if url.endswith('/'):
                                            url=url[0:len(url)-1]
                                        contact = url+'/'+string
                                        
                                        break
                                else:
                                    
                                    contact=string
                                    break
                        
                    
                        
            if flag==0:
                contact= "NULL"
        else:
            contact="NULL"
        if email_id=="NULL":
            for i in range(len(tags)):
                #regular expression for email id        
                match=re.search(r'\w+@\w+\.\w+',str(tags[i]))
                
                if match:
                    print email_id
                    break
        #finding email id from contact page, in case it is not present in home page      
        if email_id=="NULL":
        
            if contact!="NULL":
                #trying to open url using urllib. If it throws exception, then using urllib2
                try:
                    sock3=urllib.urlopen(contact)
                    doc3=sock3.read()
                    soup3 = BeautifulSoup(''.join(doc3))
                except:
                    try:
                        sock3=urllib2.urlopen(contact)
                        doc3=sock3.read()
                        soup3 = BeautifulSoup(''.join(doc3))
                    except:
                    
                        pass
                contactTags = soup3.findAll(True)
                for i in range(len(contactTags)):
                    #regular expression for email id 
                    match=re.search(r'\w+@\w+\.\w+',str(contactTags[i]))
                    if match:
                        
                        email_id=match.group()
                        print email_id
                        break
                
                
        
    except:
            pass
    
    return [str(title),str(phone),str(url),str(contact),str(email_id)]
        
            
   
    

#main    
infoAll=[]

f=open("E:\\MSbyResearch\\webMining\\Assignment3\\results.txt","w")
for index in range(1,2001):
    print index
    info=extractFromEachPage("webMiningAS3Data/business"+str(index)+".html") #call the function for extracting for each yelp page
    infoAll.append(info)

#writing to file
for i in range(1,2001):
    f.write(str(i))
    f.write(infoAll[i-1][0])
    f.write("\t")
    f.write(infoAll[i-1][1])
    f.write("\t")
    f.write(infoAll[i-1][2])
    f.write("\t")
    f.write(infoAll[i-1][3])
    f.write("\t")
    f.write(infoAll[i-1][4])
    f.write("\n")   
