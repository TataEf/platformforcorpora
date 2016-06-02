import re
import string
import json
import os
exclude = set(string.punctuation)
regex = re.compile('[%s]' % re.escape(string.punctuation))
ending=re.compile('(ой|ый|ий|ое|ее|ая|юю|ые|ие|ого|его|ых|их|ому|ему|ей|ым|им|ею|ую|юю|ою|ей|ыми|ими|ом|ем|ам|ям|у|ю|ами|ями|ах|ях|о|ов|ев|ев|ея|ия|ом|ем|ь|а|я|ы|и|е)\\b')
lookm=re.compile('(?:\\b,? ([А-ЯЁ]\\w+?(?:|-[А-ЯЁ]\\w+?)(?=[. ,])))')
lookb=re.compile('(?:\.|!|\?|\r|\n|\t|\)) ?(\\b[А-ЯЁ]\\w+?(?:|-[А-ЯЁ]\\w+?)(?:\.| |,))')

def openfile():
    info=open('info.txt','r',encoding='utf-8-sig')
    info=info.read()
    info=info.split()
    lc=eval(info[0])
    ic=eval(info[1])
    emails=''
    for root,dirs,files in os.walk('.'):
         for fname in files:
            fns=re.findall('emails[1234567890].txt',fname)
            for fn in fns:
                print(fn)
                f=open(root+'/'+fn,'r',encoding='utf-8-sig')
                text=f.read()
                emails+=text+'\r\n'
    newemails,dw,lc,ic=collectingcuts(emails,lc,ic)
    return newemails,dw,lc,ic

def collectingcuts(emails,lc,ic):
    dw={}
    youlist=['Вы','Вас','Вам','Вами','Ваш','Ваша','Вашего','Вашему','Вашей','Вашу','Ваши','Ваших','Вашим','Вашими']
    names1=open('cutnamesforbegin.txt','r',encoding='utf-8-sig')
    names1=names1.read()
    names1=re.split('\n',names1)
    names2=open('cutnamesformiddle.txt','r',encoding='utf-8-sig')
    names2=names2.read()
    names2=re.split('\n',names2)
    locations=open('cutlocations.txt','r',encoding='utf-8-sig')
    locations=locations.read()
    locations=re.split('\n',locations)
    surnames=open('cutsurnames.txt','r',encoding='utf-8-sig')
    surnames=surnames.read()
    surnames=re.split('\n',surnames)
##    mistakes=open('listm.txt','r',encoding='utf-8-sig')
##    mistakes=mistakes.read()
##    mistakes=re.split('\n',mistakes)
    emails=re.sub('(\n)+','\n',emails)
    emails=re.sub('\n \n','\n',emails)
    emails=re.sub('(\n<END>\n)+','\n<END>\n',emails)
    a,b,lc,ic,n1=introductionsandends(emails,dw,lc,ic)
    c,d,ic=otheritems(a,b,ic)
    e,f,ic=itemsinthemiddle(c,d,names1,names2,locations,youlist,surnames,ic,n1)
    g,k,ic=itemsinthebegin(e,f,names1,locations,youlist,ic)
    emails,dw,ic=timeanddate(g,k,ic)
    return emails,dw,lc,ic
    
def introductionsandends(emails,dw,lc,ic):
    emailsplitted=re.split('\n<END>\n',emails)
    emailsnew=''
    n1=0
    for email in emailsplitted:
        lines=re.split('\n',email)
        if len(lines)<3:
            continue
        email1=email
        arr=[]
        n=0
        for line in lines:
            arr.append(line)
        if len(arr[-1].split())<=6 and arr[-1]!="":
            ic+=1
            dw[ic]=arr[-1]
            email1=email1.replace(arr[-1],'DELETED_END1.'+str(ic)+'\r\n',1)
            n=1
        line1=re.match('((\\b\\w+?\\b){,3}(,|) ((з|З)дравствуйте)(\\b(\\w+?)\\b){,3}(,|\.) )',arr[0])
        if line1!=None:
            ic+=1
            dw[ic]=line1.group(1)
            email1=email1.replace(line1.group(1),'DELETED_INTRODUCTION.'+str(ic)+'\r\n',1)
        if len(arr[0].split())<=6 or arr[0][-1]==',':
            ic+=1
            dw[ic]=arr[0]
            email1=email1.replace(arr[0],'DELETED_INTRODUCTION.'+str(ic)+'\r\n',1)
        line2=re.search('(уважен|добр)',arr[-2])
        if n==1 and (arr[-2][-1]==',' or line2!=None or len(arr[-2].split())<=4):
            ic+=1
            dw[ic]=arr[-2]
            email1=email1.replace(arr[-2],'DELETED_END2.'+str(ic)+'\r\n',1)
            n=2
        if n==2 and len(arr[-3].split())<=3:
            ic+=1
            dw[ic]=arr[-3]
            email1=email1.replace(arr[-3],'DELETED_END3.'+str(ic)+'\r\n',1)
        lc+=1
        email1='EMAIL_'+str(lc)+'\r\n'+email1
        emailsnew+=email1+('\n<END>\n')
        n1+=1
    return emailsnew,dw,lc,ic,n1
    

