"""
Simple script to help us fill out the "Past Papers" section on the CJC wiki

Need to:

pip install pyperclip

"""

import webbrowser
import pyperclip

from sheetfinder import download_speaker_csv
from sendmail import get_past_dico

if __name__ == '__main__':
    download_speaker_csv()
    dico = get_past_dico()

    to_paste = (f"{dico['date']}" + '\n' +
                f"{dico['speaker']}, {dico['topic']}, @ Zoom, at 5:00pm" + '\n')
    
    pyperclip.copy(to_paste)
    print('Unformatted info is ready to paste')
    
    past_paper_url = 'https://wiki.harvard.edu/confluence/pages/editpage.action?pageId=212907933'
    webbrowser.open(past_paper_url)
