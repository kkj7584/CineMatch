# -*- coding: utf-8 -*-
"""
jinja2 표현식 
 - 템플릿에서 python 객체 표현식 
 - templates/step02 작성
"""

from flask import Flask, render_template, request # html 페이지 호출 
import os

# 1. app 객체 생성 
app = Flask(__name__) 

from sentence_transformers import SentenceTransformer # 모델 불러오기
model = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2") # 모델 불러오기
import numpy as np

genre=['드라마', '범죄', '로맨스', '공포', '스릴러', '액션', '모험', 'SF', '코미디', '역사', '미스터리', 'TV 영화', '가족', '전쟁', '애니메이션', '서부', '다큐멘터리', '판타지', '음악']
language_ko_map = {
"English": "영어",
"Spanish": "스페인어",
"Italian": "이탈리아어",
"Japanese": "일본어",
"German": "독일어",
"French": "프랑스어",
"Albanian": "알바니아어",
"Slovak": "슬로바키아어",
"Tagalog": "타갈로그어",
"Norwegian": "노르웨이어",
"Polish": "폴란드어",
"Czech": "체코어",
"Turkish": "터키어",
"Arabic": "아랍어",
"Serbo-Croatian": "세르보크로아트어",
"Navajo": "나바호어",
"Portuguese": "포르투갈어",
"Danish": "덴마크어",
"Russian": "러시아어",
"Slovenian": "슬로베니아어",
"Hungarian": "헝가리어",
"Greek": "그리스어",
"Romanian": "루마니아어",
"No Language": "언어 없음",
"Yiddish": "이디시어",
"Indonesian": "인도네시아어",
"Hindi": "힌디어",
"Persian": "페르시아어",
"Mandarin": "중국어",
"Finnish": "핀란드어",
"Tamil": "타밀어",
"Cantonese": "광둥어",
"Swedish": "스웨덴어",
"Hebrew": "히브리어",
"Latin": "라틴어",
"Icelandic": "아이슬란드어",
"Bulgarian": "불가리아어",
"Malayalam": "말라얄람어",
"Marathi": "마라티어",
"Latvian": "라트비아어",
"Dutch": "네덜란드어",
"Estonian": "에스토니아어",
"Lithuanian": "리투아니아어",
"Azerbaijani": "아제르바이잔어",
"Vietnamese": "베트남어",
"Telugu": "텔루구어",
"Northern Sami": "북부 사미어",
"Uzbek": "우즈베크어",
"Korean": "한국어",
"Shona": "쇼나어",
"Catalan": "카탈루냐어",
"Esperanto": "에스페란토어",
"Malay": "말레이어",
"Bengali": "벵골어",
"Serbian": "세르비아어",
"Sinhalese": "싱할라어",
"Kirghiz": "키르기스어",
"Thai": "태국어",
"Georgian": "조지아어",
"Mongolian": "몽골어",
"Kannada": "칸나다어",
"Oriya": "오리야어",
"Armenian": "아르메니아어",
"Ukrainian": "우크라이나어",
"Basque": "바스크어",
"Turkmen": "투르크멘어",
"Hausa": "하우사어",
"Macedonian": "마케도니아어",
"Yoruba": "요루바어",
"Gujarati": "구자라트어",
"Breton": "브르타뉴어",
"Faroese": "페로어",
"Urdu": "우르두어",
"Kazakh": "카자흐어",
"Haitian; Haitian Creole": "아이티 크리올어",
"Tahitian": "타히티어",
"Cree": "크리어",
"Aymara": "아이마라어",
"Punjabi": "펀자브어",
"Sardinian": "사르데냐어",
"Walloon": "왈롱어",
"Afrikaans": "아프리칸스어",
"Maltese": "몰타어",
"Quechua": "케추아어",
"Uighur": "위구르어",
"Gaelic": "게일어",
"Ossetian; Ossetic": "오세트어",
"Kurdish": "쿠르드어",
"Croatian": "크로아티아어",
"Burmese": "버마어",
"Wolof": "월로프어",
"Irish": "아일랜드어",
"Kongo": "콩고어",
"Bambara": "밤바라어",
"Guarani": "과라니어",
"Welsh": "웨일스어",
"Zulu": "줄루어",
"Sanskrit": "산스크리트어",
"Bosnian": "보스니아어",
"Maori": "마오리어",
"Galician": "갈리시아어",
"Moldavian": "몰도바어",
"Nepali": "네팔어",
"Khmer": "크메르어",
"Pushto": "파슈토어",
"Norwegian Bokmål": "노르웨이어(보크말)",
"Samoan": "사모아어",
"Inuktitut": "이누크티투트어",
"Fulah": "풀라어",
"Tajik": "타지크어",
"Tswana": "츠와나어",
"Occitan": "오크어",
"Xhosa": "코사어",
"Avestan": "아베스타어",
"Lao": "라오어",
"Bislama": "비슬라마어",
"Belarusian": "벨라루스어",
"Chichewa; Nyanja": "체와어",
"Assamese": "아삼어",
"Slavic": "슬라브어",
"Igbo": "이그보어",
"Swahili": "스와힐리어",
"Divehi": "디베히어",
"Javanese": "자바어",
"Hiri Motu": "히리모투어",
"Amharic": "암하라어",
"Letzeburgesch": "룩셈부르크어",
"Twi": "트위어",
"Ido": "이도어",
"Frisian": "프리지아어",
"Somali": "소말리어",
"Tibetan": "티베트어",
"Ojibwa": "오지브와어",
"Raeto-Romance": "레토로만스어",
"Ganda": "간다어",
"Ewe": "에웨어",
"Lingala": "링갈라어",
"Malagasy": "말라가시어",
"Marshall": "마셜어",
"Sotho": "소토어",
"Tigrinya": "티그리냐어",
"Avaric": "아바르어",
"Akan": "아칸어",
"Interlingua": "인터링구아",
"Sindhi": "신디어",
"Dzongkha": "종카어",
"Volapük": "볼라퓌크어",
"Fijian": "피지어",
"Rundi": "룬디어",
"Tonga": "통가어",
"Cornish": "콘월어",
"Chechen": "체첸어",
"Kikuyu": "키쿠유어",
"Corsican": "코르시카어",
"Tatar": "타타르어",
"Kinyarwanda": "키냐르완다어",
"Bashkir": "바시키르어",
"Kalaallisut": "그린란드어",
"Kuanyama": "쿠안야마어",
"Inupiaq": "이누피아크어",
"Sango": "상고어",
"Interlingue": "인터링게어",
"Komi": "코미어",
"Kashmiri": "카슈미르어",
"Herero": "헤레로어",
"Abkhazian": "압하즈어",
"Afar": "아파르어",
"Chamorro": "차모로어",
"Limburgish": "림뷔르흐어",
"Sundanese": "순다어",
"Ndebele": "은데벨레어",
"Norwegian Nynorsk": "노르웨이어(뉘노르스크)",
"Aragonese": "아라곤어",
"Oromo": "오로모어",
"Tsonga": "총가어",
"Pali": "팔리어",
"Luba-Katanga": "루바카탕가어",
"Chuvash": "추바시어",
"Venda": "벤다어",
"Swati": "스와티어",
"Ndonga": "은동가어"
}

