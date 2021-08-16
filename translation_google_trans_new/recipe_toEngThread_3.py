# import google_trans_new
import pandas as pd
import concurrent.futures
import csv
import re
import os

import cfb101_google_trans_new

translator = cfb101_google_trans_new.google_translator(timeout=5)

# 輸入recipe資料
recipe_path = "./cook1cook_cleaning.csv"
# recipe資料 to DataFrame
recipe_df = pd.read_csv(recipe_path)
# recipe英文名稱
recipeEng = list()
# 輸出recipe csv檔案位置
recipe_csv = "./recipe_toEng_test.csv"
# List of recipe index
recipe_index = list(recipe_df.index)

# 建立Function
def GoRec(inputs):

    in_csv = list()

    # 建立已存在recipe csv檔案中的index list
    if os.path.exists(recipe_csv):
        _ = pd.read_csv(recipe_csv, names=['index', 'Eng_name'])
        in_csv = list(_["index"])

    # 利用re取出recipe中各個食材
    recipe = re.findall("\'\•*\:*(\w+)\(*\w*\)*\（*\w*\）*\'", recipe_df.loc[inputs]["食材"])
    # 各食譜的英文食材List
    engList = list()

    # 檢查是否已在檔案裡
    if inputs in in_csv:
        pass
    else:
        # 將輸出儲存為csv
        fieldnames = ['index', 'Eng_name']
        with open(recipe_csv, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, delimiter=",", fieldnames=fieldnames)

            # 若長度不為0則翻譯此食譜
            if len(recipe) != 0:

                # 逐一取出食材進行翻譯
                for r in recipe:
                    output = translator.translate(r, "en", "zh")
                    engList.append(output)

                # 直接寫入單筆食譜
                writer.writerow({"index": inputs, "Eng_name": engList})
                print(f"index: {inputs} 資料寫入!!")

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(GoRec, recipe_index)