# -*- coding: utf-8 -*-
"""
银乡智护 - 农村老年金融反诈AI助手（国赛至尊版）
特性：超大字体、无缝交互、动态海报、视频嵌入、内容丰富
"""

import streamlit as st
import json
import os
import random
import time
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
from PIL import Image, ImageDraw, ImageFont
import io
import base64

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="银乡智护 - 守住养老钱",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== 超大字体 + 精美视觉CSS ====================
def load_custom_css():
    st.markdown("""
    <style>
        /* 全局超大字体 */
        html, body, .stApp, div, p, span, li, label, .stMarkdown {
            font-size: 24px !important;
            line-height: 1.8 !important;
            color: #2C3E50 !important;
        }
        /* 标题更大 */
        h1 { font-size: 52px !important; font-weight: 900 !important; color: #1A2A3A !important; }
        h2 { font-size: 40px !important; font-weight: 800 !important; color: #1A2A3A !important; border-left: 8px solid #D4A574; padding-left: 20px; }
        h3 { font-size: 32px !important; font-weight: 700 !important; color: #2C3E50 !important; }
        /* 背景 */
        .stApp {
            background: linear-gradient(145deg, #FCF6F0 0%, #F8EFE7 100%);
        }
        /* 毛玻璃卡片 */
        .glass-card {
            background: rgba(255, 252, 248, 0.8);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border-radius: 40px;
            padding: 32px 30px;
            box-shadow: 0 12px 40px rgba(160, 130, 100, 0.10);
            border: 1px solid rgba(255, 248, 240, 0.6);
            margin-bottom: 24px;
            transition: transform 0.2s ease;
        }
        .glass-card:hover {
            transform: translateY(-6px);
            box-shadow: 0 20px 60px rgba(160, 130, 100, 0.15);
        }
        /* 超大大按钮 */
        .stButton > button {
            font-size: 32px !important;
            padding: 24px 40px !important;
            min-height: 90px !important;
            border-radius: 80px !important;
            font-weight: 800 !important;
            width: 100% !important;
            color: #FFFFFF !important;
            background: linear-gradient(145deg, #D4A574, #C4906A) !important;
            border: none !important;
            box-shadow: 0 8px 28px rgba(212, 165, 116, 0.25) !important;
            transition: all 0.15s ease !important;
            letter-spacing: 2px;
        }
        .stButton > button:hover {
            transform: scale(1.04) translateY(-4px);
            box-shadow: 0 16px 48px rgba(212, 165, 116, 0.40);
        }
        /* 彩色按钮 */
        .btn-detect { background: linear-gradient(145deg, #6C8EBF, #5A7AA8) !important; }
        .btn-account { background: linear-gradient(145deg, #82BE96, #6AAA7E) !important; }
        .btn-help { background: linear-gradient(145deg, #E8A87C, #D4946A) !important; }
        .btn-danger { background: linear-gradient(145deg, #D97070, #C95A5A) !important; }
        /* 输入框 */
        .stTextArea > div > div > textarea,
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            font-size: 26px !important;
            padding: 22px 28px !important;
            border-radius: 32px !important;
            border: 3px solid #E8DDD0 !important;
            background: rgba(255, 252, 248, 0.7) !important;
            min-height: 76px !important;
            color: #2C3E50 !important;
        }
        /* 顶部横幅 */
        .hero-banner {
            background: linear-gradient(145deg, #FFFFFF, #F8EFE7);
            border-radius: 48px;
            padding: 36px 44px;
            box-shadow: 0 8px 32px rgba(180, 150, 120, 0.10);
            border: 1px solid rgba(255, 248, 240, 0.6);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        .hero-left .greeting {
            font-size: 42px;
            font-weight: 800;
            color: #1A2A3A;
        }
        .hero-left .greeting span {
            background: linear-gradient(135deg, #D4A574, #C4906A);
            padding: 4px 24px;
            border-radius: 60px;
            color: white;
            font-size: 38px;
            margin-left: 12px;
        }
        .hero-left .daily-verse {
            font-size: 26px;
            color: #5A4A3A;
            margin-top: 8px;
            font-style: italic;
        }
        .hero-stat .num {
            font-size: 40px;
            font-weight: 800;
            color: #D4A574;
        }
        .hero-stat .lbl {
            font-size: 20px;
            color: #6A5A4A;
        }
        /* 聊天气泡 */
        .chat-bubble {
            padding: 24px 32px;
            border-radius: 32px 32px 32px 12px;
            margin: 16px 0;
            font-size: 26px;
            line-height: 1.8;
            color: #2C3E50 !important;
        }
        .chat-bubble.danger {
            background: #FDECEA;
            border-left: 10px solid #D97070;
        }
        .chat-bubble.safe {
            background: #E8F5E9;
            border-left: 10px solid #82BE96;
        }
        .chat-bubble.warning {
            background: #FEF6E6;
            border-left: 10px solid #E8A87C;
        }
        /* 操作台卡片 */
        .action-card {
            background: rgba(255, 255, 255, 0.7);
            border-radius: 32px;
            padding: 28px;
            text-align: center;
            border: 2px solid #F0E8E0;
            cursor: pointer;
            transition: all 0.2s ease;
        }
        .action-card:hover {
            transform: scale(1.03);
            border-color: #D4A574;
            box-shadow: 0 8px 24px rgba(212, 165, 116, 0.20);
        }
        .action-card .icon {
            font-size: 64px;
        }
        .action-card .label {
            font-size: 30px;
            font-weight: 700;
            color: #2C3E50;
            margin-top: 8px;
        }
        /* 骗局类型卡片 */
        .fraud-type {
            background: rgba(255, 255, 255, 0.6);
            border-radius: 24px;
            padding: 18px 20px;
            border-left: 8px solid #D4A574;
            margin: 8px 0;
        }
        .fraud-type .title {
            font-size: 28px;
            font-weight: 700;
            color: #2C3E50;
        }
        .fraud-type .desc {
            font-size: 22px;
            color: #5A4A3A;
        }
        /* 响应式 */
        @media screen and (max-width: 768px) {
            .stButton > button { font-size: 26px !important; min-height: 76px; padding: 20px !important; }
            h1 { font-size: 36px !important; }
            .hero-banner { flex-direction: column; text-align: center; padding: 24px; }
            .hero-left .greeting { font-size: 32px; }
        }
        .footer {
            text-align: center;
            padding: 24px 0 12px;
            border-top: 2px solid #F0E8E0;
            margin-top: 32px;
            color: #8A7A6A;
            font-size: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# ==================== 数据与配置 ====================
ACCOUNT_FILE = "account_data.json"
PROFILE_FILE = "profile_data.json"

def load_account():
    if os.path.exists(ACCOUNT_FILE):
        try:
            with open(ACCOUNT_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"records": [], "balance": 0}
    return {"records": [], "balance": 0}

def save_account(data):
    with open(ACCOUNT_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_profile():
    default = {"checkin_days": 0, "last_checkin": None, "points": 0, "quiz_completed": 0, "risk_detected": 0}
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for k, v in default.items():
                    if k not in data:
                        data[k] = v
                return data
        except:
            return default
    return default

def save_profile(data):
    with open(PROFILE_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# ==================== 关键词 ====================
FRAUD_KEYWORDS = {
    "冒充公检法": ["涉嫌洗钱", "安全账户", "通缉令", "账户冻结", "保密协议"],
    "投资理财": ["数字货币", "稳赚不赔", "保本高息", "内部渠道", "养老投资"],
    "技术操控": ["共享屏幕", "远程控制", "屏幕录像", "验证身份"],
    "紧急恐吓": ["自动扣费", "征信拉黑", "子女被绑架", "出车祸"],
    "农村常见": ["保健品", "特效药", "免费体检", "以房养老", "扶贫款"]
}
ALL_KEYWORDS = [kw for sublist in FRAUD_KEYWORDS.values() for kw in sublist]

CASES = [
    {"title": "👮 假警察来电", "desc": "李大爷接到自称公安局电话，说涉嫌洗钱，要求转安全账户。挂断后报警，保住8万元。"},
    {"title": "💊 免费体检推销药", "desc": "王奶奶被忽悠买2万'特效药'，经核实为三无产品，报警追回损失。"},
    {"title": "👶 冒充孙子出车祸", "desc": "张爷爷接到求救电话，给儿子核实后发现是骗子。"},
    {"title": "🏠 以房养老骗局", "desc": "刘叔差点抵押房产，村干部及时制止。"}
]

KNOWLEDGE = {
    "❓ 冒充公检法": "公检法不会电话办案，不会设安全账户。",
    "💰 高回报投资": "稳赚不赔是骗局，超6%收益要警惕。",
    "💊 保健品骗局": "保健品不能治病，免费体检是诱饵。",
    "📞 子女出事": "先电话核实，绝不转账。"
}

QUIZZES = [
    {"q": "接到'安全账户'电话咋办？", "options": ["转账", "挂断报警", "配合", "给密码"], "correct": 1, "explain": "挂断并报警！"},
    {"q": "免费体检推荐'特效药'？", "options": ["买", "咨询子女", "掏钱", "介绍邻居"], "correct": 1, "explain": "先咨询子女！"}
]

def detect_risk(text):
    if not text or not text.strip():
        return "safe", [], []
    text_lower = text.lower()
    matched = []
    categories = []
    for cat, kws in FRAUD_KEYWORDS.items():
        for kw in kws:
            if kw.lower() in text_lower:
                matched.append(kw)
                if cat not in categories:
                    categories.append(cat)
    matched = list(set(matched))
    if len(matched) >= 3:
        return "high", matched, categories
    elif len(matched) >= 1:
        return "medium", matched, categories
    else:
        return "safe", matched, categories

def generate_speech(text, rate=0.9):
    js_code = f"""
    <script>
        function speakNow() {{
            var msg = new SpeechSynthesisUtterance(`{text}`);
            msg.lang = 'zh-CN';
            msg.rate = {rate};
            msg.pitch = 1.1;
            msg.volume = 1;
            window.speechSynthesis.speak(msg);
        }}
        speakNow();
    </script>
    """
    return st.components.v1.html(js_code, height=0)

def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12: return "早上好"
    elif 12 <= hour < 18: return "下午好"
    else: return "晚上好"

# ==================== 动态生成反诈海报 ====================
def generate_poster():
    img = Image.new('RGB', (800, 400), color=(252, 248, 240))
    draw = ImageDraw.Draw(img)
    try:
        font_title = ImageFont.truetype("simhei.ttf", 60)
        font_sub = ImageFont.truetype("simhei.ttf", 40)
    except:
        font_title = ImageFont.load_default()
        font_sub = ImageFont.load_default()
    draw.rectangle([20, 20, 780, 380], outline=(212, 165, 116), width=8)
    draw.text((400, 120), "🛡️ 守住养老钱", fill=(44, 62, 80), anchor="mm", font=font_title)
    draw.text((400, 220), "不轻信 · 不转账 · 不透露", fill=(212, 165, 116), anchor="mm", font=font_sub)
    draw.text((400, 300), "遇到可疑情况，立刻拨打 110", fill=(100, 80, 60), anchor="mm", font=font_sub)
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_buffer.seek(0)
    return img_buffer

# ==================== 主界面 ====================
def main():
    load_custom_css()
    account = load_account()
    records = account.get("records", [])
    balance = account.get("balance", 0)
    profile = load_profile()

    # 初始化session_state
    if "section" not in st.session_state:
        st.session_state.section = "detect"

    greeting = get_greeting()
    daily_verse = random.choice(["🌟 今天也要守护好钱袋子！", "🛡️ 不轻信、不转账、不透露！", "💪 您比骗子想象的更聪明！", "🌻 遇到拿不准的事，先问家人！"])

    # ====== 顶部 ======
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-left">
            <div class="greeting">🏡 {greeting}，<span>爷爷奶奶</span></div>
            <div class="daily-verse">{daily_verse} &nbsp; ⏰ {datetime.now().strftime('%H:%M')}</div>
        </div>
        <div class="hero-right" style="display:flex; gap:24px;">
            <div class="hero-stat"><div class="num">❤️ {profile.get('checkin_days', 0)}</div><div class="lbl">守护天数</div></div>
            <div class="hero-stat"><div class="num">🏅 {profile.get('points', 0)}</div><div class="lbl">积分</div></div>
            <div class="hero-stat"><div class="num">🛡️ {profile.get('risk_detected', 0)}</div><div class="lbl">识别风险</div></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ====== 签到 ======
    col_c1, col_c2 = st.columns([2, 1])
    with col_c1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        last = profile.get('last_checkin')
        today = datetime.now().strftime("%Y-%m-%d")
        if last == today:
            st.success("✅ 今天已签到！继续加油！")
        else:
            if st.button("📌 今日签到打卡", use_container_width=True):
                profile['checkin_days'] = profile.get('checkin_days', 0) + 1
                profile['points'] = profile.get('points', 0) + 5
                profile['last_checkin'] = today
                save_profile(profile)
                st.success("🎉 签到成功！+5积分")
                st.rerun()
        st.markdown(f"🏅 累计签到 **{profile.get('checkin_days', 0)}** 天  |  积分 **{profile.get('points', 0)}**", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_c2:
        st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown("#### 🎖️ 徽章")
        if profile.get('checkin_days', 0) >= 7:
            st.markdown('<span style="background:#F4B942;padding:6px 18px;border-radius:40px;color:white;font-size:26px;">🌟 坚持之星</span>', unsafe_allow_html=True)
        if profile.get('quiz_completed', 0) >= 2:
            st.markdown('<span style="background:#82BE96;padding:6px 18px;border-radius:40px;color:white;font-size:26px;">🧠 反诈达人</span>', unsafe_allow_html=True)
        if profile.get('risk_detected', 0) >= 5:
            st.markdown('<span style="background:#D97070;padding:6px 18px;border-radius:40px;color:white;font-size:26px;">🛡️ 守护卫士</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ====== 操作台（四个按钮直接切换内容） ======
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 我该做什么？—— 点一下就行")
    col_act1, col_act2, col_act3, col_act4 = st.columns(4)
    with col_act1:
        if st.button("📱 读短信/聊天", key="act_detect"):
            st.session_state.section = "detect"
            st.rerun()
    with col_act2:
        if st.button("📒 记个账", key="act_account"):
            st.session_state.section = "account"
            st.rerun()
    with col_act3:
        if st.button("🆘 帮帮我！", key="act_help"):
            st.session_state.section = "help"
            st.rerun()
    with col_act4:
        if st.button("🧠 练一练", key="act_quiz"):
            st.session_state.section = "quiz"
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # ====== 动态内容区域 ======
    section = st.session_state.section

    # ---- 风险识别 ----
    if section == "detect":
        col_d1, col_d2 = st.columns([3, 2])
        with col_d1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📝 把可疑信息粘贴到这里")
            user_input = st.text_area("", placeholder="例如：我是公安局的，您涉嫌洗钱，请转安全账户...", height=160, key="input_text", label_visibility="collapsed")
            if st.button("🔍 检测风险", key="detect_btn", use_container_width=True):
                if user_input and user_input.strip():
                    risk, kws, cats = detect_risk(user_input)
                    profile['risk_detected'] = profile.get('risk_detected', 0) + 1
                    save_profile(profile)
                    if risk == "high":
                        generate_speech(f"危险！检测到诈骗！涉及{cats}，关键词{','.join(kws[:3])}，请立即报警！", rate=0.85)
                        st.markdown(f"""
                        <div class="chat-bubble danger">
                            <strong>🚨 高度危险！</strong><br>
                            发现 <strong>{len(kws)}</strong> 个诈骗关键词：<br>
                            <span style="background:#D97070;color:white;padding:4px 16px;border-radius:40px;font-size:28px;">{', '.join(kws)}</span><br>
                            <strong style="font-size:34px;color:#C94D4D;">⚠️ 千万不要转账！</strong><br>
                            📞 立即拨打 <strong>110</strong> 或联系子女、村委会！
                        </div>
                        """, unsafe_allow_html=True)
                    elif risk == "medium":
                        st.markdown(f"""
                        <div class="chat-bubble warning">
                            <strong>⚠️ 存在可疑风险</strong><br>
                            涉及：{', '.join(cats)}<br>
                            关键词：{', '.join(kws)}<br>
                            💡 建议咨询子女或村委会。
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="chat-bubble safe">
                            <strong>✅ 暂未发现风险</strong><br>
                            仍要记住：不轻信、不转账、不透露验证码。
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("请先输入内容")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_d2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📖 真实案例")
            case = random.choice(CASES)
            st.markdown(f"""
            <div style="background:rgba(255,248,240,0.6);border-radius:24px;padding:20px;border:1px solid #F0E4D8;">
                <div style="font-size:30px;font-weight:700;color:#C4906A;">{case['title']}</div>
                <div style="font-size:24px;color:#2C3E50;margin-top:8px;">{case['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 换一个故事"):
                st.rerun()
            st.markdown("""
            <div style="margin-top:16px;padding:16px;background:#E8F5E9;border-radius:24px;">
                <p style="font-size:24px;">📞 <strong>反诈预警专线：96110</strong></p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ---- 养老记账 ----
    elif section == "account":
        col_a1, col_a2 = st.columns([1, 1])
        with col_a1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 💰 记一笔")
            st.markdown(f"""
            <div style="background:linear-gradient(145deg,#4A3728,#5A4A3A);color:white;border-radius:32px;padding:18px 24px;text-align:center;margin-bottom:16px;">
                <span style="font-size:26px;color:white;">💰 当前总资产</span><br>
                <span style="font-size:52px;font-weight:900;color:white;">¥{balance:,.2f}</span>
            </div>
            """, unsafe_allow_html=True)
            with st.form(key="acc_form", clear_on_submit=True):
                ca, ct = st.columns(2)
                with ca:
                    amount = st.number_input("金额", min_value=0.01, step=1.0, format="%.2f", key="amt")
                with ct:
                    ttype = st.selectbox("类型", ["收入", "支出"], key="tt")
                desc = st.text_input("用途", placeholder="买菜 / 养老金", key="desc")
                if st.form_submit_button("💾 保存记录", use_container_width=True):
                    if amount > 0 and desc.strip():
                        records.append({
                            "date": datetime.now().strftime("%m-%d %H:%M"),
                            "type": ttype,
                            "amount": float(amount),
                            "desc": desc.strip()
                        })
                        if ttype == "收入":
                            balance += float(amount)
                        else:
                            balance -= float(amount)
                        account["records"] = records
                        account["balance"] = balance
                        save_account(account)
                        profile['points'] = profile.get('points', 0) + 1
                        save_profile(profile)
                        st.success("✅ 保存成功！+1积分")
                        st.rerun()
                    else:
                        st.warning("请填写完整")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_a2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📋 最近收支")
            if records:
                today = datetime.now().strftime("%m-%d")
                today_in = sum(r["amount"] for r in records if r["type"] == "收入" and r["date"].startswith(today))
                today_out = sum(r["amount"] for r in records if r["type"] == "支出" and r["date"].startswith(today))
                st.markdown(f"""
                <div style="display:flex;gap:16px;margin:12px 0;">
                    <div style="flex:1;background:#E8F5E9;border-radius:24px;padding:14px;text-align:center;">
                        <span style="font-size:22px;">📈 今日收入</span><br>
                        <span style="font-size:36px;font-weight:800;color:#82BE96;">+¥{today_in:.0f}</span>
                    </div>
                    <div style="flex:1;background:#FDECEA;border-radius:24px;padding:14px;text-align:center;">
                        <span style="font-size:22px;">📉 今日支出</span><br>
                        <span style="font-size:36px;font-weight:800;color:#D97070;">-¥{today_out:.0f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("**最近3笔**")
                for r in records[-3:][::-1]:
                    icon = "📈" if r["type"] == "收入" else "📉"
                    color = "#82BE96" if r["type"] == "收入" else "#D97070"
                    st.markdown(f"""
                    <div style="background:rgba(255,252,248,0.5);border-radius:20px;padding:14px 20px;margin:6px 0;border:1px solid #F0E8E0;">
                        <span style="font-weight:bold;color:{color};font-size:26px;">{icon} {r['type']}</span>
                        <span style="font-weight:bold;font-size:26px;">¥{r['amount']:.2f}</span>
                        <span style="color:#5A4A3A;margin-left:12px;font-size:24px;">{r['desc']}</span>
                        <span style="float:right;color:#8A7A6A;font-size:22px;">{r['date']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("暂无记录")
            st.markdown('</div>', unsafe_allow_html=True)

    # ---- 紧急求助 ----
    elif section == "help":
        col_h1, col_h2 = st.columns([1, 1])
        with col_h1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 🆘 一键求助")
            st.markdown("""
            <div style="background:#FDF2E9;padding:20px;border-radius:32px;border:3px solid #E8A87C;text-align:center;margin-bottom:20px;">
                <p style="font-size:30px;font-weight:800;color:#6A4A2A;">🚨 遇到可疑情况，<br>请立即停止操作！</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📞 拨打 110", use_container_width=True):
                generate_speech("请立即拨打110报警", rate=0.9)
                st.success("✅ 已提醒：请立即拨打 110！")
            if st.button("👨‍👩‍👦 联系子女", use_container_width=True):
                generate_speech("请立即联系您的子女或家人", rate=0.9)
                st.info("📱 建议立即给子女打电话！")
            if st.button("🏘️ 联系村委会", use_container_width=True):
                generate_speech("请立即联系村委会", rate=0.9)
                st.info("🏛️ 联系村干部，他们会帮您！")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_h2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 👨‍👩‍👧‍👦 亲情连线")
            st.markdown("""
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">
                <div style="background:white;border-radius:24px;padding:16px;text-align:center;border:1px solid #F0E8E0;">
                    <div style="font-size:60px;">👨</div>
                    <div style="font-size:28px;font-weight:700;">张小明</div>
                    <div style="font-size:22px;">儿子</div>
                    <div style="font-size:20px;color:#8A7A6A;">📞 138****1234</div>
                </div>
                <div style="background:white;border-radius:24px;padding:16px;text-align:center;border:1px solid #F0E8E0;">
                    <div style="font-size:60px;">👩</div>
                    <div style="font-size:28px;font-weight:700;">李小芳</div>
                    <div style="font-size:22px;">女儿</div>
                    <div style="font-size:20px;color:#8A7A6A;">📞 139****5678</div>
                </div>
                <div style="background:white;border-radius:24px;padding:16px;text-align:center;border:1px solid #F0E8E0;">
                    <div style="font-size:60px;">👴</div>
                    <div style="font-size:28px;font-weight:700;">王村长</div>
                    <div style="font-size:22px;">村主任</div>
                    <div style="font-size:20px;color:#8A7A6A;">📞 137****9012</div>
                </div>
                <div style="background:white;border-radius:24px;padding:16px;text-align:center;border:1px solid #F0E8E0;">
                    <div style="font-size:60px;">👩‍⚕️</div>
                    <div style="font-size:28px;font-weight:700;">李医生</div>
                    <div style="font-size:22px;">村医</div>
                    <div style="font-size:20px;color:#8A7A6A;">📞 136****3456</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ---- 防骗闯关 ----
    elif section == "quiz":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🧠 防骗闯关")
        sub_q, sub_s = st.tabs(["📝 小测验", "🎭 风险模拟"])
        with sub_q:
            if "quiz_idx" not in st.session_state:
                st.session_state.quiz_idx = 0
                st.session_state.quiz_answered = False
                st.session_state.quiz_selected = None
            quiz = QUIZZES[st.session_state.quiz_idx]
            st.markdown(f'<p style="font-size:28px;font-weight:700;">第 {st.session_state.quiz_idx+1} / {len(QUIZZES)} 题</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:30px;">{quiz["q"]}</p>', unsafe_allow_html=True)
            for i, opt in enumerate(quiz["options"]):
                if st.button(f"{chr(65+i)}. {opt}", key=f"quiz_{i}"):
                    st.session_state.quiz_selected = i
                    st.session_state.quiz_answered = True
            if st.session_state.quiz_answered:
                selected = st.session_state.quiz_selected
                correct = quiz["correct"]
                if selected == correct:
                    st.success("🎉 回答正确！" + quiz["explain"])
                    profile['points'] = profile.get('points', 0) + 3
                    profile['quiz_completed'] = profile.get('quiz_completed', 0) + 1
                    save_profile(profile)
                else:
                    st.error("😅 再想想。" + quiz["explain"])
            col_qn, col_qr = st.columns(2)
            with col_qn:
                if st.button("⬅️ 上一题"):
                    st.session_state.quiz_idx = (st.session_state.quiz_idx - 1) % len(QUIZZES)
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_selected = None
                    st.rerun()
            with col_qr:
                if st.button("下一题 ➡️"):
                    st.session_state.quiz_idx = (st.session_state.quiz_idx + 1) % len(QUIZZES)
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_selected = None
                    st.rerun()

        with sub_s:
            st.markdown("#### 🎭 风险模拟器（沉浸式体验）")
            sim_scenes = [
                {"q": "接到陌生电话说'银行卡境外消费'，让你提供验证码。", "options": ["提供", "挂断核实", "按提示", "给密码"], "correct": 1, "explain": "挂断并官方核实！"},
                {"q": "微信好友推荐'内部投资平台'月赚50%。", "options": ["加入", "删除", "投小钱", "介绍邻居"], "correct": 1, "explain": "高收益必是骗局！"}
            ]
            if "sim_idx" not in st.session_state:
                st.session_state.sim_idx = 0
                st.session_state.sim_answered = False
                st.session_state.sim_selected = None
            sim = sim_scenes[st.session_state.sim_idx]
            st.markdown(f'<p style="font-size:28px;font-weight:700;">场景 {st.session_state.sim_idx+1}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:30px;background:#F5ECE4;padding:20px;border-radius:32px;">{sim["q"]}</p>', unsafe_allow_html=True)
            for i, opt in enumerate(sim["options"]):
                if st.button(f"{chr(65+i)}. {opt}", key=f"sim_{i}"):
                    st.session_state.sim_selected = i
                    st.session_state.sim_answered = True
            if st.session_state.sim_answered:
                selected = st.session_state.sim_selected
                correct = sim["correct"]
                if selected == correct:
                    st.success("✅ 应对正确！" + sim["explain"])
                    profile['points'] = profile.get('points', 0) + 5
                    save_profile(profile)
                else:
                    st.error("❌ 危险操作！" + sim["explain"])
            col_sn, col_sr = st.columns(2)
            with col_sn:
                if st.button("⬅️ 上一场景"):
                    st.session_state.sim_idx = (st.session_state.sim_idx - 1) % len(sim_scenes)
                    st.session_state.sim_answered = False
                    st.session_state.sim_selected = None
                    st.rerun()
            with col_sr:
                if st.button("下一场景 ➡️"):
                    st.session_state.sim_idx = (st.session_state.sim_idx + 1) % len(sim_scenes)
                    st.session_state.sim_answered = False
                    st.session_state.sim_selected = None
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # ====== 额外丰富内容 ======
    st.markdown("---")
    # 反诈海报（动态生成）
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 🖼️ 今日反诈海报")
    poster = generate_poster()
    st.image(poster, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 骗局类型展示
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### ⚠️ 常见骗局类型")
    types = {
        "冒充公检法": "公检法不会电话办案",
        "投资理财": "高回报必有诈",
        "保健品推销": "免费体检是诱饵",
        "冒充亲友": "先核实再行动",
        "中奖信息": "天上不会掉馅饼",
        "共享屏幕": "骗子会偷看密码"
    }
    cols = st.columns(3)
    for idx, (name, desc) in enumerate(types.items()):
        with cols[idx % 3]:
            st.markdown(f"""
            <div class="fraud-type">
                <div class="title">🔸 {name}</div>
                <div class="desc">{desc}</div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 防骗顺口溜
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 📢 防骗顺口溜（点击播放）")
    rhyme = random.choice([
        "陌生电话要警惕，安全账户全是戏。\n验证密码不能给，转账汇款先停一停。",
        "免费体检别轻信，特效药品是陷阱。\n养老钱要管住，问问子女再决定。",
        "中奖短信不要点，天上不会掉馅饼。\n96110 要记牢，反诈中心守护您。"
    ])
    st.markdown(f'<p style="font-size:36px;font-weight:700;color:#2C3E50;text-align:center;white-space:pre-wrap;">{rhyme}</p>', unsafe_allow_html=True)
    if st.button("🔊 播放顺口溜", use_container_width=True):
        generate_speech(rhyme.replace('\n', '。'), rate=0.85)
        st.success("已播放！")
    st.markdown('</div>', unsafe_allow_html=True)

    # 反诈视频（B站嵌入）
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 🎬 反诈宣传视频（点击播放）")
    video_url = "https://www.bilibili.com/video/BV1UY411b7xX"  # 示例反诈视频（可替换）
    st.video(video_url)
    st.caption("视频来源：国家反诈中心宣传片")
    st.markdown('</div>', unsafe_allow_html=True)

    # 防骗知识库
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 📚 防骗小贴士（点击展开）")
    for q, a in KNOWLEDGE.items():
        with st.expander(q):
            st.markdown(f'<p style="font-size:26px;">{a}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 数据看板
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 📊 守护数据看板")
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    total_in = sum(r["amount"] for r in records if r["type"] == "收入")
    total_out = sum(r["amount"] for r in records if r["type"] == "支出")
    with col_s1:
        st.markdown(f'<p style="text-align:center;"><span style="font-size:44px;font-weight:900;color:#D4A574;">{len(records)}</span><br><span style="font-size:22px;">📝 总笔数</span></p>', unsafe_allow_html=True)
    with col_s2:
        st.markdown(f'<p style="text-align:center;"><span style="font-size:44px;font-weight:900;color:#82BE96;">¥{total_in:,.0f}</span><br><span style="font-size:22px;">📈 总收入</span></p>', unsafe_allow_html=True)
    with col_s3:
        st.markdown(f'<p style="text-align:center;"><span style="font-size:44px;font-weight:900;color:#D97070;">¥{total_out:,.0f}</span><br><span style="font-size:22px;">📉 总支出</span></p>', unsafe_allow_html=True)
    with col_s4:
        st.markdown(f'<p style="text-align:center;"><span style="font-size:44px;font-weight:900;color:#E8A87C;">{len(records)}</span><br><span style="font-size:22px;">📅 守护天数</span></p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # 底部
    st.markdown("""
    <div class="footer">
        <p style="font-size:22px;">🏡 银乡智护 · 农村老年金融反诈公益项目</p>
        <p style="font-size:20px;">❤️ 完全免费 · 无需注册 · 守护乡村养老钱</p>
        <p style="font-size:18px;">🔒 数据仅保存在本地，不上传服务器</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()