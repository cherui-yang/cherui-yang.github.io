#!/usr/bin/env python3
"""
WisdomWiki Analytics Dashboard — Flask Backend
Reads page-view logs from Alibaba Cloud SLS and serves JSON APIs for the dashboard.
"""

import os
import time
import json
import math
from datetime import datetime, timedelta
from functools import lru_cache

from flask import Flask, jsonify, request, send_from_directory
from dotenv import load_dotenv

# Load env from project root
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

app = Flask(__name__, static_folder='.', static_url_path='')

# ---------------------------------------------------------------------------
# SLS configuration
# ---------------------------------------------------------------------------
SLS_ENDPOINT = 'cn-shanghai.log.aliyuncs.com'
SLS_PROJECT = 'qrshare'
SLS_LOGSTORE = 'wise'
SLS_ACCESS_KEY = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_ID', '')
SLS_ACCESS_SECRET = os.getenv('ALIBABA_CLOUD_ACCESS_KEY_SECRET', '')

_client = None


def get_sls_client():
    """Lazy-init SLS client."""
    global _client
    if _client is None:
        from aliyun.log import LogClient
        _client = LogClient(SLS_ENDPOINT, SLS_ACCESS_KEY, SLS_ACCESS_SECRET)
    return _client


def sls_query(query: str, from_time: int, to_time: int, limit: int = 1000):
    """Execute an SLS SQL query and return rows as list[dict]."""
    from aliyun.log import GetLogsRequest
    client = get_sls_client()
    req = GetLogsRequest(
        SLS_PROJECT, SLS_LOGSTORE, from_time, to_time,
        query=query, line=limit
    )
    resp = client.get_logs(req)
    return [log.get_contents() for log in resp.get_logs()]


def _parse_days(args, default=7):
    try:
        return int(args.get('days', default))
    except (ValueError, TypeError):
        return default


# ---------------------------------------------------------------------------
# Demo / fallback data (used when SLS credentials are missing)
# ---------------------------------------------------------------------------
def _demo_mode():
    return not SLS_ACCESS_KEY or not SLS_ACCESS_SECRET


def _demo_overview(days):
    """Generate realistic demo overview data."""
    return {
        'pv': 12847,
        'uv': 3621,
        'sessions': 5234,
        'avg_pages_per_session': 2.45,
        'bounce_rate': 38.2,
        'war': 1893,  # Weekly Active Readers
        'days': days,
    }


def _demo_trends(days):
    import random
    random.seed(42)
    base = datetime.now() - timedelta(days=days)
    data = []
    for i in range(days):
        d = base + timedelta(days=i)
        pv = random.randint(600, 2200)
        uv = int(pv * random.uniform(0.25, 0.4))
        data.append({'date': d.strftime('%Y-%m-%d'), 'pv': pv, 'uv': uv})
    return data


def _demo_pages():
    return [
        {'page': '/en/Foundations/logical_thinking/First-Principles-Thinking-Tutorial-en/', 'title': 'First Principles Thinking', 'pv': 1243},
        {'page': '/en/Product & User/product_development/Agile-Tutorial-en/', 'title': 'Agile', 'pv': 1087},
        {'page': '/en/Problem Solving & Decision Making/decision_making/Decision-Matrix-Tutorial-en/', 'title': 'Decision Matrix', 'pv': 982},
        {'page': '/zh/docs/foundations/logical_thinking/First-Principles-Thinking-Tutorial-zh/', 'title': '第一性原理', 'pv': 876},
        {'page': '/en/Strategy & Business/strategic_analysis/SWOT-Analysis-Tutorial-en/', 'title': 'SWOT Analysis', 'pv': 832},
        {'page': '/en/Personal & Team Productivity/time_management/Pomodoro-Technique-Tutorial-en/', 'title': 'Pomodoro Technique', 'pv': 798},
        {'page': '/en/Foundations/learning_methods/Feynman-Technique-Tutorial-en/', 'title': 'Feynman Technique', 'pv': 756},
        {'page': '/en/Product & User/product_development/Design-Thinking-Tutorial-en/', 'title': 'Design Thinking', 'pv': 723},
        {'page': '/ja/foundations/logical_thinking/Pyramid-Principle-Tutorial-ja/', 'title': 'ピラミッド原則', 'pv': 654},
        {'page': '/en/Personal & Team Productivity/goal_management/OKR-Tutorial-en/', 'title': 'OKR', 'pv': 621},
    ]


