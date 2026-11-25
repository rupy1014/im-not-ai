# 홍보 문구 실험 채점 — AI 티 표현 수(측정용 정규식)와 브리프 사실 누락.
# 사용: python3 extras/promo-bench/score.py [data 폴더]
import re,sys,os,json
B=sys.argv[1] if len(sys.argv)>1 else __import__('os').path.join(__import__('os').path.dirname(__file__),'data')
T={'드려요':r'[가-힣]*[해봐줘와어아여워려뎌겨쳐켜져내써꿔둬놔떠보]\s?드(?:려요|릴게요|립니다|릴게|리면서|리고|려\s?드)',
 '보세요.':r'[해봐아어여워뎌려겨쳐켜져]\s?보세요[.!]','재촉':r'지금\s?바로|놓치지\s?마세요|서두르세요|오늘\s?(?:당장|바로)',
 '안심':r'부담\s?없이|걱정\s?(?:마세요|하지\s?마세요)|몰라도\s?괜찮|누구나\s?(?:쉽게|편하게)|가볍게\s?(?:시작|참여)',
 '은유':r'첫걸음|열쇠|발목을\s?잡|날개를\s?달|든든한|여정','과장':r'(?<![가-힣])확\s?(?:줄|늘|바뀌|달라)|한\s?번에\s?(?:해결|끝|처리)',
 '질문훅':None}
FACTS={'d01':['무료','1시간|한 시간','코딩','보고서','메일','회의록','프롬프트','실수','자동화','질의응답','이름','이메일','다시보기','선착순','동료'],
 'd06':['대본','음성','자막','편집','몇 분','얼굴','스타일','목소리','다운로드','하루 한 편','무료','카드'],
 'e07':['매출','인사','보고서','12분','24강','VLOOKUP','피벗','게시판','24시간','79,000','평생','180일','7일','10%','미리보기']}
def body(p):
    t=open(p).read(); return t.split('<!-- HUMANIZE-SUMMARY')[0].strip()
def score(t,topic):
    c={k:(len(re.findall(v,t)) if v else int(bool(re.search(r'(?:나요|신가요|셨나요|셨다면|까요)[?,]',re.split(r'(?<=[.?!])\s',t)[0])))) for k,v in T.items()}
    miss=[f for f in FACTS[topic] if not re.search(f,t)]
    return sum(c.values()),c,miss,len(t)
arms={'0원본':'drafts/{n}.md','A원래스킬':'outputs/before/{n}.md','B정규식힌트':'outputs/after/{n}.md','C지침스킬':'outputs/guide/{n}.md',
 'D지침작성':'outputs/D/{n}.md','E작성+자가퇴고':'outputs/E/{n}.md','F초안+별도퇴고':'outputs/F/{n}.md','G지침작성+별도퇴고':'outputs/G/{n}.md','H지침작성+묶음퇴고':'outputs/H/{n}.md'}
tot={}
for a,pat in arms.items():
    row=[]
    for n in ['d01','d06','e07']:
        p=os.path.join(B,pat.format(n=n));
        if n=='e07' and a=='0원본': p=os.path.join(B,'drafts2/e07.md')
        if not os.path.exists(p): row.append(None); continue
        row.append(score(body(p),n))
    ok=[r for r in row if r]
    if not ok: continue
    print(f"{a:14} 티합계={sum(r[0] for r in ok):3}  사실누락={sum(len(r[2]) for r in ok):2} {[m for r in ok for m in r[2]]}  글자={[r[3] for r in ok]}")
    for r in ok: print('   ',{k:v for k,v in r[1].items() if v})
