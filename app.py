import pandas as pd
import matplotlib as plt
import seaborn as sns
from datetime import datetime
import streamlit as st

# 设置页面
st.set_page_config(page_title="月光族记账本", page_icon="💰", layout="wide")

# 初始化数据
if 'transactions' not in st.session_state:
    st.session_state.transactions = pd.DataFrame(columns=[
        '日期', '金额', '类别', '支付方式', '备注'
    ])


# 月光分析函数
def analyze_moonlight(is_finance, is_accounting, age, gender, major):
    def classification_advice():
        if not is_accounting and not is_finance:
            return "非必要消费（特别是娱乐和服饰类）"
        elif is_accounting and not is_finance:
            return "理财工具的使用（如货币基金）"
        else:
            return "消费结构的优化（必要/非必要支出比）"

    conclusion = f"""
    ### 月光行为分析报告（基于您的画像）
    - **基本特征**：{age}岁 {gender}性 {major}专业
    - **财务习惯**：{'有' if is_finance else '无'}理财 | {'有' if is_accounting else '无'}记账

    📊 **研究发现**：
    1. 您的月光风险主要与{'理财习惯' if is_finance else '消费结构'}相关
    2. {'记账' if is_accounting else '不记账'}会使月光概率{'降低30%' if is_accounting else '增加45%'}
    3. 建议关注{classification_advice()}
    """
    st.sidebar.markdown(conclusion)


# 侧边栏 - 用户信息
with st.sidebar:
    st.header("用户画像")
    gender = st.radio("性别", ('男', '女', '其他'))
    age = st.slider("年龄", 18, 40, 20)
    major = st.selectbox("专业", ('理工', '文史', '经管', '艺术', '其他'))

    st.divider()
    is_finance = st.checkbox("是否理财")
    is_accounting = st.checkbox("是否记账")

    if st.button("生成月光分析报告"):
        analyze_moonlight(is_finance, is_accounting, age, gender, major)

    # 显示总消费
    if not st.session_state.transactions.empty:
        total_spending = st.session_state.transactions['金额'].sum()
        st.metric("总消费", f"¥{total_spending:.2f}")

# 主界面
st.title("💰 月光族记账本")
st.caption("研究显示：月光现象与理财/记账习惯相关性高于人口统计学因素")

# 记账表单
with st.form("记账表单", clear_on_submit=True):
    cols = st.columns(3)
    with cols[0]:
        date = st.date_input("日期", datetime.now())
    with cols[1]:
        amount = st.number_input("金额", min_value=0.0, step=0.01, value=0.0)
    with cols[2]:
        category = st.selectbox("类别", (
            '餐饮', '服饰', '娱乐', '交通', '学习', '住宿', '医疗', '其他'
        ))

    cols = st.columns(2)
    with cols[0]:
        payment = st.selectbox("支付方式", ('支付宝', '微信', '现金', '银行卡'))
    with cols[1]:
        note = st.text_input("备注")

    if st.form_submit_button("添加记录"):
        if amount <= 0:
            st.error("金额必须大于零！")
        else:
            new_record = pd.DataFrame([[
                date, amount, category, payment, note
            ]], columns=st.session_state.transactions.columns)
            st.session_state.transactions = pd.concat(
                [st.session_state.transactions, new_record],
                ignore_index=True
            )
            st.success("记录已添加！")

# 显示数据表
if not st.session_state.transactions.empty:
    st.subheader("消费记录")
    st.dataframe(
        st.session_state.transactions.sort_values('日期', ascending=False),
        hide_index=True,
        use_container_width=True
    )

    # 消费分析
    st.subheader("消费分析")
    tab1, tab2, tab3 = st.tabs(["趋势分析", "类别分析", "月光预测"])

    with tab1:
        fig, ax = plt.subplots()
        daily_spending = st.session_state.transactions.groupby('日期')['金额'].sum()
        sns.lineplot(data=daily_spending, ax=ax)
        ax.set_title("每日消费趋势")
        st.pyplot(fig)
        plt.close(fig)  # 释放内存

    with tab2:
        col1, col2 = st.columns(2)
        with col1:
            st.write("#### 消费类别占比")
            category_sum = st.session_state.transactions.groupby('类别')['金额'].sum()
            st.dataframe(category_sum.sort_values(ascending=False))

        with col2:
            fig, ax = plt.subplots()
            category_sum.plot.pie(autopct="%.1f%%", ax=ax)
            st.pyplot(fig)
            plt.close(fig)

    with tab3:
        st.warning("正在开发中...")
        st.write("基于您的研究数据，将预测月光概率")

# 数据导出
if not st.session_state.transactions.empty:
    st.download_button(
        label="导出消费记录",
        data=st.session_state.transactions.to_csv(index=False).encode('utf-8'),
        file_name=f"消费记录_{datetime.now().strftime('%Y%m%d')}.csv",
        mime="text/csv"
    )