def itemsinthemiddle(emails,dw,names1,names2,locations,youlist,surnames,ic,n1):
    phones1=re.findall('(тел|телефон|факс|сот|сотовый)\.? ?([0-9()--+]{5,17})',emails)
    for i in phones1:
        print('probably phone number1 - '+i[1])
        ic+=1
        dw[ic]=i[1]
        emails=emails.replace(i[1],'DELETED_NUMBER.'+str(ic),1)
    phones2=re.findall('[0-9]+(?:[()--+0-9]{10,15})',emails)
    for i in phones2:
        print('probably phone number2 - '+i)
        ic+=1
        dw[ic]=i
        emails=emails.replace(i,'DELETED_NUMBER.'+str(ic),1)
    fullnames1=re.findall('\n((\\b[А-ЯЁ](\\w+?)\\b)( \\b[А-ЯЁ](\\w+?)\\b){2})(.){,3}\n',emails)
    for i in fullnames1:
        ic+=1
        dw[ic]=i[0]
        emails=emails.replace(i[0],'DELETED_ITEM.'+str(ic),1)
    fullnames2=re.findall('\n((\\b[А-ЯЁ](\\w+?)\\b)( \\b[А-ЯЁ](\\w+?)\\b){2})(.){,3}\n',emails)
    for i in fullnames2:
        ic+=1
        dw[ic]=i[0]
        emails=emails.replace(i[0],'DELETED_ITEM.'+str(ic),1)
    mn1=re.findall('\\b[А-Я]\\w+?вич(?:|а|у|ем|е)\\b',emails)
    for i in mn1:
        print('I delete middle name  '+i)
        ic+=1
        dw[ic]=i
        emails=emails.replace(i[:-1],'DELETED_MIDDLENAME.'+str(ic),1)
    mn2=re.findall('\\b[А-Я]\\w+?вн(?:а|ы|е|ой|у)\\b',emails)
    for i in mn2:
        print('I delete middle name  '+i)
        ic+=1
        dw[ic]=i
        emails=emails.replace(i[:-1],'DELETED_MIDDLENAME.'+str(ic),1)
    upperletters=re.findall('(([А-ЯЁ]+?\.)+?( |(\\b[А-ЯЁ](\\w+?)\\b)|\)))',emails)
    for i in upperletters:
        ic+=1
        dw[ic]=i[0][:-1]
        emails=emails.replace(i[0][:-1],'DELETED_LETTERS.'+str(ic),1)
    upperletters=re.findall('(\\b([А-ЯЁA-Z]{2,})\\b)',emails)
    for m in upperletters:
        i=m[0]
        if i!='END':
            n=len(dw)
            k=i[0]+i[1:].lower()
            emails,dw,ic=forwordsinthebegin(k,dw,names1,locations,emails,ic)
            if len(dw)==n:
                ic+=1
                dw[ic]=i
                emails=emails.replace(i,'DELETED_LETTERS.'+str(ic),1)
    englishwords=re.findall('\\b[A-Z][a-z]+?\\b',emails)
    for i in englishwords:
        ic+=1
        dw[ic]=i
        emails=emails.replace(i,'DELETED_FOREIGN_WORD.'+str(ic),1)
    middle=lookm.findall(emails)
    n2=len(dw)
    for el in middle:
        if el.strip() not in youlist:
            emails,dw,ic=forwordsinthemiddle(el,dw,names2,locations,emails,surnames,ic)
    print(((len(dw)-n2)/n1))
    nu=((len(dw))-n2)/n1
    if nu<1:
        middle2=re.findall('(?:\\b,? (\\w+?(?:|-\\w+?)(?=[. ,])))',emails)
        print('these are words beginning with low letters')
        for i in middle2:
            i=i[0].upper()+i[1:]
            if i not in youlist:
                emails,dw,ic=forwordsinthebegin(i,dw,names1,locations,emails,ic)
        print('here they end')
    return emails,dw,ic


