import streamlit as st
import pandas as pd
import io
import base64
from datetime import datetime

st.set_page_config(page_title="📋 Clipboard to Canvas", layout="wide")
st.title("📋 Clipboard to Canvas")
st.markdown("Paste Excel-style data and export beautifully")

# --- Paste Data ---
data_input = st.text_area("📋 Paste your table data here (copied from Excel)", height=200)

if data_input:
    try:
        # Convert clipboard-like tabular data into DataFrame
        df = pd.read_csv(io.StringIO(data_input), sep="\t")
        st.success("✅ Data parsed successfully!")

        # Show styled table
        st.subheader("📊 Preview")
        st.dataframe(df.style.set_table_styles(
            [{'selector': 'thead th', 'props': [('background-color', '#f2f2f2'),
                                                ('color', '#333'),
                                                ('font-weight', 'bold')]}]
        ).highlight_max(axis=0), use_container_width=True)

        # --- Export buttons ---
        col1, col2 = st.columns(2)

        # Export to Excel
        with col1:
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            excel_data = output.getvalue()

            st.download_button(
                label="📥 Download as XLSX",
                data=excel_data,
                file_name=f"clipboard_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Export to PDF (as styled HTML table)
        with col2:
            html_table = df.to_html(index=False)
            html_str = f"""
                <html>
                    <head><meta charset='utf-8'></head>
                    <body><h2>Clipboard to Canvas Export</h2>{html_table}</body>
                </html>"""
            b64 = base64.b64encode(html_str.encode()).decode()
            href = f'data:text/html;base64,{b64}'
            st.markdown(f'<a href="{href}" download="clipboard_data.html" target="_blank">🖨️ Save as Printable HTML (PDF-ready)</a>', unsafe_allow_html=True)

        # --- Sharing links ---
        st.subheader("🔗 Share")
        st.markdown("Generate a message you can copy into apps:")
        share_text = f"Check out this formatted table I created with Clipboard to Canvas! 📋✨"

        whatsapp_link = f"https://wa.me/?text={share_text}"
        gmail_link = f"mailto:?subject=Shared Table&body={share_text}"
        chat_link = f"https://chat.google.com/?message={share_text}"

        st.markdown(f"[💬 WhatsApp]({whatsapp_link}) | [📧 Gmail]({gmail_link}) | [💻 Google Chat]({chat_link})")

    except Exception as e:
        st.error("❌ Failed to parse the data. Please ensure it's copied from Excel or a spreadsheet.")
        st.exception(e)
else:
    st.info("Paste your table data copied from Excel or Google Sheets.")
