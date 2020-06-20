# Let's Mahjong app - Score tabulation

The Let's Mahjong app has allowed us to continue playing our favourite game during the lockdown measures due to Covid19.
If you played multiple rounds however, the scores had to be tabulated across multiple games.

This app was made to scan the screenshots saved from score from each round, and tabulate a final score across multiple rounds.
It uses Optical Character Recognition (OCR) to recognise names and scores, and tabulates the final score for all uploaded screenshots.

## Setup
Run  `pip install -r requirements.txt`

## User configuration
OCR has not been tuned for optimal image recognition. There is still a lot of junk characters.
Therefore, a combination of regex for finding user name has been used.

Update your username to search for in  `main.py`.

## Steps to run
1. Upload screenshots to `/images` folder.
2. Run main.py with `python main.py`
3. Program will output the tabulated scores for multiple games in the Terminal itself.
5. Separate;y, a `scores.csv` file will be created which will be used for keeping track of historical scores.