def _demo_languages():
    return [
        {'lang': 'en', 'label': 'English', 'pv': 5423},
        {'lang': 'zh', 'label': '中文', 'pv': 3210},
        {'lang': 'ja', 'label': '日本語', 'pv': 1254},
        {'lang': 'ko', 'label': '한국어', 'pv': 876},
        {'lang': 'es', 'label': 'Español', 'pv': 654},
        {'lang': 'fr', 'label': 'Français', 'pv': 432},
        {'lang': 'de', 'label': 'Deutsch', 'pv': 321},
        {'lang': 'pt', 'label': 'Português', 'pv': 234},
        {'lang': 'ru', 'label': 'Русский', 'pv': 198},
        {'lang': 'vi', 'label': 'Tiếng Việt', 'pv': 112},
        {'lang': 'nl', 'label': 'Nederlands', 'pv': 78},
        {'lang': 'sv', 'label': 'Svenska', 'pv': 55},
    ]


def _demo_referrers():
    return [
        {'source': 'Google', 'count': 4321},
        {'source': 'Direct', 'count': 3210},
        {'source': 'Twitter/X', 'count': 1432},
        {'source': 'GitHub', 'count': 1123},
        {'source': 'Bing', 'count': 876},
        {'source': 'Reddit', 'count': 654},
        {'source': 'LinkedIn', 'count': 432},
        {'source': 'Other', 'count': 799},
    ]


def _demo_categories():
    return [
        {'category': 'Foundations', 'pv': 3210},
        {'category': 'Strategy & Business', 'pv': 2876},
        {'category': 'Problem Solving & Decision Making', 'pv': 2543},
        {'category': 'Product & User', 'pv': 2198},
        {'category': 'Personal & Team Productivity', 'pv': 1654},
        {'category': 'Technology & Engineering', 'pv': 234},
        {'category': 'Sustainability & ESG', 'pv': 132},
    ]


def _demo_devices():
    return [
        {'resolution': '1920x1080', 'count': 3876},
        {'resolution': '1440x900', 'count': 2134},
        {'resolution': '2560x1440', 'count': 1876},
        {'resolution': '1366x768', 'count': 1543},
        {'resolution': '390x844', 'count': 1321},
        {'resolution': '414x896', 'count': 987},
        {'resolution': '375x812', 'count': 765},
        {'resolution': '360x780', 'count': 345},
    ]


def _demo_hourly():
    import random
    random.seed(99)
    return [{'hour': h, 'pv': random.randint(200, 900)} for h in range(24)]


# ---------------------------------------------------------------------------
# API routes
# ---------------------------------------------------------------------------
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')


@app.route('/api/overview')
def api_overview():
    days = _parse_days(request.args, default=7)
    if _demo_mode():
        return jsonify(_demo_overview(days))

    to_ts = int(time.time())
    from_ts = to_ts - days * 86400
    war_from = to_ts - 7 * 86400

    q_pv = "* | SELECT COUNT(*) AS pv"
    q_uv = "* | SELECT COUNT(DISTINCT visitor_id) AS uv"
    q_sessions = "* | SELECT COUNT(DISTINCT session_id) AS sessions"
    q_war = "* | SELECT COUNT(DISTINCT visitor_id) AS war"

    pv = sls_query(q_pv, from_ts, to_ts)
    uv = sls_query(q_uv, from_ts, to_ts)
    sessions = sls_query(q_sessions, from_ts, to_ts)
    war = sls_query(q_war, war_from, to_ts)

    pv_val = int(pv[0].get('pv', 0)) if pv else 0
    uv_val = int(uv[0].get('uv', 0)) if uv else 0
    sess_val = int(sessions[0].get('sessions', 0)) if sessions else 0
    war_val = int(war[0].get('war', 0)) if war else 0

    avg_ps = round(pv_val / sess_val, 2) if sess_val > 0 else 0

    # Bounce rate: sessions with only 1 page view
    q_bounce = ("* | SELECT COUNT(*) AS bounced FROM "
                "(SELECT session_id, COUNT(*) AS c FROM log GROUP BY session_id HAVING c = 1)")
    bounce = sls_query(q_bounce, from_ts, to_ts)
    bounced = int(bounce[0].get('bounced', 0)) if bounce else 0
    bounce_rate = round(bounced / sess_val * 100, 1) if sess_val > 0 else 0

    return jsonify({
        'pv': pv_val, 'uv': uv_val, 'sessions': sess_val,
        'avg_pages_per_session': avg_ps, 'bounce_rate': bounce_rate,
        'war': war_val, 'days': days,
    })


@app.route('/api/trends')
def api_trends():
    days = _parse_days(request.args, default=30)
    if _demo_mode():
        return jsonify(_demo_trends(days))

    to_ts = int(time.time())
    from_ts = to_ts - days * 86400
    q = ("* | SELECT date_format(from_unixtime(__time__ - __time__ % 86400), '%Y-%m-%d') AS date, "
         "COUNT(*) AS pv, COUNT(DISTINCT visitor_id) AS uv "
         "FROM log GROUP BY date ORDER BY date ASC LIMIT 1000")
    rows = sls_query(q, from_ts, to_ts)
    return jsonify(rows)


