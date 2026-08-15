# -*- coding: utf-8 -*-
"""
银乡智护 - 农村老年金融反诈AI助手（最终稳定版）
核心修复：所有按钮即时响应，无跳转异常，字体切换独立稳定
"""

import streamlit as st
import json
import os
import random
from datetime import datetime
import pandas as pd
import plotly.express as px

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="银乡智护 - 守住养老钱",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== 初始化 Session State ====================
if "section" not in st.session_state:
    st.session_state.section = "detect"
if "font_size" not in st.session_state:
    st.session_state.font_size = "large"
if "speech_text" not in st.session_state:
    st.session_state.speech_text = ""
if "family_members" not in st.session_state:
    st.session_state.family_members = [
        {"name": "张小明", "relation": "儿子", "phone": "138****1234"},
        {"name": "李小芳", "relation": "女儿", "phone": "139****5678"},
        {"name": "王村长", "relation": "村主任", "phone": "137****9012"},
        {"name": "李医生", "relation": "村医", "phone": "136****3456"}
    ]
if "editing_family" not in st.session_state:
    st.session_state.editing_family = False
if "temp_family" not in st.session_state:
    st.session_state.temp_family = st.session_state.family_members.copy()
if "quiz_idx" not in st.session_state:
    st.session_state.quiz_idx = 0
    st.session_state.quiz_answered = False
    st.session_state.quiz_selected = None
if "sim_idx" not in st.session_state:
    st.session_state.sim_idx = 0
    st.session_state.sim_answered = False
    st.session_state.sim_selected = None


# ==================== 回调函数 ====================
def set_section(section_name):
    st.session_state.section = section_name


def toggle_font():
    st.session_state.font_size = "xlarge" if st.session_state.font_size == "large" else "large"


def set_speech(text):
    st.session_state.speech_text = text


# ==================== 超大字体CSS ====================
def get_font_size_css():
    if st.session_state.font_size == "xlarge":
        return """
        html, body, .stApp, div, p, span, li, label, .stMarkdown {
            font-size: 64px !important;
            line-height: 2.4 !important;
        }
        h1 { font-size: 96px !important; }
        h2 { font-size: 76px !important; }
        h3 { font-size: 64px !important; }
        .stButton > button { font-size: 64px !important; min-height: 140px !important; padding: 32px 48px !important; }
        .stTextArea > div > div > textarea,
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            font-size: 56px !important; min-height: 120px !important; padding: 32px 40px !important;
        }
        .hero-left .greeting { font-size: 72px !important; }
        .hero-left .greeting span { font-size: 64px !important; }
        .hero-left .daily-verse { font-size: 48px !important; }
        .hero-stat .num { font-size: 68px !important; }
        .hero-stat .lbl { font-size: 36px !important; }
        .glass-card { padding: 48px 44px !important; border-radius: 64px !important; }
        .chat-bubble { font-size: 56px !important; padding: 36px 44px !important; }
        .fraud-type .title { font-size: 48px !important; }
        .fraud-type .desc { font-size: 40px !important; }
        """
    else:
        return """
        html, body, .stApp, div, p, span, li, label, .stMarkdown {
            font-size: 36px !important;
            line-height: 2.0 !important;
        }
        h1 { font-size: 68px !important; }
        h2 { font-size: 54px !important; }
        h3 { font-size: 44px !important; }
        .stButton > button { font-size: 40px !important; min-height: 100px !important; padding: 24px 40px !important; }
        .stTextArea > div > div > textarea,
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            font-size: 36px !important; min-height: 90px !important; padding: 24px 32px !important;
        }
        .hero-left .greeting { font-size: 52px !important; }
        .hero-left .greeting span { font-size: 46px !important; }
        .hero-left .daily-verse { font-size: 34px !important; }
        .hero-stat .num { font-size: 48px !important; }
        .hero-stat .lbl { font-size: 28px !important; }
        """


