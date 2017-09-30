import requests
import pandas as pd
from bs4 import BeautifulSoup
from tqdm import tqdm

base_url = 'http://www.ratemyprofessors.com/search.jsp?query=university+of+california'


def scrape_search_result_page(html):
    new_soup = BeautifulSoup(html, 'html.parser')
    names, locs, depts = [], [], []
    for li in new_soup.find_all('li', {'class': ['PROFESSOR']}):
        for span in li.find_all('span', {'class': ['main']}):
            names.append(span.text.strip())
        for span in li.find_all('span', {'class': ['sub']}):
            try:
                school, dept = span.text.split(',')
                locs.append(school[25:])
                depts.append(dept[1:])
            except:
                locs.append('')
                depts.append('')
    return names, locs, depts

if __name__ == '__main__':
    prof_data = {'name': [],
                 'location': [],
                 'department': []}
    for i in tqdm(range(1426)):
        offset = 20*i
        params = {'offset': offset}
        html = requests.get(base_url, params).content
        names, locs, depts = scrape_search_result_page(html)
        prof_data['name'] += names
        prof_data['location'] += locs
        prof_data['department'] += depts
    df = pd.DataFrame.from_dict(prof_data)
    df.to_csv('prof_data_from_rmp.csv')
