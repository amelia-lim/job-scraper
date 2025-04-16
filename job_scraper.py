import requests
from bs4 import BeautifulSoup
import pandas as pd

d={}
t=[]
start=0

try:
    TPR = int(input('Please input the number of hours to filter by: '))*3600 
except ValueError:
    print('Giving search results for past 1 hour.')
    TPR = 3600
try:
    keywords = "%20".join(str(input('Please input the keyword(s) you want to filter by: ')).split())
except ValueError:
    print('No keywords entered.')
    keywords = ''
try:
    JT = str(input("""Please select what job type to filter by:
                    F: Full-time, 
                    P: Part-time, 
                    C: Contract, 
                    T: Temporary, 
                    I: Internship, 
                    O: Other \n"""))
except ValueError:
        print('No valid job type filter selected. Extracting results for all job type.')
        JT = ''
try:
    E = int(input("""Please select what experience level to filter by:
                    1: Intern, 
                    2: Entry level, 
                    3: Associate, 
                    4: Mid-Sernior, 
                    5: Director \n"""))
except ValueError:
        print('No valid job type filter selected. Extracting results for all job type.')
        E = ''


headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"}
target_url=f'https://www.linkedin.com/jobs/jobs-in-singapore/?keywords={keywords}&location=Singapore&geoId=102454443&f_JT={JT}&f_E={E}&f_TPR=r{TPR}&position=1&pageNum=0&start=0'
print(target_url)
res = requests.get(target_url)
soup=BeautifulSoup(res.text,'html.parser')
try:
    job_count = int(soup.find('span', {'class':'results-context-header__job-count'}).text.strip())
except ValueError:
    job_count = 1000
    print('Filtering for top 1000 jobs')
print(job_count)

while job_count/10 >= 0.1:
    target_url=f'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords={keywords}&location=Singapore&geoId=102454443&f_JT={JT}&f_E={E}&f_TPR=r{TPR}&position=1&pageNum=0&start={start}'
    res = requests.get(target_url)
    soup=BeautifulSoup(res.text,'html.parser')
    print(target_url)
    for litag in soup.find_all('li'):
        d = {}
        try:
            d['Job_Title']=litag.find('div',{'class':'base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card'}).find('div',{'class':'base-search-card__info'}).find('h3',{'class':'base-search-card__title'}).text.strip()
        except:
            d['Job_Title']=None
        try:
            d['Company']=litag.find('div',{'class':'base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card'}).find('div',{'class':'base-search-card__info'}).find('h4',{'class':'base-search-card__subtitle'}).find('a',{'class':'hidden-nested-link'}).text.strip()
        except:
            d['Company']=None
        try:
            d['Link']=litag.find('div',{'class':'base-card relative w-full hover:no-underline focus:no-underline base-card--link base-search-card base-search-card--link job-search-card'}).find('a')['href']
        except:
            d['Link']=None 
        t.append(d)
    print('extracting ',start, ' jobs')
    start +=10
    job_count -= 10

#print(t)
df = pd.DataFrame(t)
print(df.shape[0])
df.to_csv('linkedinjobs.csv', index=False, encoding='utf-8')