def load_custom_css():
    font_css = get_font_size_css()
    st.markdown(f"""
    <style>
        .stApp {{
            background: linear-gradient(-45deg, #FCF6F0, #F8EFE7, #F5E8DC, #FCF6F0);
            background-size: 400% 400%;
            animation: gradientBG 15s ease infinite;
        }}
        @keyframes gradientBG {{
            0% {{ background-position: 0% 50%; }}
            50% {{ background-position: 100% 50%; }}
            100% {{ background-position: 0% 50%; }}
        }}
        .app-content {{
            animation: fadeSlideUp 0.6s ease forwards;
            opacity: 0;
            transform: translateY(20px);
        }}
        @keyframes fadeSlideUp {{
            0% {{ opacity: 0; transform: translateY(20px); }}
            100% {{ opacity: 1; transform: translateY(0); }}
        }}
        .glass-card {{
            background: rgba(255, 252, 248, 0.78);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border-radius: 48px;
            padding: 36px 34px;
            box-shadow: 0 8px 40px rgba(160, 130, 100, 0.08);
            border: 1px solid rgba(255, 248, 240, 0.5);
            margin-bottom: 28px;
            transition: transform 0.2s ease;
        }}
        .glass-card:hover {{
            transform: translateY(-4px);
        }}
        .stButton > button {{
            border-radius: 80px !important;
            font-weight: 800 !important;
            width: 100% !important;
            color: #FFFFFF !important;
            background: linear-gradient(145deg, #D4A574, #C4906A) !important;
            border: none !important;
            box-shadow: 0 8px 32px rgba(212, 165, 116, 0.25) !important;
            transition: all 0.15s ease !important;
            letter-spacing: 2px;
            cursor: pointer;
        }}
        .stButton > button:hover {{
            transform: scale(1.03) translateY(-3px);
            box-shadow: 0 12px 48px rgba(212, 165, 116, 0.35);
        }}
        .stButton > button:active {{
            transform: scale(0.97);
        }}
        .stTextArea > div > div > textarea,
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {{
            border-radius: 36px !important;
            border: 3px solid #E8DDD0 !important;
            background: rgba(255, 252, 248, 0.7) !important;
            color: #2C3E50 !important;
            transition: border 0.2s ease;
        }}
        .stTextArea > div > div > textarea:focus {{
            border-color: #D4A574 !important;
            box-shadow: 0 0 0 6px rgba(212, 165, 116, 0.15) !important;
        }}
        .hero-banner {{
            background: rgba(255, 255, 255, 0.6);
            backdrop-filter: blur(20px);
            border-radius: 56px;
            padding: 40px 48px;
            box-shadow: 0 8px 40px rgba(180, 150, 120, 0.08);
            border: 1px solid rgba(255, 248, 240, 0.4);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            animation: floatGlow 6s ease-in-out infinite;
        }}
        @keyframes floatGlow {{
            0%, 100% {{ box-shadow: 0 8px 40px rgba(180, 150, 120, 0.08); }}
            50% {{ box-shadow: 0 16px 60px rgba(212, 165, 116, 0.15); }}
        }}
        .hero-left .greeting {{
            font-weight: 800;
            color: #1A2A3A;
        }}
        .hero-left .greeting span {{
            background: linear-gradient(135deg, #D4A574, #C4906A);
            padding: 4px 28px;
            border-radius: 60px;
            color: white;
            margin-left: 12px;
        }}
        .hero-left .daily-verse {{
            color: #5A4A3A;
            margin-top: 8px;
            font-style: italic;
        }}
        .hero-stat .num {{
            font-weight: 900;
            color: #D4A574;
        }}
        .hero-stat .lbl {{
            color: #6A5A4A;
        }}
        .chat-bubble {{
            padding: 28px 36px;
            border-radius: 36px 36px 36px 12px;
            margin: 16px 0;
            line-height: 1.8;
            color: #2C3E50 !important;
        }}
        .chat-bubble.danger {{
            background: #FDECEA;
            border-left: 12px solid #D97070;
        }}
        .chat-bubble.safe {{
            background: #E8F5E9;
            border-left: 12px solid #82BE96;
        }}
        .chat-bubble.warning {{
            background: #FEF6E6;
            border-left: 12px solid #E8A87C;
        }}
        .fraud-type {{
            background: rgba(255, 255, 255, 0.5);
            border-radius: 28px;
            padding: 20px 24px;
            border-left: 10px solid #D4A574;
            margin: 10px 0;
            transition: all 0.2s ease;
        }}
        .fraud-type:hover {{
            background: rgba(255, 255, 255, 0.8);
            transform: translateX(8px);
        }}
        .fraud-type .title {{
            font-weight: 700;
            color: #2C3E50;
        }}
        .fraud-type .desc {{
            color: #5A4A3A;
        }}
        @media screen and (max-width: 768px) {{
            .hero-banner {{ flex-direction: column; text-align: center; padding: 28px; }}
            .hero-right {{ justify-content: center; }}
        }}
        .footer {{
            text-align: center;
            padding: 28px 0 16px;
            border-top: 2px solid #F0E8E0;
            margin-top: 36px;
            color: #8A7A6A;
        }}
        .footer p {{ color: #8A7A6A !important; }}
        {font_css}
    </style>
    """, unsafe_allow_html=True)


