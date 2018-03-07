# --* coding:utf-8 *--

import requests
from bs4 import BeautifulSoup
import os
import pdfkit
import re
import traceback

# Download the page
def download(url,retry=1):
    print("Downloading: "+url)
    try:
        result = requests.get(url)
        result.encoding = 'utf-8'
        content = result.text
    except :
        content = None
        if retry >0:
            if result.status_code >=500 and result.status_code <600:
                return download(url,retry-1)
    return content


def links_module(seed_url):
    seed_page = download(seed_url)
    soup = BeautifulSoup(seed_page,"lxml")
    beta = soup.find_all("div",id="beta")
    module_content = beta[0].find_all("div",class_="module-content")
    a_set = module_content[0].find_all("a")
    module_dic = {}
    #print(a_set)
    for a in a_set:
        module_link = a["href"]
        module_name = module_link.split('/')[-2]
        module_dic[module_name] = module_link
    return module_dic


def links_artitle(link_module):
    html = download(link_module)
    soup = BeautifulSoup(html, "lxml")
    alpha = soup.find_all("div",id="alpha")[0]
    module_content = alpha.find_all("div",class_="module-content")[0]
    a_set = module_content.find_all("a")
    links_dir = {}
    pattern = r"http://www.ruanyifeng.com/blog/\d{4}/\d{2}/([a-z0-9].*?-*).html"
    prog = re.compile(pattern)
    for a in a_set:
        article_link = a["href"]
        #print(article_link)
        m = prog.match(article_link)
        article_name = m.group(1)
        #print(article_name)
        links_dir[article_name] = article_link
    return links_dir

def parse_url_to_html(url,name):
    try:
        origin_html = download(url)
        html_soup = BeautifulSoup(origin_html, "lxml")
        article_tag = html_soup.find_all("article",class_="hentry")
        title = article_tag[0].h1
        content = article_tag[0].find_all("div",id="main-content")[0]
        content.insert(1,title)
        pattern = "(<img .*?src=\")(.*?)(\")"
        def func(m):
            #print(m.groups())
            if not m.group(2).startswith("http"):
                rtn = m.group(1) + "http://www.ruanyifeng.com" + m.group(2) + m.group(3)
                return rtn
            else:
                return m.group(1) + m.group(2) + m.group(3)

        html_str = str(content)
        html_str = re.compile(pattern).sub(func, html_str)
        html = html_str.encode("utf-8")
        with open(name, 'wb') as f:
            f.write(html)
        return name
    except Exception as e:
        print("Parse url to html Error")
        traceback.print_exc()


def save_pdf(htmls, file_name):
    """ 
    把所有html文件保存到pdf文件 
    :param htmls:  html文件列表 
    :param file_name: pdf文件名 
    :return: 
    """
    try:
        path_wk = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
        config = pdfkit.configuration(wkhtmltopdf=path_wk)
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
        pdfkit.from_file(htmls, file_name, options=options,configuration=config)
    except Exception as e:
        print("Save pdf Error")
        traceback.print_exc()



def main():
    base = "D:\\ruanyifeng\\"
    seed_url = "http://www.ruanyifeng.com/blog/developer/"
    module_links = links_module(seed_url)
    for m_name,m_link in module_links.items():
        article_links = links_artitle(m_link)
        base_dir = base+ m_name
        if not os.path.exists(base_dir):
            os.makedirs(base_dir)
        for a_name,a_link in article_links.items():
            path_html = base_dir + "\\" + a_name+".html"
            path_pdf = base_dir + "\\" + a_name+".pdf"
            html = parse_url_to_html(a_link,path_html)
            pdf = save_pdf(html,path_pdf)

def test():
    test_html = r"D:\ruanyifeng\html\essays\death.html"
    test_pdf = save_pdf(test_html,r"D:\ruanyifeng\html\essays\death.pdf")




if __name__ == "__main__":
    #test()
    main()




