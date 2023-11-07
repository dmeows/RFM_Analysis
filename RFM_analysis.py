import pandas as pd

class RFMAnalysis:
    def __init__(self, dataframe, customer_id_col, transaction_date_col, transaction_value_col):
        self.dataframe = dataframe
        self.customer_id_col = customer_id_col
        self.transaction_date_col = transaction_date_col
        self.transaction_value_col = transaction_value_col
        
    def calculate_rfm(self):
        # Calculate RFM metrics
        max_date = self.dataframe[self.transaction_date_col].max()
        self.dataframe['Recency'] = (max_date - self.dataframe[self.transaction_date_col]).dt.days
        self.dataframe['Frequency'] = self.dataframe.groupby(self.customer_id_col)[self.transaction_date_col].transform('count')
        self.dataframe['Monetary'] = self.dataframe.groupby(self.customer_id_col)[self.transaction_value_col].transform('sum')
        
    def create_segments(self):
        # Create RFM segments
        r_labels = range(4, 0, -1)
        f_labels = range(1, 5)
        m_labels = range(1, 5)
        
        r_quartiles = pd.qcut(self.dataframe['Recency'], q=4, labels=r_labels)
        f_quartiles = pd.qcut(self.dataframe['Frequency'], q=4, labels=f_labels)
        m_quartiles = pd.qcut(self.dataframe['Monetary'], q=4, labels=m_labels)
        
        self.dataframe = self.dataframe.assign(R=r_quartiles, F=f_quartiles, M=m_quartiles)
        
    def calculate_rfm_score(self):
        # Combine RFM segments into a single RFM score
        self.dataframe['RFM_Score'] = self.dataframe[['R', 'F', 'M']].sum(axis=1)
        
    def perform_rfm_analysis(self):
        self.calculate_rfm()
        self.create_segments()
        self.calculate_rfm_score()
        
        return self.dataframe


# import pandas as pd
# from RFMAnalysis import RFMAnalysis

# dataframe = pd.read_csv('cleaned_dataset.csv')
# rfm = RFMAnalysis(dataframe, 'customer_id', 'transaction_date', 'transaction_value')
# rfm_data = rfm.perform_rfm_analysis()

# print(rfm_data)
