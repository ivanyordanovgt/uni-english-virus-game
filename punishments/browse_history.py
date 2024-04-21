import getpass
import sqlite3
import shutil
import os
import time
import pyautogui
pyautogui.PAUSE = 0


def get_windows_username():
    return getpass.getuser()


def read_chrome_history():
    data_path = f"C:\\Users\\{get_windows_username()}\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\History"
    history_path = os.path.join(os.path.dirname(data_path), 'copy_history')

    if os.path.exists(history_path):
        os.remove(history_path)
    shutil.copy(data_path, history_path)
    connection = sqlite3.connect(history_path)
    cursor = connection.cursor()

    query = """
        SELECT url, title, visit_count, last_visit_time
        FROM urls
        ORDER BY last_visit_time DESC
    """

    try:
        cursor.execute(query)
        results = cursor.fetchall()
        string = ""
        for url, title, visit_count, last_visit_time in results:
            print(f"Title: {title}, Visits: {visit_count}, Last Visit: {last_visit_time}")
            string += f"Title: {title}, Visits: {visit_count}" + "\n"
        return string
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    cursor.close()
    connection.close()


import webbrowser


def punish_browse_history():
    url = 'https://www.facebook.com'
    webbrowser.open(url)
    time.sleep(2)
    pyautogui.click(x=841, y=285)
    time.sleep(2)
    if __name__ == "__main__":
        history = read_chrome_history().split(" ")
        for string in history:
            pyautogui.typewrite(string)
            pyautogui.moveTo(x=5, y=5)
    time.sleep(3)
    pyautogui.click(x=986, y=966)

# punish_browse_history()
