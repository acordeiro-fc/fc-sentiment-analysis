# import streamlit as st
# import pandas as pd
# import numpy as np
# import plotly.express as px
# from collections import Counter

# from sentence_transformers import SentenceTransformer
# from sklearn.metrics.pairwise import cosine_similarity
# from sqlalchemy import create_engine
    
# st.set_page_config(page_title="Survey Feedback Dashboard", layout="wide")

import streamlit as st
from streamlit_google_auth import Authenticate

authenticator = Authenticate(
    secret_credentials_path=None,
    cookie_name="my_cookie",
    cookie_key=st.secrets["googleoauth"]["cookie_secret"],
    redirect_uri=st.secrets["auth"]["redirect_uri"],
    client_id=st.secrets["googleoauth"]["client_id"],
    client_secret=st.secrets["googleoauth"]["client_secret"],
)

authenticator.check_authentification()

if not st.session_state.get("connected"):
    authenticator.login()
    st.stop()

if st.session_state["email"] not in st.secrets["ALLOWED_EMAILS"]:
    st.error("Not authorized")
    st.stop()

# Your app here
st.write(f"Hello, {st.session_state['name']}")
# # else:
# # ─────────────────────────────
# # CUSTOM CSS
# # ─────────────────────────────
# YELLOW = "#fef3b3"
# BORDER = "#828281"
# TEXT = "#2E2E2E"

# st.markdown(
#     f"""
#     <style>
#     section[data-testid="stSidebar"] {{
#         background-color: {YELLOW} !important;
#     }}

#     section[data-testid="stSidebar"] img {{
#         padding: 12px 8px 18px 8px;
#         object-fit: contain;
#     }}

#     div[data-testid="stExpander"] {{
#         background-color: white !important;
#         border: 1.5px solid {BORDER} !important;
#         border-radius: 12px !important;
#         overflow: hidden !important;
#     }}

#     .streamlit-expanderHeader {{
#         background-color: white !important;
#         color: {TEXT} !important;
#         border-radius: 12px !important;
#     }}

#     section[data-testid="stSidebar"] button {{
#         background-color: white !important;
#         color: {TEXT} !important;
#         border: 1.5px solid {BORDER} !important;
#         border-radius: 12px !important;
#         font-weight: 500 !important;
#     }}

#     section[data-testid="stSidebar"] button[kind="primary"] {{
#         background-color: white !important;
#         color: {TEXT} !important;
#         border: 3px solid {TEXT} !important;
#         font-weight: 700 !important;
#     }}

#     div[data-baseweb="tag"],
#     span[data-baseweb="tag"] {{
#         background-color: {YELLOW} !important;
#         border: 1px solid {BORDER} !important;
#         color: {TEXT} !important;
#         border-radius: 8px !important;
#     }}

#     div[data-baseweb="tag"] *,
#     span[data-baseweb="tag"] * {{
#         color: {TEXT} !important;
#         fill: {TEXT} !important;
#     }}

#     div[data-baseweb="select"] > div {{
#         background-color: #F1F3F7 !important;
#         border-radius: 12px !important;
#     }}

#     div[data-testid="metric-container"] {{
#         background-color: white !important;
#         padding: 15px !important;
#         border-radius: 12px !important;
#         border: 1px solid {BORDER} !important;
#     }}
#     </style>
#     """,
#     unsafe_allow_html=True
# )

# # ─────────────────────────────
# # LOAD DATA
# # ─────────────────────────────

# @st.cache_resource
# def get_engine():
#     print(st.secrets["DATABASE_URL"])
#     return create_engine(st.secrets["DATABASE_URL"])


# @st.cache_data(ttl=300)
# def load_data():
#     engine = get_engine()

#     customer_df = pd.read_sql(
#         "SELECT * FROM customer_survey",
#         engine
#     )

#     newsletter_df = pd.read_sql(
#         "SELECT * FROM newsletter_survey",
#         engine
#     )

#     return customer_df, newsletter_df


# customer_df, newsletter_df = load_data()

# # ─────────────────────────────
# # LOAD MODEL
# # ─────────────────────────────
# @st.cache_resource
# def load_embedding_model():
#     return SentenceTransformer("multi-qa-mpnet-base-cos-v1")


