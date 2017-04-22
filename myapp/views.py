from django.shortcuts import render
from .models import Post

# Import the necessary package to process data in JSON format
try:
    import json
except ImportError:
    import simplejson as json

# Import the necessary methods from "twitter" library
from twitter import Twitter, OAuth, TwitterHTTPError

import time
import imdb

# Variables that contains the user credentials to access Twitter API 
ACCESS_TOKEN = '778543465860915200-2e6vYoCTyhmqQdBcRV5r1LQvK8SLpez'
ACCESS_SECRET = 'RB5lFlpwWRo4Ieu3eVNEUYzrG7Wr3T2yOvTYDgcUQQump'
CONSUMER_KEY = 'Wq5WnCX5fiNyuPPmgEXHPj9G4'
CONSUMER_SECRET = 'YQhF1tAVH5Jn5AlaiE7NprgoLXJdMET0nlfrlEdplAJoY1bxsA'

oauth = OAuth(ACCESS_TOKEN, ACCESS_SECRET, CONSUMER_KEY, CONSUMER_SECRET)

# Initiate the connection to Twitter REST API
twitter = Twitter(auth=oauth)

Months=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

range1=range(2000,2018)
range2=range(1,32)

fo = open("Birthdaysorted.txt", "r")
list = fo.read()
newlist = list.split("\n")
fo.close()

date=time.strftime("%d")
month=time.strftime("%m")
ndate=int(date)
nmonth=int(month)

bd_n={ 'fn': None, 'ln': None }
#bd_ln=""
for l in newlist:
    #print l
    bd = l.split()
    #print bd
    lmonth = int(bd[4])
    ldate = int(bd[3])
    if nmonth < lmonth:
        break
    if nmonth==lmonth:
        if ndate==ldate:
            bd_n['fn']=bd[0]
            bd_n['ln']=bd[1]


            

