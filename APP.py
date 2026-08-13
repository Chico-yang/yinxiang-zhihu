# -*- coding: utf-8 -*-
"""
银乡智护 - 农村老年金融反诈AI助手（国赛巅峰版）
视觉：深色高对比文字 + 大字号 + 动态微交互
功能：签到积分 + 风险模拟器 + 个人中心 + 语音助手 + 数据看板
情感：动态问候 + 实时时钟 + 鼓励语 + 趣味反馈
"""

import streamlit as st
import json
import os
import random
import time
from datetime import datetime, timedelta
import pandas as pd
import plotly.express as px
import base64

# ==================== 页面配置 ====================
st.set_page_config(
    page_title="银乡智护 - 守护养老钱",
    page_icon="🏡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== 自定义CSS（清晰大字体 + 动态动画） ====================
def load_custom_css():
    st.markdown("""
    <style>
        /* 全局背景与文字色 */
        .stApp {
            background-color: #FCF6F0 !important;
            background-image: radial-gradient(circle at 20% 30%, rgba(244, 224, 200, 0.2) 0%, transparent 60%),
                              radial-gradient(circle at 80% 70%, rgba(200, 180, 160, 0.1) 0%, transparent 50%);
        }
        /* 所有文字默认深色，高对比度 */
        html, body, .stApp, div, p, span, li, label, .stMarkdown {
            color: #3D2C1E !important;
            font-size: 20px !important;
            line-height: 1.6 !important;
        }
        h1 { font-size: 40px !important; color: #2C3E50 !important; font-weight: 800 !important; }
        h2 { font-size: 32px !important; color: #2C3E50 !important; border-left: 6px solid #D4A574; padding-left: 16px; font-weight: 700; }
        h3 { font-size: 26px !important; color: #3D2C1E !important; font-weight: 700; }
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3 { color: #2C3E50 !important; }

        /* ---- 卡片毛玻璃 ---- */
        .glass-card {
            background: rgba(255, 252, 248, 0.85);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 30px;
            padding: 26px 24px;
            box-shadow: 0 6px 24px rgba(160, 130, 100, 0.08);
            border: 1px solid rgba(255, 248, 240, 0.5);
            margin-bottom: 20px;
            transition: transform 0.2s ease, box-shadow 0.3s ease;
        }
        .glass-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(160, 130, 100, 0.12);
        }

        /* ---- 超大大按钮（深色文字） ---- */
        .stButton > button {
            font-size: 28px !important;
            padding: 20px 32px !important;
            min-height: 76px !important;
            border-radius: 60px !important;
            font-weight: 700 !important;
            width: 100% !important;
            color: #FFFFFF !important;
            background: linear-gradient(145deg, #D4A574, #C4906A) !important;
            border: none !important;
            box-shadow: 0 6px 20px rgba(212, 165, 116, 0.25) !important;
            transition: all 0.15s ease !important;
            letter-spacing: 1px;
        }
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.02);
            box-shadow: 0 12px 32px rgba(212, 165, 116, 0.35);
        }
        .stButton > button:active {
            transform: scale(0.97);
        }
        /* 彩色按钮变体 */
        .btn-detect { background: linear-gradient(145deg, #6C8EBF, #5A7AA8) !important; box-shadow: 0 6px 20px rgba(108, 142, 191, 0.25) !important; }
        .btn-account { background: linear-gradient(145deg, #82BE96, #6AAA7E) !important; box-shadow: 0 6px 20px rgba(130, 190, 150, 0.25) !important; }
        .btn-help { background: linear-gradient(145deg, #E8A87C, #D4946A) !important; box-shadow: 0 6px 20px rgba(232, 168, 124, 0.25) !important; }
        .btn-danger { background: linear-gradient(145deg, #D97070, #C95A5A) !important; box-shadow: 0 6px 20px rgba(217, 112, 112, 0.25) !important; }

        /* ---- 输入框大字体深色 ---- */
        .stTextArea > div > div > textarea,
        .stTextInput > div > div > input,
        .stNumberInput > div > div > input {
            font-size: 22px !important;
            padding: 18px 24px !important;
            border-radius: 28px !important;
            border: 2px solid #E8DDD0 !important;
            background: rgba(255, 252, 248, 0.7) !important;
            min-height: 64px !important;
            color: #3D2C1E !important;
        }
        .stTextArea > div > div > textarea:focus {
            border-color: #D4A574 !important;
            box-shadow: 0 0 0 4px rgba(212, 165, 116, 0.15) !important;
        }

        /* ---- 顶部门廊（深色文字） ---- */
        .hero-banner {
            background: linear-gradient(145deg, #FFFFFF 0%, #F8EFE7 100%);
            border-radius: 40px;
            padding: 28px 36px;
            margin-bottom: 24px;
            box-shadow: 0 8px 32px rgba(180, 150, 120, 0.10);
            border: 1px solid rgba(255, 248, 240, 0.6);
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
        }
        .hero-left .greeting {
            font-size: 34px;
            font-weight: 700;
            color: #3D2C1E;
        }
        .hero-left .greeting span {
            background: linear-gradient(135deg, #D4A574, #C4906A);
            padding: 2px 18px;
            border-radius: 40px;
            color: white;
            font-size: 30px;
            margin-left: 8px;
        }
        .hero-left .daily-verse {
            font-size: 22px;
            color: #5A4A3A;
            margin-top: 6px;
            font-style: italic;
        }
        .hero-left .clock {
            font-size: 20px;
            color: #7A6A5A;
            margin-top: 4px;
        }
        .hero-right {
            display: flex;
            gap: 20px;
            flex-wrap: wrap;
        }
        .hero-stat {
            text-align: center;
            background: rgba(255,255,255,0.6);
            padding: 8px 20px;
            border-radius: 30px;
            backdrop-filter: blur(4px);
        }
        .hero-stat .num {
            font-size: 34px;
            font-weight: 800;
            color: #D4A574;
        }
        .hero-stat .lbl {
            font-size: 17px;
            color: #6A5A4A;
        }

        /* ---- 聊天气泡（深色文字） ---- */
        .chat-bubble {
            padding: 18px 24px;
            border-radius: 24px 24px 24px 8px;
            margin: 12px 0;
            font-size: 22px;
            line-height: 1.6;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
            color: #3D2C1E !important;
        }
        .chat-bubble.ai {
            background: #F0E8E0;
            border-left: 6px solid #D4A574;
        }
        .chat-bubble.user {
            background: #D4A574;
            color: white !important;
            border-radius: 24px 24px 8px 24px;
            margin-left: 20px;
        }
        .chat-bubble.danger {
            background: #FDECEA;
            border-left: 6px solid #D97070;
            color: #6A2A2A !important;
        }
        .chat-bubble.safe {
            background: #E8F5E9;
            border-left: 6px solid #82BE96;
            color: #2A5A3A !important;
        }
        .chat-bubble.warning {
            background: #FEF6E6;
            border-left: 6px solid #E8A87C;
            color: #5A4A2A !important;
        }

        /* ---- 亲情卡片 ---- */
        .family-card {
            background: white;
            border-radius: 20px;
            padding: 16px 20px;
            text-align: center;
            box-shadow: 0 2px 12px rgba(0,0,0,0.04);
            border: 1px solid #F0E8E0;
            transition: all 0.2s;
        }
        .family-card:hover {
            transform: translateY(-4px) scale(1.02);
            box-shadow: 0 8px 24px rgba(0,0,0,0.08);
        }
        .family-card .avatar {
            font-size: 52px;
            display: block;
        }
        .family-card .name {
            font-size: 24px;
            font-weight: 700;
            color: #3D2C1E;
            margin-top: 4px;
        }
        .family-card .relation {
            font-size: 18px;
            color: #7A6A5A;
        }

        /* ---- 动态数字滚动（CSS实现） ---- */
        .num-roll {
            display: inline-block;
            animation: rollIn 0.8s ease-out;
        }
        @keyframes rollIn {
            0% { opacity: 0; transform: translateY(-20px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        /* ---- 脉冲动画（用于提醒） ---- */
        .pulse {
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { box-shadow: 0 0 0 0 rgba(212, 165, 116, 0.4); }
            70% { box-shadow: 0 0 0 15px rgba(212, 165, 116, 0); }
            100% { box-shadow: 0 0 0 0 rgba(212, 165, 116, 0); }
        }

        /* ---- 签到徽章 ---- */
        .badge {
            display: inline-block;
            background: #D4A574;
            color: white;
            padding: 6px 18px;
            border-radius: 40px;
            font-size: 22px;
            font-weight: 700;
            margin: 4px;
        }
        .badge-gold {
            background: #F4B942;
        }

        /* ---- 响应式 ---- */
        @media screen and (max-width: 768px) {
            .stButton > button { font-size: 24px !important; min-height: 64px; padding: 16px 24px !important; }
            h1 { font-size: 32px !important; }
            .hero-banner { flex-direction: column; text-align: center; padding: 20px; }
            .hero-right { justify-content: center; }
            .hero-left .greeting { font-size: 28px; }
            .hero-left .greeting span { font-size: 24px; }
        }

        /* ---- 底部 ---- */
        .footer {
            text-align: center;
            padding: 20px 0 10px 0;
            border-top: 2px solid #F0E8E0;
            margin-top: 24px;
            color: #8A7A6A;
            font-size: 17px;
        }
        .footer p { color: #8A7A6A !important; }
    </style>
    """, unsafe_allow_html=True)

# ==================== 数据文件 ====================
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
    default = {
        "checkin_days": 0,
        "last_checkin": None,
        "points": 0,
        "quiz_completed": 0,
        "risk_detected": 0
    }
    if os.path.exists(PROFILE_FILE):
        try:
            with open(PROFILE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # 合并默认值，防止缺少字段
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

# ==================== 关键词库 ====================
FRAUD_KEYWORDS = {
    "冒充公检法": ["涉嫌洗钱", "安全账户", "通缉令", "账户冻结", "保密协议", "刑事拘捕", "配合调查"],
    "投资理财": ["数字货币", "稳赚不赔", "保本高息", "内部渠道", "专家带单", "养老投资", "解冻金", "高回报"],
    "技术操控": ["共享屏幕", "远程控制", "屏幕录像", "验证身份", "下载软件", "银联会议"],
    "紧急恐吓": ["自动扣费", "征信拉黑", "子女被绑架", "出车祸", "包裹藏毒", "健康码异常"],
    "情感诱导": ["刷单兼职", "垫付返利", "大额订单", "网络交友", "博彩漏洞", "免费领"],
    "农村常见": ["保健品", "特效药", "免费体检", "专家讲座", "以房养老", "扶贫款", "助农补贴", "神药"]
}
ALL_KEYWORDS = [kw for sublist in FRAUD_KEYWORDS.values() for kw in sublist]

# ==================== 案例库 ====================
CASES = [
    {"title": "👮 假警察来电称涉嫌洗钱", "desc": "李大爷接到自称公安局电话，说他涉嫌洗钱，要求转钱到安全账户。李大爷想起村里宣传，挂断后报警，成功保住8万元养老钱。"},
    {"title": "💊 免费体检推销特效药", "desc": "王奶奶参加村里免费体检，被推销员忽悠购买2万元'特效药'。经子女核实为三无产品，报警后追回全部损失。"},
    {"title": "👶 冒充孙子出车祸要钱", "desc": "张爷爷接到电话，对方哭着喊爷爷说自己出车祸急需3万。张爷爷给儿子打电话核实，发现是骗子。"},
    {"title": "🏠 以房养老骗局", "desc": "刘叔听信'以房养老'项目，差点抵押房产。村干部上门讲解后及时制止。"},
    {"title": "🎁 中奖短信要缴税", "desc": "赵奶奶收到'中奖10万'短信，要求先缴5000元税费。她找村干部帮忙看，被识破是诈骗。"},
    {"title": "📦 冒充客服退款诈骗", "desc": "孙大爷接到'网购客服'电话，说商品有问题要双倍退款，让他提供银行卡号。他想起反诈宣传，直接挂断。"}
]

# ==================== 知识库 ====================
KNOWLEDGE = {
    "❓ 如何识别冒充公检法诈骗？": "凡是自称公检法机关，通过电话、短信要求您转账、提供验证码、下载软件的都是诈骗！公检法机关不会通过电话办案，更不会设立'安全账户'。",
    "💰 遇到'高回报投资'怎么办？": "凡是承诺'稳赚不赔''保本高息''内部渠道'的都是诈骗！正规投资都有风险，收益率超过6%就要打问号。",
    "💊 保健品骗局有哪些套路？": "以'免费体检''专家讲座''赠送礼品'为诱饵，夸大产品功效，诱导高价购买。保健品不能代替药品！",
    "🏠 如何防范'以房养老'骗局？": "正规以房养老只有国家指定的保险公司可以开展。凡是民间机构、个人承诺'抵押房产换养老金'的都是骗局！",
    "📞 接到'子女出事'电话怎么办？": "先挂断电话，立即给子女本人打电话核实。千万不要在电话里转账！",
    "📱 什么是'共享屏幕'诈骗？": "骗子诱导您开启'屏幕共享'，就能看到您的银行卡号、密码、验证码。任何人要求共享屏幕都是诈骗！"
}

# ==================== 测验题库 ====================
QUIZZES = [
    {
        "q": "📞 您接到电话，对方说'我是公安局的，您涉嫌洗钱，请把钱转到安全账户'，您应该怎么做？",
        "options": ["立即转账证明清白", "挂断电话并拨打110核实", "按照对方要求操作", "告诉对方银行卡密码"],
        "correct": 1,
        "explain": "✅ 公检法机关不会通过电话办案！挂断并拨打110核实最正确！"
    },
    {
        "q": "💊 村里有'免费体检'活动，工作人员推荐您买3万元'特效药'，说能根治高血压，您应该？",
        "options": ["买来试试", "咨询子女或村干部后再决定", "当场掏钱购买", "介绍邻居一起来买"],
        "correct": 1,
        "explain": "✅ 保健品不能代替药品！先咨询子女或村干部，不要轻易掏钱。"
    },
    {
        "q": "🎁 您收到短信'恭喜中奖，请点击链接领取'，您应该？",
        "options": ["点击链接领奖", "拨打短信里的电话", "不点击链接，直接删除", "转发给朋友一起领"],
        "correct": 2,
        "explain": "✅ 中奖短信99%是诈骗！不要点击链接，直接删除最安全！"
    }
]

# ==================== 风险模拟场景（沉浸式） ====================
SIMULATIONS = [
    {
        "scene": "🔊 您接到一个陌生电话，对方说：'您好，我是XX银行客服，您的银行卡在境外有大额消费，需要您提供验证码进行核实。'",
        "options": ["提供验证码", "挂断电话，拨打银行官方客服核实", "按对方提示操作", "告诉对方银行卡密码"],
        "correct": 1,
        "explain": "✅ 银行不会主动索要验证码！挂断后拨打官方客服核实最安全。"
    },
    {
        "scene": "📱 您收到一条微信好友申请，对方头像是个美女，说：'大叔，我推荐您一个投资平台，一个月稳赚50%，我内部有人。'",
        "options": ["添加好友，跟着投资", "不添加，直接删除", "先投小钱试试", "介绍给邻居一起赚"],
        "correct": 1,
        "explain": "✅ 高收益必是陷阱！不添加、不理会，直接删除最明智。"
    },
    {
        "scene": "🏥 村里来了几个穿白大褂的人，免费给老人体检，然后说您有癌症早期征兆，推荐买他们的'特效药'，一疗程2万。",
        "options": ["立即购买，保命要紧", "先不买，去正规医院复查", "相信医生，买一个疗程", "借钱也要买"],
        "correct": 1,
        "explain": "✅ 正规医院检查才是正道！不要轻信流动摊贩，去大医院复查最可靠。"
    }
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
    if 5 <= hour < 12:
        return "早上好"
    elif 12 <= hour < 18:
        return "下午好"
    else:
        return "晚上好"

# ==================== 主界面 ====================
def main():
    load_custom_css()

    # 加载数据
    account = load_account()
    records = account.get("records", [])
    balance = account.get("balance", 0)
    profile = load_profile()

    # 动态问候
    greeting = get_greeting()
    current_time = datetime.now().strftime("%H:%M")
    daily_verse = random.choice([
        "🌟 今天也要守护好自己的钱袋子哦！",
        "🛡️ 不轻信、不转账、不透露验证码！",
        "💪 您比骗子想象的更聪明！",
        "🌻 遇到拿不准的事，先问问子女或村干部！",
        "❤️ 您的养老钱，我们来守护！",
        "📞 96110 是反诈预警专线，请放心接听！",
        "🌾 守住养老钱，安享幸福晚年！"
    ])

    # ====== 🏠 顶部门廊 ======
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-left">
            <div class="greeting">
                🏡 {greeting}，<span>爷爷奶奶</span>
                <span style="font-size:24px; color:#8A7A6A; margin-left:12px;">⏰ {current_time}</span>
            </div>
            <div class="daily-verse">
                {daily_verse}
            </div>
            <div class="clock">
                🌤️ 今天天气晴好，适合出门走走，顺便跟邻居聊聊反诈知识
            </div>
        </div>
        <div class="hero-right">
            <div class="hero-stat">
                <div class="num">❤️ {profile.get('checkin_days', 0)}</div>
                <div class="lbl">守护天数</div>
            </div>
            <div class="hero-stat">
                <div class="num">🏅 {profile.get('points', 0)}</div>
                <div class="lbl">守护积分</div>
            </div>
            <div class="hero-stat">
                <div class="num">🛡️ {profile.get('risk_detected', 0)}</div>
                <div class="lbl">识别风险</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ====== 🎯 操作台 ======
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### 🎯 我该做什么？—— 点一下就行")
    col_btn1, col_btn2, col_btn3, col_btn4 = st.columns(4)
    with col_btn1:
        if st.button("📱 读短信 / 聊天", key="go_detect", use_container_width=True):
            st.session_state.active_tab = "detect"
    with col_btn2:
        if st.button("📒 记个账", key="go_account", use_container_width=True):
            st.session_state.active_tab = "account"
    with col_btn3:
        if st.button("🆘 帮帮我！", key="go_help", use_container_width=True):
            st.session_state.active_tab = "help"
    with col_btn4:
        if st.button("🧠 练一练", key="go_quiz", use_container_width=True):
            st.session_state.active_tab = "quiz"
    st.markdown('</div>', unsafe_allow_html=True)

    # ====== 签到打卡 ======
    col_check1, col_check2 = st.columns([3, 1])
    with col_check1:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        last = profile.get('last_checkin')
        today = datetime.now().strftime("%Y-%m-%d")
        if last == today:
            st.success("✅ 今天已签到！ 继续加油！")
        else:
            if st.button("📌 今日签到打卡", use_container_width=True):
                profile['checkin_days'] = profile.get('checkin_days', 0) + 1
                profile['points'] = profile.get('points', 0) + 5
                profile['last_checkin'] = today
                save_profile(profile)
                st.success("🎉 签到成功！获得 5 积分！")
                st.rerun()
        st.markdown(f"<p style='font-size:20px;'>🏅 累计签到：<strong>{profile.get('checkin_days', 0)}</strong> 天  |  积分：<strong>{profile.get('points', 0)}</strong> 分</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with col_check2:
        st.markdown('<div class="glass-card" style="text-align:center;">', unsafe_allow_html=True)
        st.markdown("#### 🎖️ 徽章")
        if profile.get('checkin_days', 0) >= 7:
            st.markdown('<span class="badge badge-gold">🌟 坚持之星</span>', unsafe_allow_html=True)
        if profile.get('quiz_completed', 0) >= 3:
            st.markdown('<span class="badge">🧠 反诈达人</span>', unsafe_allow_html=True)
        if profile.get('risk_detected', 0) >= 5:
            st.markdown('<span class="badge">🛡️ 守护卫士</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # ====== 主功能区域（Tabs） ======
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📱 风险识别", "📒 养老记账", "🆘 紧急求助", "🧠 防骗闯关", "🏅 我的守护"])

    # ---- Tab 1: 风险识别 ----
    with tab1:
        col_d1, col_d2 = st.columns([3, 2], gap="large")
        with col_d1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📝 把您收到的信息粘贴到这里")
            user_input = st.text_area("", placeholder="例如：您好，我是公安局的，您涉嫌洗钱，请将资金转入安全账户...", height=140, key="input_text", label_visibility="collapsed")
            if st.button("🔍 帮我看看这是不是诈骗", key="detect", use_container_width=True):
                if user_input and user_input.strip():
                    risk, kws, cats = detect_risk(user_input)
                    # 更新风险检测计数
                    profile['risk_detected'] = profile.get('risk_detected', 0) + 1
                    save_profile(profile)
                    if risk == "high":
                        generate_speech(f"危险！检测到诈骗！涉及{cats}，关键词有{','.join(kws[:3])}。请立即报警！", rate=0.85)
                        st.markdown(f"""
                        <div class="chat-bubble danger">
                            <strong>🚨 哎呀，这太危险了！</strong><br>
                            我发现了 <strong>{len(kws)}</strong> 个诈骗关键词，涉及 <strong>{', '.join(cats)}</strong>。<br>
                            <span style="background:#D97070;color:white;padding:4px 14px;border-radius:30px;font-size:20px;display:inline-block;margin:8px 0;">{', '.join(kws)}</span><br>
                            <strong style="font-size:26px;color:#C94D4D;">⚠️ 千万不要转账！</strong><br>
                            📞 赶紧拨打 <strong>110</strong> 报警，或者联系子女、村委会！
                        </div>
                        """, unsafe_allow_html=True)
                    elif risk == "medium":
                        st.markdown(f"""
                        <div class="chat-bubble warning">
                            <strong>⚠️ 有点可疑，要当心！</strong><br>
                            我发现了 <strong>{len(kws)}</strong> 个可疑关键词，涉及 <strong>{', '.join(cats)}</strong>。<br>
                            <span style="background:#E8A87C;color:white;padding:4px 14px;border-radius:30px;font-size:20px;display:inline-block;margin:8px 0;">{', '.join(kws)}</span><br>
                            💡 建议先咨询子女或村委会，不要轻易转账或提供个人信息。
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        st.markdown("""
                        <div class="chat-bubble safe">
                            <strong>✅ 目前看起来挺安全的</strong><br>
                            我没有发现明显的诈骗关键词。<br>
                            💡 不过还是要记住：<strong>不轻信、不转账、不透露验证码</strong>，遇到拿不准的就问家人！
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.info("📝 请先输入或粘贴您要检测的内容")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_d2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📖 村里发生过的真实案例")
            case = random.choice(CASES)
            st.markdown(f"""
            <div style="background:rgba(255,248,240,0.5);border-radius:18px;padding:16px 20px;border:1px solid #F0E4D8;margin:8px 0;">
                <div style="font-size:22px;font-weight:700;color:#C4906A;">{case['title']}</div>
                <div style="font-size:20px;color:#3D2C1E;margin-top:4px;">{case['desc']}</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("🔄 换一个故事", key="refresh_case"):
                st.rerun()
            st.markdown("""
            <div style="margin-top:12px;padding:12px 16px;background:#E8F5E9;border-radius:16px;">
                <p style="font-size:18px;margin:0;">📞 <strong>反诈预警专线：96110</strong></p>
                <p style="font-size:16px;color:#4A6A4A;margin:4px 0 0 0;">这个电话一定要接！</p>
            </div>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ---- Tab 2: 养老记账 ----
    with tab2:
        col_a1, col_a2 = st.columns([1, 1], gap="large")
        with col_a1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 💰 记一笔")
            st.markdown(f"""
            <div style="background:linear-gradient(145deg,#4A3728,#5A4A3A);color:white;border-radius:24px;padding:14px 20px;text-align:center;margin:8px 0 16px 0;">
                <span style="font-size:20px;color:white;">💰 当前总资产</span><br>
                <span style="font-size:44px;font-weight:700;color:white;">¥{balance:,.2f}</span>
            </div>
            """, unsafe_allow_html=True)
            with st.form(key="acc_form", clear_on_submit=True):
                ca, ct = st.columns(2)
                with ca:
                    amount = st.number_input("金额", min_value=0.01, step=1.0, format="%.2f", key="amt")
                with ct:
                    ttype = st.selectbox("类型", ["收入", "支出"], key="tt")
                desc = st.text_input("用途", placeholder="买菜 / 养老金 / 买药", key="desc")
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
                        # 获得记账积分
                        profile['points'] = profile.get('points', 0) + 1
                        save_profile(profile)
                        st.success("✅ 记录保存成功！ +1 积分")
                        st.rerun()
                    else:
                        st.warning("请填写完整信息")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_a2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 📋 最近收支")
            if records:
                today = datetime.now().strftime("%m-%d")
                today_in = sum(r["amount"] for r in records if r["type"] == "收入" and r["date"].startswith(today))
                today_out = sum(r["amount"] for r in records if r["type"] == "支出" and r["date"].startswith(today))
                st.markdown(f"""
                <div style="display:flex;gap:12px;margin:8px 0 16px 0;">
                    <div style="flex:1;background:#E8F5E9;border-radius:18px;padding:10px;text-align:center;">
                        <span style="font-size:18px;">📈 今日收入</span><br>
                        <span style="font-size:30px;font-weight:bold;color:#82BE96;">+¥{today_in:.0f}</span>
                    </div>
                    <div style="flex:1;background:#FDECEA;border-radius:18px;padding:10px;text-align:center;">
                        <span style="font-size:18px;">📉 今日支出</span><br>
                        <span style="font-size:30px;font-weight:bold;color:#D97070;">-¥{today_out:.0f}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                st.markdown("**最近3笔**")
                for r in records[-3:][::-1]:
                    icon = "📈" if r["type"] == "收入" else "📉"
                    color = "#82BE96" if r["type"] == "收入" else "#D97070"
                    st.markdown(f"""
                    <div style="background:rgba(255,252,248,0.5);border-radius:14px;padding:10px 16px;margin:4px 0;border:1px solid #F0E8E0;">
                        <span style="font-weight:bold;color:{color};font-size:20px;">{icon} {r['type']}</span>
                        <span style="font-weight:bold;font-size:20px;">¥{r['amount']:.2f}</span>
                        <span style="color:#5A4A3A;margin-left:8px;font-size:19px;">{r['desc']}</span>
                        <span style="float:right;color:#8A7A6A;font-size:18px;">{r['date']}</span>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("📭 暂无记录，开始记账吧！")
            st.markdown('</div>', unsafe_allow_html=True)

    # ---- Tab 3: 紧急求助 ----
    with tab3:
        col_h1, col_h2 = st.columns([1, 1], gap="large")
        with col_h1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 🆘 一键求助")
            st.markdown("""
            <div style="background:#FDF2E9;padding:16px 20px;border-radius:20px;border:2px solid #E8A87C;margin-bottom:16px;text-align:center;">
                <p style="font-size:24px;font-weight:700;color:#6A4A2A;margin:0;">🚨 遇到可疑情况，<br>请立即停止操作！</p>
            </div>
            """, unsafe_allow_html=True)
            if st.button("📞 拨打 110 报警", key="c110", use_container_width=True):
                generate_speech("请立即拨打110报警", rate=0.9)
                st.success("✅ 已提醒：请立即拨打 110！")
            if st.button("👨‍👩‍👦 联系子女 / 家人", key="cf", use_container_width=True):
                generate_speech("请立即联系您的子女或家人", rate=0.9)
                st.info("📱 建议立即给子女打电话！")
            if st.button("🏘️ 联系村委会", key="cv", use_container_width=True):
                generate_speech("请立即联系村委会或社区工作人员", rate=0.9)
                st.info("🏛️ 联系村干部，他们会帮您！")
            st.markdown('</div>', unsafe_allow_html=True)

        with col_h2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown("#### 👨‍👩‍👧‍👦 亲情连线")
            st.markdown("""
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
                <div class="family-card">
                    <span class="avatar">👨</span>
                    <div class="name">张小明</div>
                    <div class="relation">儿子</div>
                    <div style="font-size:16px;color:#7A6A5A;margin-top:4px;">📞 138****1234</div>
                </div>
                <div class="family-card">
                    <span class="avatar">👩</span>
                    <div class="name">李小芳</div>
                    <div class="relation">女儿</div>
                    <div style="font-size:16px;color:#7A6A5A;margin-top:4px;">📞 139****5678</div>
                </div>
                <div class="family-card">
                    <span class="avatar">👴</span>
                    <div class="name">王村长</div>
                    <div class="relation">村主任</div>
                    <div style="font-size:16px;color:#7A6A5A;margin-top:4px;">📞 137****9012</div>
                </div>
                <div class="family-card">
                    <span class="avatar">👩‍⚕️</span>
                    <div class="name">李医生</div>
                    <div class="relation">村医</div>
                    <div style="font-size:16px;color:#7A6A5A;margin-top:4px;">📞 136****3456</div>
                </div>
            </div>
            <p style="font-size:17px;color:#7A6A5A;margin-top:12px;text-align:center;">
                💡 建议把家人电话存在手机通讯录，方便一键拨打
            </p>
            """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # ---- Tab 4: 防骗闯关（含风险模拟器） ----
    with tab4:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🧠 防骗闯关 · 问答 + 模拟场景")
        # 子tab
        sub_tab1, sub_tab2 = st.tabs(["📝 反诈小测验", "🎭 风险模拟器"])
        with sub_tab1:
            if "quiz_idx" not in st.session_state:
                st.session_state.quiz_idx = 0
                st.session_state.quiz_answered = False
                st.session_state.quiz_selected = None

            quiz = QUIZZES[st.session_state.quiz_idx]
            st.markdown(f'<p style="font-size:20px;font-weight:600;">第 {st.session_state.quiz_idx+1} / {len(QUIZZES)} 题</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:22px;">{quiz["q"]}</p>', unsafe_allow_html=True)

            for i, opt in enumerate(quiz["options"]):
                label = f"{chr(65+i)}. {opt}"
                if st.button(label, key=f"quiz_{i}"):
                    st.session_state.quiz_selected = i
                    st.session_state.quiz_answered = True

            if st.session_state.quiz_answered:
                selected = st.session_state.quiz_selected
                correct = quiz["correct"]
                if selected == correct:
                    st.success("🎉 回答正确！" + quiz["explain"])
                    # 积分增加
                    profile['points'] = profile.get('points', 0) + 3
                    profile['quiz_completed'] = profile.get('quiz_completed', 0) + 1
                    save_profile(profile)
                else:
                    st.error("😅 再想想看。" + quiz["explain"])

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

        with sub_tab2:
            if "sim_idx" not in st.session_state:
                st.session_state.sim_idx = 0
                st.session_state.sim_answered = False
                st.session_state.sim_selected = None

            sim = SIMULATIONS[st.session_state.sim_idx]
            st.markdown(f'<p style="font-size:20px;font-weight:600;">🎭 场景 {st.session_state.sim_idx+1} / {len(SIMULATIONS)}</p>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size:22px;background:#F5ECE4;padding:16px;border-radius:20px;">{sim["scene"]}</p>', unsafe_allow_html=True)

            for i, opt in enumerate(sim["options"]):
                label = f"{chr(65+i)}. {opt}"
                if st.button(label, key=f"sim_{i}"):
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
                    st.error("❌ 这样可能会有危险。" + sim["explain"])

            col_sn, col_sr = st.columns(2)
            with col_sn:
                if st.button("⬅️ 上一个场景"):
                    st.session_state.sim_idx = (st.session_state.sim_idx - 1) % len(SIMULATIONS)
                    st.session_state.sim_answered = False
                    st.session_state.sim_selected = None
                    st.rerun()
            with col_sr:
                if st.button("下一个场景 ➡️"):
                    st.session_state.sim_idx = (st.session_state.sim_idx + 1) % len(SIMULATIONS)
                    st.session_state.sim_answered = False
                    st.session_state.sim_selected = None
                    st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    # ---- Tab 5: 我的守护 ----
    with tab5:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("#### 🏅 我的守护成绩单")
        col_s1, col_s2, col_s3 = st.columns(3)
        with col_s1:
            st.markdown(f"""
            <div style="text-align:center;padding:16px;background:#F5ECE4;border-radius:20px;">
                <div style="font-size:48px;">📅</div>
                <div style="font-size:36px;font-weight:700;color:#D4A574;">{profile.get('checkin_days', 0)}</div>
                <div style="font-size:20px;">累计签到（天）</div>
            </div>
            """, unsafe_allow_html=True)
        with col_s2:
            st.markdown(f"""
            <div style="text-align:center;padding:16px;background:#F5ECE4;border-radius:20px;">
                <div style="font-size:48px;">🧠</div>
                <div style="font-size:36px;font-weight:700;color:#82BE96;">{profile.get('quiz_completed', 0)}</div>
                <div style="font-size:20px;">完成测验（道）</div>
            </div>
            """, unsafe_allow_html=True)
        with col_s3:
            st.markdown(f"""
            <div style="text-align:center;padding:16px;background:#F5ECE4;border-radius:20px;">
                <div style="font-size:48px;">🛡️</div>
                <div style="font-size:36px;font-weight:700;color:#D97070;">{profile.get('risk_detected', 0)}</div>
                <div style="font-size:20px;">识别风险（次）</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("#### 🎖️ 已获得的徽章")
        badges = []
        if profile.get('checkin_days', 0) >= 7:
            badges.append("🌟 坚持之星（签到7天）")
        if profile.get('quiz_completed', 0) >= 3:
            badges.append("🧠 反诈达人（完成3道测验）")
        if profile.get('risk_detected', 0) >= 5:
            badges.append("🛡️ 守护卫士（识别5次风险）")
        if profile.get('points', 0) >= 30:
            badges.append("🏅 积分达人（累计30分）")
        if badges:
            for b in badges:
                st.markdown(f'<span class="badge badge-gold">{b}</span>', unsafe_allow_html=True)
        else:
            st.info("继续努力，解锁更多徽章！")
        st.markdown('</div>', unsafe_allow_html=True)

    # ====== 📊 数据看板（全屏） ======
    st.markdown("---")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 📊 守护数据看板")
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        st.markdown(f'<p style="text-align:center;"><span style="font-size:38px;font-weight:700;color:#D4A574;">{len(records)}</span><br><span style="font-size:18px;color:#6A5A4A;">📝 总笔数</span></p>', unsafe_allow_html=True)
    with col_s2:
        total_in = sum(r["amount"] for r in records if r["type"] == "收入")
        st.markdown(f'<p style="text-align:center;"><span style="font-size:38px;font-weight:700;color:#82BE96;">¥{total_in:,.0f}</span><br><span style="font-size:18px;color:#6A5A4A;">📈 总收入</span></p>', unsafe_allow_html=True)
    with col_s3:
        total_out = sum(r["amount"] for r in records if r["type"] == "支出")
        st.markdown(f'<p style="text-align:center;"><span style="font-size:38px;font-weight:700;color:#D97070;">¥{total_out:,.0f}</span><br><span style="font-size:18px;color:#6A5A4A;">📉 总支出</span></p>', unsafe_allow_html=True)
    with col_s4:
        st.markdown(f'<p style="text-align:center;"><span style="font-size:38px;font-weight:700;color:#E8A87C;">{len(records)}</span><br><span style="font-size:18px;color:#6A5A4A;">📅 守护天数</span></p>', unsafe_allow_html=True)

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
                fig = px.line(df, x="日期", y="金额", title="📈 收支趋势", labels={"金额": "元"}, height=250)
                fig.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_size=16, showlegend=False)
                fig.update_traces(line_color="#D4A574", line_width=3)
                st.plotly_chart(fig, use_container_width=True)
        except Exception:
            pass
    st.markdown('</div>', unsafe_allow_html=True)

    # ====== 📚 防骗知识库 ======
    st.markdown("---")
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("#### 📚 防骗知识库（点击展开学习）")
    for q, a in KNOWLEDGE.items():
        with st.expander(q):
            st.markdown(f'<p style="font-size:20px;color:#3D2C1E;">{a}</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # ====== 语音快捷助手 ======
    st.markdown("---")
    col_voice1, col_voice2, col_voice3 = st.columns(3)
    with col_voice1:
        if st.button("🔊 播放每日防骗提醒", use_container_width=True):
            tips = random.choice([
                "不轻信陌生来电，不透露验证码，不向陌生人转账。",
                "公检法机关不会通过电话办案，更不会设立安全账户。",
                "天上不会掉馅饼，高回报投资都是骗局。",
                "遇到拿不准的事情，先问问子女或村干部。",
                "96110 是反诈预警专线，请放心接听。"
            ])
            generate_speech(tips, rate=0.9)
            st.success("✅ 已播放提醒")
    with col_voice2:
        if st.button("📣 快速报告可疑情况", use_container_width=True):
            generate_speech("请立即拨打110报警，或者联系村委会。", rate=0.9)
            st.info("已提醒报警或联系村委会")
    with col_voice3:
        if st.button("🔄 刷新页面", use_container_width=True):
            st.rerun()

    # ====== 底部 ======
    st.markdown("""
    <div class="footer">
        <p style="font-size:18px;color:#8A7A6A;">🏡 银乡智护 · 农村老年金融反诈公益项目</p>
        <p style="font-size:16px;color:#A09080;">❤️ 完全免费 · 无需注册 · 守护乡村养老钱</p>
        <p style="font-size:15px;color:#B0A090;">🔒 所有数据仅保存在本地，不会上传至任何服务器</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()