import asyncio
import aiohttp
import time

pre_url = "http://122.204.187.9/jwglxt"
pre_url2 = "http://122.204.187.9/jwglxt/xtgl/dl_loginForward.html?_t="
login_url = "http://122.204.187.9/jwglxt/xtgl/login_login.html"
table_url = "http://122.204.187.9/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdmKey=N253508"
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
                            if "error_ico" in resp_text:
                                print("密码错误")
                            elif "xskbcx_cxXskbcxIndex.html" in resp_text:
                                loginok = True
                                print("登录成功")
                            else:
                                print("未知错误")
                                print(resp_text)
                            
                            if loginok:
                                search_data = {
                                    "xnm":xnm,
                                    "xqm":xqm
                                }
                                async with session.post(table_url, data = search_data) as resp4:
                                    json_data = await resp4.json()
                                    print(json_data)


                            

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(login_szkc(2016000000, "********"))
    loop.close()
