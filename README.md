# chiliserver
This project is used for recording values from greenhouse where chilis are grown.
All files in this repository is for a server and esp32. Frontend files are in a different repository called chili-ui.\n
Server features:
- Listens requests from frontend and esp32
- Communicates with postgres database
- Handles communication between frontend and esp32

Esp32 features:
- Records required data using sensors
- Every minute it sends sensor values to the server in json format
- Updates state of the outlets with data from the server
