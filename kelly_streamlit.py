import streamlit as st
import plotly.graph_objects as go

# 页面配置
st.set_page_config(
    page_title="凯利公式计算器",
    page_icon="📊",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 页面样式
st.markdown("""
<style>
    .metric-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        margin: 10px 0;
    }
    
    /* 移动端优化 */
    body {
        max-width: 100%;
    }
    
    .st-emotion-cache-z5fcl4 {
        padding: 1rem;
    }
    
    h1, h2, h3 {
        margin-top: 1rem;
        margin-bottom: 0.5rem;
    }
    
    /* 数字输入框响应式 */
    input[type="number"] {
        font-size: 16px;
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# 标题
st.markdown("# 📊 凯利公式仓位计算器")
st.markdown("---")

# 左右两列布局（移动端自动堆叠）
col1 = st.container()
col2 = st.container()

with col1:
    st.markdown("### 📝 输入参数")
    
    # 输入胜率
    win_rate_input = st.number_input(
        "胜率 (%)",
        min_value=0.0,
        max_value=100.0,
        value=55.0,
        step=1.0,
        help="例如：55 表示 55% 胜率"
    )
    p = win_rate_input / 100
    
    # 输入赔率
    payoff_ratio = st.number_input(
        "净赔率/盈亏比",
        min_value=0.1,
        value=2.0,
        step=0.1,
        help="例如：2 表示盈亏比为 2:1"
    )
    b = payoff_ratio

with col2:
    st.markdown("### 📊 计算结果")
    
    # 计算凯利比例
    q = 1 - p
    f_star = (b * p - q) / b
    half_kelly = f_star / 2
    
    # 显示结果
    if f_star > 0:
        # 正期望值
        st.success("✅ 正期望值 - 可以投资")
        
        st.metric("全凯利仓位", f"{f_star*100:.2f}%", delta="激进")
        st.metric("半凯利仓位 (推荐)", f"{half_kelly*100:.2f}%", delta="稳健")
        st.metric("期望增长率", f"{(b*p - q)*100:.2f}%", delta="每局期望")
    else:
        # 负期望值
        st.error("❌ 负期望值 - 请勿参与")
        st.warning(f"计算结果: {f_star*100:.2f}% (需要回避)")

st.markdown("---")

# 详细分析
st.markdown("### 📈 详细分析")

st.markdown(f"""
**当前参数：**
- 胜率：{p*100:.2f}%
- 赔率：{b}:1
- 败率：{q*100:.2f}%
""")

if f_star > 0:
    st.markdown(f"""
    **推荐方案：**
    - 🎯 全凯利：{f_star*100:.2f}%
    - 💡 半凯利：{half_kelly*100:.2f}%（更稳健）
    - 🛡️ 四分之一凯利：{(f_star/4)*100:.2f}%（超保守）
    """)
else:
    st.markdown(f"""
    **风险提示：**
    ⚠️ 此局胜率或赔率过低，长期必输。
    
    建议 **规避此交易**。
    """)

# 可视化图表
st.markdown("### 📉 仓位与胜率关系图")

# 创建不同胜率下的凯利比例曲线
win_rates = [i/100 for i in range(1, 100)]
kelly_values = [(b*wr - (1-wr))/b for wr in win_rates]
kelly_values_half = [k/2 for k in kelly_values]

fig = go.Figure()

# 添加全凯利曲线
fig.add_trace(go.Scatter(
    x=[w*100 for w in win_rates],
    y=[k*100 for k in kelly_values],
    mode='lines',
    name='全凯利',
    line=dict(color='#1f77b4', width=3)
))

# 添加半凯利曲线
fig.add_trace(go.Scatter(
    x=[w*100 for w in win_rates],
    y=[k*100 for k in kelly_values_half],
    mode='lines',
    name='半凯利 (推荐)',
    line=dict(color='#ff7f0e', width=3, dash='dash')
))

# 标记当前点
fig.add_trace(go.Scatter(
    x=[p*100],
    y=[f_star*100],
    mode='markers+text',
    name='当前胜率',
    marker=dict(size=12, color='red'),
    text=['当前'],
    textposition="top center"
))

# 零线
fig.add_hline(y=0, line_dash="dash", line_color="gray", 
              annotation_text="零期望值")

fig.update_layout(
    title=f"赔率 {b}:1 下的凯利比例曲线",
    xaxis_title="胜率 (%)",
    yaxis_title="建议仓位 (%)",
    hovermode='x unified',
    height=350,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# 说明文字
st.markdown("---")
st.markdown("""
### 📚 凯利公式说明

**公式：** $f^* = \\frac{bp - q}{b}$

其中：
- $p$ = 胜率
- $q$ = 败率 (1 - p)
- $b$ = 净赔率/盈亏比
- $f^*$ = 最优仓位比例

**建议：**
- ✅ **半凯利策略** 是最常见的实战方法，风险更低
- ✅ 当计算结果为负时，说明此交易期望值为负，应该回避
- ✅ 仓位比例不应超过全凯利的 50%

**注意：** 此计算器仅用于教育目的，实际投资决策请咨询专业人士。
""")