@app.route('/api/pages')
def api_pages():
    days = _parse_days(request.args, default=7)
    if _demo_mode():
        return jsonify(_demo_pages())

    to_ts = int(time.time())
    from_ts = to_ts - days * 86400
    q = ("* | SELECT page_path AS page, "
         "ARBITRARY(page_title) AS title, COUNT(*) AS pv "
         "FROM log GROUP BY page_path ORDER BY pv DESC LIMIT 20")
    rows = sls_query(q, from_ts, to_ts)
    return jsonify(rows)


@app.route('/api/languages')
def api_languages():
    days = _parse_days(request.args, default=7)
    if _demo_mode():
        return jsonify(_demo_languages())

    to_ts = int(time.time())
    from_ts = to_ts - days * 86400
    lang_labels = {
        'en': 'English', 'zh': '中文', 'ja': '日本語', 'ko': '한국어',
        'es': 'Español', 'fr': 'Français', 'de': 'Deutsch', 'pt': 'Português',
        'ru': 'Русский', 'vi': 'Tiếng Việt', 'nl': 'Nederlands', 'sv': 'Svenska',
    }
    q = ("* | SELECT site_lang AS lang, COUNT(*) AS pv "
         "FROM log GROUP BY site_lang ORDER BY pv DESC LIMIT 20")
    rows = sls_query(q, from_ts, to_ts)
    for r in rows:
        r['label'] = lang_labels.get(r.get('lang', ''), r.get('lang', ''))
    return jsonify(rows)


@app.route('/api/referrers')
def api_referrers():
    days = _parse_days(request.args, default=7)
    if _demo_mode():
        return jsonify(_demo_referrers())

    to_ts = int(time.time())
    from_ts = to_ts - days * 86400
    q = ("* | SELECT CASE "
         "WHEN referrer = '' THEN 'Direct' "
         "WHEN referrer LIKE '%google%' THEN 'Google' "
         "WHEN referrer LIKE '%bing%' THEN 'Bing' "
         "WHEN referrer LIKE '%twitter%' OR referrer LIKE '%t.co%' THEN 'Twitter/X' "
         "WHEN referrer LIKE '%github%' THEN 'GitHub' "
         "WHEN referrer LIKE '%reddit%' THEN 'Reddit' "
         "WHEN referrer LIKE '%linkedin%' THEN 'LinkedIn' "
         "ELSE 'Other' END AS source, COUNT(*) AS count "
         "FROM log GROUP BY source ORDER BY count DESC LIMIT 20")
    rows = sls_query(q, from_ts, to_ts)
    return jsonify(rows)


@app.route('/api/categories')
def api_categories():
    days = _parse_days(request.args, default=7)
    if _demo_mode():
        return jsonify(_demo_categories())

    to_ts = int(time.time())
    from_ts = to_ts - days * 86400
    q = ("* | SELECT category, COUNT(*) AS pv "
         "FROM log WHERE category != '' GROUP BY category ORDER BY pv DESC LIMIT 20")
    rows = sls_query(q, from_ts, to_ts)
    return jsonify(rows)


@app.route('/api/devices')
def api_devices():
    days = _parse_days(request.args, default=7)
    if _demo_mode():
        return jsonify(_demo_devices())

    to_ts = int(time.time())
    from_ts = to_ts - days * 86400
    q = ("* | SELECT screen_resolution AS resolution, COUNT(*) AS count "
         "FROM log GROUP BY screen_resolution ORDER BY count DESC LIMIT 20")
    rows = sls_query(q, from_ts, to_ts)
    return jsonify(rows)


@app.route('/api/hourly')
def api_hourly():
    days = _parse_days(request.args, default=7)
    if _demo_mode():
        return jsonify(_demo_hourly())

    to_ts = int(time.time())
    from_ts = to_ts - days * 86400
    q = ("* | SELECT EXTRACT(HOUR FROM from_unixtime(__time__)) AS hour, COUNT(*) AS pv "
         "FROM log GROUP BY hour ORDER BY hour ASC")
    rows = sls_query(q, from_ts, to_ts)
    return jsonify(rows)


# ---------------------------------------------------------------------------
if __name__ == '__main__':
    mode = 'DEMO' if _demo_mode() else 'LIVE'
    print(f"\n{'='*60}")
    print(f"  WisdomWiki Analytics Dashboard  [{mode} MODE]")
    print(f"  http://localhost:5001")
    if _demo_mode():
        print(f"  ⚠  No SLS credentials found — showing demo data")
        print(f"     Set ALIBABA_CLOUD_ACCESS_KEY_ID and")
        print(f"     ALIBABA_CLOUD_ACCESS_KEY_SECRET in ../.env")
    print(f"{'='*60}\n")
    app.run(host='0.0.0.0', port=5001, debug=True)
