import pandas as pd
import openpyxl

print("Hello in my script :-")

# //// loading Data From Files[xlsx csv json] /////

# first: read csv file
researchers_df = pd.read_csv("./raw_data/researchers.csv")
print("researchers: \n ")
print(researchers_df)

# second: read xlsx file
funding_df = pd.read_excel("./raw_data/funding.xlsx")
print("funding: \n ")
print(funding_df)

# third: read json file
publications_df = pd.read_json("./raw_data/publications.json")
print("publications: \n ")
print(publications_df)

# //// 1- Merge all 3 files /////

# first: merge researchers and funding by inner
res_fund_merged_df = pd.merge(
    researchers_df,
    funding_df,
    on = "researcher_id",
    how="inner"
)
print("this is researchers && funding inner merged\n")
print(res_fund_merged_df)

# second: merge researchers-funding && publications  by inner
res_fund_pub_merged_df = pd.merge(
    res_fund_merged_df,
    publications_df,
    on = "researcher_id",
    how="inner"
)
print("this is researchers && funding and publication inner merged\n")
print(res_fund_pub_merged_df)






