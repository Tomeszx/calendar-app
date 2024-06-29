# custom-api
 
The purpose of this app is scheduling events and integration with Google Calendar. 
The client could schedule some event if the maximum amount of events in this day is not exceeded (setup in config file).
Then the owner can accept or decline the event in Google Calendar.
All actions will be visible in this app.


## How to run the app locally
`uvicorn main:app`