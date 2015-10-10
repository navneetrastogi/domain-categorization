__author__ = 'Navneet Rastogi'
from bs4 import BeautifulSoup
import urllib
import json
import re
import thread
import concurrent.futures
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem.porter import *
import time
from nltk.stem import WordNetLemmatizer

# title extractor
def PrintTitle(soup):
    title = ''
    if soup.find('title'):
        title = soup.find('title').string
    return title


# meta description extractor
def PrintMetaDescription(soup):
    md = ''
    l = soup.findAll("meta", attrs={"name": "description"})
    if l == []:
        return md
    else:
        md = l[0]['content'].encode('utf-8')
    return md


# meta keywords extractor
def PrintMetaKeywords(soup):
    mk = ''
    l = soup.findAll("meta", attrs={"name": "keywords"})
    if l == []:
        return mk
    else:
        mk = l[0]['content'].encode('utf-8')
    return mk


# meta robots extractor
def PrintMetaRobots(soup):
    mr = ''
    l = soup.findAll("meta", attrs={"name": "robots"})
    if l == []:
        return mr
    else:
        mr = l[0]['content']
    return mr


# finds all p elements without links
def PrintParagraphs(soup):
    list = []
    paras = soup.findAll('p')
    if paras != []:
        for link in paras:
            list.append(link.string)
    return list


# print all links
def PrintLinks(soup):
    l = soup.findAll("a", attrs={"href": True})

    externallinks = []
    for link in l:
        if link['href'].find("http://") == 0:
            externallinks = externallinks + [link]
    print
    externallinks
    list = []
    if len(externallinks) > 0:
        for link in externallinks:
            if link.text != '':
                list.append(link.text.encode('utf-8'))
    return list


# headers printer
def PrintHeaders(soup):
    list = []
    l = soup.findAll(re.compile("^h\d"))
    if l == []:
        return list
    for el in l:
        list.append(el.text.encode('utf-8'))
    return list


# return all alt tags
def ReturnAltTags(soup):
    l = soup.findAll(attrs={"alt": True})
    if l == []:
        return ''
    ret = ""
    for el in l:
        ret = ret + " " + el['alt']
    return ret


# return title tags
def ReturnTitleTags(soup):
    l = soup.findAll(attrs={"title": True})
    if l == []:
        return ''
    ret = ""
    for el in l:
        ret = ret + " " + el['title']
    return ret


def getAllText(url):
    response = []
    if not url.startswith('http'):
        url = '%s%s' % ('http://', url)
    ur = urllib.urlopen(url);

    soup = BeautifulSoup(ur.read(), "html5lib")
    response.append({'url': url})
    response.append({'title': PrintTitle(soup)})
    response.append({'description': PrintMetaDescription(soup)})
    response.append({'keywords': PrintMetaKeywords(soup)})
    response.append({'paragraphs': PrintParagraphs(soup)})
    response.append({'links': PrintLinks(soup)})
    response.append({'headers': PrintHeaders(soup)})
    response.append({'alttags': ReturnAltTags(soup)})
    response.append({'titletags': ReturnTitleTags(soup)})
    return json.dumps(response)

def lemmitize_tokens(tokens, wordnet_lemmatizer):
    lemmitized = []
    for item in tokens:
        lemmitized.append(wordnet_lemmatizer.lemmatize(item))
    return lemmitized


