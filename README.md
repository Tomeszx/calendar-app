# custom-api
 
The purpose of this app is scheduling events and integration with Google Calendar.
- The client could schedule some event if the maximum amount of events in this day is not exceeded (setup in config file).
- Then the owner can accept or decline the event via Google Calendar.
- All actions will be visible in this app.

<img width="600" alt="Zrzut ekranu 2024-06-29 o 16 26 02" src="https://github.com/Tomeszx/calendar-app/assets/91263441/de15b3e3-a8dc-4729-9ddc-304d759a3ac8">
<img width="600" alt="Zrzut ekranu 2024-06-29 o 16 26 42" src="https://github.com/Tomeszx/calendar-app/assets/91263441/183d1253-4295-4d91-9d2f-51b27c6159fa">
<img width="600" alt="Zrzut ekranu 2024-06-29 o 16 27 07" src="https://github.com/Tomeszx/calendar-app/assets/91263441/3c34318e-dff0-4dea-b5e2-626faa0480b8">

## How to run the app locally
- You need to get the oauth2 file from Google.
- Update the config.
- Then run this command:
```
pip install -r requirements.txt
```
```
uvicorn main:app
```