def home(request):

    bb = request.GET.get('bb', None )
    t = request.GET.get('t', None )
    search = request.GET.get('search', None )

    cnt=request.GET.get('notw', None )
    fot=request.GET.get('fot', None )
    pg=request.GET.get('pg', None )
    pgg=request.GET.get('pgg', None )

    if pg == None:
        pg=pgg

    sd = request.GET.get('sd', None )
    if sd:
        fm=request.GET.get('fmonth', None)
        fy=request.GET.get('fyear', None)
        fd=request.GET.get('fday', None)
        tm=request.GET.get('tmonth', None)
        ty=request.GET.get('tyear', None)
        td=request.GET.get('tday', None)


    
    if bb or pg == "Twitterati":
        s=""
        if pg == "Movies":
            if bb=="Trailers":
            #movie%20trailers%20OR%20actors%20trailors
            #s="movie "+bb+" OR actors "+bb
            #s="movie%20trailer%20OR%20actor%20trailer"
            #s="movie%20celebrities"
                s="upcoming%20movie%20trailers-filter:retweets"
            elif bb=="Controversies":
                s="bollywood%20fights-filter:retweets"
            elif bb=="Famous Dialogues":
                s="famous%20movie%20dialogues-filter:retweets"
            elif bb=="Actors":
                s="movie%20celebrities-filter:retweets"
            elif bb=="Birthdays":
                s="actors%20birthdays-filter:retweets"
            elif bb=="Facts":
                s="movies%20behind%20the%20scenes%20-porn%20-sex%20-naked%20-filter:retweets"
            else:
                s="movie%20"+bb+"%20OR%20actor%20"+bb+"-filter:retweets"                    
            #movie%20trailers%20OR%20actors%20trailors
            #s="movie "+bb+" OR actors "+bb
            #s="movie%20trailer%20OR%20actor%20trailer"
                
        elif pg == "Books":
            s="book%20"+bb+"%20OR%20books%20author%20"+bb+"-filter:retweets"
            
        elif pg == "Theatre":
            if bb=="Plays":
                s=" theatre stage plays-filter:retweets"
            else:
                s="theatre%20"+bb+"%20OR%20play%20"+bb+"-filter:retweets"
                
        elif pg == "Television Soap Opera":
            if bb=="Facts":
                s="tv%20series%20facts-filter:retweets"
            elif bb=="Actors":
                s="tv%20series%20actors-filter:retweets"
            else:
                #s="series%20"+bb+"%20OR%20tv%20actor%20"+bb+"%20OR%20tv%20"+bb
                s=s="series%20"+bb

        elif pg == "Twitterati":
            fo = open("twitteratis.txt", "r")
            str = fo.read()
            ta = str.split()
            fo.close()
            tweet_count = 0
            if bb:
                c1=request.GET.get('c1', None)
                c2=request.GET.get('c2', None)
                c3=request.GET.get('c3', None)

                c1t=request.GET.get('c1t', None)
                if c1=="on" and c1t:
                    cot=c1t
                else:
                    cot=5
                    
                c2t1=request.GET.get('c2t1', None)
                if c2=="on" and c2t1:
                    fr=c2t1
                else:
                    fr=1
                c2t2=request.GET.get('c2t2', None)
                if c2=="on" and c2t2:
                    tr=c2t2
                else:
                    tr=10

                c3t=request.GET.get('c3t', None)
                if c3=="on" and c3t:
                    keyword=c3t
                else:
                    keyword=""
            else:
                cot=5
                fr=1
                tr=10
                keyword=""

            #for i in range(int(fr), int(tr)+1):
            trn=int(tr)+1
            frn=int(fr)
            
        
        if fot=="embed":
            inentities='false'
        else:
            inentities='true'
        
        if sd:
            snc=fy+"-"+fm+"-"+fd
            untl=ty+"-"+tm+"-"+td

        if pg == "Twitterati":
            tweetz = ""
            for i in range(frn, trn): 
                s=keyword+"%20from:"+ta[i]
                if sd:
                    iterator = twitter.search.tweets(q=s, lang='en', since=snc, until=untl, result_type='mixed', count=cot, include_entities=inentities)
                else:
                    iterator = twitter.search.tweets(q=s, lang='en', result_type='mixed', count=cot, include_entities=inentities)
                tweets = iterator["statuses"]
                tweetz += fetch(tweets, fot)
            
        else:
            if sd:
                iterator = twitter.search.tweets(q=s, lang='en', since=snc, until=untl, result_type='mixed', count=cnt, include_entities=inentities)
            else:
                iterator = twitter.search.tweets(q=s, lang='en', result_type='mixed', count=cnt, include_entities=inentities)
            tweets = iterator["statuses"]
            tweetz = fetch(tweets, fot)


        if sd:
            return render(request, 'myapp/home.html', { 'pg_name':'Home', 'pg':pg, 'pgg':pgg, 'bb':bb, 'date':time.strftime("%d/%m"), 'fot':fot, 'bd_n':bd_n, 'tweetz':tweetz, 'sd':sd, 'fm':fm, 'fy':fy, 'fd':fd, 'tm':tm, 'ty':ty, 'td':td, 'range':range1, 'range2':range2, 'Months':Months} )
        else:
            return render(request, 'myapp/home.html', { 'pg_name':'Home', 'pg':pg, 'pgg':pgg, 'bb':bb, 'date':time.strftime("%d/%m"), 'fot':fot, 'bd_n':bd_n, 'tweetz':tweetz, 'range':range1, 'range2':range2, 'Months':Months} )
                   
    else:
        if sd:
            return render(request, 'myapp/home.html', { 'pg_name':'Home', 'pg':pg, 'pgg':pgg, 'bb':bb, 'date':time.strftime("%d/%m"), 'bd_n':bd_n, 'sd':sd, 'fm':fm, 'fy':fy, 'fd':fd, 'tm':tm, 'ty':ty, 'td':td, 'range':range1, 'range2':range2, 'Months':Months} )
        else:
            return render(request, 'myapp/home.html', { 'pg_name':'Home', 'pg':pg, 'pgg':pgg, 'bb':bb, 'date':time.strftime("%d/%m"), 'bd_n':bd_n, 'range':range1, 'range2':range2, 'Months':Months} )
        


