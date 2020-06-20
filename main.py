# import the necessary packages
from PIL import Image
import pytesseract
import cv2
import os
import glob
import re
import pandas as pd
from datetime import datetime

results_path = "/Users/kiansiong/ks_projects/mahjong_ocr/scores.csv"
players = ['DTYL', 'SC', 'jiale', 'seigua.yat']
image_path = "/Users/kiansiong/ks_projects/mahjong_ocr/images"

score = {}
for player in players:
    score[player] = 0

# Get all jpeg files in current directory
file_list = []
file_types = ['jpg','jpeg']

for type in file_types:
    search_str = '*.{}'
    search_path = os.path.join(image_path, search_str.format(type))
    f = glob.glob(search_path)
    file_list.extend(f)


# load the example image and convert it to grayscale
for file in file_list:
    print(f"\nProcessing file {file}")
    image = cv2.imread(file)

    # Preprocess image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bitwise_not(gray)
    gray = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)[1]

    # write the grayscale image to disk as a temporary file so we can apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    # OCR and remove temp file
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)

    ''' For debugging '''
    # print('Text')
    # print(text)

    # Parse text
    recon_game = 0
    for player in players:
        search = "{p}[\s\S]*?([\+\-]\d*?)[\s\+\-]*?\(".format(p=player)
        x = re.search(search, text, re.DOTALL)
        score[player] += int(x.group(1))
        recon_game += int(x.group(1))
        ''' For debugging '''
        print(f'{player} = {int(x.group(1))}')
    print(f'RECON_GAME = {recon_game}')

# Format
score['ks'] = score['seigua.yat']
del score['seigua.yat']

# Recon
recon = 0
for key, value in score.items():
    recon += value
score['recon'] = recon

print('\n\n')
print(score)
print('\n\n')


# Append scores to existing dataframe
results = []

try:
    past_df = pd.read_csv(results_path)
    results.append(past_df)
except Exception:
    print("No existing results file.")

dt = datetime.now().strftime("%Y%m%d")
df = pd.DataFrame(data=list(score.values()), index=list(score.keys()), columns=[dt])
df_t = df.transpose()
df_t.reset_index(inplace=True)
df_t.rename(columns={"index":"dt"}, inplace=True)
results.append(df_t)

final_df = pd.concat(results)
final_df.to_csv(results_path, index=False)
