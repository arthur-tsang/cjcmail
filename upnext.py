"""
Simple script to help us fill out the "Up Next" section on the CJC wiki

Need to:

pip install pyperclip


"""

import webbrowser
import pyperclip # automatically copies formatted text into clipboard

from sheetfinder import download_speaker_csv
from sendmail import get_today_dico

if __name__ == '__main__':
    download_speaker_csv()
    dico = get_today_dico()

    to_paste = f"{dico['date']}    {dico['speaker']}"
    pyperclip.copy(to_paste)
    print('Speaker date and name are ready to paste')

    up_next_url = 'https://wiki.harvard.edu/confluence/pages/editpage.action?pageId=212907948'
    webbrowser.open(up_next_url)
