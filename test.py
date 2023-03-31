import pickle

table_at_first, table_1_to_1, table_2_to_1 = pickle.load(open('data/match.pkl', 'rb'))
# sort the dict by frequency
dic = sorted(table_2_to_1['会与'].items(), key=lambda x: x[1], reverse=True)
print(dic)
