# Contact Manager

A simple desktop application for managing your contacts, built with Python and Tkinter.

## Features

- Add, edit, and delete contacts
- Store contact information (name, email, phone)
- Track last contact date
- Modern, native-looking interface that works on macOS
- Data is stored locally in a JSON file

## Setup

1. Make sure you have Python 3.x installed on your system
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python app.py
   ```

## Usage

- To add a contact: Fill in the fields at the bottom and click "Add Contact"
- To edit a contact: Select a contact from the list, modify the fields, and click "Update Contact"
- To delete a contact: Select a contact and click "Delete Contact"

## Data Storage

All contact data is stored in a `contacts.json` file in the same directory as the application. The data is automatically saved whenever you make changes. 