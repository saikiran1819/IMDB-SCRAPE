### TOP 250 MOVIES ALL INFORMATION
import json,requests
from bs4 import BeautifulSoup
url=requests.get('https://www.imdb.com/india/top-rated-indian-movies')
str=url.text
soup=BeautifulSoup(str,'html.parser')
results=soup.find_all('td',class_='titleColumn')
top_movies_list=[]
for res in results:
    position=res.text.strip()
    rank=''
    for i in position:
        if '.' not in i:
            rank=rank+i
        else:
            break
    rank=int(rank)
    title=res.a.get_text()
    year=res.span.get_text()
    year=int(year[1:5])
    imdb_rating=soup.find('td',class_="ratingColumn imdbRating").strong.get_text()
    imdb_rating=float(imdb_rating)
    link=res.a['href']
    movie_link='https://www.imdb.com'+link
    dict1={}
    dict1['position']=rank
    dict1['name']=title
    dict1['year']=year
    dict1['rating']=imdb_rating
    dict1['url']=movie_link
    top_movies_list.append(dict1)

top_250_movieslist=[]
for d_movie in top_movies_list:
    ### MOVIE 1.POSITION,2.TITLE,3.YEAR,4.RATING,5.URL 
    url=d_movie['url']
    url_str=requests.get(url)
    soup=BeautifulSoup(url_str.text,'html.parser')

    ### MOVIE 6.GENERICS
    list_of_generics=[]
    try:
        l_gen=soup.find('div',class_="ipc-chip-list GenresAndPlot__GenresChipList-cum89p-4 gtBDBL")
        for gen in l_gen:
            list_of_generics.append(gen.text)
    except:
            list_of_generics.append('unable to find path')

    ### MOVIE 7.POSTER URL
    p_url=soup.find('a',class_="ipc-lockup-overlay ipc-focusable")['href']
    p_link='https://www.imdb.com/title/tt0093603/'+p_url
    d_movie['poster link']=p_link


    ### MOVIE 8.STORYLINE
    story_line=soup.find('span',class_="GenresAndPlot__TextContainerBreakpointXS_TO_M-cum89p-0 dcFkRD")
    d_movie['story_line']=story_line.text

    ### MOVIE TOP CREDITS-->9.DIRECTOR,10.WRITER,11.STARS
    top_credits=soup.find('div',class_="PrincipalCredits__ExpandablePrincipalCreditsPanelNarrowScreen-hdn81t-2 hbUbKF")
    credits=top_credits.find('ul')
    list_of_credits=[]
    c=0
    for ul in credits:
        credit=ul.text
        for l in range(1,len(credit)):
            if credit[l].isupper():
                d_movie[credit[:l]]=credit[l:]
                break

    ### MOVIE 12.RELEASE DATE,13.COUNTRY OF ORIGIN,14.LANGUAGE,15.ALSO KNOWN AS,16.PRODUCTION COMPANIES
    details=soup.find('ul',class_="ipc-metadata-list ipc-metadata-list--dividers-all ipc-metadata-list--base")
    for detail in details:
        det=detail.text
        for l in range(1,len(det)):
            if det[l].isupper():
                d_movie[det[:l]]=det[l:]
                break
            elif det[l].isdigit():
                d_movie[det[:l]]=det[l:]
                break

    ### MOVIE 17.RUNTIME,18.COLOR,19.SOUND MIX,20.ASPECT RATIO,,,,.ETC
    colors=soup.find('ul',class_="ipc-metadata-list ipc-metadata-list--dividers-none ipc-metadata-list--compact ipc-metadata-list--base")
    run=1
    for col in colors:
        c=col.text
        if run==1:
            time=c[-8:]
            min=''
            for m in time:
                if m.isdigit():
                    min+=m
            try:
                d_movie['Runtime']=f'{int(min[0])*60+int(min[1:])}'+' min'
            except:
                d_movie['Runtime']=f'{int(min[0])*60}'+' min'
            run+=1
        else:
            for l in range(1,len(c)):
                if c[l].isupper():
                    d_movie[c[:l]]=c[l:]
                    break
                elif c[l].isdigit():
                    d_movie[c[:l]]=c[l:]
                    break
    top_250_movieslist.append(d_movie)
    print(top_250_movieslist)

### TOP 250 MOVIES DUMPED INTO JSON FILE
import os,json
if os.path.exists('task4.json'):
    print('file exists')
else:
    with open('task4.json','w') as file:
        json.dump(top_250_movieslist,file,indent=4)