def itemsinthebegin(emails,dw,names,locations,youlist,ic):
    begin_of_sen=lookb.findall(emails)
    for i in begin_of_sen:
        if i not in youlist:
            emails,dw,ic=forwordsinthebegin(i,dw,names,locations,emails,ic)
    return emails,dw,ic


def otheritems(emails,dw,ic):
    nicommas=re.findall('((\"|«)(.+?)(\"|»))',emails)
    for el in nicommas:
        ic+=1
        dw[ic]=el[2]
        emails=emails.replace(el[2],'DELETED_ITEM.'+str(ic),1)
    links=re.findall('((http://[A-Za-z-\/\._?%1234567890]*)|([A-Za-z1234567890.]+?@[a-z\.]*))',emails,re.DOTALL)
    for link in links:
        ic+=1
        dw[ic]=link[0]
        emails=emails.replace(link[0],'DELETED_ITEM.'+str(ic),1)
    streetsandother2=re.findall('((улиц|проспект|станци|переул|бульвар|пропект|шоссе|проул|область|обл\.|г\.|д\.|ул\.|проезд|тупик([а-я]*)) (\\b[А-ЯЁ]\\w+?(|-[А-ЯЁ]\\w+?)(\.| |,)))',emails)
    for i in streetsandother2:
        ic+=1
        dw[ic]=i[0]
        emails=emails.replace(i[0],'DELETED_ITEM.'+str(ic),1)
        print('I can find some streets and their adjective is          '+i[0])
    streetsandother1=re.findall('((\\b[А-ЯЁ]\\w+?(|-[А-ЯЁ]\\w+?)(\.| |,)) (улиц|проспект|станци|переул|бульвар|пропект|шоссе|проул|область|обл\.|г\.|ул\.|проезд|тупик([а-я]*)))',emails)
    for i in streetsandother1:
        ic+=1
        dw[ic]=i[0]
        emails=emails.replace(i[0],'DELETED_ITEM.'+str(ic),1)
        print('I can find some streets and their adjective is          '+i[0])
    return emails,dw,ic

def timeanddate(emails,dw,ic):
    dates=re.findall('(([0123456789]{1,2}-?(го|ье|ое|ым|) (янв|фев|март|апр|ма|июн|июл|авг|сент|окт|ноя|дек)\\w{,6})|((янв|фев|март|апр|ма|июн|июл|авг|сент|окт|ноя|дек)\\w{,6} [0123456789]{1,2}(го|ье|ое|)))',emails)
    for date in dates:
        ic+=1
        dw[ic]=date[0]
        emails=emails.replace(date[0],'DELETED_DATE.'+str(ic),1)
    return emails,dw,ic
    
    
def forwordsinthebegin(ngram,dw,names,locations,emails,ic):
    if len(ngram)<3:
        return emails,dw,ic
    oldversion,newngram=cuttingend(ngram)
##    for i in mistakes:
##        if newngram==i:
##            print('ngram probably false '+newngram+' '+ngram)
##            return emails,dw  включить в функцию
    if len(newngram)<2:
        return emails,dw,ic
    for name in names:
        if name==newngram:
            ic+=1
            dw[ic]=ngram
            print('i delete name '+oldversion)
            emails=emails.replace(oldversion,'DELETED_NAME.'+str(ic),1)
            return emails,dw,ic
    for location in locations:
        if location==ngram:
            ic+=1
            dw[ic]=newngram
            print('i delete location '+oldversion)
            emails=emails.replace(oldversion,'DELETED_LOCATION.'+str(ic),1)
            return emails,dw,ic
    return emails,dw,ic

