import re,json,glob,sys
B=sys.argv[1]
ai=[open(f).read() for f in sorted(glob.glob(B+'/drafts/d*.md'))]
hu=[r['text'] for r in json.load(open(B+'/human/toss_pre2022.json'))]
P={
 'deuryeo':r'(?:해|아|어|여|워|줘)\s?드(?:려요|릴게요|립니다|릴게|려\s?드|리고|릴\s)',
 'qhook_start':None,
 'cta_try':r'(?:해|아|어|여|워)\s?보세요[.!]',
 'cta_now':r'지금\s?바로|놓치지\s?마세요|서두르세요|오늘\s?(?:당장|바로)',
 'burden':r'부담\s?없이|걱정\s?(?:마세요|하지\s?마세요|없이)|몰라도\s?괜찮|누구나\s?(?:쉽게|편하게)|가볍게\s?(?:시작|참여|들)',
 'metaphor':r'첫걸음|열쇠|발목을\s?잡|날개를\s?달|든든한\s?(?:동반자|파트너)|여정|한\s?걸음\s?더',
 'run':r'(?<![가-힣])(?:돌려요|돌려\s?(?:놓|두)|도는\s?법|돌아가게|알아서\s?돌)',
 'alaseo':r'알아서',
 'hanbeone':r'한\s?번에|한\s?곳에서',
 'hwak':r'확\s?(?:줄|늘|바뀌)',
}
def qhook(t):
    s=re.split(r'(?<=[.?!])\s',t.strip())[0]
    return bool(re.search(r'(?:나요|신가요|셨나요|으신가요|인가요|까요)\?$',s))
def rate(docs,k,rx):
    if k=='qhook_start':
        hit=[qhook(d) for d in docs]; return sum(hit)/len(docs), None
    n=[len(re.findall(rx,d)) for d in docs]; chars=sum(len(d) for d in docs)
    return sum(1 for x in n if x)/len(docs), sum(n)/chars*1000
# human: also cut into 600-char windows to compare doc-presence fairly
win=[]
for d in hu:
    for i in range(0,len(d)-600,600): win.append(d[i:i+600])
print(f"{'pattern':12} {'AI doc%':>8} {'HU win%':>8} {'AI /1k':>7} {'HU /1k':>7}")
for k,rx in P.items():
    a=rate(ai,k,rx); h=rate(win if k!='qhook_start' else hu,k,rx)
    f=lambda x: '-' if x is None else f'{x:.2f}'
    print(f"{k:12} {a[0]*100:7.0f}% {h[0]*100:7.1f}% {f(a[1]):>7} {f(h[1]):>7}")
print('HU windows',len(win),'yo-ratio',sum(d.count('요.') for d in hu)/max(1,sum(d.count('다.') for d in hu)))
