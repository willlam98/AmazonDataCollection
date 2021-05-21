import numpy as np
import pandas as pd
import openpyxl
import xlsxwriter
import sys
import os
import re

regex = '([0-9]+\.?[0-9]*) ?[xX] ?([0-9]+\.?[0-9]*) ?[xX] ?([0-9]+\.?[0-9]*)'
r = re.compile(regex)

def get_dimension(df):
  tmp = df.copy()
  dimensions = []
  for i in range(len(tmp)):
    input = tmp.iloc[i, 0]
    dimension = r.findall(input)
    if len(dimension) == 0:
      dimensions.append(['other', 'other', 'other'])
    else:
      L, W, H = dimension[0]
      dimensions.append([str(L), str(W), str(H)])
  return dimensions, tmp

def update_spreadsheet(df, file_path):
    writer = pd.ExcelWriter(file_path)
    df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False, index=False)
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']

    for idx, val in enumerate(df.columns):
        worksheet.write(0, idx, val)
    writer.save()

def main():
    file_path = sys.argv[-1]
    if not file_path.endswith('.xlsx') or not os.path.exists(file_path):
        print('File do not exist, expecting a .xlsx file')
        return
    spreadsheet = pd.read_excel(file_path)

    size, df = get_dimension(spreadsheet)
    size = np.asarray(size)

    df['Length'] = size[:, 0]
    df['Width'] = size[:, 1]
    df['Height'] = size[:, 2]

    update_spreadsheet(df, file_path)

if __name__ == '__main__':
    main()
