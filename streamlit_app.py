import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Email Merger Tool", layout="centered")

st.title("📧 Restaurant Email Merger Tool (Cleaned)")
st.write("""
Upload two files:
- **File 1**: Restaurant data with `Website` and optional `Email`
- **File 2**: URL list with `Url` and `Email`

This app will merge by URL, fill in missing emails, **remove rows without email**, and let you download the clean data.
""")

# File uploaders
file1 = st.file_uploader("📂 Upload the restaurant file (Website + Email)", type=["csv", "xls", "xlsx"])
file2 = st.file_uploader("📂 Upload the URL + Email file", type=["csv", "xls", "xlsx"])

def read_file(uploaded_file):
    if uploaded_file.name.endswith('.csv'):
        return pd.read_csv(uploaded_file)
    else:
        return pd.read_excel(uploaded_file)

if file1 and file2:
    try:
        df1 = read_file(file1)
        df2 = read_file(file2)

        # Validation
        if 'Website' not in df1.columns:
            st.error("❌ File 1 must contain a 'Website' column.")
        elif 'Url' not in df2.columns or 'Email' not in df2.columns:
            st.error("❌ File 2 must contain both 'Url' and 'Email' columns.")
        else:
            # Normalize URLs
            df1['Website'] = df1['Website'].astype(str).str.strip().str.lower()
            df2['Url'] = df2['Url'].astype(str).str.strip().str.lower()

            # Merge and fill missing emails
            merged = pd.merge(
                df1,
                df2[['Url', 'Email']],
                left_on='Website',
                right_on='Url',
                how='left',
                suffixes=('', '_from_file2')
            )

            merged['Email'] = merged.apply(
                lambda row: row['Email_from_file2'] if pd.isna(row['Email']) or row['Email'].strip() == '' else row['Email'],
                axis=1
            )

            merged.drop(columns=['Url', 'Email_from_file2'], inplace=True)

            # Remove rows without valid email
            cleaned = merged[merged['Email'].notna() & merged['Email'].str.strip().ne("")]
            cleaned.reset_index(drop=True, inplace=True)

            st.success(f"✅ Done! Valid emails remaining: {len(cleaned)}")
            st.dataframe(cleaned.head(20))

            # Downloadable CSV
            def to_csv_bytes(df):
                output = BytesIO()
                df.to_csv(output, index=False)
                output.seek(0)
                return output

            st.download_button(
                label="📥 Download Cleaned CSV (With Emails Only)",
                data=to_csv_bytes(cleaned),
                file_name="cleaned_restaurant_emails.csv",
                mime="text/csv"
            )
    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("⬆️ Please upload both files to begin.")
