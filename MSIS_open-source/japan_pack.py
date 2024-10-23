from datetime import datetime

import pytz
import calendar
import requests
import pygame
import os
import importlib
import random
import sys

import language_pack_ja
from main import return_dummy_menu
import shared_credentials

folder_path = "zk_sys"

def easter_egg(outputs):
  print(outputs["easter_egg"])

def basic_shell(files):
  should_return = False
  while True:
    input_text = input("$ ")
    if input_text == "exit":
      should_return = True
      break
    elif input_text == "view":
      view_files()
    elif input_text == "create":
      filename = input("作成するファイル名を入力してください: ")
      create_file(filename)
      files.append(filename)
    elif input_text == "delete":
      filename = input("削除するファイル名を入力してください: ")
      delete_file(filename)
      if filename in files:
        files.remove(filename)
    else:
      if input_text:
        print("エラー: 不明なコマンド")
  return should_return


def create_file(filename):
  file_path = os.path.join(folder_path, filename)
  with open(file_path, 'w'):
      pass
  print(f"ファイル {filename} 正常に {folder_path} フォルダに作成されました。")


def delete_file(filename):
  file_path = os.path.join(folder_path, filename)
  try:
    os.remove(file_path)
    print(f"ファイル {filename} 正常に {folder_path} フォルダから削除されました。")
  except OSError as e:
    print(f"ファイル削除エラー: {e}")


def view_files():
  print(f"{folder_path} フォルダに保存されているファイル:")
  files = os.listdir(folder_path)
  if not files:
    print("ファイルが見つかりませんでした。")
  else:
    for file in files:
      print(file)


def file_explorer():
  files = []
  while True:
    print(
        "ファイル エクスプローラー メニュー:\n1. ファイルの作成\n2. ファイルを削除する\n3. ビューファイル\n4. メインメニューに戻る"
    )
    choice = input("選択内容を入力してください： ")
    if choice == '1':
      filename = input("作成するファイル名を入力してください: ")
      create_file(filename)
      files.append(filename)
    elif choice == '2':
      filename = input("削除するファイル名を入力してください: ")
      delete_file(filename)
      if filename in files:
        files.remove(filename)
    elif choice == '3':
      view_files()
    elif choice == '4':
      print("\nメインメニューに戻る...")
      break
    else:
      print("\n無効な選択です。 もう一度試してください。")


def clear_screen():  #clears screen, find way to implement
  os.system('cls' if os.name == 'nt' else 'clear')


#buffer zone------------------------------------------------------------------------
def get_weather(city_name, api_key):
  outputs = language_pack_ja.ja_translation()
  url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name},JP&appid={api_key}&units=metric"
  response = requests.get(url)
  data = response.json()
  if data["cod"] == 200:
    weather_description = data["weather"][0]["description"]
    temperature = data["main"]["temp"]
    print(
        f"{outputs['weather_in']} {city_name}: {weather_description}, {outputs['temperature']}: {temperature}°C"
    )
  else:
    print(outputs["weather_nonavailable"])


def display_jap_calander():
  outputs = language_pack_ja.ja_translation()
  year = int(input(outputs["year_character"]))
  month = int(input(outputs["month_character"]))

  # Create a calendar instance
  cal = calendar.TextCalendar(calendar.SUNDAY)

  # Get the calendar for the specified month
  month_calendar = cal.formatmonth(year, month)

  # Print the calendar
  print(month_calendar)


def get_news(api_key='PLACE_HOLDER'): # service has been shut down

  url = 'https://newsapi.org/v2/top-headlines'
  params = {'country': 'jp', 'apiKey': api_key}

  try:
    # Fetch top headlines from Japan
    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] == 'ok':
      articles = data['articles']

      if not articles:
        print("No articles found.")
        return

      # Print out the news
      print("Top News from Japan:")
      for article in articles:
        print(f"Title: {article['title']}")
        print(f"Source: {article['source']['name']}")
        print(f"Description: {article['description']}")
        print(f"URL: {article['url']}")
        print()
    else:
      print(f"Error: {data['message']}")

  except Exception as e:
    print(f"An error occurred while fetching news: {e}")


def play_music(music_directory):
  try:
    pygame.mixer.init()
    pygame.mixer.music.set_volume(1.0)

    if not pygame.mixer.get_init():
      print("Error initializing mixer. Please check your audio settings.")
      return

    music_files = [
        f for f in os.listdir(music_directory)
        if f.endswith('.mp3') or f.endswith('.wav')
    ]

    if not music_files:
      print("No music files found in the directory.")
      return

    random.shuffle(music_files)

    for music_file in music_files:
      print(f"Playing: {music_file}")
      pygame.mixer.music.load(os.path.join(music_directory, music_file))
      pygame.mixer.music.play()

      while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

  except pygame.error as e:
    print(f"An error occurred while playing music: {e}")

  finally:
    pygame.mixer.quit()


def get_time_in_japan():
  japan_timezone = pytz.timezone("Asia/Tokyo")
  japan_time = datetime.now(japan_timezone)
  return japan_time


def display_time_in_japan(outputs):
  japan_time = get_time_in_japan()
  formatted_time = japan_time.strftime("%Y-%m-%d %H:%M:%S %Z")
  print(outputs["the_time_is"], formatted_time)


def load_japan_data():
  outputs = language_pack_ja.ja_translation()
  while True:
    username = shared_credentials.username
    if username == "Miyamii":
      easter_egg(outputs)
    display_time_in_japan(outputs)
    print(outputs["what_will_we_be_doing_today?"])
    print(outputs["weather"], outputs["calander"], outputs["radio"],
          outputs["news"], outputs["file_explorer"], outputs["user_shell"],
          outputs["user_details"], outputs["exit"], outputs["return"])
    option_picked = input(outputs["input_choice_here"])

    if option_picked == "weather":

      api_key = "PLACE_HOLDE" #service has been shut down
      city_name = input(outputs["enter_city"])
      get_weather(city_name, api_key)
    elif option_picked == "calendar":
      display_jap_calander()
    elif option_picked == "music":
      pygame.init()
      music_directory = "music/ja_music"
      play_music(music_directory)
    elif option_picked == "news":
      get_news()
    elif option_picked.lower() == "n":
      print("Returning to main menu...")
      break
    elif option_picked.lower() == "exit":
      print("Exiting...")
      clear_screen()
      sys.exit(0)
    elif option_picked == "files":
      file_explorer()
    elif option_picked == "shell":
      files = []
      basic_shell(files)
    elif option_picked == "user details":
      print("Username:", shared_credentials.username)
      #print("Password:", shared_credentials.password)
    elif option_picked == "return":
      dummy_menu = importlib.import_module("main")
      dummy_menu.return_dummy_menu()
      clear_screen()
    else:
      print("Invalid option")
