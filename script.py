import argparse
from datetime import datetime
from tweet import tweet

parser = argparse.ArgumentParser()
parser.add_argument("--force", help="ignores the specified tweet hours", action="store_true")
args = parser.parse_args()

TWEET_HOURS = (6, 8, 10, 12, 14, 16, 18, 20, 22)

if datetime.now().hour in TWEET_HOURS or args.force:
    print('Attemping tweet.')
    tweet()
else:
    print('Triggered but not attempting tweet.')