# Installation Guide for Philippine Utility Tools

This guide will help you set up and run the Philippine Utility Tools application on your computer.

## Prerequisites

Before you begin, you need to have Python installed on your computer. This application requires Python 3.7 or higher.

### Installing Python

1. Download Python from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check the box that says "Add Python to PATH" during installation
4. Complete the installation

## Setting Up the Application

### Method 1: Using the Batch File (Windows)

1. Simply double-click the `run_app.bat` file in the project folder
2. The script will:
   - Check if Python is installed
   - Install required packages
   - Download necessary NLTK resources
   - Start the application

3. If everything is successful, the application will start and you can access it at [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your web browser

### Method 2: Manual Setup

If you prefer to set up the application manually or if you're using macOS or Linux, follow these steps:

1. Open a terminal or command prompt
2. Navigate to the project directory:
   ```
   cd path/to/project
   ```

3. Create a virtual environment (optional but recommended):
   ```
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. Install the required packages:
   ```
   # Windows
   python -m pip install -r requirements.txt

   # macOS/Linux
   python3 -m pip install -r requirements.txt
   ```

5. Download NLTK resources:
   ```
   # Windows
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

   # macOS/Linux
   python3 -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

6. Run the application:
   ```
   # Windows
   python app.py

   # macOS/Linux
   python3 app.py
   ```

7. Open your web browser and go to [http://127.0.0.1:5000/](http://127.0.0.1:5000/)

## Troubleshooting

### "Python is not recognized as an internal or external command"

This error means Python is not in your PATH. Try:
- Reinstalling Python and make sure to check "Add Python to PATH"
- Or manually add Python to your PATH environment variable

### "No module named 'flask'" or other missing modules

This means the required packages are not installed. Run:
```
python -m pip install -r requirements.txt
```

### "Port 5000 is already in use"

Another application is using port 5000. You can:
- Close the other application
- Or modify the `app.py` file to use a different port:
  ```python
  if __name__ == '__main__':
      app.run(debug=True, port=5001)  # Change 5001 to any available port
  ```

## Need Help?

If you encounter any issues during installation or while using the application, please refer to the README.md file or contact the developer for assistance.