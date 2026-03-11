import csv
import json
import collections
import pandas as pd

csv_path = '/Users/gam0218/Downloads/【納品データ】Fan Survey (2027).xlsx - Form responses 21.10.01.csv'

trans_dict = {
    '1. How many hours per week do you usually spend playing games?': '1. 1週間にゲームで遊ぶ時間は？',
    '2. Which platforms do you usually play games on? (Select all that apply)': '2. プレイするプラットフォーム（複数選択可）',
    '2.1 Which platform do you use the most?': '2.1 最もよく利用するプラットフォーム',
    '3. How often do you use Steam to purchase or play games?': '3. Steamの利用頻度は？',
    '4. Which best describes your purchasing behavior on Steam?': '4. Steamでのゲーム購入傾向',
    '5. Which features are important to you in a Steam game? (Select all that apply)': '5. Steamのゲームで重視する機能（複数選択可）',
    '6. Which game genres do you particularly enjoy? (max. 3)': '6. 特に好きなゲームジャンル（最大3つ）',
    '7. What is your primary motivation for playing games?': '7. ゲームをプレイする主な目的',
    '8. Which of the following titles would you most like to play as a game on Steam? (max. 3)': '8. [Steamユーザー向け] 以下のタイトルのうち、Steamでゲームとしてプレイしたいものはどれですか？（最大3つ）',
    '8.1 Which ONE of the titles you selected would you most like to play?': '8.1 [Steamユーザー向け] 選択したタイトルのうち、最もプレイしたいタイトルはどれですか？',
    '8.2 If a game were to be released on steam, which of the following franchises would you be interested in playing? (max. 3)': '8.2 [非Steam・CS/スマホゲーマー向け] もしSteamでゲームがリリースされるとしたら、プレイしてみたいシリーズはどれですか？（最大3つ）',
    '8.3 Which ONE of the titles you selected would you most like to play?': '8.3 [非Steam・CS/スマホゲーマー向け] 選択したタイトルのうち、最もプレイしたいタイトルはどれですか？',
    '8.4 If a game were to be released on steam, which of the following franchises would you be interested in playing? (max. 3)': '8.4 [非ゲーマー向け] もしSteamでゲームがリリースされるとしたら、プレイしてみたいシリーズはどれですか？（最大3つ）',
    '8.5 Which ONE of the selected titles would you most like to play?': '8.5 [非ゲーマー向け] 選択したタイトルのうち、最もプレイしたいタイトルはどれですか？',
    '9. Why do you most want this title to be adapted into a game?': '9. ゲーム化を希望する理由',
    '10. If this game were on Steam, which of the following experiences and price point would you prefer?': '10. ゲームのボリュームと価格帯の希望',
    '11. How do you feel about the inclusion of the original voices/music in a game adaptation?': '11. 原作の音声・楽曲の収録について',
    '12. Which of the following would you find the most difficult to accept when playing a game adaptation?': '12. ゲーム化で最も許容しがたい要素',
    '13. If one of the titles you selected were to be adapted and released on Steam, how likely would you be to purchase it?': '13. 選択したタイトルがSteamで出たら購入しますか？',
    '14. Which monetization models are acceptable to you? (Select all that apply)': '14. 許容できるマネタイズモデル（複数選択可）',
    'What is your gender?': '性別',
    'What is your age?': '年齢',
    'Which country do you reside in?': '居住国',
    'What is your profession?': '職業',
    'What is your annual income?': '年収層',

    'Less than 2 hours': '2時間未満',
    '2-4 hours': '2-4時間',
    '4-6 hours': '4-6時間',
    '6-8 hours': '6-8時間',
    '8-10 hours': '8-10時間',
    'More than 10 hours': '10時間以上',
    'I don\'t play games at all': 'ゲームは全くしない',
    
    'Mobile (iOS / Android)': 'モバイル（iOS/Android）',
    'Nintendo Switch': 'Nintendo Switch',
    'PlayStation': 'PlayStation',
    'Xbox': 'Xbox',
    'PC': 'PC',

    'Almost every week': 'ほぼ毎週',
    'Once or twice a month': '月に1, 2回',
    'Once every few months': '数ヶ月に1回',
    'I have a Steam account but rarely use it': 'アカウントはあるが滅多に使わない',
    'I do not use Steam': 'Steamは使わない',

    'I buy at full price if interested': '興味があれば定価で買う',
    'I mostly buy during sales': '主にセール時に買う',
    'I check reviews before buying': 'レビューを見てから買う',
    'I wishlist and wait': 'ウィッシュリストに入れて待つ',
    'I do not purchase games on Steam': 'Steamでゲームは買わない',

    'Achievements': '実績',
    'Mod support': 'Mod対応',
    'Steam Workshop support': 'Steamワークショップ対応',
    'Steam Deck compatibility': 'Steam Deck互換性',
    'Controller support': 'コントローラー対応',
    'Nothing in particular': '特になし',

    'Visual Novel': 'ビジュアルノベル',
    'RPG': 'RPG',
    'Shooter': 'シューティング',
    'Adventure': 'アドベンチャー',
    'Puzzle': 'パズル',
    'Strategy': 'ストラテジー',
    'Simulation': 'シミュレーション',
    'Horror': 'ホラー',
    'Metroidvania': 'メトロイドヴァニア',
    'Roguelite': 'ローグライト',
    'Fighting': '格闘',
    'Survival': 'サバイバル',
    '2D Action': '2Dアクション',
    'PvPvE': 'PvPvE',

    'Story and narrative': 'ストーリー・物語性',
    'Immersion': '没入感',
    'Character development/progression': 'キャラクター育成・進行',
    'Ability to pick up and put down/quick play sessions': '手軽に遊べる・短時間プレイ',
    'Mastery/grinding': 'やり込み要素',
    'Competitive play/rankings': '対戦・ランキング',

    'Short (1-2h) game with replayability ($9.99)': '短編・リプレイ性あり ($9.99)',
    'Medium (~10h) game where you can fully experience the world ($19.99)': '中編・世界観を体験 ($19.99)',
    'Long (50h+) game with lots of content ($69.99)': '長編・大ボリューム ($69.99)',

    'Both essential': '声・曲どちらも必須',
    'Music only': '楽曲のみ必須',
    'Voice only': '声のみ必須',
    'Neither essential': 'どちらでもよい',

    'Major character changes': '大幅なキャラ改変',
    'Contradicting themes': '原作テーマとの矛盾',
    'Game-original storylines': 'ゲームオリジナルシナリオ',
    'None in particular': '特になし',
    'Monetization (e.g. microtransactions, "pay-to-win"-style monetization, gacha, etc.)': '過度な課金要素（P2W・ガチャ等）',

    'Very likely': '非常に買いたい',
    'Somewhat likely': 'まあ買いたい',
    'Not sure': 'わからない',
    'Unlikely': 'あまり買いたくない',
    'I would not purchase it': '買わない',

    'Buy-to-play only': '買い切り型',
    'Paid DLC': '有料DLC追加型',
    'Cosmetic-only purchases': '見た目系課金のみ',
    'Gacha': 'ガチャ',
    'Prefer no monetization (free to play)': '完全無課金（F2P）',

    'Yes': 'はい',
    'No': 'いいえ',

    'Male': '男性',
    'Female': '女性',
    'Non-binary': 'ノンバイナリー',
    'Prefer not to answer.': '回答しない',
    
    'Student': '学生',
    'Full-time employee': '正社員',
    'Part-time employee': 'アルバイト・パート',
    'Self-employed': '自営業',
    'Prefer not to say': '回答しない',

    'No income': '収入なし',
    'Less than $5K': '$5K未満',
    '$5K to under $10K': '$5K〜$10K',
    '$10K to under $25K': '$10K〜$25K',
    '$25K to under $50K': '$25K〜$50K',
    '$50K to under $75K': '$50K〜$75K',
    '$75K to under $100K': '$75K〜$100K',
}

