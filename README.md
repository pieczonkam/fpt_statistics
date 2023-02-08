#fpt_statistics

Python app for analysis of automotive related data (could be easily adjusted to analyze any other kind of data).

## Setup
To install necessary dependencies, run command:
```
pip install -r requirements.txt
```
To run the app, execute following command:
```
python3 main.py
```
The app can also be built as a single file executable, using Pyinstaller (requires changing paths in ```main.spec``` file):
```
pyinstaller main.spec
```

## Functionalities
- Load Excel data
- Show data in table
- Show data on 2D and 3D plots
- Adjust parameters (e.g. select ceratin rows, choose date range)
- Save plots to file

## Screenshots
<img src="/screenshots/main_menu.jpg" />
<img src="/screenshots/tth.jpg" />
<img src="/screenshots/3dc.jpg" />
