import urllib2
from bs4 import BeautifulSoup as bs


def get_job_name():
    return raw_input("Enter job name: ")  # comment1


def check_pages(link):
    html = urllib2.urlopen(link).read()
    soup = bs(html, "lxml")
    page_no = soup.find_all('a', class_="desktopPagin_item_link")  # finds all tags for Paging,
    if page_no == []:  # returns 1 if no Paging tags are found
        return 1
    else:
        last_page = []
        for p in page_no:
            last_page.append(p.get('href')[-1])
        return int(last_page[-2])  # returns number of Paging tags


def create_first_link(job_name):
    # function returning full link to site with links for given job positions
    url_job_name = urllib2.quote(job_name)
    return "https://www.pracuj.pl/praca/{};kw".format(url_job_name)


def get_all_links(url, url_no):
    # change to loop over pages
    full_link = []
    for u in range(1, url_no + 1):
        full_link.append(url+'?pn={}'.format(u))
    list_of_links = []
    for f in full_link:
        html = urllib2.urlopen(f).read()
        soup = bs(html, "lxml")
        links = soup.find_all('a', class_="o-list_item_link_name")
        for link in links:
            list_of_links.append(link.get('href'))
    return list_of_links

# print check_pages(create_first_link('Senior Data Scientist'))
parsed = create_first_link('Data Scientist')

links1 = get_all_links(parsed, check_pages(parsed))[0:11]


def job_offers_dict(links):
    job_offers = {}
    for l in links:
        job_offers[l] = {}
    for key in job_offers.keys():
        url = "https://www.pracuj.pl" + str(key)
        html = urllib2.urlopen(url).read()
        soup = bs(html, "lxml")
        if soup.find(id='description') is not None:
            job_offers[key]["Job_Description"] = soup.find(id='description').get_text()
        else:
            job_offers[key]["Job_Description"] = soup.find(id='offer').get_text()
    return job_offers

print job_offers_dict(links1)