# embed_model = load_embedding_model()


# @st.cache_data(show_spinner=False)
# def build_embeddings(texts):
#     return embed_model.encode(texts, show_progress_bar=False)


# # ─────────────────────────────
# # SESSION STATE
# # ─────────────────────────────
# if "survey_page" not in st.session_state:
#     st.session_state.survey_page = "Customer Survey"

# if "subpage" not in st.session_state:
#     st.session_state.subpage = "Overview"


# # ─────────────────────────────
# # SIDEBAR
# # ─────────────────────────────
# st.sidebar.image("logo.png", width=330)
# st.sidebar.title("Dashboard Menu")


# def nav_button(label, survey, page, key):
#     active = (
#         st.session_state.survey_page == survey
#         and st.session_state.subpage == page
#     )

#     if st.button(
#         label,
#         key=key,
#         use_container_width=True,
#         type="primary" if active else "secondary"
#     ):
#         st.session_state.survey_page = survey
#         st.session_state.subpage = page
#         st.rerun()


# with st.sidebar.expander("Customer Survey", expanded=True):
#     nav_button("Overview", "Customer Survey", "Overview", "customer_overview")
#     nav_button("Semantic Search", "Customer Survey", "Semantic Search", "customer_search")

# with st.sidebar.expander("Newsletter Survey", expanded=True):
#     nav_button("Overview", "Newsletter Survey", "Overview", "newsletter_overview")
#     nav_button("Semantic Search", "Newsletter Survey", "Semantic Search", "newsletter_search")


# survey_page = st.session_state.survey_page
# subpage = st.session_state.subpage

# # ─────────────────────────────
# # COLUMN SETTINGS
# # ─────────────────────────────
# if survey_page == "Customer Survey":
#     df = customer_df.copy()

#     TEXT_COL = "Are there any other things you'd wish to share with us?"
#     CLEAN_TEXT_COL = "clean_answer"
#     SENTIMENT_COL = "sentiment_category"
#     TOPIC_COL = "topic_label"
#     DATE_COL = "Submit Date (UTC)"
#     EMAIL_COL = "Email"

#     AGE_COL = "How old are you?"
#     INCOME_COL = "What is your gross income level per year"
#     WORK_COL = "What field do you work in?"
#     NATIONALITY_COL = "What is your nationality?"
#     NEWSLETTER_COL = "Are you currently subscribed to our newsletter?"

# else:
#     df = newsletter_df.copy()

#     DATE_COL = "Submit Date (UTC)"
#     EMAIL_COL = "Email"

#     newsletter_question = st.selectbox(
#         "Choose newsletter question",
#         [
#             "What topics would you like to see covered in our 2026 newsletters?",
#             "Are there any improvements you would suggest for our newsletters?"
#         ],
#         key=f"newsletter_question_{subpage}"
#     )

#     if newsletter_question == "What topics would you like to see covered in our 2026 newsletters?":
#         TEXT_COL = "Topics 2026 newsletter"
#         CLEAN_TEXT_COL = "clean_translated_1"
#         SENTIMENT_COL = "sentiment"
#         TOPIC_COL = "topic_label"
#     else:
#         TEXT_COL = "Are there any improvements you would suggest for our newsletter"
#         CLEAN_TEXT_COL = "clean_translated_2"
#         SENTIMENT_COL = "sentiment_2"
#         TOPIC_COL = "topic_label_2"


# if CLEAN_TEXT_COL not in df.columns:
#     df[CLEAN_TEXT_COL] = df[TEXT_COL]

# # ─────────────────────────────
# # PREPARE DATA
# # ─────────────────────────────
# df[DATE_COL] = pd.to_datetime(df[DATE_COL], errors="coerce")
# df["month"] = df[DATE_COL].dt.to_period("M").astype(str)

# df[TEXT_COL] = df[TEXT_COL].fillna("").astype(str)
# df[CLEAN_TEXT_COL] = df[CLEAN_TEXT_COL].fillna("").astype(str)
# df[SENTIMENT_COL] = df[SENTIMENT_COL].fillna("Unknown").astype(str)
# df[TOPIC_COL] = df[TOPIC_COL].fillna("Unknown").astype(str)

