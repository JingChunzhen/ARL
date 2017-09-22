import sqlite3
import copy
import csv
import random

def data_preprocess(file_in, file_out, sample, sample_size):
    '''
    Args:
        file_in (string): file path for database
        file_out (string): file path 
        sample (boolean): True for sample False for not sample
        sample_size (int): 
    Return:
    '''
    conn = sqlite3.connect(file_in)
    c = conn.cursor()
    query_sql = "SELECT %s,%s,%s FROM maidian ORDER BY %s,%s ASC"    
    sql_params = ["roleid", "op", "relative_timestamp", "roleid", "relative_timestamp"]

    transactions = []       
    previous_relative_timestamp = None
    previous_roleid = None    
    time_stamp = 1
    roleid_list = []

    role_index = 100000
    for row in c.execute(query_sql % tuple(sql_params)):
        roleid = str(row[0])
        op = row[1]     
        relative_timestamp = row[2]                     

        if previous_roleid == None:
            transaction = [str(role_index), str(time_stamp), op]
            transactions.append(transaction)
            roleid_list.append(str(role_index))

        elif roleid == previous_roleid:
            if relative_timestamp != previous_relative_timestamp:
                transaction = [str(role_index), str(time_stamp), op]
                transactions.append(transaction)
            else:
                flag = True
                for i in range(2, len(transactions[-1])):
                    if op == transactions[-1][i]:
                        flag = False
                        break
                if flag:
                    transactions[-1].append(op)    
                time_stamp -= 1                                   
        else:
            # roleid != previous_roleid
            time_stamp = 1
            role_index += 1
            transaction = [str(role_index), str(time_stamp), op]
            transactions.append(transaction)            
            roleid_list.append(str(role_index))
            
    
        time_stamp += 1
        previous_roleid = roleid
        previous_relative_timestamp = relative_timestamp
            
    if sample:
        # sample roleid 
        sample_roleids = [] 
        for i in range(sample_size):
            while True:
                random_index = random.randint(0, len(roleid_list))
                if random_index not in sample_roleids:  
                    sample_roleids.append(roleid_list[random_index])
                    break
                pass

        
        sample_transactions = []
        
        for i in range(len(transactions)):        
            if transactions[i][0] in sample_roleids:
                sample_transactions.append(transactions[i])

        for i in range(len(sample_transactions)):
            sample_transactions[i].insert(2, str(len(sample_transactions[i]) - 2))
            sample_transactions[i] = ','.join(sample_transactions[i])
        
        print(len(sample_transactions))
        print('transaction sampled!')
        
        with open(file_out, 'wb') as f_out:        
            for transaction in sample_transactions:            
                f_out.write((transaction + '\n').encode('utf-8'))
        
    else:
        with open(file_out, 'wb') as f_out:
            for i in range(len(transactions)):
                transactions[i].insert(2, str(len(transactions[i]) - 2))
                transactions[i] = ','.join(transactions[i])
                f_out.write((transactions[i] + '\n').encode('utf-8'))
        


def check_file(file_in):
    '''
    using arulesSequence sid and eid have to be ordered blockwise
    and the sid has to be the same length 
    '''
    sid = []
    with open(file_in, 'rb') as f_in:
        for line in f_in:
            line = line.decode('utf-8')                    
            roleid = eval(line.split(',')[0])
            sid.append(roleid)            

    print(len(sid))
    
    i = 0

    previous_sid = None
    distinct_sid = []
    for i in range(len(sid)):
        if sid[i] != previous_sid:            
            distinct_sid.append(sid[i])
        previous_sid = sid[i]        
    
    
    for i in range(1, len(distinct_sid)):
        if distinct_sid[i] < distinct_sid[i - 1]:
            print("{} {}".format(distinct_sid[i-1], distinct_sid[i]))
        if len(str(distinct_sid[i])) != len(str(distinct_sid[i - 1])):
            print("{} {}".format(distinct_sid[i-1], distinct_sid[i]))
        

if __name__ == '__main__':
    file_in = './data/awfeia.db2'    
    file_out = './output/test_09211629.txt'
    data_preprocess(file_in, file_out, True, 1000)
    check_file(file_in='./output/test_09211629.txt')
    pass






    






        
        
        
        
        


    
