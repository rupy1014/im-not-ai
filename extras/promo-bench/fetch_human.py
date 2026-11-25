import re,sys,json,random,urllib.request,html,concurrent.futures as cf
# 2018~2022 토스피드 글(사람 해요체 비교군)을 다시 받는다. 본문은 저장소에 넣지 않는다(저작권).
# 사용: python3 fetch_human.py <작업폴더>  (작업폴더/human/urls.txt 필요 — data/toss_urls.txt 를 복사)
B=sys.argv[1]
urls=[u.strip().replace('alpha.toss.im','toss.im') for u in open(B+'/human/urls.txt') if u.strip()]
random.seed(7);random.shuffle(urls)
def get(u):
    try:
        h=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=20).read().decode('utf-8','ignore')
    except Exception: return None
    m=re.search(r'\\"publishedTime\\":\\"(\d{4}-\d\d-\d\d)',h)
    if not m: return None
    d=m.group(1)
    body=re.sub(r'(?s)<(script|style)[^>]*>.*?</\1>','',h)
    ps=[html.unescape(re.sub(r'<[^>]+>','',p)).strip() for p in re.findall(r'(?s)<p[^>]*>(.*?)</p>',body)]
    ps=[p for p in ps if len(p)>25 and re.search(r'[가-힣]',p)]
    return {'url':u,'date':d,'text':'\n'.join(ps)}
out=[]
with cf.ThreadPoolExecutor(8) as ex:
    for r in ex.map(get,urls[:400]):
        if r and r['date']<'2022-11-01' and len(r['text'])>400: out.append(r)
json.dump(out,open(B+'/human/toss_pre2022.json','w'),ensure_ascii=False)
print(len(out), sum(len(r['text']) for r in out), min(r['date'] for r in out), max(r['date'] for r in out))