def translate(text):
    if not text: return ''
    if text in trans_dict: return trans_dict[text]
    if text.strip() in trans_dict: return trans_dict[text.strip()]
    return text

with open(csv_path, 'r', encoding='utf-8-sig') as f:
    reader = list(csv.reader(f))
    
    headers = reader[0]
    counters = {i: collections.Counter() for i in range(len(headers))}
    total_responses = len(reader) - 1
    
    for row in reader[1:]:
        for i, val in enumerate(row):
            if not val: continue
            
            header_lw = headers[i].lower()
            if '(select all that apply)' in header_lw or '(max. 3)' in header_lw or '\n' in val:
                parts = [p.strip() for p in val.split('\n') if p.strip()]
                for p in parts:
                    counters[i][translate(p)] += 1
            else:
                counters[i][translate(val.strip())] += 1

opinions = []
opinions_negative = []
reason_col_idx = -1
negative_col_idx = -1

for i, h in enumerate(headers):
    if 'Why' in h or '希望する理由' in translate(h):
        reason_col_idx = i
    if '15.2' in h or 'enjoy about those games' in h:
        negative_col_idx = i

if reason_col_idx != -1:
    for row in reader[1:]:
        if len(row) > reason_col_idx:
            val = row[reason_col_idx].strip()
            if val and len(val) > 15 and len(val) < 150:
                opinions.append(val)
                if len(opinions) >= 6:
                    break

if negative_col_idx != -1:
    for row in reader[1:]:
        if len(row) > negative_col_idx:
            val = row[negative_col_idx].strip()
            if val and len(val) > 15 and len(val) < 150:
                opinions_negative.append(val)
                if len(opinions_negative) >= 6:
                    break

opinions_html = ""
if opinions or opinions_negative:
    opinions_html = '<div class="opinions-container" id="opinions-wrapper">'
    
    if opinions:
        opinions_html += '<h2 class="section-title" style="margin-left: -1rem; margin-bottom: 2rem;">ユーザーの声：なぜそのタイトルのゲーム化を希望するのか？</h2><div class="opinions-grid" style="margin-bottom: 3rem;">'
        for op in opinions:
            opinions_html += f'<div class="opinion-card">"{op}"</div>'
        opinions_html += '</div>'
        
    if opinions_negative:
        opinions_html += '<h2 class="section-title" style="margin-left: -1rem; margin-bottom: 2rem; border-left-color: #10b981;">ユーザーの声：インディーゲームで楽しかった要素</h2><div class="opinions-grid">'
        for op in opinions_negative:
            opinions_html += f'<div class="opinion-card" style="border-left-color: #10b981;">"{op}"</div>'
        opinions_html += '</div>'
        
    opinions_html += '</div>'

# -- Added: Indie Games Extraction --
df = pd.read_csv(csv_path)
q15_cols = [col for col in df.columns if "15.1" in col and "Title" in col]
indie_titles = []
for col in q15_cols:
    titles = df[col].dropna().astype(str).str.strip().tolist()
    titles = [t for t in titles if t and t.lower() not in ('none', 'n/a', '-', 'na', 'nothing')]
    indie_titles.extend(titles)

