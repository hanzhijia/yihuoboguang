import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ==========================================
# 1. 页面基本配置 (必须放在第一行)
# ==========================================
st.set_page_config(
    page_title="艺火玻光", 
    page_icon="🎨", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# ==========================================
# 2. 注入自定义 CSS 样式
# ==========================================
st.markdown("""
<style>
/* 整个页面的极浅青色/薄荷蓝渐变背景 (对标参考图) */
.stApp {
    background-color: #e0f2f1; /* 极浅的青绿色底色 */
    background-image: 
        radial-gradient(circle at 85% 60%, rgba(128, 203, 196, 0.4) 0%, transparent 50%), /* 右上柔和青蓝发光 */
        radial-gradient(circle at 15% 40%, rgba(178, 223, 219, 0.5) 0%, transparent 50%), /* 左下极浅薄荷发光 */
        linear-gradient(rgba(0, 105, 92, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 105, 92, 0.03) 1px, transparent 1px);
    background-size: 100% 100%, 100% 100%, 40px 40px, 40px 40px;
    color: #263238; /* 调整为更中性的深蓝灰，以适应更浅的背景 */
}

/* --- 隐藏顶部默认空白和 Header，使页面更像全屏 App --- */
header { visibility: hidden; }
.block-container {
    padding-top: 5rem;
    max-width: 1200px;
}

/* --- 文字组件样式 --- */
.pill-tag {
    display: inline-block;
    border: 1px solid #00897b;
    color: #00897b;
    border-radius: 20px;
    padding: 8px 24px;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 2px;
    margin-bottom: 30px;
    background-color: rgba(255, 255, 255, 0.4); /* 标签底色改白提亮 */
}

.main-title {
    font-size: 5rem;
    font-weight: 900;
    color: #004d40;
    background: -webkit-linear-gradient(0deg, #004d40, #00897b);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 30px;
    line-height: 1.1;
    letter-spacing: -1px;
}

.desc-text {
    font-size: 1.15rem;
    color: #37474f; /* 恢复为更易读的深灰蓝 */
    line-height: 1.9;
    max-width: 900px;
    margin-bottom: 40px;
}

/* --- 适配基础组件颜色 (文本框、选择框等，提亮去绿) --- */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background-color: rgba(255, 255, 255, 0.5) !important; /* 更白的输入框底色 */
    color: #263238 !important;
    border: 1px solid #b2dfdb !important; /* 极浅的青蓝边框 */
}

/* 将所有 Markdown 文本、标签调整为深色以保证在极浅背景上的对比度 */
.stMarkdown, .stText, p, span, label, h1, h2, h3, h4, h5, h6 {
    color: #263238 !important;
}

/* 覆盖刚才强制修改的主标题和副标题颜色 */
.stMarkdown h3 {
    color: #00695c !important;
}
.main-title {
    color: transparent !important; /* 保留渐变效果 */
}
.pill-tag {
    color: #00897b !important;
}

/* --- 项目简介模块定制样式 --- */
.intro-section {
    text-align: center;
    margin-top: 60px;
    margin-bottom: 50px;
}
.intro-subtitle {
    color: #00897b;
    font-size: 0.9rem;
    font-weight: 800;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-bottom: 10px;
}
.intro-maintitle {
    color: #004d40;
    font-size: 2.8rem;
    font-weight: 900;
    margin-bottom: 20px;
}
.intro-desc {
    color: #37474f;
    font-size: 1.1rem;
    line-height: 1.8;
    max-width: 900px;
    margin: 0 auto 40px auto;
}

/* 六宫格卡片样式 */
.grid-card {
    background-color: rgba(255, 255, 255, 0.6);
    border: 1px solid rgba(0, 150, 136, 0.15);
    border-radius: 20px;
    padding: 35px 25px;
    text-align: left;
    height: 100%;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(0, 105, 92, 0.03);
    backdrop-filter: blur(5px);
}
.grid-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 12px 25px rgba(0, 105, 92, 0.1);
    background-color: rgba(255, 255, 255, 0.8);
    border-color: rgba(0, 150, 136, 0.3);
}
.card-icon {
    font-size: 2.5rem;
    margin-bottom: 20px;
}
.card-title {
    color: #00695c;
    font-size: 1.3rem;
    font-weight: 800;
    margin-bottom: 15px;
}
.card-text {
    color: #455a64;
    font-size: 0.95rem;
    line-height: 1.7;
}

/* --- 痛点分析模块样式 --- */
.pain-card {
    background-color: rgba(255, 255, 255, 0.6);
    border-top: 4px solid #f48fb1; /* 柔和的浅红/粉色，不打破整体浅色调 */
    border-radius: 15px;
    padding: 25px;
    height: 100%;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
    backdrop-filter: blur(5px);
}
.pain-title {
    color: #d81b60;
    font-weight: 800;
    font-size: 1.15rem;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.pain-text {
    color: #546e7a;
    font-size: 0.95rem;
    line-height: 1.6;
}

/* --- 路线图 (Roadmap) 样式 --- */
.roadmap-container {
    position: relative;
    padding-left: 30px;
    margin-top: 20px;
}
.roadmap-container::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 2px;
    background: rgba(0, 137, 123, 0.3);
}
.roadmap-item {
    position: relative;
    margin-bottom: 30px;
}
.roadmap-item::before {
    content: '';
    position: absolute;
    left: -35px;
    top: 5px;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #00897b;
    border: 3px solid #e0f2f1;
}
.roadmap-date {
    font-weight: 800;
    color: #00695c;
    margin-bottom: 5px;
}
.roadmap-content {
    background: rgba(255, 255, 255, 0.5);
    padding: 15px 20px;
    border-radius: 12px;
    border: 1px solid rgba(0, 150, 136, 0.15);
}

/* --- 按钮自定义样式 --- */
div.stButton > button {
    border-radius: 12px !important;
    padding: 0.6rem 1.5rem !important;
    font-weight: 600 !important;
    border: 1px solid #80cbc4 !important;
    background-color: rgba(255, 255, 255, 0.5) !important; /* 提亮普通按钮 */
    color: #00695c !important;
    transition: all 0.3s ease !important;
}
div.stButton > button:hover {
    background-color: #00695c !important;
    color: white !important;
    box-shadow: 0 4px 12px rgba(0, 105, 92, 0.2) !important;
    border-color: #00695c !important;
}
div.stButton > button[kind="primary"] {
    background: linear-gradient(90deg, #26a69a, #00897b) !important;
    color: white !important;
    border: none !important;
    font-weight: 800 !important;
}
div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(90deg, #00897b, #00695c) !important;
    box-shadow: 0 6px 15px rgba(0, 105, 92, 0.3) !important;
    transform: translateY(-2px);
}

/* --- 三个 AI 模块的定制背景样式 (极浅色系，统一提亮) --- */
/* 模块 1: AI 废料智能配比 (晶莹剔透的玻璃质感，偏青绿色) */
div[data-testid="stVerticalBlock"]:has(#ai-module-marker) {
    background: url("https://images.unsplash.com/photo-1550859492-d5da9d8e45f3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80") no-repeat center center;
    background-size: cover;
    /* 遮罩颜色更白，降低绿色饱和度 */
    box-shadow: inset 0 0 0 2000px rgba(224, 242, 241, 0.90);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid rgba(0, 105, 92, 0.15);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

/* 模块 2: 情绪诊断疗愈 (童趣治愈感，极浅色调) */
div[data-testid="stVerticalBlock"]:has(#therapy-module-marker) {
    /* 使用带有童趣涂鸦/自然元素的矢量图案 */
    background: url("data:image/svg+xml,%3Csvg width='80' height='80' viewBox='0 0 80 80' xmlns='http://www.w3.org/2000/svg'%3E%3Cpath d='M10 20c-5.523 0-10 4.477-10 10s4.477 10 10 10 10-4.477 10-10-4.477-10-10-10zm0 18c-4.418 0-8-3.582-8-8s3.582-8 8-8 8 3.582 8 8-3.582 8-8 8zm50-18c-5.523 0-10 4.477-10 10s4.477 10 10 10 10-4.477 10-10-4.477-10-10-10zm0 18c-4.418 0-8-3.582-8-8s3.582-8 8-8 8 3.582 8 8-3.582 8-8 8zm-25 12c-5.523 0-10 4.477-10 10s4.477 10 10 10 10-4.477 10-10-4.477-10-10-10zm0 18c-4.418 0-8-3.582-8-8s3.582-8 8-8 8 3.582 8 8-3.582 8-8 8z' fill='%2300897b' fill-opacity='0.05' fill-rule='evenodd'/%3E%3C/svg%3E"), linear-gradient(135deg, rgba(232, 245, 233, 0.95) 0%, rgba(224, 242, 241, 0.95) 100%);
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0 8px 20px rgba(0, 105, 92, 0.05);
    border: 2px dashed rgba(0, 137, 123, 0.3); /* 改为青色虚线 */
    margin-bottom: 2rem;
}

/* 模块 3: 商业收益预估 (文创手工感，自然叶片生态纹理) */
div[data-testid="stVerticalBlock"]:has(#profit-module-marker) {
    /* 使用自然生态/绿叶的高清背景图来体现“废旧回收、环保文创” */
    background: url("https://images.unsplash.com/photo-1533038590840-1cbea6e54c86?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80") no-repeat center center;
    background-size: cover;
    /* 遮罩颜色更白更浅 */
    box-shadow: inset 0 0 0 2000px rgba(241, 248, 233, 0.93);
    border-radius: 20px;
    padding: 30px;
    border: 1px solid rgba(139, 195, 74, 0.3);
    margin-bottom: 2rem;
    position: relative;
}
</style>
""", unsafe_allow_html=True)

# ==========================================
# 3. 页面头部区域 (Hero Section)
# ==========================================

st.markdown('<div class="pill-tag">GREEN DESIGN · AI DATA · GLASS ART · QINGXI CREATION</div>', unsafe_allow_html=True)
st.markdown('<div class="main-title">艺火玻光</div>', unsafe_allow_html=True)

st.markdown('''
    <div class="desc-text">
        项目依托自研700℃低温电炉热熔工艺及AI智能配比系统，将废旧玻璃艺术化再生为公共装置、家居文创、美育课程及全龄段社会服务载体。面向青少年开展心理艺术疗愈，面向中年困难群体提供灵活就业培训，面向银龄群体开展认知疗愈服务。已累计无害化处理废玻璃3吨，落地艺术装置580余件，覆盖中小学美育课堂3800余人，初步实现环保、社会与商业价值的协同落地。
    </div>
''', unsafe_allow_html=True)

# 渲染按钮区 (利用 Streamlit 的 columns 布局实现同行排列)
col1, col2, col3, _ = st.columns([1.2, 1.2, 1.2, 6])
with col1:
    # 跳转到 AI 配比与烧制预测系统 (VR/核心技术演示)
    if st.button("进入低温热熔重生工厂 (VR)", type="primary", use_container_width=True):
        st.components.v1.html(
            """
            <script>
                window.parent.document.getElementById('ai').scrollIntoView({behavior: 'smooth'});
            </script>
            """, height=0
        )
with col2:
    # 跳转到商业收益预估仪 (数据库与转化价值)
    if st.button("查看商业收益预估模型", use_container_width=True):
        st.components.v1.html(
            """
            <script>
                window.parent.document.getElementById('profit').scrollIntoView({behavior: 'smooth'});
            </script>
            """, height=0
        )
with col3:
    # 跳转到情绪诊断系统
    if st.button("全龄段疗愈色彩匹配", use_container_width=True):
        st.components.v1.html(
            """
            <script>
                window.parent.document.getElementById('therapy').scrollIntoView({behavior: 'smooth'});
            </script>
            """, height=0
        )

# ==========================================
# 3.2 行业痛点分析 (提出问题)
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<h3 style="color: #00695c; font-weight: 800; margin-bottom: 20px;">🚨 亟待解决的社会与行业痛点</h3>', unsafe_allow_html=True)

pain_col1, pain_col2, pain_col3 = st.columns(3)
with pain_col1:
    st.markdown('''
    <div class="pain-card">
        <div class="pain-title"><span>⚠️</span> 环境痛点：废旧玻璃难降解</div>
        <div class="pain-text">城市每年产生大量废旧玻璃，自然降解需百万年。传统回收重熔温度高达1500℃，能耗极大，导致大量废料被直接填埋，严重破坏土壤与生态。</div>
    </div>
    ''', unsafe_allow_html=True)

with pain_col2:
    st.markdown('''
    <div class="pain-card">
        <div class="pain-title"><span>⚠️</span> 社会痛点：弱势群体缺关怀</div>
        <div class="pain-text">青少年面临升学压力与心理亚健康，老年阿尔茨海默症群体缺乏有效的认知干预手段，且中年困难群体亟需低门槛的灵活就业渠道。</div>
    </div>
    ''', unsafe_allow_html=True)

with pain_col3:
    st.markdown('''
    <div class="pain-card">
        <div class="pain-title"><span>⚠️</span> 产业痛点：艺术下沉门槛高</div>
        <div class="pain-text">传统玻璃艺术创作成本高昂且工艺复杂，缺乏面向大众普及的美育载体，难以将环保理念转化为具有市场化造血能力的文创产业。</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 3.5 星罗工坊 · 项目简介
# ==========================================
st.markdown('''
<div class="intro-section" id="intro">
    <div class="intro-subtitle">ABOUT US</div>
    <div class="intro-maintitle">星罗工坊 · 项目简介</div>
    <div class="intro-desc">
        “艺火玻光”项目由<strong>星罗工坊</strong>团队倾力打造，致力于解决废旧玻璃回收难题。我们创新结合700℃低温热熔工艺与AI智能配比技术，将城市废旧玻璃转化为具有高度艺术价值的环保文创产品。更重要的是，项目构建了“变废为宝”的社会服务闭环，为不同年龄段的群体提供专属的帮扶与疗愈。
    </div>
</div>
''', unsafe_allow_html=True)

# 使用 Streamlit 的 columns 布局实现六宫格 (分两行，每行三列)
intro_col1, intro_col2, intro_col3 = st.columns(3)

with intro_col1:
    st.markdown('''
    <div class="grid-card">
        <div class="card-icon">♻️</div>
        <div class="card-title">绿色低碳工艺</div>
        <div class="card-text">打破传统高温重熔的高能耗壁垒，自主研发700℃低温电炉热熔技术。无害化处理废旧玻璃，大幅降低碳排放，践行可持续发展理念。</div>
    </div>
    ''', unsafe_allow_html=True)

with intro_col2:
    st.markdown('''
    <div class="grid-card">
        <div class="card-icon">🧠</div>
        <div class="card-title">AI智能驱动</div>
        <div class="card-text">基于上万组熔融数据训练的AI模型，精准预测物理形变与色彩重组，自动匹配最优助熔剂配比与升温曲线，将报废率从35%降至8%。</div>
    </div>
    ''', unsafe_allow_html=True)

with intro_col3:
    st.markdown('''
    <div class="grid-card">
        <div class="card-icon">🌱</div>
        <div class="card-title">青少年心理疗愈</div>
        <div class="card-text">将玻璃艺术与心理色彩疗法结合，开发专属美育课程。在“破碎到重塑”的艺术创作中，帮助青少年释放压力，实现心灵疗愈与成长。</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
intro_col4, intro_col5, intro_col6 = st.columns(3)

with intro_col4:
    st.markdown('''
    <div class="grid-card">
        <div class="card-icon">🤝</div>
        <div class="card-title">中年灵活就业</div>
        <div class="card-text">面向中年困难群体提供常温UV胶转化工艺培训，零基础易上手。建立回收与文创制作网络，创造稳定的灵活就业岗位与商业收益。</div>
    </div>
    ''', unsafe_allow_html=True)

with intro_col5:
    st.markdown('''
    <div class="grid-card">
        <div class="card-icon">👵</div>
        <div class="card-title">银发认知干预</div>
        <div class="card-text">针对阿尔茨海默症等老年群体，设计安全无锐角的玻璃触觉感知课程。通过色彩刺激与动手协作，延缓认知衰退，提升晚年生活质量。</div>
    </div>
    ''', unsafe_allow_html=True)

with intro_col6:
    st.markdown('''
    <div class="grid-card">
        <div class="card-icon">🏆</div>
        <div class="card-title">社会商业协同</div>
        <div class="card-text">已累计处理废旧玻璃3吨，落地艺术装置580余件，覆盖中小学生3800人次。形成“技术研发-环保制造-社会服务”的完整闭环，实现价值共赢。</div>
    </div>
    ''', unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# 3.8 环保与社会效益数据大屏
# ==========================================
st.markdown('<div class="intro-section" style="margin-top: 30px; margin-bottom: 30px;"><div class="intro-maintitle" style="font-size: 2.2rem;">📊 环保与社会效益数据大屏</div></div>', unsafe_allow_html=True)

# 核心指标
dash_col1, dash_col2, dash_col3, dash_col4 = st.columns(4)
with dash_col1:
    st.metric(label="♻️ 累计无害化处理废玻璃", value="3,200 kg", delta="月新增 150 kg")
with dash_col2:
    st.metric(label="🌿 等效减少碳排放", value="1,850 kg", delta="优于传统工艺 42%")
with dash_col3:
    st.metric(label="👩‍🎨 覆盖美育与疗愈人次", value="3,800+", delta="包含青老群体")
with dash_col4:
    st.metric(label="🛍️ 落地转化艺术文创", value="580 余件", delta="帮扶就业 45 人")

st.markdown("<br>", unsafe_allow_html=True)

# 图表区
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    # 碳排放对比柱状图
    df_carbon = pd.DataFrame({
        "工艺类型": ["传统高温重熔 (1500℃)", "星罗低温热熔 (700℃)", "常温 UV 胶工艺"],
        "能耗/碳排放指数": [100, 58, 12]
    })
    fig1 = px.bar(df_carbon, x="工艺类型", y="能耗/碳排放指数", 
                  color="工艺类型", 
                  color_discrete_sequence=["#ffcc80", "#4db6ac", "#aed581"],
                  title="核心工艺能耗与碳排放对比")
    fig1.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", 
                       margin=dict(l=20, r=20, t=40, b=20),
                       font=dict(color="#263238"))
    st.plotly_chart(fig1, use_container_width=True)

with chart_col2:
    # 社会服务人群覆盖饼图
    df_people = pd.DataFrame({
        "服务群体": ["青少年美育/疗愈", "银发认知干预", "中年灵活就业", "社区公益普及"],
        "覆盖比例": [45, 25, 15, 15]
    })
    fig2 = px.pie(df_people, names="服务群体", values="覆盖比例", 
                  color="服务群体",
                  color_discrete_sequence=["#4dd0e1", "#80cbc4", "#c5e1a5", "#ffd54f"],
                  title="社会服务人群分布矩阵", hole=0.4)
    fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                       margin=dict(l=20, r=20, t=40, b=20),
                       font=dict(color="#263238"))
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

# ==========================================
# 4. AI 废料智能配比与烧制预测系统 (原有核心模块，调整到第一个)
# ==========================================
# 创建一个带边框的容器来包裹整个模块 (结合 CSS :has 伪类实现独立背景)
with st.container():
    st.markdown('<div id="ai-module-marker"></div>', unsafe_allow_html=True)
    st.markdown('<div id="ai"></div>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #00695c; margin-top: 0px;">🤖 AI 废料智能配比与烧制预测系统</h3>', unsafe_allow_html=True)
    st.markdown('<p class="desc-text" style="margin-bottom: 20px;">基于上万组不同成分的玻璃废料熔融数据训练。输入原材料参数，AI 自动匹配最优助熔剂配比与升温曲线，将产品报废率从 35% 降至 8%。</p>', unsafe_allow_html=True)

    # 上方排版：左侧为多模态输入（图片+文本），右侧为参数滑块
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown("**1. 废料多模态摄取**")
        uploaded_file = st.file_uploader("📸 上传废旧玻璃实物图 (分析杂色与成分)", type=["jpg", "jpeg", "png"])
        user_desc = st.text_area("📝 目标人群与工艺需求", placeholder="例如：面向老年阿尔茨海默症群体的疗愈课程，需要色彩柔和、边缘绝对圆润安全、无锐角...")
        
        if uploaded_file is not None:
            st.image(uploaded_file, caption="已上传的原材料", width=150)
            
    with col_right:
        st.markdown("**2. 基础物理参数**")
        glass_amount = st.number_input("⚖️ 玻璃原材料量 (克)", min_value=10, max_value=5000, value=200, step=50)
        glass_color = st.selectbox("🎨 主要颜色", ["透明", "海蓝", "翠绿", "琥珀", "混合幻彩", "曜黑"])
        temperature = st.slider("🔥 目标烧制温度 (°C)", min_value=600, max_value=1100, value=820, step=10)
        
    st.markdown("<br>", unsafe_allow_html=True)
    # 生成按钮
    predict_btn = st.button("🔮 运行 AI 多模态预测", type="primary", use_container_width=True)
    
    # 预测结果展示区
    if predict_btn:
        with st.spinner("AI 正在深度演算物理形变与色彩重组过程..."):
            import time
            time.sleep(1.5) # 模拟 AI 接口的请求延迟
            
            # --- 模拟 AI 生成的文本逻辑 ---
            # 形态预测
            state = ""
            if temperature < 700:
                state = "玻璃仅边缘稍微圆润，整体保持原有尖锐碎块形态，未完全融合。"
            elif 700 <= temperature < 800:
                state = "玻璃达到塔克熔（Tack Fuse）状态，碎块之间相互粘连，表面呈现波浪起伏的纹理，保留了强烈的立体感。"
            elif 800 <= temperature < 900:
                state = "玻璃达到全熔（Full Fuse）状态，原材料完全融合成一个平滑的整体。边缘圆润，表面如水面般平整。"
            else:
                state = "玻璃过度熔化，可能产生意外的气泡和边缘流淌扩散，厚度变薄，形态难以控制。"
            
            # 色彩预测
            color_effect = ""
            if glass_color == "混合幻彩":
                color_effect = "不同色彩的碎玻璃在高温下相互渗透，交界处呈现出迷人的渐变与拉丝效果，极具艺术张力。"
            elif glass_color == "透明":
                color_effect = "透光率极高，内部可能包裹少量细微的晶莹气泡，折射出纯净的光影效果。"
            else:
                color_effect = f"{glass_color}色的碎块在高温煅烧后色彩更加醇厚，呈现出宝石般的温润光泽。"
                
            # 组装多模态分析结果 (基于图片和文本)
            multimodal_analysis = ""
            if uploaded_file is not None or user_desc:
                multimodal_analysis = "\n*   **🔍 AI 多模态意图解析：**"
                if uploaded_file is not None:
                    multimodal_analysis += "\n    *   *材质视觉特征提取：* 识别出废料含有较高的金属氧化物杂质，建议在 700℃ 低温区间内适当延长保温时间，以提升透光率并保留天然肌理。"
                if user_desc:
                    multimodal_analysis += f"\n    *   *全龄段疗愈需求响应：* 针对您提到的“{user_desc}”，AI 已自动匹配【银龄认知干预】大纲，调整升温曲线确保成品无锐角边缘，安全性达标。"
            
            # 组装生成的 Markdown 文本报告
            report = f"""
### 📊 AI 工艺智能诊断报告
{multimodal_analysis}
*   **物理形态推演：** {state}
*   **光学重组效果：** {color_effect}
*   **低碳减排核算：** 本次 700℃ 低温工艺较传统高温熔炉节省能耗约 **42%**。使用 **{glass_amount}g** 废料，等效减少碳排放约 **{glass_amount * 0.6:.1f}g**。
*   **💡 专家投产提示：** {temperature}°C 为当前配比最佳区间，系统已生成对应的降温退火曲线下发至终端设备，预计成品率可达 **92%** 以上。
            """
            
            # --- 集成 AI 实时绘图接口 (Pollinations.ai) ---
            # 将中文颜色翻译为对应的英文提示词，以便 AI 更好地理解
            color_map = {
                "透明": "transparent clear", 
                "海蓝": "ocean blue", 
                "翠绿": "emerald green", 
                "琥珀": "amber", 
                "混合幻彩": "iridescent mixed colorful", 
                "曜黑": "obsidian black"
            }
            eng_color = color_map.get(glass_color, "colorful")
            
            import urllib.parse
            import requests
            
            # 稳定的关键词图库接口 (根据你选择的颜色提取对应色彩的玻璃艺术图片)
            image_url = f"https://loremflickr.com/800/400/glass,art,{eng_color.split()[0]}"
            
            st.success("✨ 预测演算完成！正在生成视觉效果图...")
            
            # 使用两列布局，左边文字，右边图片
            col_text, col_img = st.columns([1, 1.2])
            with col_text:
                st.info(report)
            with col_img:
                st.image(image_url, caption=f"效果演示图: {glass_color}玻璃 @ {temperature}°C", use_container_width=True)

st.markdown("---")

# ==========================================
# 模块 B: 银发/青少年心理状态与色彩映射系统 (对应痛点三 & 产品6)
# ==========================================
with st.container():
    st.markdown('<div id="therapy-module-marker"></div>', unsafe_allow_html=True)
    st.markdown('<div id="therapy"></div>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #00695c; margin-top: 0px;">🎨 情绪诊断与色彩疗愈映射系统</h3>', unsafe_allow_html=True)
    st.markdown('<p class="desc-text" style="margin-bottom: 20px;">基于心理学色彩疗法模型，通过简易情绪问卷分析当前心理状态，为银龄与青少年群体自动匹配专属的“千人千面”再生玻璃治愈色彩组合。</p>', unsafe_allow_html=True)

    col_t1, col_t2 = st.columns([1, 1])
    
    with col_t1:
        st.markdown("**1. 快速情绪问卷**")
        q1 = st.slider("近一周睡眠质量如何？", min_value=1, max_value=10, value=5, help="1为极差，10为极好")
        q2 = st.slider("今天感觉精力充沛吗？", min_value=1, max_value=10, value=5, help="1为疲惫，10为活力满满")
        q3 = st.selectbox("此刻你最想去的场景是？", ["安静的深海底", "阳光明媚的森林", "温暖的壁炉旁", "浩瀚的星空"])
        
        therapy_btn = st.button("🧠 运行 AI 情绪诊断", use_container_width=True)
        
    with col_t2:
        st.markdown("**2. AI 疗愈色彩处方**")
        if therapy_btn:
            # 简单的心情映射逻辑
            score = q1 + q2
            if score <= 8 or q3 == "温暖的壁炉旁":
                mood = "轻度疲惫 / 缺乏安全感"
                rec_color = "琥珀色 (Amber) + 暖橙"
                desc = "温暖的琥珀色有助于提升安全感，仿佛阳光包裹，适合缓解情绪低落与孤独感。"
                color_hex = "#FFC107"
            elif score >= 15 and q3 == "阳光明媚的森林":
                mood = "积极活跃 / 渴望成长"
                rec_color = "翠绿色 (Emerald Green)"
                desc = "翠绿色象征生命与活力，能够进一步激发内在的创造力与生机。"
                color_hex = "#4CAF50"
            else:
                mood = "轻度焦虑 / 精神紧绷"
                rec_color = "海蓝色 (Ocean Blue)"
                desc = "深邃的海蓝具有极佳的镇静效果，有助于平复过度活跃的神经，带来内心的宁静。"
                color_hex = "#2196F3"
                
            st.info(f"**当前心理状态评估**：{mood}")
            st.success(f"**推荐再生玻璃色彩**：{rec_color}")
            st.write(f"**疗愈机理**：{desc}")
            
            # 展示色块
            st.markdown(f'''
                <div style="background-color: {color_hex}; height: 80px; border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                    专属疗愈配方提取中...
                </div>
            ''', unsafe_allow_html=True)
        else:
            st.write("请在左侧完成问卷以生成疗愈配方...")

st.markdown("---")

# ==========================================
# 模块 C: “变废为宝”商业收益预估仪 (对应痛点四 & 中年灵活就业)
# ==========================================
with st.container():
    st.markdown('<div id="profit-module-marker"></div>', unsafe_allow_html=True)
    st.markdown('<div id="profit"></div>', unsafe_allow_html=True)
    st.markdown('<h3 style="color: #00695c; margin-top: 0px;">💰 “变废为宝”商业收益预估仪</h3>', unsafe_allow_html=True)
    st.markdown('<p class="desc-text" style="margin-bottom: 20px;">面向中年灵活就业群体，输入手头收集的废旧玻璃重量，一键测算可通过“常温 UV 胶工艺”转化的文创产品数量及预估市场收益。</p>', unsafe_allow_html=True)

    # 统一列宽比例为 [1, 1, 1] 等宽
    col_p1, col_p2, col_p3 = st.columns([1, 1, 1])
    
    with col_p1:
        st.markdown("**1. 废料输入**")
        raw_weight = st.number_input("📥 收集的废旧玻璃重量 (公斤)", min_value=0.5, max_value=100.0, value=5.0, step=0.5)
        
    with col_p2:
        st.markdown("**2. 产品转化**")
        # 假设 1 公斤 = 1000克。一个冰箱贴约耗材 25克，钥匙扣约耗材 15克
        fridge_magnet_count = int((raw_weight * 1000 * 0.6) / 25) # 60% 做冰箱贴
        keychain_count = int((raw_weight * 1000 * 0.4) / 15)      # 40% 做钥匙扣
        
        st.metric(label="可制作环保冰箱贴", value=f"{fridge_magnet_count} 个")
        st.metric(label="可制作艺术钥匙扣", value=f"{keychain_count} 个")
        
    with col_p3:
        st.markdown("**3. 收益测算**")
        # 市场定价假设：冰箱贴 15元/个，钥匙扣 9.9元/个
        revenue = fridge_magnet_count * 15 + keychain_count * 9.9
        # 扣除辅料成本 (UV胶、底托等约 20%)
        net_profit = revenue * 0.8
        
        st.metric(label="预估总营收", value=f"¥ {revenue:.2f}")
        st.metric(label="预估净收益 (扣除辅料)", value=f"¥ {net_profit:.2f}", delta="灵活就业帮扶成效")

st.markdown("---")

# ==========================================
# 5. 商业计划发展路线图 (Roadmap)
# ==========================================
st.markdown('<div class="intro-section" style="margin-top: 40px; margin-bottom: 20px;"><div class="intro-maintitle" style="font-size: 2.2rem;">🚀 商业计划发展路线图</div></div>', unsafe_allow_html=True)

col_road_left, col_road_right = st.columns([1, 5])
with col_road_right:
    st.markdown('''
    <div class="roadmap-container">
        <div class="roadmap-item">
            <div class="roadmap-date">第一阶段：技术突破与跑通闭环 (已完成)</div>
            <div class="roadmap-content">
                成功自研 700℃ 低温热熔工艺，打通 AI 配比大模型，完成首批 3 吨废旧玻璃的回收与无害化处理。在 5 所试点学校开展青少年心理色彩疗愈美育课。
            </div>
        </div>
        <div class="roadmap-item">
            <div class="roadmap-date">第二阶段：社会服务与商业化扩张 (进行中)</div>
            <div class="roadmap-content">
                联合社区街道，建立 20 个“星罗废玻璃回收点”与“灵活就业帮扶站”。面向中年群体提供 UV 胶工艺培训，拓展文创产品线上线下销售渠道，实现初步盈利。
            </div>
        </div>
        <div class="roadmap-item">
            <div class="roadmap-date">第三阶段：产业赋能与全龄段覆盖 (未来展望)</div>
            <div class="roadmap-content">
                打造区域级“零碳玻璃艺术体验中心”，全面铺开银发认知干预服务。将 AI 模型开放 API 接口赋能给更多环保文创企业，树立低碳艺术领域的标杆品牌。
            </div>
        </div>
    </div>
    ''', unsafe_allow_html=True)
with col_road_left:
    # 留白或放个插图
    st.markdown('<div style="text-align:center; font-size:4rem; margin-top:20px; color:rgba(0,137,123,0.3);">🛣️</div>', unsafe_allow_html=True)

st.markdown("<br><br><br><div style='text-align:center; color:#78909c; font-size:0.9rem;'>星罗工坊 © 2026 - 让每一片废玻璃都有温度</div>", unsafe_allow_html=True)
