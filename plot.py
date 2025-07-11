import pandas as pd                      # 資料處理
import plotly.graph_objects as go        # 繪圖軟體
import streamlit as st                   # 網頁互動式應用
import numpy as np                       # 數學函數

# 基本網頁設置
st.set_page_config(page_title="IV Curve Viewer", layout="centered")
st.title("📈 多檔案 I-V 曲線 疊圖（可選欄位）")

# 多檔案上傳
files = st.file_uploader("請上傳一或多個 .csv / .txt 檔案", type=["csv", "txt"], accept_multiple_files=True)

if files:
    try:
        all_columns = set()
        dfs = []
        for file in files:
            df = pd.read_csv(file)
            dfs.append((file.name, df))
            all_columns.update(df.columns)

        x_col = st.selectbox("請選擇 X 軸欄位", sorted(all_columns))
        y_col = st.selectbox("請選擇 Y 軸欄位", sorted(all_columns))

        apply_abs = st.checkbox("Y-axis (絕對值)")
        apply_log = st.checkbox("Y-axis (log scale)")

        fig = go.Figure()
        color_palette = ["blue", "red", "green", "orange", "purple", "brown", "black"]

        for i, (name, df) in enumerate(dfs):
            if x_col in df.columns and y_col in df.columns:
                y_data = pd.to_numeric(df[y_col], errors='coerce')  # 將欄位轉成數字，非數值設為 NaN

                if apply_abs:
                    y_data = np.abs(y_data)
                if apply_log:
                    A = np.abs(y_data)
                    B = A.replace(0, np.nan)
                    y_data = np.log10(B)

                fig.add_trace(go.Scatter(
                    x=df[x_col],
                    y=y_data,
                    mode='lines+markers',
                    name=name,
                    line=dict(color=color_palette[i % len(color_palette)]),
                    marker=dict(size=10),
                    hovertemplate=f'{name}<br>{x_col}: %{{x}}<br>{y_col}: %{{y}}<extra></extra>'
                ))
            else:
                st.warning(f"❗ 檔案 {name} 缺少欄位 {x_col} 或 {y_col}，已略過")

        yaxis_config = dict(title=y_col, title_font=dict(size=20), tickfont=dict(size=14))


        fig.update_layout(
            title="I-V Curve 疊圖比較（自選欄位）",
            xaxis=dict(title=x_col, title_font=dict(size=20), tickfont=dict(size=14)),
            yaxis=yaxis_config,
            legend=dict(x=0.01, y=0.99),
            template="plotly_white"
        )

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
else:
    st.info("請上傳一個或多個檔案來開始")
