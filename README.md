License Plate Recognition System
Description
Application for automatic license plate recognition from video stream. It processes video in real time, extracts license plate text, checks license plate numbers for correctness and saves the results (text and image) to SQL Server database.

Main functions
Real-time video stream capture from a camera.
License plate license plate detection using Haar classifier.
License plate text recognition using EasyOCR.
Saving recognized license plates and their images in SQL Server database.
User-friendly graphical user interface (GUI) based on Tkinter.

Installation
Requirements
Python 3.8 or newer
SQL Server (customized database)
Dependencies installed (see below)
Installing dependencies
Make sure you have pip installed.

Install the required libraries:

pip install -r requirements.txt
Create a requirements.txt file with the contents:
opencv-python
easyocr
pillow
pyodbc
Make sure that the Haar classifier file haarcascade_russian_plate_number.xml is in the root folder of the project. It can be downloaded from the official OpenCV repository.

Database setup
Create a table in SQL Server to save the recognized numbers:

sql
CREATE TABLE NumberPlates (
    ID INT IDENTITY(1,1) PRIMARY KEY,
    PlateNumber NVARCHAR(50),
    ImagePath NVARCHAR(255)
);
Change the connection parameters in the code:

conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=YOUR_SERVER;'
    'DATABASE=YOUR_DATABASE;'
    'Trusted_Connection=yes;'
)
Startup
Make sure all dependencies are installed and the database is configured.
Run the application:
python main.py

Project structure
.
├─── main.py # Main project file
├─── haarcascade_russian_plate_number.xml # Haar Classifier
├──── IMAGES/ # Folder for saving license plate images
├──── requirements.txt # Dependencies
└─── README.md # Project documentation
How to use
Click the Start Detection button to turn on the camera.
The program will start detecting license plates and saving them to the database.
The recognized license plates are displayed in the Matched License Plates list.
Press the Esc key to exit the program.
Opportunities for improvement
Improvement of recognition accuracy using more powerful models (e.g. YOLO).
Adding video upload functionality.
Introduction of advanced camera and user interface settings.
License
The project is available under the MIT License.
