""" 代码说明：   用于modis数据的下载。 
                get_download_list 函数，是数据下载部分。download_wait：待下载的数据列表，例如：['MOD09GQ.006/2018.01.01/MOD09GQ.A2018001.h31v06.006.2018003030441.hdf', 'MOD09GQ.006/2018.01.02/MOD09GQ.A2018002.h31v06.006.2018004031248.hdf'],
                save_path：数据保存地址。
                get_cookie 函数，是登录网页。
                username,password：用户名和密码
                """

from bs4 import BeautifulSoup
import requests
import os

def get_download_list():
    # 登录网址，获取cookie
    cookie=get_cookie('liqian634126236','Liqian5217319')
    #get里有俩参数，一个是你的下载地址url，一个是cookie，你不用管，你只需要for循环下载地址就行了
    filename = '/home/lss/data/python/zr.txt'
    with open(filename,'r') as f:
        lines = f.readlines()
        for line in lines[2:]:
            URL = line[:-1]
            print(URL)
            r=requests.get(URL,cookies=cookie)
            year = line[53:57]
            month = line[58:60]
            day = line[61:63]

            fout = '/home/lss/data/python/OMI'+year+'_'+day+'.he5'
            if (os.path.isfile(fout)):
                print("ok",fout)
            else:
                with open(fout,"wb") as f:
                    f.write(r.content)

# 获取下载的cookie
def get_cookie(username,password):
    
    Base_URL = "https://urs.earthdata.nasa.gov/home"
    Login_URL = "https://urs.earthdata.nasa.gov/login"
    
    '''
    这里用于获取登录页的html，以及cookie
    :param url: https://urs.earthdata.nasa.gov/home
    :return: 登录页面的HTML,以及第一次的cooke
    '''
    html = requests.get(Base_URL)
    first_cookie = html.cookies.get_dict()
    print("first_cookie:",first_cookie)
    #return response.text,first_cookie
    
    '''
    处理登录后页面的html
    :param html:
    :return: 获取csrftoken
    '''
    soup = BeautifulSoup(html.text,'html.parser')
    res = soup.find("input",attrs={"name":"authenticity_token"})
    token = res["value"]
    print("token:",token)
    #return token
    
    '''
    这个是用于登录
    :param url: https://urs.earthdata.nasa.gov/login
    :param token: csrftoken
    :param cookie: 第一次登录时候的cookie
    :return: 返回第一次和第二次合并后的cooke
    '''
    
    data= {
        "commit": "Log in",
        "utf8":"✓",
        "authenticity_token":token,
        "username":username,
        "password":password
    }
    response = requests.post(Login_URL,data=data,cookies=first_cookie)
    print(response.status_code)
    cookie = response.cookies.get_dict()
    #这里注释的解释一下，是因为之前是通过将两次的cookie进行合并的
    #现在不用了可以直接获取就行
    # cookie.update(second_cookie)
    print("cookie:",cookie)
    return cookie


#调用函数
get_download_list()

