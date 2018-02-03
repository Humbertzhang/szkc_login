import asyncio
import aiohttp
import time

pre_url = "http://122.204.187.9/jwglxt"
pre_url2 = "http://122.204.187.9/jwglxt/xtgl/dl_loginForward.html?_t="
login_url = "http://122.204.187.9/jwglxt/xtgl/login_login.html"
table_url = "http://122.204.187.9/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdmKey=N253508"
grade_url = "http://122.204.187.9/jwglxt/cjcx/cjcx_cxDgXscj.html?doType=query&gnmkdmKey=N305005"

TEST_SID = 2016210942
TEST_PWD = "humbert123456781"
xnm = 2017
xqm = 3


headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36"        
}


async def login_szkc(sid, pwd):
    async with aiohttp.ClientSession(cookie_jar = aiohttp.CookieJar(unsafe=True),
                                     headers = headers) as session:
        async with session.get(pre_url) as resp:
            if resp.status == 200:
                tlist = str(time.time()).split('.')
                t = tlist[0] + tlist[1][0:3]
                async with session.get(pre_url2 + t) as resp2:
                    if resp2.status == 200:
                        payload = {
                            "yhm":sid,
                            "mm":pwd,
                            "yzm":""
                        }
                        async with session.post(login_url, data = payload) as resp3:
                            resp_text = await resp3.text()
                            loginok = False
                            msg = ""
                            if "用户名或密码不正确" in resp_text:
                                msg = "用户名或密码错误"
                            elif "xskbcx_cxXskbcxIndex.html" in resp_text:
                                loginok = True
                            elif "登录超时" in resp_text:
                                msg = "登录超时"
                            else:
                                msg = "未知错误"

                            cookies = {}
                            if loginok: 
                                for cookie in session.cookie_jar:
                                    cookies[cookie.key] = cookie.value
                                print(cookies)
                                return cookies
                            else:
                                return {"msg":msg}

async def get_grade(sid, s, ip):
    cookies = {
        'BIGipServerpool_xg_szxk':ip,
        'JSESSIONID':s,
    }

    tlist = str(time.time()).split('.')
    t = tlist[0] + tlist[1][0:3]
    payload = {
        "xnm": xnm,
        "xqm": xqm,
        "_search": False,
        "nd": t,
        "queryModel.showCount":100,
        "queryModel.currentPage":1,
        "queryModel.sortName":"",
        "queryModel.sortOrder":"asc",
        "time":0
    }
    async with aiohttp.ClientSession(headers = headers, cookies = cookies,
                                     data = payload) as session:
        async with session.post(grade_url, data = payload) as resp:
            json_data = await resp.json()
            print(json_data)


#############TEST ZONE###############
async def bound_login(sem):
    async with sem:
        print("|||Started|||")
        await login_szkc(TEST_SID, TEST_PWD)


async def test_login():
    TASK_NUM = 50
    tasks = []
    sem = asyncio.Semaphore(50)
    for i in range(TASK_NUM):
        task = asyncio.ensure_future(bound_login(sem))
        tasks.append(task)
    resp = asyncio.gather(*tasks)
    await resp
#############TEST ZONE###############

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(login_szkc(TEST_SID, TEST_PWD))
    #loop.run_until_complete(test())
    loop.close()