from babel import Locale

locale = Locale('ko')

country_dict = {
    code: locale.territories.get(code)
    for code in locale.territories
    if len(code) == 2  # ISO alpha-2 코드만
}

import pandas as pd
import glob
from huggingface_hub import hf_hub_download

'''
path = "Crawled_Data/*.csv"
file_list = glob.glob(path)

df_list = [pd.read_csv(file) for file in file_list]

df = pd.concat(df_list, ignore_index=True)
'''
files = [
"Crawled_Data/backup_until_1976_1986.csv",
"Crawled_Data/backup_until_1987_2001.csv",
"Crawled_Data/backup_until_2002_2006.csv",
"Crawled_Data/backup_until_2007_2011.csv",
"Crawled_Data/backup_until_2012_2025.csv",
"Crawled_Data/backup_until_2026_2026.csv"
]

dfs = []

for f in files:
    path = hf_hub_download(
        repo_id="kkj7584/movie-embeddings",
        filename=f,
        repo_type="dataset"
    )
    
    dfs.append(pd.read_csv(path))

df = pd.concat(dfs).reset_index(drop=True)

df = df.fillna("")
df = df[
    (df["overview"].str.len() > 20) |
    (df["genres"].str.len() > 0)
].reset_index(drop=True)



df = df[df['title'] != ""].reset_index(drop=True)
df["year"] = df["year"].astype(str).str[:4]

