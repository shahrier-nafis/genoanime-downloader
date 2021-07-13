from bs4 import BeautifulSoup
import re
import os
import requests

#CONFIG
#quality = 360P or 480P or 720P or 1080P
URL_PATTERN = 'https://genoanime.com/{}&episode={}' #General URL pattern for every anime on genoanime

def init(): #init function

    string = "welcome to gogoanime.so batch downloader / link generator. \n"
    string += "by default it fetches at 1080P\n"
    string += "link example: \n"
    string += "https://genoanime.com/watch?name=shingeki-no-kyojin-the-final-season-dub&episode=1 \n"

    return string 

def getlink(): #get the anime link
    return input("Enter Link to the first episode of your Anime Series : ")  #User Enters URL

def getstart(): #get the anime start
    start = int(input("Enter Episode Number to start with : "))
    if start <= 0:
        start = 1
    return start

def getend(): #get the anime end
    end = int(input("Enter Episode Number to end with : "))
    return end
def getquality():
    quality = 0
    quality = int(input("quality:(360p=1|480p=2|720p=3|1080p=4|default=PRESS ENTER)") or 0 )
    valid = [0,1,2,3,4]
    if quality in valid :
        return quality
    else :
        return getquality()
def getfiletype():
    filetype = 0
    filetype = int(input("filetype:(m3u8=1|mp4=0|default=PRESS ENTER)") or 0 )
    valid = [0,1]
    if filetype in valid :
        return filetype
    else :
        return getfiletype()
def formatname(animelink):
    animename = animelink.split("/")  #splits link by /
    animearr = animename[3].split("&")
    animearr.pop()
    animename = "-".join(animearr)
    return (animename)

def dl():
    print(init())
    animelink = getlink()
    start = getstart()
    end = getend()
    quality =  getquality()
    filetype = getfiletype()
    main(animelink, start,end, quality, filetype)

ajax_parse = lambda dt: (
    dt.get('source', [{}])[0].get('file'), dt.get('source', [{}])[0].get('label'), dt.get('source', [{}])[0].get('type'), 
    dt.get('source_bk', [{}])[0].get('file'), dt.get('source_bk', [{}])[0].get('label'), dt.get('source_bk', [{}])[0].get('type'))

def bypass_encrypted_content(session, streaming_url):
    with session.get('%s' % streaming_url.replace('streaming', 'loadserver')) as server_load:
        for urls in re.finditer(r"(?<=sources:\[{file: ')[^']+", server_load.text):
            yield urls.group(0)

def main(alink, startt, endd, quality, filetype):
    start = int(startt)
    end = int(endd)
    animename = formatname(alink)
    quality = {
        0: 0,
        1: "360P",
        2: "480P",
        3: "720P",
        4: "1080P"
    }.get(quality)
    try:
        filename = "{}.txt".format(animename[11:])
        f = open(filename)
        f.close()
        os.remove(filename)
    except:
        #do nothing i don't care
        dummy = "dummy"

    longstring = ""
    end=end+1 # Increased by 1 for range function
    session = requests.Session()
    for episode in range(start,end):
        url = URL_PATTERN.format(animename,episode)
        srcCode = requests.get(url)
        soup = BeautifulSoup(srcCode.content,'html.parser')
        #get link from GenoAnime A
        if quality == 0 :
            if animename.find("-dub") != -1:
                print("Dub")
                dl_wrapper = soup.find_all('iframe', id="iframeplayer")
                dl_wrapper = str(dl_wrapper).split('"')
                try:
                    link =(dl_wrapper[11])
                except:
                    print("[ERROR :The media could not be loaded, either because the server or network failed or because the format is not supported.]")
                    print("[Retry Later]")
                    print("[EXITING]")
                    quit()
                links = ([{c} for c in bypass_encrypted_content(session, link)])
                if filetype == 0 :    
                    f = open('{}.txt'.format(animename[11:]), "a") #opens file with name of "test.txt"
                    f.write(str(links[0])+"\n")             
                    links += str(longstring) + "\n" 
                    #print the link for good measure
                    print(links[0])
                else :  
                    f = open('{}.txt'.format(animename[11:]), "a") #opens file with name of "test.txt"
                    f.write(str(links[1])+"\n")
                    links += str(longstring) + "\n" 
                    #print the link for good measure
                    print(links[1])
            else:
                if filetype == 0 : 
                    regex = re.compile("mountain?.*?\.mp4") #pattern for .mp4 urls 
                    soup = str(soup)
                    m = regex.finditer(soup) #finding direct urls
                    for match in m :
                        preferredlink = match.group(0)
                        #write it into a file
                        f = open('{}.txt'.format(animename[11:]), "a") #opens file with name of "test.txt"
                        f.write(preferredlink+"\n")
                
                        #print the link for good measure
                        print(preferredlink)
                        break
                else :
                    dl_wrapper = soup.find_all('iframe', id="iframeplayer")
                    dl_wrapper = str(dl_wrapper).split('"')
                    try:
                        link =(dl_wrapper[11])
                    except:
                        print("[ERROR :The media could not be loaded, either because the server or network failed or because the format is not supported.]")
                        print("[Retry Later]")
                        print("[EXITING]")
                        quit()
                    links = ([{c} for c in bypass_encrypted_content(session, link)])
                    f = open('{}.txt'.format(animename[11:]), "a") #opens file with name of "test.txt"
                    f.write(str(links[1])+"\n")
                    links += str(longstring) + "\n" 
                    #print the link for good measure
                    print(links[1])


        else :
            dl_wrapper = soup.find_all('iframe', id="iframeplayer")
            dl_wrapper = str(dl_wrapper).split('"')
            try:
                link =(dl_wrapper[11])
            except:
                print("[ERROR :The media could not be loaded, either because the server or network failed or because the format is not supported.]")
                print("[Retry Later]")
                print("[EXITING]")
                quit()

            with session.get('%s' % link.replace('streaming', 'ajax')) as response:
                content = response.json()

            if content == 404:
                print("[ERROR:streamani.net:(Sorry, Links multiquanlity temporary disable.)]")
                links = ([{c} for c in bypass_encrypted_content(session, link)])
            else:
                s1, l1, t1, s2, l2, t2 =  ajax_parse(content)        
                links = [{'quality': "%s [%s]" % (l1, t1), 'stream_url': s1}] + ([{'quality': "%s [%s]" % (l2, t2), 'stream_url': s2}] if s2 else [])

            if filetype == 0 :    
                f = open('{}.txt'.format(animename[11:]), "a") #opens file with name of "test.txt"
                f.write(str(links[0])+"\n")             
                links += str(longstring) + "\n" 
                #print the link for good measure
                print(links[0])
            else :  
                f = open('{}.txt'.format(animename[11:]), "a") #opens file with name of "test.txt"
                f.write(str(links[1])+"\n")
                links += str(longstring) + "\n" 
                #print the link for good measure
                print(links[1])
    return longstring


#print(init())

#print(main())

#forget deleting the file for now



def success(alink):
    animename = formatname(alink)
    print("----- -----------------------------------------------------")
    print("success. you can copy the links here or from {}.txt in this folder".format(animename))
    print("----------------------------------------------------------")



