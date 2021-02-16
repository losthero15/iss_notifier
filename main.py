import requests
from datetime import datetime
import smtplib
import time
from os import system, name

MY_EMAIL = "___YOUR_EMAIL_HERE____"
MY_PASSWORD = "___YOUR_PASSWORD_HERE___"
SMTP_ADDRESS = "___YOUR_SMTP_SERVER_ADDRESS_HERE___"
MY_LAT = 51.507351  # Your latitude in float
MY_LONG = -0.127758  # Your longitude in float


def clear():  # define our clear function
    # for windows
    if name == 'nt':
        _ = system('cls')

    else:  # for mac and linux(here, os.name is 'posix')
        _ = system('clear')


def is_iss_overhead():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    # Your position is within +5 or -5 degrees of the iss position.
    if MY_LAT - 5 <= iss_latitude <= MY_LAT + 5 and MY_LONG - 5 <= iss_longitude <= MY_LONG + 5:
        return True


def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    if is_iss_overhead() and is_night():
        try:
            connection = smtplib.SMTP(SMTP_ADDRESS)
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject:Look Up👆\n\nThe ISS is above you in the sky."
            )
        except():
            print("Look Up👆\n\nThe ISS is above you in the sky.")
    else:
        print(
            f"International Space Station (ISS) Notifier\n\nProgram is running...\nCurrent time: {datetime.now().hour}:{datetime.now().minute}\n\n")
    time.sleep(60)
    clear()
