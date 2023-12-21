import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules
from sklearn.metrics.pairwise import cosine_similarity


# apriori
def find_rules(df):
    scaler = MinMaxScaler()
    records = []
    for i in range(len(df)):
        records.append([str(df.values[i, j])
                        for j in range(len(df.columns)) if not pd.isna(df.values[i, j])])
    # print(records[0])

    # encoding
    te = TransactionEncoder()
    te_ary = te.fit(records).transform(records, sparse = True)
    te_df = pd.DataFrame.sparse.from_spmatrix(te_ary, columns = te.columns_)

    # min_support: 상품 지지도 중 가장 작은 값으로 설정
    df_ap = apriori(te_df, min_support = 0.00371, max_len = None,
                           use_colnames = True, verbose = 1)

    # apriori dataframe
    association_rules_ap = association_rules(df_ap, metric = 'confidence', min_threshold = 0.2)
    association_rules_ap['antecedents'] = association_rules_ap['antecedents'].apply(lambda x: list(x))
    association_rules_ap['consequents'] = association_rules_ap['consequents'].apply(lambda x: list(x))
    association_rules_ap['len'] = association_rules_ap['antecedents'].apply(lambda x: len(x))
    association_rules_ap['conviction_scaled'] = scaler.fit_transform(association_rules_ap[['conviction']])
    
    cosine_similarities = []
    for _, row in association_rules_ap.iterrows():
        cosine_similarity = row['support'] / np.sqrt(row['antecedent support'] * row['consequent support'])
        cosine_similarities.append(cosine_similarity)
    association_rules_ap['score'] = association_rules_ap['conviction_scaled'] + association_rules_ap['lift'] + association_rules_ap['confidence']
    association_rules_ap['cosine similarity'] = cosine_similarities
    return association_rules_ap


# 카테고리별 유사도 계산
def category_sim(df):
    replace_dict = {'홈':np.nan,'어웨이':np.nan,'마킹':np.nan,'FC서울SoulofSeoul니트머플러':np.nan,'FC서울브랜딩니트머플러':np.nan,
                                                     'FC서울WHITE니트머플러':np.nan,'레트로전사머플러':np.nan,'40주년기념극세사머플러':np.nan,
                                                     '40주년기념머플러':np.nan,'선수단볼캡블랙':'악세서리','선수단동계비니':'악세서리','40주년백구':'악세서리',
                                                     '선수단신발주머니':'악세서리','FC서울포토레인보우':'악세서리','유니폼뱃지':'악세서리','엠블럼뱃지':'악세서리',
                                                     '레터링뱃지':'악세서리','입장용트랙탑':'트레이닝','레인자켓':'트레이닝','패딩수트상의':'트레이닝',
                                                     '선수단롱다운':'트레이닝','패딩베스트':'트레이닝','이동복상의':'트레이닝','트레이닝상의':'트레이닝',
                                                     '바람막이피스테':'트레이닝','연습복긴팔':'트레이닝','연습복반팔':'트레이닝','폴로티긴팔':'트레이닝',
                                                     '폴로티반팔':'트레이닝','트레이닝하의':'트레이닝','연습복반바지':'트레이닝',
                                                     'FC서울 벌룬':'응원용품','FC서울 응원깃발':'응원용품'}
    category_df = df.replace(replace_dict)
    category_counts = category_df.apply(lambda x: x.value_counts(), axis = 1)
    category_counts.dropna(how = 'all', inplace = True)
    category_counts.fillna(0, inplace = True)
    # print(category_counts.columns)
    # 코사인 유사도 출력
    category_counts_T = category_counts.transpose()
    category_sim = cosine_similarity(category_counts_T, category_counts_T)
    category_sim_df = pd.DataFrame(data=category_sim, index=category_counts.columns, columns = category_counts.columns)
    return category_sim_df