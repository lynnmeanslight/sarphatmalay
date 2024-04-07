from colorama import just_fix_windows_console
from termcolor import colored
from libgen_api import LibgenSearch
from tqdm import tqdm
import shutil
import requests
import os


def print_dot_dashed_line(color='green'):
    terminal_width = shutil.get_terminal_size().columns
    line = '-' * (terminal_width // 2)
    dashed_line = '-'.join(line[i:i+2] for i in range(0, len(line), 2))
    colored_line = colored(dashed_line, color)
    print(colored_line)
    
def getTheBookByBookId(books,bookId):
    for book in books:
        if book["ID"]==bookId:
            return book

def downloadBook(url,bookFileName):
    response = requests.get(url,stream=True)
    if response.status_code == 200:
        total_size = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size, unit='iB', unit_scale=True)
        folder_path=os.path.join(os.getcwd(),"downloads")
        checkDownloadDirExists = os.path.exists(folder_path) and os.path.isdir(folder_path)
        if not checkDownloadDirExists:
            os.mkdir("downloads")
        with open("downloads/"+bookFileName, "wb") as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        print("File downloaded successfully.")
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
    
# use Colorama to make Termcolor work on Windows too
just_fix_windows_console()
s = LibgenSearch()

print(colored('Welcome To SarPhatMal.\nIt is just a cli decoration of https://github.com/harrison-broadbent/libgen-api', 'green', 'on_black'))
book_title=input(colored('Enter the title of your desired book : ','white','on_green'))
while book_title!="exit":
    results = s.search_title(book_title)
    for result in results:
        print_dot_dashed_line()
        print("""
ID          : {}
Title       : {}
Author      : {}
Year        : {}
Size        : {}
Extension   : {}
          """.format(result["ID"],result["Title"],result["Author"],result["Year"],result["Size"],result["Extension"]))
        print_dot_dashed_line()
    bookId=input(colored("Enter the book ID to get the download links : "))
    desired_book=getTheBookByBookId(results,bookId)
    bookFileName= desired_book["Title"].lower() + desired_book["ID"].lower() + "." + desired_book["Extension"].lower()
    download_links = s.resolve_download_links(desired_book)
    downloadBook(download_links["GET"],bookFileName)
    book_title=input(colored('Enter the title of your desired book : ','white','on_green'))









