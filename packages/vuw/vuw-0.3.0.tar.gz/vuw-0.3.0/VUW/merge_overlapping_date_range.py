# '''
# 데이터프레임에서 특정 날짜 범위를 기반으로 그룹화 및 처리하는 작업 수행
# '''

# import pandas as pd
# from datetime import timedelta
# from .glue_code import glue_code_


# from datetime import timedelta

# # Redefine the required functions for the example

# def index_overlapping_date_range(ids, from_dates, to_dates, interval=0):
#     '''
#     R에서 rcpp_index_overlapping_date_range 대체 함수
#     주어진 id와 날짜 범위에 대해 중첩된 인덱스 생성
#     '''
#     loc = []
#     sub = []

#     for i, (id_, from_date, to_date) in enumerate(zip(ids, from_dates, to_dates)):
#         overlapping = (
#             (ids == id_) &
#             (from_date <= to_dates + timedelta(days=interval)) &
#             (to_date >= from_dates - timedelta(days=interval))
#         )
#         loc.append(i)
#         sub.append(overlapping.sum() - 1) # 자기 자신 제외
    
#     return {'loc': loc, 'sub': sub}

# def merge_overlapping_date_range(df, id_var, gender, age, age_band, kcd, sdate, edate, interval=0):
#     # 필요한 컬럼 추출 및 이름 변경
#     tmp = df.copy()
#     tmp.rename(columns={id_var: 'id', kcd: 'kcd', sdate: 'sdate', edate: 'edate'}, inplace=True)

#     # 날짜 정렬
#     tmp.sort_values(by=['id', 'sdate', 'edate'], inplace=True)

#     # id, from, to로 중첩 인덱스 계산
#     ids = tmp['id'].values
#     from_dates = pd.to_datetime(tmp['sdate']).values
#     to_dates = pd.to_datetime(tmp['edate']).values

#     # 중첩 날짜 병합
#     merged_rows = []
#     for id_, group in tmp.groupby('id'):
#         group = group.sort_values(by='sdate')
#         current_start = None
#         current_end = None
#         current_kcds = []
        
#         for _, row in group.iterrows():
#             row_start = pd.to_datetime(row['sdate'])
#             row_end = pd.to_datetime(row['edate'])
            
#             if current_start is None:  # 첫 행
#                 current_start = row_start
#                 current_end = row_end
#                 current_kcds.append(row['kcd'])
#             elif row_start <= current_end + timedelta(days=interval):  # 겹침
#                 current_end = max(current_end, row_end)
#                 current_kcds.append(row['kcd'])
#             else:  # 겹치지 않음 -> 병합 후 새로운 기간 시작
#                 merged_rows.append({
#                     'id': id_, 'gender': row['gender'], 'age': row['age'], 
#                     'age_band': row['age_band'], 'kcd': glue_code_(current_kcds), 
#                     'sdate': current_start, 'edate': current_end
#                 })
#                 current_start = row_start
#                 current_end = row_end
#                 current_kcds = [row['kcd']]
        
#         # 마지막 병합 데이터 추가
#         if current_start is not None:
#             merged_rows.append({
#                 'id': id_, 'gender': group['gender'].iloc[0], 'age': group['age'].iloc[0], 
#                 'age_band': group['age_band'].iloc[0], 'kcd': glue_code_(current_kcds), 
#                 'sdate': current_start, 'edate': current_end
#             })

#     # 결과 데이터프레임 생성
#     result = pd.DataFrame(merged_rows)

#     # 추가 계산: stay 열 생성
#     result['stay'] = (pd.to_datetime(result['edate']) - pd.to_datetime(result['sdate'])).dt.days + 1

#     return result

# if __name__ == '__main__':
#     data = {
#         'id': ['A', 'A', 'A', 'B', 'B'],
#         'gender': [1, 1, 1, 2, 2],
#         'age': [16, 16, 16, 16, 16],
#         'age_band': ['10-19', '10-19', '10-19', '10-19', '10-19'],
#         'kcd': ['x', 'y', 'z', 'w', 'p'],
#         'from_date': ['2024-01-01', '2024-01-05', '2024-01-10', '2024-01-01', '2024-01-03'],
#         'to_date':  ['2024-01-06', '2024-02-10', '2024-01-15', '2024-01-05', '2024-01-06']
#     }
    
#     df = pd.DataFrame(data)
#     result = merge_overlapping_date_range(df, id_var='id', gender='gender', age='age', age_band='age_band', kcd='kcd', sdate='from_date', edate='to_date', interval=0)
#     print(result)
import pandas as pd
from datetime import timedelta
from joblib import Parallel, delayed
from .glue_code import glue_code_
import numpy as np
from multiprocessing import Pool, cpu_count

