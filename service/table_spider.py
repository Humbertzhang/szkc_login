import asyncio
import aiohttp

table_url = "http://122.204.187.9/jwglxt/kbcx/xskbcx_cxXsKb.html?gnmkdmKey=N253508"

async def get_table(cookies, xnm, xqm):
    payload = {
        "xnm":xnm,
        "xqm":xqm,
    }
    async with aiohttp.ClientSession(headers = headers,
                                     cookies = cookies) as session:
        async with session.post(table_url, data = payload) as resp:
            json_data = await resp.json()
            prased_table = prase_table(json_data)
            return prased_table


def prase_table(json_data):
    try:
        kbList = json_data.get('kbList')
        kcList = []
        weeks_list = []
        for item in kbList:
            _weeks = item.get('zcd')
            if '(' in _weeks:
                weeks = _weeks.split('(')
                time = weeks[0]
                mode = weeks[-1]
                if ',' in time:
                    times = time.split(',')
                    weeks_list.append(times[0][:-1])
                    time = times[1]
                _time = time.split('-')
                _start = int(_time[0])
                _last = int(_time[-1][:-1])
                if mode: # 奇偶
                    weeks_list = range(_start, _last+1, 2)
            elif ',' in _weeks:
                weeks = _weeks.split(',')
                weeks_list = []
                for week in weeks:
                    if '-' in week:
                        _start = int(week.split('-')[0])
                        _last = int(week.split('-')[1][:-1])
                        _weeks_list = range(_start, _last+1)
                        weeks_list += _weeks_list
                    else:
                        weeks_list.append(week[:-1])
            elif '-' in _weeks:
                weeks = _weeks.split('-')
                _start = int(weeks[0])
                _last = int(weeks[-1][:-1])
                weeks_list = range(_start, _last+1)
            else:
                weeks_list = [int(_weeks[:-1])]
            str_weeks_list = [str(i) for i in weeks_list]
            _class = item.get('jcs').split('-')
            s_class = int(_class[0])
            e_class = int(_class[-1])
            d_class = e_class - s_class + 1
            _item_dict = {
                'course': item.get('kcmc'),
                'teacher': item.get('xm').split("\n")[0],
                'weeks': ','.join(str_weeks_list),
                'day': item.get('xqjmc'),
                'start': s_class,
                'during': d_class,
                'place': item.get('xqmc') + item.get('cdmc'),
                'remind': False
            }
            kcList.append(_item_dict)
        return(kcList)
    except json.decoder.JSONDecodeError as e:
        return None
