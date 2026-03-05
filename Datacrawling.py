

import requests
import pandas as pd
import time

BASE_DISCOVER = "https://api.themoviedb.org/3/discover/movie"
BASE_DETAIL = "https://api.themoviedb.org/3/movie"

headers = {
    "accept": "application/json",
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwZDVmZDYxZTIyMTFhY2IyMjY1M2ZhYjlmYTMwMjEzNCIsIm5iZiI6MTc3MDQ0ODE2OS41OTIsInN1YiI6IjY5ODZlNTI5ODU3YmZhYTAyMTVjYTFhNSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.uyWeJTCEOYcoSfATY0yl0-tuAg8-uVRP7kyKYsxBEQc"
}

def movie_to_row(data, count):
    return {
        "no": count,
        "id": data.get("id"),
        "title": data.get("title"),
        "original_title": data.get("original_title"),
        "genres": ", ".join(g["name"] for g in data.get("genres", [])),
        "companies": ", ".join(c["name"] for c in data.get("production_companies", [])),
        "countries": ", ".join(data.get("origin_country", [])),
        "languages": ", ".join(l["english_name"] for l in data.get("spoken_languages", [])),
        "year": data.get("release_date", "")[:4] if data.get("release_date") else "",
        "overview": data.get("overview"),
        "tagline": data.get("tagline"),
        "vote_average": data.get("vote_average"),
        "poster_path": data.get("poster_path")
    }

rows = []
count = 1

START_YEAR = 1976
END_YEAR = 2025

for year in range(START_YEAR, END_YEAR + 1):
    print(f"\n===== {year}년 수집 시작 =====")
    
    page = 1
    
    while True:
        discover_params = {
            "language": "ko-KR",
            "primary_release_date.gte": f"{year}-01-01",
            "primary_release_date.lte": f"{year}-12-31",
            "sort_by": "popularity.desc",
            "page": page
        }
        
        try:
            res = requests.get(BASE_DISCOVER, params=discover_params,headers=headers)
            
            if res.status_code != 200:
                print("Discover 에러:", res.status_code)
                break
            
            data = res.json()
            results = data.get("results", [])
            
            if not results:
                break
            
            for movie in results:
                movie_id = movie["id"]
                
                detail_url = f"{BASE_DETAIL}/{movie_id}"
                detail_params = {
                    "language": "ko-KR"
                }
                
                detail_res = requests.get(detail_url, params=detail_params, headers=headers)
                
                if detail_res.status_code != 200:
                    continue
                
                detail_data = detail_res.json()
                
                row = movie_to_row(detail_data, count)
                rows.append(row)
                
                print(f"{count}번째 수집 완료: {row['title']}")
                count += 1
                
                time.sleep(0.25)  # rate limit 보호
            
            if page >= 500:
                break
            
            page += 1
            time.sleep(0.3)
            
        except Exception as e:
            print("에러 발생:", e)
            time.sleep(2)

    # 🔥 연도별 백업 저장 (Colab 안전장치)
    pd.DataFrame(rows).to_csv(f"backup_until_{year}.csv",
                              index=False,
                              encoding="utf-8-sig")

print("\n총 수집 개수:", len(rows))

df = pd.DataFrame(rows)
df.to_csv("tmdb_movies_all.csv", index=False, encoding="utf-8-sig")