# app 초기화 시 한 번만 실행
df["countries_list"] = df["countries"].str.split(", ")
df["languages_list"] = df["languages"].str.split(", ")

# 앱 초기화 시 1회 실행
country_index = {}  # {'KR': [0, 5, 23, ...], 'US': [...]}
language_index = {}

for idx, row in df.iterrows():
    for c in row["countries_list"]:
        country_index.setdefault(c, []).append(idx)
    for l in row["languages_list"]:
        language_index.setdefault(l, []).append(idx)

'''
movie_texts = []

for _, row in df.iterrows():

    parts = []

    if row["title"]:
        parts.append(f"제목은 {row['title']}이다.")

    if row["original_title"]:
        parts.append(f"원제는 {row['original_title']}이다.")

    if row["languages"]:
        parts.append(f"언어는 {row['languages']}이다.")

    if len(row["overview"]) > 20:
        parts.append(f"줄거리는 {row['overview']}이다.")

    if row["tagline"]:
        parts.append(f"태그라인은 {row['tagline']}이다.")

    if row["genres"]:
        parts.append(f"장르는 {row['genres']}이다.")

    if row["companies"]:
        parts.append(f"제작사는 {row['companies']}이다.")

    if row["countries"]:
        parts.append(f"국가는 {row['countries']}이다.")

    if row["year"]:
        parts.append(f"연도는 {row['year']}이다.")

    movie_texts.append(". ".join(parts))

movie_embeddings = model.encode(movie_texts, normalize_embeddings=True)
'''
embedding_path = hf_hub_download(
    repo_id="kkj7584/movie-embeddings",
    filename="movie_embeddings.npy",
    repo_type="dataset"
)

movie_embeddings = np.load(embedding_path)

# 2. 서버 요청 & 응답
@app.route("/") # 요청1 : http://127.0.0.1:80/
def index() : # 응답 함수 
    return render_template('index.html',genrep=genre) # 응답 페이지 

def matchorder(oq,q,klang,kcount,method,t,ot,plang,pcount):
    if not q:return 0
    if method=='title':
        import re
        x1=t.lower()
        x2=ot.lower()
        t=t.lower().replace(' ','')
        ot=ot.lower().replace(' ','')
        if x1==oq or x2==oq:
            return 1
        elif t==q or ot==q:
            return 0.9
        elif oq and (bool(re.match(rf'^{re.escape(oq)} (?:[1-9]|[1-4][0-9]|50)(?!\d)', x1)) or bool(re.match(rf'^{re.escape(oq)} (?:[1-9]|[1-4][0-9]|50)(?!\d)', x2))):
            return 0.8
        elif q and (bool(re.match(rf'^{re.escape(q)}(?:[1-9]|[1-4][0-9]|50)(?!\d)', t)) or bool(re.match(rf'^{re.escape(q)}(?:[1-9]|[1-4][0-9]|50)(?!\d)', ot))):
            return 0.7
        elif ((q in x1.split(' ')) and t.startswith(q)) or ((q in x2.split(' ')) and ot.startswith(q)):
            return 0.65
        elif x1.startswith(oq) or x2.startswith(oq):
            return 0.6
        elif t.startswith(q) or ot.startswith(q):
            return 0.5
        elif q in x1.split(' ') or q in x2.split(' '):
            return 0.4
        elif oq in x1 or oq in x2:
            return 0.3
        elif q in x1 or q in x2:
            return 0.2
        else:
            return 0
    elif method=='language':
        nlang=[a for a in klang if (language_ko_map[a]).startswith(q)]
        for nl in nlang:
            if nl in plang:
                return 1
        return 0
    elif method=='country':
        ncount=[a for a in kcount if (country_dict[a]).startswith(q)]
        for nc in ncount:
            if nc in pcount:
                return 1
        return 0
    return 0