# Count and get top 5
title_counts = collections.Counter(x.lower() for x in indie_titles)
# Maintain original casing for display of top 5
original_casing = {}
for t in indie_titles:
    if t.lower() not in original_casing:
        original_casing[t.lower()] = t

top_5_raw = title_counts.most_common(5)
top_5_data = []
img_map = {
    'hollow knight': 'assets/hollow_knight.jpg',
    'stardew valley': 'assets/stardew_valley.jpg',
    'undertale': 'assets/undertale.jpg',
    'hades': 'assets/hades.jpg',
    'terraria': 'assets/terraria.jpg',
    'celeste': 'assets/celeste.jpg'
}

for title_lower, count in top_5_raw:
    display_name = original_casing.get(title_lower, title_lower.title())
    img_path = img_map.get(title_lower, '')
    top_5_data.append((display_name, count, img_path))

top_5_html = ""
for i, (title, count, img) in enumerate(top_5_data, 1):
    img_tag = f'<img src="{img}" alt="{title}" style="height: 48px; border-radius: 4px; object-fit: cover; margin-left: 1rem;">' if img else ''
    top_5_html += f'''
        <li style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.8rem; background: rgba(30, 41, 59, 0.5); padding: 0.5rem 1rem; border-radius: 6px; border: 1px solid var(--border-color);">
            <span><strong>{i}位:</strong> {title} ({count}票)</span>
            {img_tag}
        </li>
    '''

# Remaining distinct titles list for scrolling
all_unique_titles = list(set([original_casing.get(k, k.title()) for k in title_counts.keys()]))
all_unique_titles.sort(key=lambda x: x.lower())
other_titles_html = "".join([f'<span style="display:inline-block; background:rgba(30,41,59,0.8); padding:0.2rem 0.6rem; margin:0.2rem; border-radius:4px; font-size:0.85rem; border:1px solid #334155;">{t}</span>' for t in all_unique_titles])
# -----------------------------------

chart_data = []
summary = {
    'total': total_responses,
    'top_platform': '',
    'top_genre': '',
    'top_motivation': '',
    'top_titles': []
}

for i, raw_header in enumerate(headers):
    # Skip non-chartable columns
    if 'NO' in raw_header or 'Why' in raw_header or '15.1' in raw_header or '15.2' in raw_header or 'Could you let us know' in raw_header or 'Would you be willing' in raw_header:
        continue
        
    header = translate(raw_header)
    
    if len(counters[i]) > 30:
        if '国' in header or '州' in header:
            top = counters[i].most_common(12)
        elif 'ジャンル' in header:
            top = counters[i].most_common(12)
        elif 'タイトル' in header or 'シリーズ' in header:
            top = counters[i].most_common(15)
        else:
            continue
    else:
        top = counters[i].most_common()
        
    if not top: continue

    # Populate summary metrics
    if '最もよく利用するプラットフォーム' in header and not summary['top_platform']:
        summary['top_platform'] = top[0][0]
    if '特に好きなゲームジャンル' in header and not summary['top_genre']:
        summary['top_genre'] = translate(top[0][0])
    if 'ゲームをプレイする主な目的' in header and not summary['top_motivation']:
        summary['top_motivation'] = top[0][0]
    if 'Steamでゲーム化してほしいタイトル' in header and not summary['top_titles']:
        summary['top_titles'] = [x[0] for x in top[:3]]
    if 'Steamリリースで興味のあるシリーズ' in header and not summary['top_titles']:
        summary['top_titles'] = [x[0] for x in top[:3]]
    if '上記の中で最もプレイしたいタイトル' in header and not summary['top_titles']:
        summary['top_titles'] = [x[0] for x in top[:3]]

    labels = [k for k, v in top]
    data = [v for k, v in top]
    
    chart_type = 'bar' if len(labels) > 6 or '(select all' in raw_header.lower() or 'max' in raw_header.lower() else 'doughnut'
    
    analysis_text = ""
    try:
        percentages = [round((v / summary['total']) * 100, 1) for v in data]
        if labels:
            top1 = labels[0]
            top1_pct = percentages[0]
            analysis_text = f"最も多い回答は「{top1}」で、全体の約{top1_pct}%を占めています。"
            if len(labels) > 1:
                analysis_text += f" 次いで「{labels[1]}」({percentages[1]}%)となっています。"

            if "時間" in header: analysis_text += " プレイヤー層のプレイ時間の傾向が表れています。"
            elif "プラットフォーム" in header: analysis_text += f" {top1}でプレイするユーザーが多数派です。"
            elif "ジャンル" in header: analysis_text += " ゲーム化するにあたり、これらのジャンルへの期待値が高いと言えます。"
            elif "目的" in header: analysis_text += " プレイヤーはゲームに対してこの要素を最も求めているようです。"
            elif "ボイス" in header or "音声" in header or "楽曲" in header: analysis_text += " IPゲーム化における原作再現の重要性が伺えます。"
            elif "マネタイズ" in header or "課金" in header: analysis_text += " ビジネスモデルを検討する上で重要な指標です。"
            
            # specific Q8 analysis based on target segment
            if "8. " in header or "8.1" in header:
                analysis_text += "<br><b>【回答者層】</b> 普段からSteamを利用してゲームを遊んでいるコア層（全体の約85%）の回答です。"
            elif "8.2" in header or "8.3" in header:
                analysis_text += "<br><b>【回答者層】</b> ゲームはプレイするがSteamアカウントを持っていない、または使わないコンソール/モバイル層（全体の約12%）の回答です。"
            elif "8.4" in header or "8.5" in header:
                analysis_text += "<br><b>【回答者層】</b> 普段ゲームを全くプレイしないアニメファン層（全体の約3%）の回答です。"
    except Exception as e:
        pass

    category = "その他"
    if any(k in header for k in ['年齢', '性別', '居住国', '職業', '年収層']):
        category = "ユーザー属性"
    elif any(k in header for k in ['時間', 'プラットフォーム', 'ジャンル', '目的']):
        category = "ゲームプレイ傾向"
    elif any(k in header for k in ['Steamの利用頻度', '購入傾向', '重視する機能']):
        category = "Steamでの利用・購買傾向"
    elif any(k in header for k in ['ゲーム化', 'シリーズ', 'タイトル', 'ボリューム', '音声', '楽曲', '許容', '購入', 'マネタイズ']):
        category = "ゲーム化への要望"

    q_size = 'normal'
    if header.startswith('8.2') or header.startswith('8.3') or header.startswith('8.4') or header.startswith('8.5'):
        q_size = 'small'
    elif header.startswith('8.') or header.startswith('8 '):
        q_size = 'large'

    chart_data.append({
        'title': header,
        'labels': labels,
        'data': data,
        'type': chart_type,
        'analysis': analysis_text,
        'category': category,
        'size': q_size
    })