def fetch(tweets, fot):

    #tweets = iterator["statuses"]
    tweetz = ""

    if fot=="embed":
        
        for tweet in tweets:                                                     
            if 'text' in tweet:
                resp = twitter.statuses.oembed(_id=tweet['id_str'])
                tweetz += "<div class='polaroid'>"+resp['html']+" </div><br>"
                #tweetz += "<div class='polaroid'>"+resp['html'].encode('utf-8')+" </div><br>"
                
    else:
        for tweet in tweets:
            
            if 'text' in tweet:                                    
                tweetz += "<div class='polaroid'>"
                text = tweet['text']
                entities = tweet['entities']
        
                if 'media' in entities:
                    for media_element in entities['media']:
                        if media_element['type'] == 'photo':
                            text = text.replace(media_element['url'], '')
                        #if media_element['type'] == 'video':
                            #text = text.replace(media_element['url'], '')

                if 'urls' in entities:
                    for url_element in entities['urls']:
                        if url_element['url']:
                            us="<a href='"+url_element['url']+"' title='"+url_element['expanded_url']+"'>"+ url_element['display_url']+"</a>"
                            text = text.replace(url_element['url'], us)

                if 'extended_entities' in tweet:
                    ee = tweet['extended_entities']
                    if ee['media']:
                        media=ee['media'][0]
                        #print "EE: type:", media['type']
                        if media['type']=='video':
                            variants=media['video_info']['variants']
                            for variant in variants:
                                if variant['content_type']=='video/mp4':
                                    tweetz += "<br><video  style='width:100%;' controls><source src='"+variant['url']+"' type='video/mp4'>Video cannot be played</video>"
                                    break;
                        else:
                            tweetz += "<br><img src='" + media['media_url_https']
                            tweetz += "' alt='Image cannot be displayed.' style='width:100%;'/>"
                    
                tweetz += "<div class='container'> "
                tweetz += "<img src='"+tweet["user"]["profile_image_url_https"]+"' alt='img' style='vertical-align:middle;'>"
                if tweet['user']['name']:
                    #tweetz += "<b>&nbsp;&nbsp;"+tweet['user']['name'].encode('utf-8')+"</b>"
                    tweetz += "<b> &nbsp;&nbsp;"+tweet['user']['name']+" </b>"
                if tweet['user']['screen_name']:
                    #tweetz += "<font color='gray'>&nbsp;&nbsp;@"+tweet['user']['screen_name'].encode('utf-8')+"</font><br>"
                    tweetz += "<font color='gray'>&nbsp;&nbsp;@"+tweet['user']['screen_name']+"</font><br>"

                #tweetz += "<br>Tweet:    " + text.encode('utf-8')
                tweetz += "<br>Tweet:    " + text

                tweetz += "<br><small><font color='gray'>"

                crt=tweet["created_at"].split();
                crt1=""+crt[1]+" "+crt[2]+" "+crt[5]

                tweetz += " <hr> Created at: "+crt[3]+" - "+crt1
                
                if tweet["favorite_count"]:
                    tweetz += "  &nbsp;&nbsp;&nbsp;&nbsp;     Likes:" + str(tweet["favorite_count"])
                if tweet["retweet_count"]:
                    tweetz += "  &nbsp;&nbsp;&nbsp;&nbsp;     Re-tweets:" + str(tweet["retweet_count"])
                tweetz += "</font></small></p> </div></div><br>"

    return tweetz