# if survey_page == "Customer Survey":
#     df[NEWSLETTER_COL] = df[NEWSLETTER_COL].replace({
#         1: "Yes",
#         0: "No",
#         "1": "Yes",
#         "0": "No"
#     })


# # ─────────────────────────────
# # HELPER FUNCTIONS
# # ─────────────────────────────
# def get_all_topics(data, topic_col):
#     topics = []

#     for row in data[topic_col].dropna():
#         topics.extend([t.strip() for t in str(row).split(",")])

#     topics = sorted(set(topics))

#     topics = [
#         topic for topic in topics
#         if str(topic).strip().lower() != "unknown"
#         and str(topic).strip() != ""
#     ]

#     return topics


# def topic_match(row, selected_topics):
#     row_topics = [t.strip() for t in str(row).split(",")]
#     return any(t in selected_topics for t in row_topics)


# def save_widget_value(widget_key, permanent_key):
#     st.session_state[permanent_key] = st.session_state[widget_key]


# def apply_filters(data, sentiment_col, topic_col, date_col, key_prefix=""):
#     sentiments = sorted([
#         x for x in data[sentiment_col].dropna().unique()
#         if str(x).strip().lower() != "unknown"
#         and str(x).strip() != ""
#     ])

#     all_topics = get_all_topics(data, topic_col)

#     valid_dates = data[data[date_col].notna()]
#     has_valid_dates = not valid_dates.empty

#     if has_valid_dates:
#         min_date = valid_dates[date_col].min().date()
#         max_date = valid_dates[date_col].max().date()
#     else:
#         min_date = None
#         max_date = None

#     sentiment_perm_key = f"saved_{key_prefix}_sentiment"
#     topic_perm_key = f"saved_{key_prefix}_topic"
#     date_perm_key = f"saved_{key_prefix}_date"

#     sentiment_widget_key = f"widget_{key_prefix}_sentiment"
#     topic_widget_key = f"widget_{key_prefix}_topic"
#     date_widget_key = f"widget_{key_prefix}_date"

#     if sentiment_perm_key not in st.session_state:
#         st.session_state[sentiment_perm_key] = sentiments

#     if topic_perm_key not in st.session_state:
#         st.session_state[topic_perm_key] = all_topics

#     if has_valid_dates and date_perm_key not in st.session_state:
#         st.session_state[date_perm_key] = (min_date, max_date)

#     st.session_state[sentiment_perm_key] = [
#         x for x in st.session_state[sentiment_perm_key] if x in sentiments
#     ]

#     st.session_state[topic_perm_key] = [
#         x for x in st.session_state[topic_perm_key] if x in all_topics
#     ]

#     if sentiment_widget_key not in st.session_state:
#         st.session_state[sentiment_widget_key] = st.session_state[sentiment_perm_key]

#     if topic_widget_key not in st.session_state:
#         st.session_state[topic_widget_key] = st.session_state[topic_perm_key]

