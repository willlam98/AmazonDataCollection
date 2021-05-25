import numpy as np
import pandas as pd
import openpyxl
import xlsxwriter
import sys
import os
import re

def get_material(df):
  '''
  We can label by using simple if-else statement
  as currently we only have the following output
  classes for materials:

  paper, wood, plastic, metal, ceramic, glass, foam, other
  '''
  tmp = df.copy()
  materials = []
  for i in range(len(tmp)):
    input = tmp.iloc[i, 0].lower()
    if 'steel' in input or 'metal' in input:
      material = 'metal'
    elif 'plastic' in input or 'silicone' in input or 'rubber' in input:
      material = 'plastic'
    elif 'wood' in input:
      material = 'wood'
    elif 'glass' in input:
      material = 'glass'
    elif 'ceramic' in input:
      material = 'ceramic'
    elif 'paper' in input:
      material = 'paper'
    elif 'foam' in input:
      material = 'foam'
    else:
      material = '' # can be double checked after automatically labelling
    materials.append(material)
  return materials, tmp

def get_colour(df):
  '''
  Using regular expression to find colour
  as normally the colour is written in the table
  if nothing is found just append an empty string
  such that we can double checked afterwards

  NOTE: when manually checking the colour, I put some
  of the label as 'other' although the colour is appeared
  in the text. For example,
  Colour Transparent
  Colour Steel

  I label this as 'other' as I think on the Robotics side
  it is difficult to define these 'colour'
  This needs to be discussed with Krystian.
  Also note that this is minor issue as colour can be
  predicted alongside with an image input
  '''
  regex = 'colour ([a-z]+)\n?'
  r = re.compile(regex)

  tmp = df.copy()
  colours = []
  for i in range(len(tmp)):
    input = tmp.iloc[i, 0].lower()
    colour = r.findall(input)
    if len(colour) == 0:
      colours.append('')
    else:
      colours.append(colour[0])
  return colours, tmp

def get_weight(df):
  # The regex also considers type
  regex = '([0-9]+\.?[0-9]*) ?(grams|g|gram|kg|kilograms|kilogram)\n?'
  r = re.compile(regex)
  
  tmp = df.copy()
  weights = []
  for i in range(len(tmp)):
    input = tmp.iloc[i, 0].lower()
    weight = r.findall(input)
    if len(weight) == 0:
      weights.append('')
    else:
      # This will output a tuple if found (the value and unit e.g. (100) (g))
      # and we want the last found match as normally the weight appears in the
      # end of the text (in the table)
      weight = weight[-1]
      value, unit = weight

      if unit in ['g', 'gram', 'grams']:
        weights.append(value + 'g')
      elif unit in ['kg', 'kilogram', 'kilograms']:
        weights.append(value + 'kg')
      else:
        # unknown unit
        weights.append('')
  return weights, tmp

def get_volume(df):
  '''
  The mechanism is similar to how the weight is extracted
  '''
  # Similar to weight, the regex also considers type
  regex = '([0-9]+\.?[0-9]*) ?(ml|l|oz|cl|millilitres|millilitre|milliliters|milliliter|litre|litres|liter|liters)\n?'
  r = re.compile(regex)

  tmp = df.copy()
  volumes = []
  for i in range(len(tmp)):
    input = tmp.iloc[i, 0].lower()
    volume = r.findall(input)
    if len(volume) == 0:
      volumes.append('')
    else:
      volume = volume[-1]
      val, unit = volume
      if unit in ['ml', 'millilitres', 'millilitre', 'milliliters', 'milliliter']:
        volumes.append(val + 'ml')
      elif unit in ['l', 'litre', 'litres', 'liter', 'liters']:
        volumes.append(val + 'L')
      elif unit in ['oz']:
        volumes.append(val + 'oz')
      elif unit in ['cl']:
        volumes.append(val + 'cl')
      else:
        volumes.append('')
  return volumes, tmp

def get_dimension(df):
  regex = '([0-9]+\.?[0-9]*) ?[xX] ?([0-9]+\.?[0-9]*) ?[xX] ?([0-9]+\.?[0-9]*)'
  r = re.compile(regex)

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
        print('File doess not exist, expecting a .xlsx file')
        return
    spreadsheet = pd.read_excel(file_path)

    materials, df = get_material(spreadsheet)
    colours, _ = get_colour(spreadsheet)
    weights, _ = get_weight(spreadsheet)
    volumes, _ = get_volume(spreadsheet)
    size, _ = get_dimension(spreadsheet)

    # Label material
    df['Material'] = materials

    # Label colour
    df['Colour'] = colours

    # Label weight
    df['Weight'] = weights

    # Label volume
    df['Volume'] = volumes

    # Label dimension L x W x H
    size = np.asarray(size)
    df['Length'] = size[:, 0]
    df['Width'] = size[:, 1]
    df['Height'] = size[:, 2]

    update_spreadsheet(df, file_path)

if __name__ == '__main__':
    main()