def search(request):

    dd=request.GET.get('dropdown', None )
    if dd == 'maps':
        return maps(request)

    bb = request.GET.get('bb', None )
    t = request.GET.get('t', None )
    search = request.GET.get('search', None )

    cnt=request.GET.get('notw', None )
    fot=request.GET.get('fot', None )
    pg=request.GET.get('pg', None )
    pgg=request.GET.get('pgg', None )

    if pg == None:
        pg=pgg

    sd = request.GET.get('sd', None )
    if sd:
        fm=request.GET.get('fmonth', None)
        fy=request.GET.get('fyear', None)
        fd=request.GET.get('fday', None)
        tm=request.GET.get('tmonth', None)
        ty=request.GET.get('tyear', None)
        td=request.GET.get('tday', None)
    

    i=0
    stext=request.GET.get('stext', None )
    tweetz=""

    
        
    if stext:
        
        if fot=="embed":
            inentities='false'
        else:
            inentities='true'
        
        if sd:
            snc=fy+"-"+fm+"-"+fd
            untl=ty+"-"+tm+"-"+td
            

        if dd=="IMDbM":
            ia = imdb.IMDb()
            search_results = ia.search_movie(stext)

            if search_results:
                movieID = search_results[0].movieID
                print movieID
                movie = ia.get_movie(movieID)
                tweetz += "<div class='polaroid' style='width:500px; font-size:16px; font-weight:normal; overflow:scroll;'><br> - " + movie.summary().encode('utf-8')
                tweetz += "</a><br><br></div><br><br>"

        if dd=="IMDbP":
            ia = imdb.IMDb()
            search_results2 = ia.search_person(stext)

            if search_results2:
                personID = search_results2[0].personID
                print personID
                person = ia.get_person(personID)
                tweetz += "<div class='polaroid' style='width:500px; font-size:16px; font-weight:normal; overflow:scroll;'><br> - " + person.summary().encode('utf-8')
                tweetz += "</a><br><br></div><br><br>"

            
        if dd=="hash":
            s="%23"+stext+"%20-filter:retweets"
            if sd:
                iterator = twitter.search.tweets(q=s, lang='en', since=snc, until=untl, result_type='mixed', count=cnt, include_entities=inentities)
            else:
                iterator = twitter.search.tweets(q=s, lang='en', result_type='mixed', count=cnt, include_entities=inentities)
            tweets = iterator["statuses"]
        
        elif dd=="key":
            qq=""
            keyarr=stext.split()
            for k in keyarr:
                #qq=qq+"AND"+k
                qq=qq+"%20"+k
            qq=qq+"%20-filter:retweets"
            if sd:
                iterator = twitter.search.tweets(q=qq, lang='en', since=snc, until=untl, result_type='mixed', count=cnt, include_entities=inentities)
            else:
                iterator = twitter.search.tweets(q=qq, lang='en', result_type='mixed', count=cnt, include_entities=inentities)
            #iterator = twitter.search.tweets(q=qq, lang='en',geocode='12.9005,77.5942,100.0km')
            tweets = iterator["statuses"]
            
        elif dd=="user":
            #qq=" "
            #iterator = twitter.search.tweets(q=qq, lang='en',geocode='12.9005,77.5942,100.0km',from:stext)
            iterator = twitter.statuses.user_timeline(screen_name=stext)
            tweets = iterator
            
        elif dd=="location":
            fo = open("id.txt", "r")
            str = fo.read(70);
            s=str.split()
            for t in s:
                if stext==s[i]:
                    id=s[i+1]
                i=i+1
            results = twitter.trends.place(_id = id)
            for location in results:
                for trend in location["trends"]:
                    tweetz += "<div class='polaroid' style='width:500px; font-size:16px; font-weight:bold; overflow:scroll;'><br> - " + trend["name"].encode('utf-8')
                    tweetz += "<br><br><hr><br>URL: <a href='" + trend["url"].encode('utf-8')
                    tweetz += "'>" + trend["url"].encode('utf-8')
                    tweetz += "</a><br><br></div><br><br>"
        
        if dd=="hash" or dd=="user" or dd=="key":
            tweetz += fetch(tweets, fot)


        if sd:
            return render(request, 'myapp/search.html', { 'pg_name':'Search', 'dd':dd, 'stext':stext, 'date':time.strftime("%d/%m"), 'fot':fot, 'bd_n':bd_n, 'tweetz':tweetz, 'sd':sd, 'fm':fm, 'fy':fy, 'fd':fd, 'tm':tm, 'ty':ty, 'td':td, 'range':range1,'range2':range2, 'Months':Months} )
        else:
            return render(request, 'myapp/search.html', { 'pg_name':'Search', 'dd':dd, 'stext':stext, 'date':time.strftime("%d/%m"), 'fot':fot, 'bd_n':bd_n, 'tweetz':tweetz, 'range':range1, 'range2':range2, 'Months':Months} )
                   
    else:
        if sd:
            return render(request, 'myapp/search.html', { 'pg_name':'Search', 'dd':dd, 'stext':stext, 'date':time.strftime("%d/%m"), 'bd_n':bd_n, 'sd':sd, 'fm':fm, 'fy':fy, 'fd':fd, 'tm':tm, 'ty':ty, 'td':td, 'range':range1,'range2':range2, 'Months':Months} )
        else:
            return render(request, 'myapp/search.html', { 'pg_name':'Search', 'dd':dd, 'stext':stext, 'date':time.strftime("%d/%m"), 'bd_n':bd_n, 'range':range1, 'range2':range2, 'Months':Months} )
        