# ==================== 数据管理 ====================
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


# ==================== 反诈数据 ====================
FRAUD_KEYWORDS = {
    "冒充公检法": ["涉嫌洗钱", "安全账户", "通缉令", "账户冻结", "保密协议", "配合调查", "刑事拘捕"],
    "投资理财": ["数字货币", "稳赚不赔", "保本高息", "内部渠道", "专家带单", "养老投资", "解冻金", "高回报"],
    "技术操控": ["共享屏幕", "远程控制", "屏幕录像", "验证身份", "下载软件"],
    "紧急恐吓": ["自动扣费", "征信拉黑", "子女被绑架", "出车祸", "包裹藏毒", "健康码异常"],
    "情感诱导": ["刷单兼职", "垫付返利", "网络交友", "博彩漏洞", "免费领"],
    "农村常见": ["保健品", "特效药", "免费体检", "专家讲座", "以房养老", "扶贫款", "助农补贴", "神药"],
    "通用高危": ["转账", "验证码", "银行卡", "密码", "保证金", "手续费", "贷款", "中奖", "红包"]
}

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
    {"q": "接到'安全账户'电话咋办？", "options": ["转账", "挂断报警", "配合", "给密码"], "correct": 1,
     "explain": "挂断并报警！"},
    {"q": "免费体检推荐'特效药'？", "options": ["买", "咨询子女", "掏钱", "介绍邻居"], "correct": 1,
     "explain": "先咨询子女！"}
]


# ==================== 辅助函数 ====================
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
    if len(matched) >= 1:
        return "high", matched, categories
    else:
        return "safe", matched, categories


def get_greeting():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return "早上好"
    elif 12 <= hour < 18:
        return "下午好"
    else:
        return "晚上好"


# ==================== 语音播报组件（独立渲染） ====================
def render_speech():
    if st.session_state.speech_text:
        js_code = f"""
        <script>
            (function() {{
                var msg = new SpeechSynthesisUtterance(`{st.session_state.speech_text}`);
                msg.lang = 'zh-CN';
                msg.rate = 0.85;
                msg.pitch = 1.1;
                msg.volume = 1;
                window.speechSynthesis.speak(msg);
            }})();
        </script>
        """
        st.components.v1.html(js_code, height=0)
        # 播报后清空，避免重复
        st.session_state.speech_text = ""


