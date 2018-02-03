from aiohttp import web
from aiohttp.web import Response, json_response, Application
from .decorator import require_szkc_login
from .login_spider import login_szkc
from .grade_spider import get_grade
from .table_spider import get_table
import os

api = web.Application()

async def login_szkc_api(request):
    jdata = await request.json()
    sid = jdata['sid']
    pwd = jdata['pwd']
    cookies = await login_szkc(sid, pwd)
    return json_response(cookies)

@require_szkc_login
async def grade_all_api(request, sid, cookies):
    query_string = request.rel_url.query_string
    if query_string:
        keys = []; vals = []
        for _ in query_string.split('&'):
            keys.append(_.split('=')[0])
            vals.append(_.split('=')[1])
        args = dict(zip(keys, vals))
        xnm = args.get('xnm'); xqm = args.get('xqm')
    gradeList = await get_grade(cookies, sid, xnm, xqm)
    if gradeList:
        return json_response(gradeList)
    else:
        return Response(body=b'', content_type='application/json', status=403)

@require_szkc_login
async def szkc_table_api(request, sid, cookies):
    #先查询出课表，再添加到数据库中
    xnm = os.getenv('XNM')
    xqm = os.getenv('XQM')
    tabledb = request.app['tabledb']
    userdb = request.app['userdb']
    document = await tabledb.tables.find_one({'sid': sid})
    userdoc = await userdb.users.find_one({'sid': sid})
    usertables = []
    if userdoc:
        usertables = userdoc['table']
    #用户还没有普通课表
    if not document:
        return Response(body = b'{"msg":"user have no normal table"}',
                        content_type='application/json', status=400)
    #获取素质课课表
    tables = await get_table(cookies, xnm, xqm)
    #若有则加入到数据库中
    if tables:
        for index, item in enumerate(tables):
            tables[index]['id'] = str(index+1) #分配ID
            tables[index]['color'] = index-4*(index//4) # 分配color
        await tabledb.tables.insert_one({'sid': sid, 'table': tables})
        return web.json_response(tables+usertables)
    #否则返回403
    return web.Response(body=b'{"msg": "can not get szkc table"}',
                        content_type='application/json', status=403)


api.router.add_route('POST', '/szkc/login/', login_szkc_api, name='login_szkc_api')
api.router.add_route('GET', '/szkc/grade/', grade_all_api, name='szkc_grade_api')
api.router.add_route('GET', '/szkc/table/', szkc_table_api, name='szkc_table_api')