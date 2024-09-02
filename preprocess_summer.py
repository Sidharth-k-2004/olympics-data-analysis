import pandas as pd
def preprocess_summer(df,df_region):
    df_summer=df[df['Season']=="Summer"]
    df_summer=df_summer.merge(df_region,on='NOC',how='left')
    df_summer.drop_duplicates(inplace=True)
    one_hot_encoded_summer = pd.get_dummies(df_summer['Medal']).astype(int)
    df_summer=pd.concat([df_summer,one_hot_encoded_summer],axis=1)
    return df_summer