# ==================== 主界面 ====================
def main():
    load_custom_css()
    account = load_account()
    records = account.get("records", [])
    balance = account.get("balance", 0)
    profile = load_profile()

    st.markdown('<div class="app-content">', unsafe_allow_html=True)

    # ====== 字体切换按钮（稳定） ======
    col_font1, col_font2 = st.columns([6, 1])
    with col_font2:
        current_label = "🔍 超大" if st.session_state.font_size == "large" else "🔍 标准"
        st.button(current_label, key="toggle_font", on_click=toggle_font)

    # ====== 顶部横幅 ======
    greeting = get_greeting()
    daily_verse = random.choice([
        "🌟 今天也要守护好自己的钱袋子！",
        "🛡️ 不轻信、不转账、不透露验证码！",
        "💪 您比骗子想象的更聪明！",
        "🌻 遇到拿不准的事，先问问子女！",
        "❤️ 您的养老钱，我们来守护！",
        "📞 96110 是反诈预警专线！"
    ])

    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-left">
            <div class="greeting">
                🏡 {greeting}，<span>爷爷奶奶</span>
                <span style="color:#8A7A6A; margin-left:16px;">⏰ {datetime.now().strftime('%H:%M')}</span>
            </div>
            <div class="daily-verse">{daily_verse}</div>
        </div>
        <div class="hero-right" style="display:flex; gap:28px;">
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
            if st.button("📌 今日签到打卡 +5积分", key="checkin_btn", use_container_width=True):
                profile['checkin_days'] = profile.get('checkin_days', 0) + 1
                profile['points'] = profile.get('points', 0) + 5
                profile['last_checkin'] = today
                save_profile(profile)
                st.session_state.speech_text = "签到成功！获得5积分！"
                st.success("🎉 签到成功！+5积分")
        st.markdown(f"🏅 累计签到 **{profile.get('checkin_days', 0)}** 天  |  积分 **{profile.get('points', 0)}**",
                    unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_c2:
        st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown("#### 🎖️ 徽章")
        if profile.get('checkin_days', 0) >= 7:
            st.markdown(
                '<span style="background:#F4B942;padding:8px 24px;border-radius:60px;color:white;">🌟 坚持之星</span>',
                unsafe_allow_html=True)
        if profile.get('quiz_completed', 0) >= 2:
            st.markdown(
                '<span style="background:#82BE96;padding:8px 24px;border-radius:60px;color:white;">🧠 反诈达人</span>',
                unsafe_allow_html=True)
        if profile.get('risk_detected', 0) >= 5:
            st.markdown(
                '<span style="background:#D97070;padding:8px 24px;border-radius:60px;color:white;">🛡️ 守护卫士</span>',
                unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ====== 操作台（稳定回调） ======
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 我该做什么？—— 点一下就行")
    col_act1, col_act2, col_act3, col_act4 = st.columns(4)
    with col_act1:
        st.button("📱 读短信/聊天", key="act_detect", on_click=set_section, args=("detect",))
    with col_act2:
        st.button("📒 记个账", key="act_account", on_click=set_section, args=("account",))
    with col_act3:
        st.button("🆘 帮帮我！", key="act_help", on_click=set_section, args=("help",))
    with col_act4:
        st.button("🧠 练一练", key="act_quiz", on_click=set_section, args=("quiz",))
    st.markdown('</div>', unsafe_allow_html=True)

    # ====== 动态内容 ======
    section = st.session_state.section

    # ---- 风险识别 ----
    if section == "detect":
        col_d1, col_d2 = st.columns([3, 2])
        with col_d1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📝 把可疑信息粘贴到这里")
            user_input = st.text_area("", placeholder="例如：我是公安局的，您涉嫌洗钱，请转安全账户...", height=160,
                                      key="input_text", label_visibility="collapsed")
            if st.button("🔍 检测风险", key="detect_btn", use_container_width=True):
                if user_input and user_input.strip():
                    risk, kws, cats = detect_risk(user_input)
                    profile['risk_detected'] = profile.get('risk_detected', 0) + 1
                    save_profile(profile)
                    if risk == "high":
                        st.session_state.speech_text = f"危险！检测到诈骗！涉及{cats}，关键词{','.join(kws[:3])}，请立即报警！"
                        st.markdown(f"""
                        <div class="chat-bubble danger">
                            <strong style="font-size:1.3em;">🚨 高度危险！</strong><br>
                            发现 <strong>{len(kws)}</strong> 个诈骗关键词：<br>
                            <span style="background:#D97070;color:white;padding:6px 20px;border-radius:60px;">{', '.join(kws)}</span><br>
                            <strong style="font-size:1.3em;color:#C94D4D;">⚠️ 千万不要转账！</strong><br>
                            📞 立即拨打 <strong>110</strong> 或联系子女、村委会！
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="chat-bubble safe">
                            <strong style="font-size:1.3em;">✅ 暂未发现风险</strong><br>
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
            <div style="background:rgba(255,248,240,0.6);border-radius:28px;padding:24px;border:1px solid #F0E4D8;">
                <div style="font-weight:700;color:#C4906A;">{case['title']}</div>
                <div style="color:#2C3E50;margin-top:8px;">{case['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 换一个故事", key="refresh_case"):
                pass
            st.markdown("""
            <div style="margin-top:16px;padding:18px;background:#E8F5E9;border-radius:28px;">
                <p>📞 <strong>反诈预警专线：96110</strong></p>
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
            <div style="background:linear-gradient(145deg,#4A3728,#5A4A3A);color:white;border-radius:36px;padding:20px 28px;text-align:center;margin-bottom:16px;">
                <span style="color:white;">💰 当前总资产</span><br>
                <span style="font-size:1.5em;font-weight:900;color:white;">¥{balance:,.2f}</span>
            </div>
            """, unsafe_allow_html=True)
            with st.form(key="acc_form", clear_on_submit=True):
                ca, ct = st.columns(2)
                with ca:
                    amount = st.number_input("金额", min_value=0.01, step=1.0, format="%.2f", key="amt")
                with ct:
                    ttype = st.selectbox("类型", ["收入", "支出"], key="tt")
                desc = st.text_input("用途", placeholder="买菜 / 养老金", key="desc")
                submitted = st.form_submit_button("💾 保存记录", use_container_width=True)
                if submitted:
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
                        st.session_state.speech_text = "记账保存成功！加1积分"
                        st.success("✅ 保存成功！+1积分")
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
                    <div style="flex:1;background:#E8F5E9;border-radius:28px;padding:16px;text-align:center;">
                        <span>📈 今日收入</span><br>
                        <span style="font-size:1.4em;font-weight:800;color:#82BE96;">+¥{today_in:.0f}</span>
                    </div>
                    <div style="flex:1;background:#FDECEA;border-radius:28px;padding:16px;text-align:center;">
                        <span>📉 今日支出</span><br>
                        <span style="font-size:1.4em;font-weight:800;color:#D97070;">-¥{today_out:.0f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("**最近3笔**")
                for r in records[-3:][::-1]:
                    icon = "📈" if r["type"] == "收入" else "📉"
                    color = "#82BE96" if r["type"] == "收入" else "#D97070"
                    st.markdown(f"""
                    <div style="background:rgba(255,252,248,0.5);border-radius:24px;padding:16px 24px;margin:8px 0;border:1px solid #F0E8E0;">
                        <span style="font-weight:bold;color:{color};">{icon} {r['type']}</span>
                        <span style="font-weight:bold;">¥{r['amount']:.2f}</span>
                        <span style="color:#5A4A3A;margin-left:12px;">{r['desc']}</span>
                        <span style="float:right;color:#8A7A6A;">{r['date']}</span>
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
            <div style="background:#FDF2E9;padding:24px;border-radius:36px;border:4px solid #E8A87C;text-align:center;margin-bottom:20px;">
                <p style="font-weight:800;color:#6A4A2A;">🚨 遇到可疑情况，<br>请立即停止操作！</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📞 拨打 110", key="call_110", use_container_width=True):
                st.session_state.speech_text = "请立即拨打110报警"
                st.success("✅ 已提醒：请立即拨打 110！")
            if st.button("👨‍👩‍👦 联系子女", key="call_family", use_container_width=True):
                st.session_state.speech_text = "请立即联系您的子女或家人"
                st.info("📱 建议立即给子女打电话！")
            if st.button("🏘️ 联系村委会", key="call_village", use_container_width=True):
                st.session_state.speech_text = "请立即联系村委会"
                st.info("🏛️ 联系村干部，他们会帮您！")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_h2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 👨‍👩‍👧‍👦 亲情连线")

            if st.button("✏️ 编辑联系人", key="edit_family"):
                st.session_state.editing_family = not st.session_state.editing_family
                if st.session_state.editing_family:
                    st.session_state.temp_family = [m.copy() for m in st.session_state.family_members]

            if st.session_state.editing_family:
                st.markdown("**📝 修改联系人信息：**")
                new_members = []
                for idx, member in enumerate(st.session_state.temp_family):
                    st.markdown(f"--- 联系人 {idx + 1} ---")
                    c_name, c_relation, c_phone = st.columns(3)
                    with c_name:
                        name = st.text_input("姓名", value=member["name"], key=f"f_name_{idx}")
                    with c_relation:
                        relation = st.text_input("称呼", value=member["relation"], key=f"f_rel_{idx}")
                    with c_phone:
                        phone = st.text_input("电话", value=member["phone"], key=f"f_phone_{idx}")
                    new_members.append({"name": name, "relation": relation, "phone": phone})
                if st.button("💾 保存联系人", key="save_family"):
                    st.session_state.family_members = new_members
                    st.session_state.editing_family = False
                    st.session_state.speech_text = "联系人已保存"
                    st.success("✅ 联系人已保存！")

            st.markdown('<div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;">', unsafe_allow_html=True)
            for member in st.session_state.family_members:
                st.markdown(f"""
                <div style="background:white;border-radius:28px;padding:20px;text-align:center;border:1px solid #F0E8E0;">
                    <div style="font-size:2em;">👤</div>
                    <div style="font-weight:700;">{member['name']}</div>
                    <div>{member['relation']}</div>
                    <div style="color:#8A7A6A;">📞 {member['phone']}</div>
                </div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ---- 防骗闯关 ----
    elif section == "quiz":
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🧠 防骗闯关")
        sub_q, sub_s = st.tabs(["📝 小测验", "🎭 风险模拟"])
        with sub_q:
            quiz = QUIZZES[st.session_state.quiz_idx]
            st.markdown(f'<p style="font-weight:700;">第 {st.session_state.quiz_idx + 1} / {len(QUIZZES)} 题</p>',
                        unsafe_allow_html=True)
            st.markdown(f'<p>{quiz["q"]}</p>', unsafe_allow_html=True)
            for i, opt in enumerate(quiz["options"]):
                if st.button(f"{chr(65 + i)}. {opt}", key=f"quiz_{i}"):
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
                    st.session_state.speech_text = "回答正确！继续加油！"
                else:
                    st.error("😅 再想想。" + quiz["explain"])
            col_qn, col_qr = st.columns(2)
            with col_qn:
                if st.button("⬅️ 上一题", key="quiz_prev"):
                    st.session_state.quiz_idx = (st.session_state.quiz_idx - 1) % len(QUIZZES)
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_selected = None
            with col_qr:
                if st.button("下一题 ➡️", key="quiz_next"):
                    st.session_state.quiz_idx = (st.session_state.quiz_idx + 1) % len(QUIZZES)
                    st.session_state.quiz_answered = False
                    st.session_state.quiz_selected = None

        with sub_s:
            sim_scenes = [
                {"q": "接到陌生电话说'银行卡境外消费'，让你提供验证码。",
                 "options": ["提供", "挂断核实", "按提示", "给密码"], "correct": 1, "explain": "挂断并官方核实！"},
                {"q": "微信好友推荐'内部投资平台'月赚50%。", "options": ["加入", "删除", "投小钱", "介绍邻居"],
                 "correct": 1, "explain": "高收益必是骗局！"}
            ]
            sim = sim_scenes[st.session_state.sim_idx]
            st.markdown(f'<p style="font-weight:700;">场景 {st.session_state.sim_idx + 1}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="background:#F5ECE4;padding:24px;border-radius:36px;">{sim["q"]}</p>',
                        unsafe_allow_html=True)
            for i, opt in enumerate(sim["options"]):
                if st.button(f"{chr(65 + i)}. {opt}", key=f"sim_{i}"):
                    st.session_state.sim_selected = i
                    st.session_state.sim_answered = True
            if st.session_state.sim_answered:
                selected = st.session_state.sim_selected
                correct = sim["correct"]
                if selected == correct:
                    st.success("✅ 应对正确！" + sim["explain"])
                    profile['points'] = profile.get('points', 0) + 5
                    save_profile(profile)
                    st.session_state.speech_text = "应对正确！你很棒！"
                else:
                    st.error("❌ 危险操作！" + sim["explain"])
            col_sn, col_sr = st.columns(2)
            with col_sn:
                if st.button("⬅️ 上一场景", key="sim_prev"):
                    st.session_state.sim_idx = (st.session_state.sim_idx - 1) % len(sim_scenes)
                    st.session_state.sim_answered = False
                    st.session_state.sim_selected = None
            with col_sr:
                if st.button("下一场景 ➡️", key="sim_next"):
                    st.session_state.sim_idx = (st.session_state.sim_idx + 1) % len(sim_scenes)
                    st.session_state.sim_answered = False
                    st.session_state.sim_selected = None
        st.markdown('</div>', unsafe_allow_html=True)

    # ====== B站视频（默认暂停） ======
    st.markdown('''
    <div class="glass-card">
        <h4>🎬 反诈宣传视频</h4>
        <iframe 
            src="https://player.bilibili.com/player.html?bvid=BV1vN4y1N7CG&loop=1" 
            scrolling="no" 
            border="0" 
            frameborder="no" 
            framespacing="0" 
            allowfullscreen="true"
            allow="encrypted-media; fullscreen"
            style="width:100%; height:500px; border-radius:20px; background:#000;">
        </iframe>
        <p style="color:#8A7A6A; margin-top:10px;">📺 点击播放按钮开始观看</p>
    </div>
    ''', unsafe_allow_html=True)

    # ====== 骗局类型 ======
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

    # ====== 防骗顺口溜 ======
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 📢 防骗顺口溜（点击播放）")
    rhyme = random.choice([
        "陌生电话要警惕，安全账户全是戏。\n验证密码不能给，转账汇款先停一停。",
        "免费体检别轻信，特效药品是陷阱。\n养老钱要管住，问问子女再决定。",
        "中奖短信不要点，天上不会掉馅饼。\n96110 要记牢，反诈中心守护您。"
    ])
    st.markdown(f'<p style="text-align:center;white-space:pre-wrap;">{rhyme}</p>', unsafe_allow_html=True)
    if st.button("🔊 播放顺口溜", key="play_rhyme", use_container_width=True):
        st.session_state.speech_text = rhyme.replace('\n', '。')
        st.success("已播放！")
    st.markdown('</div>', unsafe_allow_html=True)

    # ====== 防骗知识库 ======
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 📚 防骗小贴士（点击展开学习）")
    for q, a in KNOWLEDGE.items():
        with st.expander(q):
            st.markdown(f'<p>{a}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ====== 数据看板 ======
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 📊 守护数据看板")
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    total_in = sum(r["amount"] for r in records if r["type"] == "收入")
    total_out = sum(r["amount"] for r in records if r["type"] == "支出")
    with col_s1:
        st.markdown(
            f'<p style="text-align:center;"><span style="font-size:1.5em;font-weight:900;color:#D4A574;">{len(records)}</span><br>📝 总笔数</p>',
            unsafe_allow_html=True)
    with col_s2:
        st.markdown(
            f'<p style="text-align:center;"><span style="font-size:1.5em;font-weight:900;color:#82BE96;">¥{total_in:,.0f}</span><br>📈 总收入</p>',
            unsafe_allow_html=True)
    with col_s3:
        st.markdown(
            f'<p style="text-align:center;"><span style="font-size:1.5em;font-weight:900;color:#D97070;">¥{total_out:,.0f}</span><br>📉 总支出</p>',
            unsafe_allow_html=True)
    with col_s4:
        st.markdown(
            f'<p style="text-align:center;"><span style="font-size:1.5em;font-weight:900;color:#E8A87C;">{len(records)}</span><br>📅 守护天数</p>',
            unsafe_allow_html=True)

    if len(records) >= 3:
        try:
            df_data = []
            for r in records:
                try:
                    date_obj = datetime.strptime(r["date"], "%m-%d %H:%M")
                    date_obj = date_obj.replace(year=datetime.now().year)
                    df_data.append({
                        "日期": date_obj,
                        "金额": r["amount"] if r["type"] == "收入" else -r["amount"],
                        "类型": r["type"]
                    })
                except:
                    continue
            if df_data:
                df = pd.DataFrame(df_data)
                df = df.sort_values("日期")
                fig = px.line(df, x="日期", y="金额", title="📈 收支趋势", labels={"金额": "元"}, height=300)
                fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_size=20,
                                  showlegend=False)
                fig.update_traces(line_color="#D4A574", line_width=4)
                st.plotly_chart(fig, use_container_width=True)
        except Exception:
            pass
    st.markdown('</div>', unsafe_allow_html=True)

    # ====== 底部 ======
    st.markdown("""
    <div class="footer">
        <p>🏡 银乡智护 · 农村老年金融反诈公益项目</p>
        <p>❤️ 完全免费 · 无需注册 · 守护乡村养老钱</p>
        <p>🔒 数据仅保存在本地，不上传服务器</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # ====== 统一语音播报渲染 ======
    render_speech()


if __name__ == "__main__":
    main()