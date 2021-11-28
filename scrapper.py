import requests
from bs4 import BeautifulSoup

LIMIT = 50

def get_last_page(url):
  result = requests.get(url)
  soup = BeautifulSoup(result.text, "html.parser")
  pagination = soup.find("div", {"class":"pagination"})
  links = pagination.find_all('a')
  
  pages = []
  for link in links[:-1]:
    pages.append(int(link.string))
  
  max_page = pages[-1]
  return max_page

def extract_job(html):
  title = html.find("h2", {"class":"jobTitle"}).span.get('title')
  if title is None:
    return None

  companyClass = html.find("span", {"class":"companyName"})
  company = companyClass.a
  if company is None:
    company = companyClass.getText()
  else:
    company = company.getText()

  location = html.find("div", {"class":"companyLocation"}).getText()

  return {'title':title, 'company':company, 'location':location}

def extract_jobs(last_page, url):
  jobs = []
  for page in range(last_page):
    print(f"Extract {page} page")
    result = requests.get(f"{url}&start={page*LIMIT}")
    soup = BeautifulSoup(result.text, "html.parser")
    
    results = soup.find_all("td", {"class":"resultContent"})
    for result in results:
      job = extract_job(result)
      if job is not None:
        jobs.append(job)
      
  return jobs

def get_jobs(word):
  url = f"https://www.indeed.com/jobs?q={word}&limit={LIMIT}"
  last_page = get_last_page(url)
  jobs = extract_jobs(last_page, url)
  return jobs