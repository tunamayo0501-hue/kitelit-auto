"""Collect dated official Junior-site NEWS cards mentioning KEY TO LIT/members.
Dates in this feed are publication dates, NOT appearance or sale times.
"""
import datetime as dt
import hashlib
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

HOME = 'https://jr-official.starto.jp/'
TERMS = ('KEY TO LIT', '岩﨑大昇', '岩崎大昇', '井上瑞稀', '中村嶺亜', '猪狩蒼弥', '佐々木大光')
OUT = Path(__file__).with_name('schedule.json')
JST = dt.timezone(dt.timedelta(hours=9))
DATE = re.compile(r'\b(20\d\d)[.\-/](\d{1,2})[.\-/](\d{1,2})\b')


def main():
    response = requests.get(HOME, timeout=30, headers={'User-Agent': 'Mozilla/5.0 (compatible; KEYTOLIT-personal-checker/1.0)'})
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    found = {}
    for link in soup.select('a[href]'):
        title = ' '.join(link.stripped_strings)
        if len(title) < 8 or len(title) > 220 or not any(t.casefold() in title.casefold() for t in TERMS):
            continue
        url = urljoin(HOME, link.get('href', ''))
        if urlparse(url).scheme != 'https':
            continue
        # Find the smallest parent card that contains a publication date.
        date_match = None
        ancestor = link
        for _ in range(5):
            ancestor = ancestor.parent
            if ancestor is None:
                break
            context = ' '.join(ancestor.stripped_strings)
            if len(context) > 650:
                break  # Avoid accidentally borrowing a different article's date.
            date_match = DATE.search(context)
            if date_match:
                break
        if date_match is None:
            continue
        try:
            published = dt.date(*map(int, date_match.groups()))
        except ValueError:
            continue
        digest = hashlib.sha256(url.encode()).hexdigest()[:16]
        found[digest] = {
            'id': 'junior-news-' + digest,
            'title': '【公式お知らせ】' + title,
            'date': published.isoformat() + 'T12:00:00+09:00',
            'type': 'グッズ・円盤' if any(w in title for w in ('グッズ', '商品', '写真', '販売')) else 'その他',
            'member': 'グループ', 'status': '公式発表', 'url': url,
            'memo': 'お知らせの掲載日です。12:00は仮の確認時刻で、出演日時・発売時刻ではありません。'
        }
    previous = []
    if OUT.exists():
        try:
            previous = json.loads(OUT.read_text(encoding='utf-8')).get('events', [])
        except (ValueError, OSError, AttributeError):
            pass
    merged = {str(e['id']): e for e in previous if isinstance(e, dict) and 'id' in e}
    merged.update({e['id']: e for e in found.values()})
    data = {'updated_at': dt.datetime.now(JST).isoformat(), 'events': sorted(merged.values(), key=lambda e: e.get('date', ''), reverse=True)[:200]}
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Matched official announcements:', len(found), 'Saved events:', len(data['events']))


if __name__ == '__main__':
    main()
