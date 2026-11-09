"""Collect official public announcements mentioning KEY TO LIT / current members.

Announcement publication dates are not broadcast dates. No event time is invented.
"""
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

HOME = 'https://jr-official.starto.jp/'
TERMS = ('KEY TO LIT', '岩﨑大昇', '岩崎大昇', '井上瑞稀', '中村嶺亜', '猪狩蒼弥', '佐々木大光')
OUT = Path(__file__).with_name('schedule.json')
JST = dt.timezone(dt.timedelta(hours=9))

def main():
    resp = requests.get(HOME, timeout=25, headers={'User-Agent': 'Mozilla/5.0 (compatible; personal-schedule-checker/1.0)'})
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Prefer announcement cards containing a published date and matching name.
    seen, found = set(), []
    for link in soup.select('a[href]'):
        title = ' '.join(link.stripped_strings)
        parent = link.parent
        context = ' '.join(parent.stripped_strings) if parent else title
        if not any(t.casefold() in context.casefold() for t in TERMS):
            continue
        url = urljoin(HOME, link.get('href',''))
        if not url.startswith('https://') or url in seen or len(title) < 8:
            continue
        # Extract publication date from the card. This is NOT the scheduled event date.
        date_match = re.search(r'(20\d\d)[.\-/](\d{1,2})[.\-/](\d{1,2})', context)
        if not date_match:
            continue
        yyyy, mm, dd = map(int,date_match.groups())
        try:
            published = dt.date(yyyy,mm,dd)
        except ValueError:
            continue
        # Announcements have no known start time; put at noon as a clearly labeled reminder,
        # not as an official appearance slot.
        event_date = published.isoformat()+'T12:00:00+09:00'
        category = 'グッズ・円盤' if any(k in title for k in ('グッズ','商品','写真','販売')) else 'その他'
        digest = hashlib.sha256(url.encode()).hexdigest()[:16]
        found.append({
            'id':'junior-news-'+digest,
            'title':'【お知らせ掲載】'+title[:130],
            'date':event_date,
            'type':category,
            'member':'グループ',
            'status':'公式発表',
            'url':url,
            'memo':'公式サイト掲載日を12:00の確認メモとして登録。出演・発売時刻ではありません。詳細はリンク先で確認してください。'
        })
        seen.add(url)
    # Keep previously collected announcements to avoid losing history, while avoiding duplicates.
    previous=[]
    if OUT.exists():
        try: previous=json.loads(OUT.read_text(encoding='utf-8')).get('events',[])
        except (ValueError, OSError, AttributeError): pass
    merged={e['id']:e for e in previous if isinstance(e,dict) and 'id' in e}
    merged.update({e['id']:e for e in found})
    OUT.write_text(json.dumps({'updated_at':dt.datetime.now(JST).isoformat(), 'events':sorted(merged.values(),key=lambda x:x['date'],reverse=True)[:200]},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('New/updated public announcements:',len(found),'Total:',len(merged))

if __name__=='__main__':main()