def get_tf(text):
    lowers = text.lower()

    splitted_words = re.compile('[^a-zA-Z]').split(lowers)

    remove_empty = filter(None, splitted_words)
    cachedStopWords = set(('a','about','above','access','acop','across','adclient','adme','adpos','adsize','advanced','advert','adverts','afc','after','again','against','agofid','algo','all','allx','almost','alnlk','alone','along','already','also','alt','although','alttags','always','am','amebidx','among','an','and','another','any','anybody','anyone','anything','anywhere','approx','are','area','areas','around','as','ask','asked','asking','asks','aspx','at','atcustom','atoz','aunknown','autorefresh','avc','away','awnlpxnraw','b','back','backed','backing','backs','bba','bbbc','be','became','because','become','becomes','been','before','began','behind','being','beings','below','best','better','between','bhour','big','black','bmftaxnjaczyzwdpb','bnoa','bnoc','booty','both','browse','btghco','but','butt','by','c','came','can','cannot','case','cases','category','categorytype','cdn','certain','certainly','cgi','channel','class','classes','classified','clear','clearly','clpd','cnearlynew','cnew','com','combinedmatrix','come','comment','contact','could','count','cpc','crdt','crlp','cstreet','ctonode','currentpage','d','dagv','date','daterange','dcat','dczzaxrlpxdlymrljnnly','deavg','default','defaultdomain','denied','depairport','der','description','details','dhttp','did','didnt','differ','different','differently','disclaimer','do','does','doing','don','done','doubleclickcontainer','down','downed','downing','downs','dsic','dtag','during','e','each','early','edit','either','end','ended','ending','ends','enough','error','even','evenly','ever','every','f','face','faces','fact','facts','false','far','fcr','fdrp','felt','few','fff','find','finds','first','for','found','four','fpos','from','fromnode','fsch','ftab','full','fully','further','furthered','furthering','furthers','g','gave','gclid','general','generally','get','gets','ghosttext','give','given','gives','go','got','h','had','has','hash','have','having','he','help','her','here','hers','herself','hfboards','high','higher','highest','him','himself','his','hkuevdt','how','however','htm','http','https','i','iezg','iezh','if','image','img','important','in','include','index','into','is','isasync','ispconfig','it','item','itemid','itm','its','itself','j','jenna','jpg','jsp','just','k','keyword','keywords','kind','knew','know','known','knows','l','let','lets','like','likely','likes','link','links','listing','listings','lnlk','log','logcode','login','loginform','logo','logon','logout','long','longer','longest','m','may','mccann','me','meid','mesx','might','mmo','more','most','mostly','msg','msgid','much','must','my','mybeta','myci','mynextsummary','myself','n','next','nkw','no','nobody','non','noone','nor','not','nothing','now','nowhere','nqfmyci','null','o','oayh','odkw','of','off','often','on','once','one','onesearchad','only','open','opened','opening','opens','or','org','osacat','other','others','our','ours','ourselves','out','over','own','p','page','pagenumber','paragraphs','param','paramt','part','parted','parting','parts','per','perhaps','permalink','pgn','php','post','prd','prefloc','prod','psrc','put','puts','q','qcfsrmtaodvk','quicksearch','r','reg','replytomessages','requested','restrict','rffrid','right','rpp','s','sacat','said','same','saw','say','says','sch','scrollto','searchreskin','shall','she','should','sierra','since','siteui','so','some','sspagename','stateid','still','strk','styp','such','t','tagid','tatl','tells','terms','text','tgt','than','that','the','their','theirs','them','themselves','then','there','therefore','these','they','this','those','three','through','thus','title','titles','titletags','to','today','together','too','took','topic','topics','tpid','tqfmyci','transactid','transactionid','trkparms','trksid','true','tswjrk','ttyp','type','u','ucgylduwkvmokfbyawnllgepkvyovw','uff','uimserv','uk','unanimisad','under','until','up','upon','url','us','usedcfs','userid','useridto','utd','utm','uywjszwxvz','v','valid','vend','very','vfpa','viewwidth','voip','vqfmyci','vrc','w','was','way','ways','wdzocysdbkd','we','website','were','what','when','where','whether','which','while','who','whole','whom','whose','why','will','with','within','without','wont','would','www','wwwp','x','xaqaq','y','year','years','yet','you','young','younger','youngest','your','youre','yours','yourself','yourselves','z','zcgrid','zetec','zgumywdvzj','zkuuqywn'))
    #cachedStopWords = set(stopwords.words("english"))

    #filtered = [w for w in remove_empty if len(w) > 2 and not w in stopwords.words('english')]
    filtered = [w for w in remove_empty if len(w) > 2 and not w in cachedStopWords]
    wordnet_lemmatizer = WordNetLemmatizer()
    refined_text = lemmitize_tokens(filtered,wordnet_lemmatizer)

    count = Counter(refined_text)
    result = count.most_common(10)
    return result


def readURLFile(fileName):
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    outputfile = open('/home/sajan/projects/hackathon/output', 'w')
    with open(fileName, "r") as ins:
        future_to_url = {executor.submit(getAllText, line): line for line in ins}
        for future in concurrent.futures.as_completed(future_to_url):
            url = future_to_url[future]
            try:
                data = future.result()
                count = get_tf(data)
                print url
                keywordsList = str(count).strip('[]')
                print keywordsList
                json.dump({'url':url[:-2], 'keywords':keywordsList}, outputfile, indent=4)
                outputfile.flush()
            except Exception as exc:
                print('%r generated an exception: %s' % (url, exc))
    outputfile.close()
    executor.shutdown()


tf = open('/home/sajan/projects/hackathon/starttime', 'w')

ts = time.time()
tf.write("starttime"+str(ts))
tf.close()

# getAllText("http://www.ebay.in/cln/tech_curator/Top-Gear/224449655019")
readURLFile('/home/sajan/projects/hackathon/url')

kk = open('/home/sajan/projects/hackathon/endtime', 'w')

ts = time.time()
kk.write("end time"+str(ts))
kk.close()