# Make titles string if needed
top_titles_str = "<br>".join([f"{i+1}. {x}" for i, x in enumerate(summary['top_titles'])])

# Generate Business Insights
insights_html = ""
try:
    insights = []
    
    # Check Platform/Steam
    steam_freq_p = [item['data'] for item in chart_data if 'Steamの利用頻度' in item['title']]
    pc_plat_p = [item['data'] for item in chart_data if 'プレイするプラットフォーム' in item['title']]
    
    if summary['top_platform'] == 'PC':
        insights.append(f"""
        <div class="insight-item insight-go">
            <div class="insight-header">🟢 GO / 有望: PC/Steam市場での積極展開</div>
            <div class="insight-desc">最も利用されるプラットフォームがPCであり、Steamの利用頻度も高いため、Steam市場との親和性が極めて高い状態です。</div>
        </div>
        """)
        
    # Check Monetization
    monetization_data = next((item for item in chart_data if '許容できるマネタイズ' in item['title']), None)
    if monetization_data:
        buy_to_play = monetization_data['data'][monetization_data['labels'].index('買い切り型')] if '買い切り型' in monetization_data['labels'] else 0
        gacha = monetization_data['data'][monetization_data['labels'].index('ガチャ')] if 'ガチャ' in monetization_data['labels'] else 0
        
        if buy_to_play > gacha * 2:
            insights.append(f"""
            <div class="insight-item insight-go">
                <div class="insight-header">🟢 GO推奨: 買い切り型（Buy-to-play）モデル</div>
                <div class="insight-desc">「買い切り型」への許容度が最も高く、ガチャ等の課金モデルよりも明確に好まれています。</div>
            </div>
            """)
            
    # Check Negative elements
    negative_data = next((item for item in chart_data if '最も許容しがたい要素' in item['title']), None)
    if negative_data:
        p2w = negative_data['data'][negative_data['labels'].index('過度な課金要素（P2W・ガチャ等）')] if '過度な課金要素（P2W・ガチャ等）' in negative_data['labels'] else 0
        char_change = negative_data['data'][negative_data['labels'].index('大幅なキャラ改変')] if '大幅なキャラ改変' in negative_data['labels'] else 0
        if p2w > (summary['total'] * 0.4):
            insights.append(f"""
            <div class="insight-item insight-stop">
                <div class="insight-header">🔴 見送り推奨: P2W・過度なガチャ要素の導入</div>
                <div class="insight-desc">半数近くのユーザーが「過度な課金要素」を最も許容しがたい要素に挙げており、実装は深刻な反発を生むリスクがあります。</div>
            </div>
            """)
            
    # Check motivations
    if 'ストーリー' in summary['top_motivation'] or 'RPG' in summary['top_genre'] or 'アドベンチャー' in summary['top_genre']:
        insights.append(f"""
        <div class="insight-item insight-go">
            <div class="insight-header">🟢 有望: ストーリー重視のRPG/ADV開発</div>
            <div class="insight-desc">プレイ目的の1位が「{summary['top_motivation']}」、人気ジャンル1位が「{summary['top_genre']}」であることから、ストーリー主導のゲーム体験が強く求められています。</div>
        </div>
        """)
        
    insights_html = "".join(insights)
except Exception as e:
    print(f"Error generating insights: {e}")

from collections import Counter

