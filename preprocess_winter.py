import pandas as pd
def preprocess_winter(df,df_region):
    df_winter=df[df['Season']=="Winter"]
    df_winter=df_winter.merge(df_region,on='NOC',how='left')
    df_winter.drop_duplicates(inplace=True)
    one_hot_encoded_winter = pd.get_dummies(df_winter['Medal']).astype(int)
    df_winter=pd.concat([df_winter,one_hot_encoded_winter],axis=1)
    return df_winter