def forwordsinthemiddle(ngram,dw,names,locations,emails,surnames,ic):
    n=0
    if len(ngram)<3:
        return emails,dw,ic
    oldversion,newngram=cuttingend(ngram)
    if len(newngram)<2:
        return emails,dw,ic
    for surname in surnames:
        surname=surname.strip()
        if surname==newngram:
            ic+=1
            dw[ic]=oldversion
            print('i delete surname '+oldversion)
            emails=emails.replace(oldversion,'DELETED_SURNAME.'+str(ic))
            n=1
            return emails,dw,ic
    for name in names:
        name=name.strip()
        if name==newngram:
            ic+=1
            dw[ic]=oldversion
            print('i delete name '+oldversion)
            emails=emails.replace(oldversion,'DELETED_NAME.'+str(ic))
            return emails,dw,ic
    for location in locations:
        location=location.strip()
        if location==newngram:
            print('i delete location '+oldversion)
            ic+=1
            dw[ic]=oldversion
            emails=emails.replace(ngram,'DELETED_LOCATION.'+str(ic))
            n=1
            return emails,dw,ic
    if n==0:
        ic+=1
        dw[ic]=newngram
        print('i delete item '+newngram)
        emails=emails.replace(newngram,'DELETED_ITEM.'+str(ic))
    return emails,dw,ic
            
def cuttingend(s):
    s=s.strip()
    word=test_re(s)
    newword=''
    newword1=''
    for w in word.split():
        nw=w
        nw=nw.replace('ё','e')
        nw=nw.replace('Ё','Е')
        w=ending.sub('',w)
        nw=ending.sub('',nw)
        newword+=str(w)+' '
        newword1+=str(nw)+' '
    newword=newword.strip()
    print(newword)
    newword1=newword1.strip()
    return newword,newword1

def test_re(s): 
    return regex.sub('', s)

def writenewfile(newemails,dw,lc,ic):
    print(len(dw))
    f=open('changedemails.txt','w',encoding='utf-8')
    f.write(newemails)
    f.close()
    l=open('deletedwords.txt','w',encoding='utf-8')
    s=json.dumps(dw,indent=2,ensure_ascii=False)
    dw=json.loads(s)
    l.write(s)
    l.close()
    line=str(lc)+'\n'+str(ic)
    info=open('info.txt','w',encoding='utf-8-sig')
    info.write(line)
    info.close()
    
def finalstage(emails,dw,lc,ic):
    check=emails
    n=len(dw)
    emails,dw,ic=userdeleteswords(emails,dw,ic)
    emails=userdeletesemails(emails)
    line=socialinfo()
    f=open('socialinfo.txt','w',encoding='utf-8-sig')
    f.write(line)
    if n!=len(dw) or check!=emails:
        a=writenewfile(emails,dw,lc,ic)
    

    
def userdeleteswords(emails,dw,ic):
    print('Откройте файл "changedemails" и найдите слово или абзац, которые вы хотите удалить. Если таких нет, нажмите Enter')
    also=input('удалить слово\абзац   ')
    while also!='':
        result=re.search(also,emails)
        if result==None or len(also)<3:
            print('Не найдено в тексте. Пропробуйте еще раз.')
            also=input('удалить слово\абзац   ')
            continue
        ic+=1
        dw[ic]=also
        emails=emails.replace(also,'DELETED_BY_AUTHOR'+str(ic))
        print(also+' удалено')
        also=input('Еще удалить слово\абзац   ')
    return emails,dw,ic

def userdeletesemails(emails):
    print('Если вы хотите удалить какое-то письмо целиком, введите его номер (просто число). Если таких писем нет, нажмите Enter')
    letter=input('номер - ')
    while letter!='':
        l=eval(letter)
        e=re.search('EMAIL_'+letter+'\r\n.+?<END>',emails,flags=re.DOTALL)
        if e==None:
            print('Письмо с таким номером не найдено. Попробуйте еще раз.')
            also=input('номер - ')
            continue
        emails=re.sub('EMAIL_'+letter+'.+?<END>','EMAIL_DELETED_BY_AUTHOR',emails,flags=re.DOTALL)
        print('EMAIL_'+letter+' удалено')
        letter=input('номер - ')
    return(emails)
        
def socialinfo():
    print('Немного информации о вас')
    name=input('Ваше имя - ')
    mail=input('Ваш электронный адрес для связи - ')
    age=input('Ваш возраст (число) - ')
    edu=input('Ваш уровень образования (законченное\незаконченное + высшее\среднее\...) - ')
    print('Спасибо')
    line='name - '+name+'\r\n'+'email - '+mail+'\r\n'+'age - '+age+'\r\n'+'education - '+edu+'\r\n'
    return line
    
k,l,z,c=openfile()        
a=writenewfile(k,l,z,c)
sndstage=finalstage(k,l,z,c)