@app.route('/result', methods=['POST']) # post방식 전송 
def result() :  # 응답 함수
    
    # start

    query=request.form['query']
    realoriginq=query
    originq=query.lower()
    query = query.lower().replace(" ", "")
    query_embedding = model.encode(query, normalize_embeddings=True)
    
    exact_idx=[]
    
    method=request.form.get('method')
    
    if query and method=='title':
        title_lower = df["title"].str.lower().str.replace(" ", "")
        original_lower = df["original_title"].str.lower().str.replace(" ", "")

        mask = (
            title_lower.str.contains(query, na=False, regex=False) |
            original_lower.str.contains(query, na=False, regex=False)
            )

        exact_idx = df[mask].index

    keygenre=[]
    
    alls=request.form.get('all')
    
    selectedg=[]
    sec_exact_idx=[]
    st_exact_idx=[]
    if alls:
        selectedg.append('all')
        for g in genre:
            selectedg.append(g)
    else:
        for g in genre:
            if g.lower() in query:
                keygenre.append(g)
            else:
                if request.form.get(g):
                    keygenre.append(g)
                    selectedg.append(g)
    
        if '스릴' in query and '스릴러' not in keygenre:
            keygenre.append('스릴러')
        if 'tv' in query and 'TV 영화' not in keygenre:
            keygenre.append('TV 영화')
        
        if len(keygenre)>0:
            mask = df.apply(
                lambda row: all(
                g in str(row["genres"])
                for g in keygenre
                ),
                axis=1
            )
            sec_exact_idx = df[mask].index
            
            if len(sec_exact_idx)<500:
                mask = df.apply(
                    lambda row: any(
                    g in str(row["genres"])
                    for g in keygenre
                    ),
                    axis=1
                )
                st_exact_idx = df[mask].index
                

    keylang=[]
    
    splitq1=query.split(',')
    splitq2=originq.split(' ')
    splitq=list(set(splitq1+splitq2))
    
    for sq in splitq:
        if not sq:continue
        for u,v in language_ko_map.items():
            if v==sq or v==sq+'어':
                keylang.append(u)
                break

    if keylang==[]:
        for u,v in language_ko_map.items():
            if query in v:
                keylang.append(u)
    
    thr_exact_idx=[]
    thr2_exact_idx=[]
    
    if len(keylang)>0 and method=='language':
        sets = [set(language_index.get(l, [])) for l in keylang]
        thr_exact_idx = sets[0].intersection(*sets[1:])  # all
        if len(keylang) > 1:
            thr2_exact_idx = sets[0].union(*sets[1:])    # any

    keycount=[]
    if '한국' in query:
        keycount.append('KR')
    
    for sq in splitq:
        if not sq:continue
        for u,v in country_dict.items():
            if v==sq:
                keycount.append(u)
                break
            
    if keycount==[]:
        for u,v in country_dict.items():
            if query in v:
                keycount.append(u)
    
    fth_exact_idx=[]
    fth2_exact_idx=[]

    if len(keycount)>0 and method=='country':
        sets = [set(country_index.get(c, [])) for c in keycount]
        fth_exact_idx = sets[0].intersection(*sets[1:])  # all
        if len(keycount)>1:
            fth2_exact_idx = sets[0].union(*sets[1:]) # any
    
    getyear=request.form.get('year')
    import re
    year_match = re.search(r"(\d{4})년", query)

    if getyear!='all' or year_match:
        if getyear!='all':
            year=getyear
        elif year_match:
            year = year_match.group(1)
        fif_exact_idx = df[df["year"] == year].index.tolist()
    else:
        fif_exact_idx = []
    
    # start
    
    #if not query:
    #    scores = np.dot(movie_embeddings, query_embedding)
    #    top_k_idx_before = set(np.argsort(scores)[-5000:][::-1].tolist())

    top_k_idx_before = set()
    
    exact_idx     = set(exact_idx)
    sec_exact_idx = set(sec_exact_idx)
    st_exact_idx  = set(st_exact_idx)
    fif_exact_idx = set(fif_exact_idx)
    
    top_k_idx_before.update(exact_idx) # 제목 일치 인덱스 - 쿼리 기반
    if not query :
        for e in sec_exact_idx: # 장르 all 일치 인덱스 - 쿼리 기반 아님 - alls가 false면 필터링
            top_k_idx_before.add(e)
            if len(top_k_idx_before)>=10000:
                break
        for e in st_exact_idx: # 장르 any 일치 인덱스 - 쿼리 기반 아님
            top_k_idx_before.add(e)
            if len(top_k_idx_before)>=20000:
                break
        for e in fif_exact_idx: # 연도 일치 인덱스 - 쿼리 기반 아님 - getyear!='all'이면 필터링
            top_k_idx_before.add(e)
            if len(top_k_idx_before)>=30000:
                break
    
    
    top_k_idx_before.update(thr_exact_idx) # 언어 all 일치 인덱스 - 쿼리 기반

    top_k_idx_before.update(thr2_exact_idx) # 언어 any 일치 인덱스 - 쿼리 기반
    
    top_k_idx_before.update(fth_exact_idx) # 국가 all 일치 인덱스 - 쿼리 기반
    
    top_k_idx_before.update(fth2_exact_idx) # 국가 any 일치 인덱스 - 쿼리 기반
    
    # end
    
    top_k_idx=[]
    for indexes in top_k_idx_before:
        if not alls:
            if (indexes not in sec_exact_idx) and (indexes not in st_exact_idx):
                continue
        if getyear!='all' or year_match:
            if (indexes not in fif_exact_idx):
                continue
        top_k_idx.append(indexes)
    
    scores_map = {
        x: matchorder(originq,query,keylang,keycount,method,df.iloc[x]['title'],df.iloc[x]['original_title'],df.iloc[x]['languages'].split(', '),df.iloc[x]['countries'].split(', '))
        for x in top_k_idx
        }
    dfilocxyear={
        x:df.iloc[x]['year']
        for x in top_k_idx
        }
    dfilocxno={
        x:df.iloc[x]['no']
        for x in top_k_idx
        }

    top_k_idx = sorted(
        top_k_idx,
        key=lambda x: (scores_map[x],1 if x in sec_exact_idx else 0,1 if x in st_exact_idx else 0,1 if x in thr_exact_idx else 0,1 if x in thr2_exact_idx else 0,1 if x in fth_exact_idx else 0,1 if x in fth2_exact_idx else 0,dfilocxyear[x],-dfilocxno[x])
        )
    
    t=[]
    o=[]
    l=[]
    c=[]
    g=[]
    y=[]
    overv=[]
    v=[]
    p=[]
    
    for idx in top_k_idx[-1:-(min(10,len(top_k_idx))+1):-1]:
        t.append(df.iloc[idx]["title"])
        o.append(df.iloc[idx]["original_title"])
        
        lang_list = df.iloc[idx]["languages"].split(", ")

        lang_ko_list = [
            language_ko_map.get(lang, lang)  # 매핑 없으면 원본 유지
            for lang in lang_list
        ]

        l.append(", ".join(lang_ko_list))
        
        country_codes = df.iloc[idx]["countries"].split(", ")

        country_names = [
            country_dict.get(code, code)  # 없으면 그냥 코드 반환
            for code in country_codes
        ]

        c.append(", ".join(country_names))
        g.append(df.iloc[idx]["genres"])
        y.append(str(df.iloc[idx]["year"])[:4])
        overv.append(df.iloc[idx]["overview"])
        v.append(df.iloc[idx]["vote_average"])
        p.append(df.iloc[idx]["poster_path"])
    
    return render_template('result.html',
                                    topklength=min(10,len(top_k_idx)),keywordq=realoriginq,title=t,original_title=o,languages=l,country=c,genre=g,year=y,overview=overv,vote=v,poster=p,genrep=genre,sg=selectedg,gys=getyear,meth=method) # 응답 페이지 
    # end

# 프로그램 시작점 
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port)