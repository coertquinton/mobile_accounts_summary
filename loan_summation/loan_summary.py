'''
Created on 20 Aug 2017

@author: Quinton
'''

import csv
from os import listdir
from os.path import isfile, join
import shutil
from test.test_buffer import prod

#==============================================================================
class LoanSummary(object):
      
    def __init__(self):
        summary_data = {}
        self._summary_data = summary_data

    #--------------------------------------------------------------------------
    def process_loan_data(self):
        
        data_files = self.get_files()
        for f in data_files:
            print ("processing %s" % f)
            self.process_file(f)
            self.create_output_file()
            self.move_file(f)
            
    #--------------------------------------------------------------------------
    def get_files(self):
        files = [f for f in listdir('data_files') if isfile(join('data_files', f))]
        return files
    
    #--------------------------------------------------------------------------
    def process_file(self, data_file):
        
        with open (join('data_files', data_file), 'r') as csv_file:
            for row in csv.DictReader(csv_file):
                self.insert_summary(row)
    
    #--------------------------------------------------------------------------        
    def insert_summary(self, row):
        '''
        '''
        network = row['Network']
        product = row['Product']
        month = row['Date'][4:]        
        amount = float(row['Amount'])
        
        if network in self._summary_data:
            if product in self._summary_data[network]:
                if month in self._summary_data[network][product]:
                    self.increment_totals(network, product, month, amount)
                else:
                    self._summary_data[network][product][month] = {'total_loans': 1, 'total_amount': amount}
            else:
                self._summary_data[network][product] = {month: {'total_loans': 1, 'total_amount': amount}}
        else:
            self._summary_data[network] = {product: {month: {'total_loans': 1, 'total_amount': amount}}}
                
        
    #--------------------------------------------------------------------------
    def increment_totals(self, network, product, month, amount):
        '''
        '''
        self._summary_data[network][product][month]['total_amount'] += amount
        self._summary_data[network][product][month]['total_loans'] += 1
        
    #--------------------------------------------------------------------------
    def create_output_file(self):
        
        output_file = join('data_files', 'completed_files', 'Output.csv')
        open_file = open(output_file, 'w', newline='')
        
        try:
            writer = csv.writer(open_file)
            writer.writerow(['Network', 'Product', 'Month', 'Count', 'Amount'])
            
            for network, network_data in self._summary_data.items():
                for product, product_data in network_data.items():
                    for month, month_data in product_data.items():
                        writer.writerow([network, product, month, month_data['total_loans'], month_data['total_amount']])                        
        finally:
            open_file.close()
    
    #--------------------------------------------------------------------------          
    def move_file(self, data_file):
        shutil.move(join('data_files', data_file), join('data_files', 'completed_files', data_file))
        
    
#------------------------------------------------------------------------------
if __name__ == '__main__':
    print('Start summarize data')

    loan_summary = LoanSummary()
    loan_summary.process_loan_data()


    print('Data summarize completed')
        
        
