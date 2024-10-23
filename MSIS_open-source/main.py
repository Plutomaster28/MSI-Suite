import os
import importlib
import shared_credentials


def is_valid_license_key(key, valid_keys):
  return key in valid_keys


def copy_prevent():
  valid_license_keys = [
      "KDwJX7PkvnAU0RHd", "7Fze4iNq0FQDZnPu", "NkNb8bkw4zG5fPmx",
      "JvnJA4D9g4BK2pWK", "3aFfeBKPs5oUrzjg", "VNAMdXpf4NmpDVhM",
      "vjJpW6H7VxF1JjbE", "5yoScnP8FMhmnjUz", "hPuFUKN7PvMDi1ZY",
      "Cu4ASE8HWCzSvCfi", "test"
  ]

  while True:
    user_input = input("Enter license key: ")
    if is_valid_license_key(user_input, valid_license_keys):
      print("\nLicense key is valid. Thank you for using our software.")
      break
    else:
      print("\nError: Invalid license key. Please try again.")


#--------------------------------------------------------------------------------------


def enter_credentials():
  shared_credentials.username = input("\nEnter your username: ")
  #shared_credentials.password = input("Enter your password: ")


#--------------------------------------------------------------------------------------


def load_program(location):
  if location == "US":
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
    print("\nWelcome!", shared_credentials.username, "!")
    us_data_module = importlib.import_module("united_states_pack")
    us_data_module.load_us_data()
  elif location == "JA":
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
    print("\nようこそ！", shared_credentials.username, "!")
    japan_pack_module = importlib.import_module("japan_pack")
    japan_pack_module.load_japan_data()
  else:
    print("\nInvalid location, please make a proper selection.")


def return_dummy_menu():
  print("\nWelcome to the Zora Suite Setup!",
        shared_credentials.username, "!")
  location_input = input("\nWhat is your location? [US/JA]").strip().upper()
  load_program(location_input)


def main():
  copy_prevent()
  enter_credentials()
  print("\nWelcome to the Zora Suite Setup!",
        shared_credentials.username, "!")
  location_input = input("\nWhat is your location? [US/JA]").strip().upper()
  load_program(location_input)


if __name__ == "__main__":
  main()