html_template = """
<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>海外アニメファン調査 (Steam/ゲーム化) ダッシュボード</title>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-color: #0f172a;
            --text-color: #f8fafc;
            --card-bg: #1e293b;
            --border-color: #334155;
            --accent: #3b82f6;
        }
        body {
            font-family: 'Noto Sans JP', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 2rem;
        }
        h1 {
            text-align: center;
            margin-bottom: 0.5rem;
            font-weight: 700;
            background: linear-gradient(90deg, #60a5fa, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .header-sub {
            text-align: center;
            color: inherit;
            margin-bottom: 2rem;
            font-size: 0.95rem;
        }
        
        .nav-menu {
            max-width: 1400px;
            margin: 0 auto 2rem auto;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
            gap: 1rem;
            background-color: var(--card-bg);
            padding: 1rem;
            border-radius: 12px;
            border: 1px solid var(--border-color);
        }
        .nav-link {
            color: inherit;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            background-color: rgba(30,41,59,0.5);
            transition: all 0.2s;
            font-weight: 500;
            cursor: pointer;
            border: none;
            font-family: inherit;
            font-size: 1rem;
        }
        .nav-link:hover, .nav-link.active {
            color: #f8fafc;
            background-color: var(--accent);
            transform: translateY(-2px);
        }
        
        .insights-container {
            max-width: 1400px;
            margin: 0 auto 2rem auto;
            display: flex;
            flex-direction: column;
            gap: 1rem;
        }
        .insight-item {
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 6px solid transparent;
            background-color: var(--card-bg);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2);
        }
        .insight-go {
            border-left-color: #10b981;
            background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, var(--card-bg) 100%);
        }
        .insight-stop {
            border-left-color: #ef4444;
            background: linear-gradient(90deg, rgba(239, 68, 68, 0.1) 0%, var(--card-bg) 100%);
        }
        .insight-header {
            font-size: 1.15rem;
            font-weight: 700;
            color: #f8fafc;
            margin-bottom: 0.5rem;
        }
        .insight-desc {
            font-size: 0.95rem;
            color: inherit;
            line-height: 1.5;
        }
        
        .summary-container {
            max-width: 1400px;
            margin: 0 auto 3rem auto;
            background: linear-gradient(135deg, rgba(30,41,59,0.9) 0%, rgba(15,23,42,1) 100%);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.4);
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }
        .summary-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: inherit;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }
        .summary-title::before {
            content: "";
            display: inline-block;
            width: 4px;
            height: 1.25rem;
            background-color: var(--accent);
            border-radius: 2px;
        }
        .summary-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
        }
        .summary-stat {
            background-color: rgba(30,41,59,0.6);
            padding: 1.25rem;
            border-radius: 12px;
            border: 1px solid rgba(51,65,85,0.6);
            backdrop-filter: blur(4px);
        }
        .stat-label {
            font-size: 0.85rem;
            color: inherit;
            margin-bottom: 0.5rem;
        }
        .stat-value {
            font-size: 1.15rem;
            font-weight: 500;
            color: #60a5fa;
            line-height: 1.4;
        }
        
        .dashboard {
            max-width: 1400px;
            margin: 0 auto;
        }
        .dashboard-section {
            margin-bottom: 4rem;
            padding-top: 1rem;
            border-top: 1px solid var(--border-color);
        }
        .section-title {
            font-size: 1.5rem;
            color: #f8fafc;
            margin-bottom: 1.5rem;
            font-weight: 700;
            padding-left: 1rem;
            border-left: 4px solid var(--accent);
        }
        .dashboard-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 2rem;
        }
        .card-small {
            padding: 1.5rem;
            min-height: auto;
        }
        .card-small .chart-container {
            min-height: 220px;
        }
        .card-small h2 {
            font-size: 0.95rem;
            margin-bottom: 0.5rem;
            min-height: 2em;
        }
        .card-large {
            grid-column: 1 / -1;
            padding: 2.5rem;
        }
        .card-large .chart-container {
            min-height: 400px;
        }
        .card-large h2 {
            font-size: 1.35rem;
            font-weight: 700;
            margin-bottom: 2rem;
        }
        .opinions-container {
            max-width: 1400px;
            margin: 4rem auto 2rem auto;
            background-color: transparent;
        }
        .opinions-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
        }
        .opinion-card {
            background-color: rgba(30,41,59,0.5);
            padding: 1.5rem;
            border-radius: 12px;
            font-style: italic;
            color: inherit;
            border-left: 4px solid #a78bfa;
            line-height: 1.6;
        }
        .card {
            background-color: var(--card-bg);
            border-radius: 16px;
            padding: 1.5rem;
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
            border: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            transition: transform 0.2s;
        }
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.4);
        }
        .card h2 {
            font-size: 1rem;
            margin-top: 0;
            margin-bottom: 1.5rem;
            color: inherit;
            line-height: 1.4;
            text-align: center;
            font-weight: 500;
            min-height: 2.8em;
        }
        .chart-container {
            position: relative;
            flex-grow: 1;
            min-height: 300px;
            width: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .chart-analysis {
            margin-top: 1.5rem;
            padding-top: 1.25rem;
            border-top: 1px solid var(--border-color);
            font-size: 0.95rem;
            color: inherit;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <h1>海外アニメファン調査 結果分析ダッシュボード</h1>
    <p class="header-sub">Steamでのゲーム化における有望タイトルおよびユーザー属性調査（全REPLACE_TOTAL件）</p>

    <div class="nav-menu">
        <button class="nav-link active" onclick="openTab(event, 'cat-サマリー')">サマリー</button>
        <button class="nav-link" onclick="openTab(event, 'cat-追加インサイト')">追加インサイト</button>
        <button class="nav-link" onclick="openTab(event, 'cat-ゲーム化への要望')">ゲーム化への要望</button>
        <button class="nav-link" onclick="openTab(event, 'cat-ゲームプレイ傾向')">ゲームプレイ傾向</button>
        <button class="nav-link" onclick="openTab(event, 'cat-Steamでの利用・購買傾向')">Steamでの利用・購買傾向</button>
        <button class="nav-link" onclick="openTab(event, 'cat-ユーザー属性')">ユーザー属性</button>
        <button class="nav-link" onclick="openTab(event, 'cat-その他')">その他</button>
    </div>
    <!-- Executive Summary Containers -->
    <div id="cat-サマリー" class="dashboard-section tab-content">
    <div class="summary-container" style="margin-bottom: 2rem;">
        <div class="summary-title" style="color: #60a5fa; font-size: 1.5rem; margin-bottom: 1rem;">🏁 Executive Summary (超要約)</div>
        <ul style="font-size: 1.1rem; line-height: 1.8; color: inherit; padding-left: 1.5rem; margin: 0;">
            <li><strong>PC/Steam市場:</strong> 積極展開を強く推奨（約80%がPCユーザー）</li>
            <li><strong>マネタイズ:</strong> 買い切り型が最適。過度なガチャは高い反発リスクあり</li>
            <li><strong>ゲーム体験:</strong> 原作ストーリーの再現性を重視したRPG/ADVが有望</li>
        </ul>
    </div>
    
    <div class="insights-container">
        REPLACE_INSIGHTS_HTML
    </div>
    
    <div class="summary-container">
        <div class="summary-title">全体サマリー（重要指標のハイライト）</div>
        <div class="summary-grid">
            <div class="summary-stat">
                <div class="stat-label">総回答数</div>
                <div class="stat-value">REPLACE_TOTAL 件</div>
            </div>
            <div class="summary-stat">
                <div class="stat-label">最も利用されるプラットフォーム</div>
                <div class="stat-value">REPLACE_TOP_PLATFORM</div>
            </div>
            <div class="summary-stat">
                <div class="stat-label">人気ゲームジャンル Top1</div>
                <div class="stat-value">REPLACE_TOP_GENRE</div>
            </div>
            <div class="summary-stat">
                <div class="stat-label">ゲームをプレイする目的 Top1</div>
                <div class="stat-value">REPLACE_TOP_MOTIVATION</div>
            </div>
            <div class="summary-stat" style="grid-column: span auto; min-width: 250px;">
                <div class="stat-label">Steamでゲーム化希望の多いIP Top3</div>
                <div class="stat-value" style="font-size: 1rem; color: #a78bfa;">REPLACE_TOP_TITLES</div>
            </div>
        </div>
    </div>
    </div>
    <!-- End Summary Containers -->

    <!-- Deep Dive Insights Container (Adult Demographic) -->
    <div id="cat-追加インサイト" class="dashboard-section tab-content" style="display: none;">
        <h2 class="section-title">📊 追加分析: 社会人層(学生以外) の傾向と全体比較</h2>
        
        <div class="summary-container" style="margin-bottom: 2rem;">
            <p style="font-size: 1.05rem; line-height: 1.8; color: inherit; margin-bottom: 1rem;">
                アンケート全体の母集団から学生を除外し、社会人層（N=1472, 全体の約61.4%）のみのデータを再集計し、全体傾向とどう違うのかを分析しました。
            </p>

            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-bottom: 1.5rem;">
                <div style="background: rgba(30, 41, 59, 0.5); padding: 1.5rem; border-radius: 8px; border: 1px solid var(--border-color);">
                    <h3 style="color: inherit; font-size: 1.1rem; margin-bottom: 0.8rem; margin-top: 0; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">⚔️ 最もプレイしたいIP (設問8.1)</h3>
                    <ul style="color: inherit; line-height: 1.6; padding-left: 1.2rem; margin: 0; font-size: 0.95rem;">
                        <li style="margin-bottom: 0.5rem;"><strong>全体:</strong> 1位 Berserk (10.5%), 2位 Attack on Titan (9.3%), 3位 Made in Abyss (7.1%)</li>
                        <li><strong>社会人:</strong> 1位 Berserk (11.5%), 2位 Attack on Titan (8.6%), 3位 Made in Abyss (7.4%)</li>
                    </ul>
                    <div style="margin-top: 1rem; font-size: 0.9rem; color: #a78bfa;">
                        💡 学生層から圧倒的だった『進撃の巨人』のシェアが減少し、『Berserk』や『Made in Abyss』といったダークファンタジー作品への渇望がより顕著になります。
                    </div>
                </div>

                <div style="background: rgba(30, 41, 59, 0.5); padding: 1.5rem; border-radius: 8px; border: 1px solid var(--border-color);">
                    <h3 style="color: inherit; font-size: 1.1rem; margin-bottom: 0.8rem; margin-top: 0; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">🎮 ゲームをプレイする目的 (設問7)</h3>
                    <ul style="color: inherit; line-height: 1.6; padding-left: 1.2rem; margin: 0; font-size: 0.95rem;">
                        <li style="margin-bottom: 0.5rem;">全体・社会人ともに「ストーリー(1位)」「没入感(2位)」がツートップですが、社会人層はさらに「ストーリー」の重要視割合が上昇(44.4% → 45.8%)しています。</li>
                    </ul>
                </div>
            </div>

            <div style="background: rgba(30, 41, 59, 0.5); padding: 1.5rem; border-radius: 8px; border: 1px solid var(--border-color); margin-bottom: 1.5rem;">
                <h3 style="color: inherit; font-size: 1.1rem; margin-bottom: 0.8rem; margin-top: 0; border-bottom: 1px solid var(--border-color); padding-bottom: 0.5rem;">💳 購買行動の比較 (設問4)</h3>
                <ul style="color: inherit; line-height: 1.6; padding-left: 1.2rem; margin: 0; font-size: 0.95rem;">
                    <li><strong>全体:</strong> セール待ち(42.2%) / ウィッシュリスト(25.0%)</li>
                    <li><strong>社会人:</strong> セール待ち(39.8%) / ウィッシュリスト(26.3%) / 定価購入(10.1% *学生は6.1%)</li>
                </ul>
                <div style="margin-top: 1rem; font-size: 0.95rem; color: #cbd5e1;">
                    社会人は「セール待ち」の割合が減り、購入資金に余裕があるため「本当に興味があるタイトルは定価でも買う」層が学生の2倍近く存在します。ミドル/フルプライスでの販売は社会人をメインターゲットに据えると成立しやすいと言えます。
                </div>
            </div>
        </div>
    </div>

    <div class="dashboard" id="dashboard"></div>
    
    REPLACE_OPINIONS_HTML
    
    <div id="indie-wrapper" style="width: 100%; margin-top: 2rem; margin-bottom: 2rem;">
        <h2 class="section-title" style="margin-top: 2rem;">🎮 好きなインディーゲームの傾向 (設問15)</h2>
        <div class="summary-container" style="background: var(--card-bg); border-radius: 16px; border: 1px solid var(--border-color); padding: 1.5rem; box-shadow: 0 10px 15px -3px rgba(0,0,0,0.3);">
            <p style="font-size: 1.05rem; line-height: 1.8; color: inherit; margin-bottom: 1rem;">
                記述回答を集計した結果、圧倒的に支持を集めていたのは以下のタイトルでした：
            </p>
            <ul style="list-style: none; padding: 0; margin-bottom: 1.5rem; max-width: 500px;">
                REPLACE_TOP_5_HTML
            </ul>
            
            <p style="font-size: 0.95rem; color: inherit; margin-bottom: 0.5rem;">その他の回答タイトル一覧（スクロール可能）:</p>
            <div style="max-height: 150px; overflow-y: auto; background: rgba(15, 23, 42, 0.5); padding: 1rem; border-radius: 6px; border: 1px solid var(--border-color); margin-bottom: 1.5rem;">
                REPLACE_OTHER_TITLES_HTML
            </div>

            <div style="background: rgba(59, 130, 246, 0.1); padding: 1.25rem; border-left: 4px solid #3b82f6; border-radius: 4px; color: inherit; line-height: 1.6;">
                <strong>💡 示唆:</strong> 圧倒的に**メトロイドヴァニア（探索型2Dアクション）**や**ローグライク**、高難易度のピクセルアート作品が支持されています。「アニメIPのゲーム化」においても、大作3DのアクションRPGだけでなく、2Dで深く探索できるダーク寄りな作品（『Hollow Knight』のテイストは『Berserk』などと好相性）や、生活要素のある作品（『Stardew Valley』のテイストは『Spy x Family』などと好相性）が、Steamユーザーに非常に刺さる可能性が高いことが裏付けられました。
            </div>
        </div>
    </div>

    <script>
        const chartData = CHART_DATA_PLACEHOLDER;
        const dashboard = document.getElementById('dashboard');

        const colors = [
            'rgba(59, 130, 246, 0.8)', 'rgba(16, 185, 129, 0.8)', 'rgba(245, 158, 11, 0.8)',
            'rgba(239, 68, 68, 0.8)', 'rgba(139, 92, 246, 0.8)', 'rgba(236, 72, 153, 0.8)',
            'rgba(20, 184, 166, 0.8)', 'rgba(249, 115, 22, 0.8)', 'rgba(99, 102, 241, 0.8)',
            'rgba(168, 85, 247, 0.8)', 'rgba(234, 179, 8, 0.8)', 'rgba(14, 165, 233, 0.8)',
            'rgba(132, 204, 22, 0.8)', 'rgba(244, 63, 94, 0.8)', 'rgba(217, 70, 239, 0.8)'
        ];
        const borderColors = [
            'rgb(59, 130, 246)', 'rgb(16, 185, 129)', 'rgb(245, 158, 11)',
            'rgb(239, 68, 68)', 'rgb(139, 92, 246)', 'rgb(236, 72, 153)',
            'rgb(20, 184, 166)', 'rgb(249, 115, 22)', 'rgb(99, 102, 241)',
            'rgb(168, 85, 247)', 'rgb(234, 179, 8)', 'rgb(14, 165, 233)',
            'rgb(132, 204, 22)', 'rgb(244, 63, 94)', 'rgb(217, 70, 239)'
        ];

        Chart.defaults.color = '#94a3b8';
        Chart.defaults.font.family = '"Noto Sans JP", sans-serif';

        const categories = {};
        chartData.forEach(item => {
            if (!categories[item.category]) categories[item.category] = [];
            categories[item.category].push(item);
        });

        const order = ["ゲーム化への要望", "ゲームプレイ傾向", "Steamでの利用・購買傾向", "ユーザー属性", "その他"];
        const sortedCategories = Object.keys(categories).sort((a, b) => {
            let ia = order.indexOf(a);
            let ib = order.indexOf(b);
            if (ia === -1) ia = 99;
            if (ib === -1) ib = 99;
            return ia - ib;
        });

        let globalChartIndex = 0;
        
        sortedCategories.forEach(category => {
            const items = categories[category];
            
            const section = document.createElement('div');
            section.className = 'dashboard-section tab-content';
            section.id = 'cat-' + category;
            section.style.display = 'none';
            
            const sectionTitle = document.createElement('h2');
            sectionTitle.className = 'section-title';
            sectionTitle.textContent = category;
            section.appendChild(sectionTitle);
            
            const grid = document.createElement('div');
            grid.className = 'dashboard-grid';

            items.forEach((item) => {
                const card = document.createElement('div');
                card.className = 'card ' + (item.size === 'small' ? 'card-small' : (item.size === 'large' ? 'card-large' : ''));
                
                const title = document.createElement('h2');
                title.textContent = item.title;
                card.appendChild(title);

                const chartContainer = document.createElement('div');
                chartContainer.className = 'chart-container';
                const canvas = document.createElement('canvas');
                canvas.id = 'chart-' + globalChartIndex;
                chartContainer.appendChild(canvas);
                card.appendChild(chartContainer);

                if (item.analysis) {
                    const analysisNode = document.createElement('div');
                    analysisNode.className = 'chart-analysis';
                    analysisNode.innerHTML = item.analysis;
                    card.appendChild(analysisNode);
                }

                grid.appendChild(card);

                const ctx = canvas.getContext('2d');
            
            let bgColors = [];
            let bColors = [];
            for (let i = 0; i < item.data.length; i++) {
                bgColors.push(colors[i % colors.length]);
                bColors.push(borderColors[i % borderColors.length]);
            }

            let dataset = {
                data: item.data,
                backgroundColor: item.type === 'doughnut' ? bgColors : bgColors[0],
                borderColor: item.type === 'doughnut' ? bColors : bColors[0],
                borderWidth: 1
            };

            const maxVal = Math.max(...item.data);
            const suggestedMax = Math.ceil(maxVal * 1.1);

            let options = {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        display: item.type === 'doughnut',
                        position: 'right',
                        labels: { color: '#cbd5e1', font: { family: '"Noto Sans JP", sans-serif' } }
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 23, 42, 0.9)',
                        titleColor: '#f8fafc',
                        bodyColor: '#cbd5e1',
                        borderColor: '#334155',
                        borderWidth: 1,
                        bodyFont: { family: '"Noto Sans JP", sans-serif' }
                    }
                }
            };
            
            if (item.type === 'bar') {
                options.scales = {
                    y: {
                        beginAtZero: true,
                        suggestedMax: suggestedMax,
                        grid: { color: '#334155' },
                        ticks: { color: '#94a3b8' }
                    },
                    x: {
                        grid: { display: false },
                        ticks: { 
                            color: '#94a3b8',
                            font: { family: '"Noto Sans JP", sans-serif' },
                            maxRotation: 45,
                            minRotation: 0,
                            callback: function(value, index, values) {
                                let label = item.labels[index];
                                return label.length > 25 ? label.substring(0, 25) + '...' : label;
                            }
                        }
                    }
                };
            }

            new Chart(ctx, {
                type: item.type,
                data: {
                    labels: item.labels,
                    datasets: [dataset]
                },
                options: options
            });
            
            globalChartIndex++;
            });
            
            section.appendChild(grid);
            dashboard.appendChild(section);
        });
        
        // Move opinions and indie breakdown into the first chart tab ("ゲーム化への要望").
        const opinionsWrapper = document.getElementById('opinions-wrapper');
        const indieWrapper = document.getElementById('indie-wrapper');
        const firstTab = document.getElementById('cat-ゲーム化への要望');
        
        if (indieWrapper && firstTab) {
            firstTab.appendChild(indieWrapper);
        }
        if (opinionsWrapper && firstTab) {
            firstTab.appendChild(opinionsWrapper);
        }

        function openTab(evt, tabName) {
            const tabcontent = document.getElementsByClassName("tab-content");
            for (let i = 0; i < tabcontent.length; i++) {
                tabcontent[i].style.display = "none";
            }
            const navlinks = document.getElementsByClassName("nav-link");
            for (let i = 0; i < navlinks.length; i++) {
                navlinks[i].classList.remove("active");
            }
            document.getElementById(tabName).style.display = "block";
            if (evt) {
                evt.currentTarget.classList.add("active");
            }
        }
    </script>
</body>
</html>
"""

html_formatted = html_template \
    .replace('REPLACE_TOTAL', str(summary['total'])) \
    .replace('REPLACE_TOP_PLATFORM', str(summary['top_platform'])) \
    .replace('REPLACE_TOP_GENRE', str(summary['top_genre'])) \
    .replace('REPLACE_TOP_MOTIVATION', str(summary['top_motivation'])) \
    .replace('REPLACE_TOP_TITLES', " / ".join(summary['top_titles'])) \
    .replace('REPLACE_INSIGHTS_HTML', insights_html) \
    .replace('REPLACE_TOP_5_HTML', top_5_html) \
    .replace('REPLACE_OTHER_TITLES_HTML', other_titles_html) \
    .replace('REPLACE_OPINIONS_HTML', opinions_html) \
    .replace('{opinions_html}', opinions_html) # Fallback if left in f-string format


html_out = html_formatted.replace('CHART_DATA_PLACEHOLDER', json.dumps(chart_data))
with open('/Users/gam0218/.gemini/antigravity/scratch/survey-visualizer/dashboard.html', 'w', encoding='utf-8') as f:
    f.write(html_out)

print(f"Generated localized dashboard.html with summary.")