#     if has_valid_dates and date_widget_key not in st.session_state:
#         st.session_state[date_widget_key] = st.session_state[date_perm_key]

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         selected_sentiments = st.multiselect(
#             "Sentiment",
#             sentiments,
#             key=sentiment_widget_key,
#             on_change=save_widget_value,
#             args=(sentiment_widget_key, sentiment_perm_key)
#         )

#     with col2:
#         selected_topics = st.multiselect(
#             "Topic",
#             all_topics,
#             key=topic_widget_key,
#             on_change=save_widget_value,
#             args=(topic_widget_key, topic_perm_key)
#         )

#     with col3:
#         if has_valid_dates:
#             selected_dates = st.date_input(
#                 "Date range",
#                 min_value=min_date,
#                 max_value=max_date,
#                 key=date_widget_key,
#                 on_change=save_widget_value,
#                 args=(date_widget_key, date_perm_key)
#             )
#         else:
#             selected_dates = None
#             st.info("No valid dates available.")

#     filtered = data[
#         data[sentiment_col].isin(selected_sentiments)
#         & data[topic_col].apply(lambda x: topic_match(x, selected_topics))
#     ]

#     if (
#         has_valid_dates
#         and selected_dates is not None
#         and len(selected_dates) == 2
#     ):
#         start_date, end_date = selected_dates

#         # Only apply date filtering if the user changed the default range
#         if start_date != min_date or end_date != max_date:
#             start_date = pd.to_datetime(start_date)
#             end_date = pd.to_datetime(end_date)

#             filtered = filtered[
#                 filtered[date_col].isna()
#                 |
#                 (
#                     (filtered[date_col] >= start_date)
#                     & (filtered[date_col] <= end_date)
#                 )
#             ]

#     return filtered


# def retrieve_top_responses(query, data, clean_text_col, top_k=10, threshold=0.30):
#     search_data = data[data[clean_text_col].notna()].copy()
#     search_data = search_data[search_data[clean_text_col].astype(str).str.strip() != ""]

#     if search_data.empty:
#         return pd.DataFrame()

#     texts = search_data[clean_text_col].astype(str).tolist()

#     with st.spinner("Running your search..."):
#         embeddings = build_embeddings(texts)
#         query_embedding = embed_model.encode([query])
#         similarity_scores = cosine_similarity(query_embedding, embeddings)[0]

#     sorted_indices = np.argsort(similarity_scores)[::-1]
#     selected = []

#     for idx in sorted_indices[:top_k]:
#         score = similarity_scores[idx]

#         if score >= threshold:
#             row = search_data.iloc[idx].copy()
#             row["similarity_score"] = float(score)
#             selected.append(row)

#     return pd.DataFrame(selected)


# def plot_bar(data, column, title, top_n=None):
#     if column in data.columns:
#         counts = (
#             data[column]
#             .fillna("Unknown")
#             .astype(str)
#             .value_counts()
#             .reset_index()
#         )

#         counts.columns = [column, "Count"]

#         if top_n:
#             counts = counts.head(top_n)

#         fig = px.bar(counts, x=column, y="Count", title=title)
#         fig.update_layout(xaxis_tickangle=-30)
#         st.plotly_chart(fig, use_container_width=True)


# def normalize_brand_name(brand):
#     if pd.isna(brand):
#         return None

#     brand = str(brand).strip().lower()

#     if brand == "":
#         return None

#     brand = brand.replace(".", "")
#     brand = brand.replace("  ", " ")

#     brand_mapping = {
#         "pom": "Pom Amsterdam",
#         "pom amsterdam": "Pom Amsterdam",
#         "pom-amsterdam": "Pom Amsterdam",
#         "pomamsterdam": "Pom Amsterdam",

#         "sezane": "Sezane",
#         "sézane": "Sezane",

#         "ganni": "Ganni",
#         "mango": "Mango",
#         "zara": "Zara",
#         "h&m": "H&M",
#         "hm": "H&M",

#         "maje": "Maje",
#         "sandro": "Sandro",

#         "essentiel": "Essentiel Antwerp",
#         "essentiel antwerp": "Essentiel Antwerp",

#         "baum": "Baum und Pferdgarten",
#         "baum und pferdgarten": "Baum und Pferdgarten",
#         "baum und pferdgarden": "Baum und Pferdgarten",

#         "other stories": "& Other Stories",
#         "& other stories": "& Other Stories",
#         "and other stories": "& Other Stories",

#         "isabel marant": "Isabel Marant",
#         "rixo": "Rixo",
#         "stieglitz": "Stieglitz",
#         "summum": "Summum",
#         "yaya": "Yaya",
#         "jacquemus": "Jacquemus",
#         "samsøe samsøe": "Samsøe Samsøe",
#         "samsoe samsoe": "Samsøe Samsøe",
#         "samsøe": "Samsøe Samsøe",
#         "samsoe": "Samsøe Samsøe",
#         "levi": "Levi's",
#         "levi's": "Levi's",
#         "levis": "Levi's",
#         "levi s": "Levi's",
#         "levi’s": "Levi's",
#         "levis jeans": "Levi's",
#         "levi strauss": "Levi's",
#         "Leviâ€™S": "Levi's"
#     }

#     return brand_mapping.get(brand, brand.title())


# def plot_brand_mentions(data):
#     brand_col = "Which other fashion brands do you like wearing/engaging with the most?"

#     if brand_col not in data.columns:
#         return

#     counter = Counter()

#     for response in data[brand_col].dropna():
#         brands = str(response).split(",")

#         for brand in brands:
#             normalized_brand = normalize_brand_name(brand)
#             print(f"Original: '{brand}' -> Normalized: '{normalized_brand}'")
#             if normalized_brand:
#                 counter[normalized_brand] += 1

#     if not counter:
#         st.info("No brand mentions available.")
#         return

#     brand_counts = pd.DataFrame(
#         counter.items(),
#         columns=["Brand", "Count"]
#     ).sort_values("Count", ascending=False).head(15)

#     fig = px.bar(
#         brand_counts,
#         x="Brand",
#         y="Count",
#         title="Other Fashion Brands Mentioned"
#     )

#     fig.update_layout(xaxis_tickangle=-30)
#     st.plotly_chart(fig, use_container_width=True)


# def plot_newsletter_product_interest(data):
#     product_cols = [
#         "Dresses & Skirts",
#         "Tops & Blouses",
#         "T-shirts & Tank tops",
#         "Sweaters & Cardigans",
#         "Jackets & Coats",
#         "Pants & Jeans",
#         "Accessories (dcarves, belts, hats,...)",
#         "Shoes & Footwear"
#     ]

#     existing_cols = [col for col in product_cols if col in data.columns]

#     if existing_cols:
#         product_counts = data[existing_cols].notna().sum().reset_index()
#         product_counts.columns = ["Product Category", "Count"]

#         fig = px.bar(
#             product_counts,
#             x="Product Category",
#             y="Count",
#             title="Product Categories Mentioned"
#         )
#         fig.update_layout(xaxis_tickangle=-30)
#         st.plotly_chart(fig, use_container_width=True)


# def show_selected_response_from_table(results, table_event):
#     selected_rows = table_event.selection.rows

#     if selected_rows:
#         selected_position = selected_rows[0]
#         selected_row = results.iloc[selected_position]

#         st.subheader("Selected Response")
#         st.info(selected_row[TEXT_COL])

#         col1, col2 = st.columns(2)

#         with col1:
#             st.write("**Sentiment:**", selected_row[SENTIMENT_COL])
#             st.write("**Topic:**", selected_row[TOPIC_COL])

#         with col2:
#             st.write("**Similarity Score:**", round(selected_row["similarity_score"], 2))
#             st.write("**Email:**", selected_row[EMAIL_COL])

#         st.write("**Date:**", selected_row[DATE_COL])
#     else:
#         st.caption("Click on a row in the table to view the full response details.")


# # ─────────────────────────────
# # OVERVIEW PAGE
# # ─────────────────────────────
# if subpage == "Overview":
#     st.title(f"{survey_page} - Overview")

#     df_filtered = apply_filters(
#         df,
#         SENTIMENT_COL,
#         TOPIC_COL,
#         DATE_COL,
#         key_prefix=f"{survey_page}_Overview"
#     )

#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.metric("Responses in scope", len(df_filtered))

#     with col2:
#         st.metric("Unique emails", df_filtered[EMAIL_COL].nunique())

#     with col3:
#         st.metric("Topics", df_filtered[TOPIC_COL].nunique())

#     st.subheader("Responses")

#     display_cols = [TEXT_COL, SENTIMENT_COL, TOPIC_COL, EMAIL_COL, DATE_COL]

#     st.dataframe(
#         df_filtered[display_cols],
#         use_container_width=True,
#         hide_index=True
#     )

#     st.subheader("Sentiment Breakdown")
#     fig_sentiment = px.histogram(df_filtered, x=SENTIMENT_COL, color=SENTIMENT_COL)
#     st.plotly_chart(fig_sentiment, use_container_width=True)

#     st.subheader("Topic Distribution")
#     topic_counts = df_filtered[TOPIC_COL].value_counts().reset_index()
#     topic_counts.columns = ["Topic", "Count"]

#     fig_topics = px.bar(topic_counts, x="Topic", y="Count")
#     st.plotly_chart(fig_topics, use_container_width=True)

#     st.subheader("Sentiment Over Time")
#     trend = (
#         df_filtered[df_filtered[DATE_COL].notna()]
#         .groupby(["month", SENTIMENT_COL])
#         .size()
#         .reset_index(name="count")
#     )

#     if not trend.empty:
#         fig_trend = px.line(
#             trend,
#             x="month",
#             y="count",
#             color=SENTIMENT_COL,
#             markers=True
#         )
#         st.plotly_chart(fig_trend, use_container_width=True)
#     else:
#         st.info("No valid dates available for the sentiment over time chart.")

#     st.subheader("Additional Survey Insights")

#     if survey_page == "Customer Survey":
#         demo_col1, demo_col2 = st.columns(2)

#         with demo_col1:
#             plot_bar(df_filtered, AGE_COL, "Age Distribution")

#         with demo_col2:
#             plot_bar(df_filtered, INCOME_COL, "Income Distribution")

#         demo_col3, demo_col4 = st.columns(2)

#         with demo_col3:
#             plot_bar(df_filtered, WORK_COL, "Working Field Distribution", top_n=10)

#         with demo_col4:
#             plot_bar(df_filtered, NEWSLETTER_COL, "Newsletter Subscription")

#         plot_bar(df_filtered, NATIONALITY_COL, "Nationality Distribution", top_n=15)

#     else:
#         plot_bar(
#             df_filtered,
#             "How satisfied are you with our newsletters in 2025?",
#             "Newsletter Satisfaction"
#         )

#         plot_newsletter_product_interest(df_filtered)

#         plot_brand_mentions(df_filtered)

#     st.subheader("Download")

#     col1, col2 = st.columns(2)

#     with col1:
#         st.download_button(
#             "Download filtered responses",
#             df_filtered.to_csv(index=False).encode("utf-8"),
#             file_name=f"{survey_page.lower().replace(' ', '_')}_responses.csv"
#         )

#     with col2:
#         email_list = df_filtered[[EMAIL_COL]].drop_duplicates()

#         st.download_button(
#             "Download email list",
#             email_list.to_csv(index=False).encode("utf-8"),
#             file_name=f"{survey_page.lower().replace(' ', '_')}_emails.csv"
#         )


# # ─────────────────────────────
# # SEMANTIC SEARCH PAGE
# # ─────────────────────────────
# elif subpage == "Semantic Search":
#     st.title(f"{survey_page} - Semantic Search")

#     df_search = apply_filters(
#         df,
#         SENTIMENT_COL,
#         TOPIC_COL,
#         DATE_COL,
#         key_prefix=f"{survey_page}_Semantic_Search"
#     )

#     st.caption(f"{len(df_search)} responses in scope")

#     query = st.text_input(
#         "Search responses",
#         key=f"{survey_page}_semantic_query"
#     )

#     top_k = st.slider(
#         "Number of results",
#         min_value=5,
#         max_value=30,
#         value=10,
#         key=f"{survey_page}_top_k"
#     )

#     if query:
#         results = retrieve_top_responses(
#             query=query,
#             data=df_search,
#             clean_text_col=CLEAN_TEXT_COL,
#             top_k=top_k,
#             threshold=0.30
#         )

#         if results.empty:
#             st.info("No matching responses found.")
#         else:
#             st.subheader("Search Results")

#             results = results.reset_index(drop=True)

#             display_cols = [
#                 TEXT_COL,
#                 SENTIMENT_COL,
#                 TOPIC_COL,
#                 EMAIL_COL,
#                 DATE_COL,
#                 "similarity_score"
#             ]

#             table_event = st.dataframe(
#                 results[display_cols],
#                 use_container_width=True,
#                 hide_index=True,
#                 on_select="rerun",
#                 selection_mode="single-row",
#                 key=f"{survey_page}_{subpage}_results_table"
#             )

#             show_selected_response_from_table(results, table_event)

#             st.subheader("Download")

#             col1, col2 = st.columns(2)

#             with col1:
#                 st.download_button(
#                     "Download search results",
#                     results.to_csv(index=False).encode("utf-8"),
#                     file_name=f"{survey_page.lower().replace(' ', '_')}_search_results.csv"
#                 )

#             with col2:
#                 email_list = results[[EMAIL_COL]].drop_duplicates()

#                 st.download_button(
#                     "Download email list",
#                     email_list.to_csv(index=False).encode("utf-8"),
#                     file_name=f"{survey_page.lower().replace(' ', '_')}_search_emails.csv"
#                 )
