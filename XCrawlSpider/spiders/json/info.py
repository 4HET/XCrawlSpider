import re
import json

fp = open('./info.json', 'r', encoding='utf-8')
# 读取 json文件
data = json.load(fp)
reviewAllDOList = data['reviewAllDOList']
fp = open('./review.json', 'r', encoding='utf-8')
kv = json.load(fp)
for reviewDataVO in reviewAllDOList:
    # 评论体
    repl = reviewDataVO['reviewDataVO']['reviewData']['reviewBody']
    # print(repl)
    # print(repl)
    repl = re.sub('<svgmtsi class="review">', '', reviewDataVO['reviewDataVO']['reviewData']['reviewBody'])
    repl = re.sub('</svgmtsi>', '', repl)
    repl = re.sub(r'<br />', '', repl, re.DOTALL)
    repl = re.sub(r'<img class=".*?" src=".*?" alt=""/>', '', repl, re.DOTALL)
    repl = re.sub(r'&nbsp;', '', repl, re.DOTALL)
    print(repl)
    # # print(kv.keys())
    for k in kv.keys():
        key = k.replace('uni', '&#x') + ';'
        # print(key)
        # 将key替换为kv[k]
        repl = repl.replace(key, kv[k])
        print(key, kv[k])
    print(repl)