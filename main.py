import pandas as pd
import numpy as np
import openpyxl

# 2- clean function
def clean_df(df):
    df_cleaned = df.copy()
    for col in df_cleaned.columns:
        print(col)
        df_cleaned[col] = df_cleaned[col].replace(["N/A", "", "None", "-"], np.nan)
    return df_cleaned

def clean_funding_table(df):
    df_cleaned = df.copy()
    # handle missing data
    df_cleaned['amount_cad'] =  df_cleaned['amount_cad'].replace(["N/A", "", "None", "-"], np.nan)
    df_cleaned['amount_cad'] = pd.to_numeric(df_cleaned['amount_cad'])
    # handle negative value
    df_cleaned.loc[df_cleaned['amount_cad'] < 0, 'amount_cad' ] = np.nan
    return df_cleaned



print("Hello in my script :-")

# //// loading Data From Files[xlsx csv json] /////

# first: read csv file
researchers_df = pd.read_csv("./raw_data/researchers.csv")
# print("researchers: \n ")
# print(researchers_df)

# second: read xlsx file
funding_df = pd.read_excel("./raw_data/funding.xlsx")
funding_clean_df = clean_funding_table(funding_df)
print("funding: \n ")
# print(funding_clean_df["amount_cad"])


# third: read json file
publications_df = pd.read_json("./raw_data/publications.json")
# print("publications: \n ")
# print(publications_df)

# //// 1- Merge all 3 files /////

# merge researchers and funding && publications by inner
res_fund_merged_inner_df = pd.merge(
    researchers_df,
    funding_clean_df,
    on = "researcher_id",
    how="inner"
)

res_fund_pub_merged_inner_df = pd.merge(
    res_fund_merged_inner_df,
    publications_df,
    on = "researcher_id",
    how="inner"
)
# print("this is researchers && funding and publication inner merged\n")
# print(res_fund_pub_merged_inner_df)

# merge researchers and funding && publications by left
res_fund_merged_left_df = pd.merge(
    researchers_df,
    funding_clean_df,
    on = "researcher_id",
    how="left"
)
res_fund_pub_merged_left_df = pd.merge(
    res_fund_merged_left_df,
    publications_df,
    on = "researcher_id",
    how="left"
)
# contrast between Left and inner
# answer 86 row by left way
# answer 49 row by inner way
print(f"the inner result {res_fund_pub_merged_inner_df.shape[0]} rows")
print(f"the inner result {res_fund_pub_merged_left_df.shape[0]} rows")

# معرفة الباحثين المفقودين
researcher_left = set(res_fund_pub_merged_left_df['researcher_id'].unique())
researcher_inner = set(res_fund_pub_merged_inner_df['researcher_id'].unique())
researcher_lost = researcher_left - researcher_inner

lost_names = researchers_df[researchers_df["researcher_id"].isin(researcher_lost)][['researcher_id','first_name','last_name']]
print("lost names:")
print(lost_names)

# //// 3- First Question /////
#  ////////////////////     First Question //////////////
res_fund_pub_merged_left_df = clean_df(res_fund_pub_merged_left_df)
citations = res_fund_pub_merged_left_df.groupby("researcher_id")['citations'].sum().sort_values(ascending = False)
cit_index = citations.index[0]
top_cit = citations.iloc[0]
print(citations.index[0])
print(top_cit)
# جلب بيانات الباحث الذي يمتلك اقتباسلت أكثر
res_data = researchers_df[researchers_df["researcher_id"] == cit_index].iloc[0]
print("Question one")
print(res_data)

#  ////////////////////     Second Question //////////////

funding_per_res = res_fund_pub_merged_left_df.groupby("field")["amount_cad"].sum().sort_values(ascending=False)
top_field =funding_per_res.index[0]
top_funding =funding_per_res.iloc[0]
print("Question 2")
print(top_field, top_funding)

#  ////////////////////     third Question //////////////

active_res = researchers_df[researchers_df["is_active"] == True].copy()
oldest_active = active_res.sort_values("joined_year").iloc[0]
print("oldest_active: Question 3")
print(oldest_active )

# print csv file with new data
res_fund_pub_merged_left_df.to_csv("output/new_dataframe.csv")




