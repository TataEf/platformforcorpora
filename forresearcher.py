import re
import string
import json
import os

def openfile():
##    base=open('base.txt','r',encoding='utf-8-sig')
##    base=base.read()
##    infobase=open('infobase.json','r',encoding='utf-8-sig')
    base=''
    infobase=[]
    for root,dirs,files in os.walk('.'):
         for dirname in dirs:
            drns=re.findall('user[0-9]{1,3}',dirname)
            for drn in drns:
                print(drn)
                emails=open(root+'/'+drn+'/'+'changedemails.txt','r',encoding='utf-8-sig')
                sinfo=open(root+'/'+drn+'/'+'socialinfo.txt','r',encoding='utf-8-sig')
                codedwords=open(root+'/'+drn+'/'+'deletedwords.txt','r',encoding='utf-8-sig')
##                numbers=open(root+'/'+drn+'/'+'info.txt','r',encoding='utf-8-sig')
                key=open(root+'/'+drn+'/'+'sessionkey.txt','r',encoding='utf-8-sig')
                emails=emails.read()
                print(len(emails))
                sinfo=sinfo.read()
                codedwords=codedwords.read()
                key=key.read()
                base,infobase=first(base,infobase,sinfo,emails)
                name,line=second(drn,key,codedwords)
                print(len(infobase))
                f=open(root+'/'+'coded'+'/'+name,'w',encoding='utf-8-sig')
                f.write(line)
    f1=open('base.txt','w',encoding='utf-8-sig')
    f1.write(base)
    f2=open('infobase.json','w',encoding='utf-8-sig')
    s=json.dumps(infobase,indent=2,ensure_ascii=False)
    infobase=json.loads(s)
    f2.write(s)
    f1.close()
    f2.close()
                

def first(base,infobase,si,emails):
    openi='Social information:\n'
    closedi=[]
    sinfo=re.split('\n',si)
    username=[sinfo[0],sinfo[1]]
    for line in sinfo[2:]:
        openi+=line+'\r\n'
        closedi.append(line)
    letters=re.findall('(EMAIL_[0-9]{1,})\n',emails,flags=re.DOTALL)
    ls=[]
    for letter in letters:
        ls.append(letter)
        l=letter
        emails=emails.replace(letter,l+'\n'+openi+'\n'+'<TEXT>:\n')
    small=[closedi,ls]
    info=[username,small]
    infobase.append(info)
    base+=emails
    return base,infobase

def second(drn,key,codedwords):
    name=drn+'_key_and_deleted_words.txt'
    line='sessionkey:\r\n'+key+'\r\nCodedwords:\r\n'+codedwords
    return name,line 
    
m=openfile()
