# TimetableUI
An app that allows you to view or change your class schedule.</br>
Written in Python using PostgreSQL and PyQt5:
```python
import psycopg2
import sys
from datetime import datetime, date

from PyQt5.QtWidgets import (QApplication, QWidget, QTabWidget, QAbstractScrollArea, QVBoxLayout, QHBoxLayout, QTableWidget,
                             QGroupBox, QTableWidgetItem, QPushButton, QMessageBox, QAbstractButton, QButtonGroup)
```
## App interface
![image](https://user-images.githubusercontent.com/90320303/146548585-7dd45684-8a90-44ae-b16c-9938378dfae2.png)