def merge_group(group, additional_col, interval=0):
    """
    각 그룹에 대해 날짜 범위를 병합하며 실제 치료 날짜를 기반으로 stay를 계산합니다.
    """

    group = group.sort_values(by='sdate')
    merged_rows = []
    current_start, current_end = None, None
    current_kcds = []
    unique_treatment_days = set()
    additional_values = {col: None for col in additional_col}

    for _, row in group.iterrows():
        row_start = row['sdate']
        row_end = row['edate']
        if pd.isna(row_start) or pd.isna(row_end):
            continue
            
        row_days = set(pd.date_range(start=row_start, end=row_end))  # 치료 날짜들
        for col in additional_col:
            if col in group.columns:
                additional_values[col] = row[col]
        if current_start is None:
            # Initialize the first range
            current_start = row_start
            current_end = row_end
            current_kcds.append(row['kcd'])
            unique_treatment_days.update(row_days)
        elif row_start <= current_end + timedelta(days=interval):
            # Merge overlapping or adjacent ranges
            current_end = max(current_end, row_end)
            current_kcds.append(row['kcd'])
            unique_treatment_days.update(row_days)  # 중복 제거된 치료 날짜 업데이트
        else:
            # Append merged range and reset
            merged_row = {
                'ID': row['ID'],
                'gender': row['gender'],
                'age': row['age'],
                'age_band': row['age_band'],
                'kcd': glue_code_(current_kcds),
                'sdate': current_start,
                'edate': current_end,
                'stay': len(unique_treatment_days),  # 고유 치료 날짜 수
            }
            merged_row.update(additional_values)
            merged_rows.append(merged_row)
            current_start = row_start
            current_end = row_end
            current_kcds = [row['kcd']]
            unique_treatment_days = row_days

    # Add the last merged range
    if current_start is not None:
        merged_row = {
            'ID': group['ID'].iloc[0],
            'gender': group['gender'].iloc[0],
            'age': group['age'].iloc[0],
            'age_band': group['age_band'].iloc[0],
            'kcd': glue_code_(current_kcds),
            'sdate': current_start,
            'edate': current_end,
            'stay': len(unique_treatment_days),  # 고유 치료 날짜 수
        }
        merged_row.update(additional_values)
        merged_rows.append(merged_row)

    return merged_rows

from joblib import Parallel, delayed

def merge_overlapping_date_range(
    df, additional_col=[], interval=0, n_jobs=-1
):
    """
    최적화된 중첩 날짜 병합 함수.
    치료가 발생한 고유 날짜를 기준으로 stay를 계산합니다.
    """

    tmp = df.copy()
    # if ('cat_10' not in tmp.columns) & ('dis_inj' not in tmp.columns):
    #     tmp['cat_10'] = np.nan
    #     tmp['dis_inj'] = np.nan
        
    # tmp.rename(
    #     columns={id_var: 'id', kcd: 'kcd', sdate: 'sdate', edate: 'edate', cat_10: 'cat_10', dis_inj: 'dis_inj'},
    #     inplace=True,
    # )
    tmp['sdate'] = pd.to_datetime(tmp['sdate'])
    tmp['edate'] = pd.to_datetime(tmp['edate'])

    # 그룹화 및 병렬 처리
    groups = tmp.groupby('ID')
    results = Parallel(n_jobs=n_jobs)(
        delayed(merge_group)(group, additional_col, interval) for _, group in groups
    )

    # 결과 병합
    merged_rows = [row for group in results for row in group]
    result = pd.DataFrame(merged_rows)

    return result


# def merge_group(group, interval=0):
#     """
#     각 그룹에 대해 날짜 범위를 병합합니다.
#     """
#     group = group.sort_values(by='sdate')
#     merged_rows = []
#     current_start, current_end = None, None
#     current_kcds = []

    
#     for _, row in group.iterrows():
#         row_start = row['sdate']
#         row_end = row['edate']

#         if current_start is None:
#             # Initialize the first range
#             current_start = row_start
#             current_end = row_end
#             current_kcds.append(row['kcd'])
#             stay = 0
#             stay = stay + (current_end - current_start).days
#         elif row_start <= current_end + timedelta(days=interval):
#             # Merge overlapping ranges
#             stay = stay + (current_end - current_start).days
#             current_end = max(current_end, row_end)
#             current_kcds.append(row['kcd'])
            
#         else:
#             # Append merged range and reset
#             merged_rows.append({
#                 'id': row['id'],
#                 'gender': row['gender'],
#                 'age': row['age'],
#                 'age_band': row['age_band'],
#                 'kcd': glue_code_(current_kcds), 
#                 'sdate': current_start,
#                 'edate': current_end,
#                 'stay': stay
#             })
#             current_start = row_start
#             current_end = row_end
#             current_kcds = [row['kcd']]

#     # Add the last merged range
#     if current_start is not None:
#         merged_rows.append({
#             'id': group['id'].iloc[0],
#             'gender': group['gender'].iloc[0],
#             'age': group['age'].iloc[0],
#             'age_band': group['age_band'].iloc[0],
#             'kcd': glue_code_(current_kcds),
#             'sdate': current_start,
#             'edate': current_end,
#             'stay': stay
#         })

#     return merged_rows


# def merge_overlapping_date_range(
#     df, id_var, kcd, sdate, edate, interval=0, n_jobs=-1
# ):
#     """
#     최적화된 중첩 날짜 병합 함수
#     """
#     tmp = df.copy()
#     tmp.rename(
#         columns={id_var: 'id', kcd: 'kcd', sdate: 'sdate', edate: 'edate'},
#         inplace=True,
#     )
#     tmp['sdate'] = pd.to_datetime(tmp['sdate'])
#     tmp['edate'] = pd.to_datetime(tmp['edate'])

#     # 그룹화 및 병렬 처리
#     groups = tmp.groupby('id')
#     results = Parallel(n_jobs=n_jobs)(
#         delayed(merge_group)(group, interval) for _, group in groups
#     )

#     # 결과 병합
#     merged_rows = [row for group in results for row in group]
#     result = pd.DataFrame(merged_rows)

#     # # 추가 계산: stay 열 생성
#     # result['stay'] = (result['edate'] - result['sdate']).dt.days + 1
#     return result
