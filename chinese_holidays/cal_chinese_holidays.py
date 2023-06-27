import requests
import json
import datetime
import os


now = datetime.datetime.now()


def get_baidu_almanac(year=str(now.year), month=now.month):
    headers = {
        "Content-Type": "application/json;charset=UTF-8"
    }
    param = {
        "query": year + "年" + month + "月",
        "resource_id": "39043",
        "t": "1604395059555",
        "ie": "utf8",
        "oe": "gbk",
        "format": "json",
        "tn": "wisetpl",
        "cb": ""
    }
    # 抓取位置：百度搜索框搜索日历，上面的日历的接口，可以在页面上进行核对
    r = requests.get(url="https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php", headers=headers, params=param).text
    almanac = json.loads(r)["data"][0]["almanac"]
    return almanac


def get_holidays(year=str(now.year), result_save_dir=None):
    months = ['2', '5', '8', '11'] # 传'2'，返回1-3月数据，依次类推，这里仅需调用4次即可获得全年数据
    almanacs = []
    for month in months:
        almanac = get_baidu_almanac(year=year, month=month)
        almanacs += almanac
    # 对每天进行分析: (1) 是否为周末 (2)是否为休息日 (3) 是否为国家法定节假日 (4) 农历、忌宜事项等
    days_info = []
    for ele in almanacs:
        day_info = dict()
        day_info['animal'] = ele['animal']
        day_info['avoid'] = ele['avoid']
        day_info['suit'] = ele['suit']
        day_info['weekday'] = ele['cnDay']
        day_info['year'] = ele['year']
        day_info['month'] = ele['month']
        day_info['day'] = ele['day']
        date_str = datetime.datetime(int(ele['year']), int(ele['month']), int(ele['day'])).strftime('%Y-%m-%d')
        day_info['date'] = date_str
        day_info['gzDate'] = ele['gzDate']
        day_info['gzMonth'] = ele['gzMonth']
        day_info['gzYear'] = ele['gzYear']
        day_info['lunarDay'] = ele['lunarDate']
        day_info['lunarMonth'] = ele['lunarMonth']
        day_info['lunarYear'] = ele['lunarYear']
        day_info['lunarDate'] = ele['lunarYear'] + '-' + ele['lunarMonth'] + '-' + ele['lunarDate']
        day_info['lDay'] = ele['lDate']
        day_info['lMonth'] = ele['lMonth']
        day_info['status'] = ele.get('status', None)
        day_info['generalFestival'] = ele.get('festivalList', None)
        day_info['traditionalFestival'] = None
        day_info['nationalHoliday'] = None
        day_info['isRestDay'] = False
        if 'festivalList' in ele and 'type' in ele:
            if ele['type'] == 't':  # 中国传统节日
                if 'term' in ele and len(ele['term']) > 0:
                    day_info['traditionalFestival'] = ele['term']
                elif 'value' in ele:
                    day_info['traditionalFestival'] = ele['value']
            if 'status' in ele:
                if ele['status'] == '1':  # '1'表示放假
                    day_info['nationalHoliday'] = ele['term']
        # 判断周末是否为休息日
        if ele["cnDay"] == '日' or ele["cnDay"] == '六':
            if 'status' in ele:
                if ele["status"] == "2":
                    # status为2的时候表示周末的工作日,百度日历上会有班标志的数据
                    day_info['isRestDay'] = False
                else:
                    # 普通周末时间
                    day_info['isRestDay'] = True
            else:
                day_info['isRestDay'] = True
        if 'status' in ele and ele["status"] == "1":
            # status为1的时候表示休息日，百度日历上会有休标志的数据
            day_info['isRestDay'] = True
        if day_info not in days_info:
            days_info.append(day_info)
    # 升序排序
    days_info = sorted(days_info, key=lambda x: x['date'])
    national_info, traditional_info,  general_info, rest_day_info = [], [], [], []
    for ele in days_info:
        if ele['nationalHoliday']:
            national_info.append({'value': ele['nationalHoliday'], 'date': ele['date']})
        if ele['traditionalFestival']:
            traditional_info.append({'value': ele['traditionalFestival'], 'date': ele['date']})
        if ele['generalFestival']:
            general_info.append({'value': ele['generalFestival'], 'date': ele['date']})
        if ele['isRestDay']:
            rest_day_info.append({'value': ele['isRestDay'], 'date': ele['date']})
    result = {'data': days_info, 'nationalHolidays': national_info, 'traditionalFestivals': traditional_info,
              'generalFestivals': general_info, 'isRestDays': rest_day_info}
    if result_save_dir:
        # 写入json
        json_path = os.path.join(result_save_dir, f'{year}_holidays_info.json')
        with open(json_path, 'w', encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False)
    return result


if __name__ == '__main__':
    info = get_holidays(year='2023', result_save_dir=r'/')
    print(info)