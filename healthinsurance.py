import numpy as np
import pandas as pd
import pickle

class HealthInsurance():
    def __init__(self):
        self.home_path=''
        self.annual_premium_scaler       = pickle.load(open(self.home_path + 'src/features/annual_premium.pkl', 'rb'))
        self.age_scaler                  = pickle.load(open(self.home_path + 'src/features/age.pkl', 'rb'))
        self.days_scaler                 = pickle.load(open(self.home_path + 'src/features/days_client_associate.pkl', 'rb'))
        self.gender_scaler               = pickle.load(open(self.home_path + 'src/features/gender.pkl', 'rb'))
        self.region_code_scaler          = pickle.load(open(self.home_path + 'src/features/region_code.pkl', 'rb'))
        self.sales_channel_scaler        = pickle.load(open(self.home_path + 'src/features/sales_channel.pkl', 'rb'))
        self.vehicle_damage_scaler       = pickle.load(open(self.home_path + 'src/features/vehicle_damage.pkl', 'rb'))             
             

    def feature_engineering(self, df2):

        # vericle_age
        df2['vehicle_age'] = df2['vehicle_age'].apply(lambda x: 'bellow_1_year' if x == '< 1 Year' else 
                                                             'between_1_2_year' if x == '1-2 Year' else 
                                                             'over_2_years')

        df2['vehicle_damage'] = df2['vehicle_damage'].apply(lambda x: 1 if x == 'Yes' else 0)
        
        return df2
    
    
    def data_preparation(self, df5):
        
        ## annual_premium
        df5['annual_premium'] = self.annual_premium_scaler.transform(df5[['annual_premium']].values)

        ## age
        df5['age'] = self.age_scaler.transform( df5[['age']].values )

        ## days_client_associate
        df5['days_client_associate'] = self.days_scaler.transform( df5[['days_client_associate']].values )

        ## vehicle_age
        df5 = pd.get_dummies(df5, prefix='vehicle_age',columns=['vehicle_age'])

        # gender 
        df5.loc[:,'gender'] = df5['gender'].map(self.gender_scaler)

        # region_code 
        df5.loc[:,'region_code'] = df5['region_code'].map(self.region_code_scaler)

        # vehicle damage
        df5.loc[:,'vehicle_damage'] = df5['vehicle_damage'].map(self.vehicle_damage_scaler)

        ## sales_channel 
        df5.loc[:,'sales_channel'] = df5['sales_channel'].map(self.sales_channel_scaler)

        cols_selected = [
                'gender',
                'annual_premium',
                'age',
                'region_code',
                'vehicle_damage',
                'sales_channel',
                'vehicle_insured',
                'days_client_associate']

        
        return df5[cols_selected]

    def get_prediction(self, model, original_data, test_data):
        
        # model prediction
        pred = model.predict_proba(test_data)
        
        # join prediction into original data
        original_data['prediction'] = pred[:,1].tolist()
        
        return original_data.to_json(orient='records', date_format='iso')