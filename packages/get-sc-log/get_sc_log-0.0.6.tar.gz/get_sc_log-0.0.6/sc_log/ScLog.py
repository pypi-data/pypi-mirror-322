import re
import requests
import time
from datetime import datetime, timedelta,timezone
import json

def get_original_log(data):
    """默认查询最近15min,返回最原始的日记信息"""
    # 从输入数据中提取参数
    project = data["project"]
    logStore = data["logStore"]
    url = "https://xjp-logger-service-s-backend-sysop.inshopline.com/api/getLogs"
    headers = {"Content-Type": "application/json"}
    line = data.get("line", 2)
    offset = data.get("offset", 0)

    # 计算时间范围
    time_15_minutes_ago = datetime.now() - timedelta(days=5)
    timestamp_15_minutes_ago = int(time_15_minutes_ago.timestamp())
    start_time = timestamp_15_minutes_ago
    end_time = int(time.time())
    # 覆盖默认时间范围，如果提供了自定义时间
    start_time = data.get("from",start_time)
    end_time = data.get("to", end_time)
    # 设置请求参数
    params = {"project": project, "logStore": logStore, "from": start_time, "to": end_time,"line":line,"offset":offset}
    # 添加查询条件
    if "query" in data:
        query = data["query"]
        params["query"] = query
    response = requests.get(url, params=params, headers=headers).json()
    return response


def get_msg_log(data):
    """处理返回的日记，"""
    response = get_original_log(data)
    logs = response["data"]["logs"]
    # print("logs",logs)
    m_contents = [log["mLogItem"]["mContents"] for log in logs]
    # print(json.dumps(m_contents))
    log_msg_list = []
    for cotent in m_contents:
        log_msg = {}
        for t in cotent:
            if t["mKey"]=="msg":
                log_msg["msg"] = t["mValue"]
            elif t["mKey"]=="traceId":
                log_msg["traceId"] = t["mValue"]
        log_msg_list.append(log_msg)
    return log_msg_list

def get_http_data(http_data):
    fields = {}
    patterns = {
        'method': r'(?<=method: )\s*(\w+)',
        'uri': r'(?<=uri: )\s*(?P<uri>.+)',
        'requestHeader': r'(?<=requestHeader: )\s*(\{.*?\})',
        'requestParams': r'(?<=requestParams: )\s*(\{.*?\})',
        'requestBody': r'(?<=requestBody: )(\{[^}]+\})[\s\S]*?(?=responseCode)',
        'responseCode': r'(?<=responseCode: )\s*(\d+)',
        'responseHeader': r'(?<=responseHeader: )\s*(\{.*?\})',
        'responseBody': r'(?<=responseBody: )\s*(\{.*?\})[\s\S]*?(?=error)'
    }
    for i in patterns.keys():
        # print(i)
        match = re.search(patterns[i], http_data)
        if match:
            result = match.group(0)
            fields[i] = result
            # print("%s:"%i,result)
    # print(json.dumps(fields))
    #JSON 字符串进行序列化
    # print(fields["requestBody"])
    fields['requestHeader'] = json.loads(fields['requestHeader'])
    fields['requestParams'] = json.loads(fields['requestParams'])
    fields['requestBody'] = json.loads(fields['requestBody'])
    fields['responseHeader'] = json.loads(fields['responseHeader'])
    fields['responseBody'] = json.loads(fields['responseBody'])
    return fields

def sc_assert(data):
    #data = 格式如下
    # assert_data = [{"actual": "123", "expect": "123", "type": "eq"}, {"actual": "1234", "expect": "123", "type": "in"},
    #                {"actual": "123", "expect": "123"}]
    for i in data:
        actual = i["actual"]
        expect = i["expect"]
        type= i.get("type","eq")
        if type=="eq":
            try:
                assert actual==expect
            except AssertionError:
                return "实际值:%s,期望值：%s断言失败"%(actual,expect)
        elif type == "neq":
            try:
                assert actual != expect
            except AssertionError:
                return "实际值:%s,期望值：%s断言失败" % (actual, expect)
        elif type=="in":
            try:
                assert actual in expect or expect in actual
            except AssertionError:
                return "实际值:%s,期望值：%s断言失败" % (actual, expect)
        elif type == "notin":
            try:
                assert actual not in expect or expect not in actual
            except AssertionError:
                return "实际值:%s,期望值：%s断言失败" % (actual, expect)
        elif type == "gt":
            try:
                assert actual>expect
            except AssertionError:
                return "实际值:%s,期望值：%s断言失败" % (actual, expect)
        elif type == "egt":
            try:
                assert actual >= expect
            except AssertionError:
                return "实际值:%s,期望值：%s断言失败" % (actual, expect)
        elif type == "lt":
            try:
                assert actual < expect
            except AssertionError:
                return "实际值:%s,期望值：%s断言失败" % (actual, expect)
        elif type == "elt":
            try:
                assert actual <= expect
            except AssertionError:
                return "实际值:%s,期望值：%s断言失败" % (actual, expect)



def get_current_utc_time():
    # 获取当前 UTC 时间
    current_utc_time = datetime.now(timezone.utc)
    # 格式化为 YYYY-MM-DDTHH:MM
    formatted_time = current_utc_time.strftime('%Y-%m-%dT%H:%M')
    return formatted_time




if __name__=="__main__":
    data = {"project":"sl-aquaman-sl-user-center-sz","logStore":"sl-aquaman-sl-user-center_test"}
    data["query"] = 'af63259b535e60f4aaf358fed72b5811 and http and msg: "completed." and msg: open_host and msg: jobs '
    log_msg = get_msg_log(data)
    fields = get_http_data(log_msg[1]["msg"])
    print(fields["responseBody"])
    # assert_data = [{"actual":"123","expect":"123","type":"eq"},{"actual":"我","expect":"是","type":"in"},{"actual":"123","expect":"123"}]
    # res = sc_assert(assert_data)
    # print(res)
    # 获取并打印当前时间的零时区格式
    # current_time = get_current_utc_time()
    # print(current_time)
    # assert "2025-01-18T02:20" in "2025-01-18T02:20:03.158Z"

