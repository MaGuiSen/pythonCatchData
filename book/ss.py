#
# import sys,os
# print sys.path
# print os.path.dirname(__file__)

v = '''JSESSIONID=2ad86e161f283d233e71da3c062f07350257435a809e0fe4189cb72ebe5d6317; wuid=567120835966164; wuid_createAt=2017-06-30 12:47:59; weather_auth=2; captcha=s%3A09685a3044a9a523ec779191971ae559.cSQoBtWi18ke52SSAYkRzvu4RmMrakOgQgFxeJpimYQ; Hm_lvt_15fafbae2b9b11d280c79eff3b840e45=1499861822,1500904156,1500989430,1501067829; Hm_lpvt_15fafbae2b9b11d280c79eff3b840e45=1501073083; cn_9a154edda337ag57c050_dplus=%7B%22distinct_id%22%3A%20%2215cf753c1ce41e-01a3b15fcaada1-4383666-100200-15cf753c1cf393%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201501073081%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201501073081%2C%22%E6%9D%A5%E6%BA%90%E6%B8%A0%E9%81%93%22%3A%20%22%22%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D%2C%22initial_view_time%22%3A%20%221499857767%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%7D; UM_distinctid=15cf753c1ce41e-01a3b15fcaada1-4383666-100200-15cf753c1cf393; CNZZDATA1255169715=359892489-1498797024-null%7C1501070424'''
map = v.split(';')
cookie = {}
for m in map:
    m = m.strip(' ')
    keyValue = m.split('=')
    cookie[keyValue[0]] = keyValue[1]
print cookie