def maps(request):

    mapb = request.GET.get("mapb", None)
    stext=request.GET.get('stext', None )
    dd=request.GET.get('dropdown', None )    
    tid = request.GET.get("tid", None)

    if mapb==None or mapb!='Worldwide':

        it = twitter.trends.available()

        country_woeid="[['Country', 'WOEID']"
        cw=[['Country',0, 'CountryName']]
        town_woeid="[['countryCode', 'Town', 0]"
        tw=[['Town',0]]
        twn=0
        for i in it:
            if i['placeType']['code'] == 12:

                c1=[i['countryCode'], i['woeid'], i['name']]
                cw.append(c1)
                country_woeid += ", ['"+i['name']+"', "+str(i['woeid'])+"]"
                
            if i['placeType']['code'] == 7:

                t1=[i['name'], i['woeid']]
                tw.append(t1)
                town_woeid += ", ['"+i['countryCode']+"', '"+i['name']+"', "+str(i['woeid'])+"]"
                twn += 1
        country_woeid += "]"
        town_woeid += "];"

    selected_place=""
    slctd_id=-1
    if mapb=='Worldwide':
        slctd_id=1
        selected_place='Worldwide'
        
    elif tid!=None and tid!='None':
        slctd_id=tid
        for i in tw:
            if str(i[1])==str(slctd_id):
                selected_place=i[0]
                break
    else:
        ecc = request.GET.get('ecc', None)
        if ecc:
            print ecc
            for i in cw:
                if i[0]==ecc:
                    slctd_id=i[1]
                    selected_place=i[2]
                    #print slctd_id
                    break
    tweetz = "<h2>"+selected_place+" Trends:</h2>" 
    if slctd_id>0 :
        results = twitter.trends.place(_id = slctd_id, lang='en')
        #tweets = results
        for location in results:
            #print "<br><br><br><br>loc:", location
            for trend in location["trends"]:
                #print "<br><br>trends:", trend 
                tweetz += "<div class='polaroid' style='width:500px; font-size:16px; font-weight:bold; overflow:scroll;'><br> - " + trend["name"]
                tweetz += "<br><br><hr><br>URL: <a href='" + trend["url"]
                tweetz += "'>%s" + trend["url"] + "</a><br><br></div><br><br>"

    if mapb==None or mapb!='Worldwide':
        return render(request, 'myapp/maps.html', {'tweetz':tweetz, 'tid':tid, 'pg_name':'Maps', 'twn':twn, 'town_woeid':town_woeid, 'country_woeid':country_woeid, 'mapb': mapb, 'dd':dd, 'stext':stext, 'date':time.strftime("%d/%m"), 'bd_n':bd_n, 'range':range1, 'range2':range2, 'Months':Months} )
    else:
        return render(request, 'myapp/maps.html', {'tweetz':tweetz, 'tid':tid, 'pg_name':'Maps', 'mapb': mapb, 'dd':dd, 'stext':stext, 'date':time.strftime("%d/%m"), 'bd_n':bd_n, 'range':range1, 'range2':range2, 'Months':Months} )




