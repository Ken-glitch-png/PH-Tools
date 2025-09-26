# Philippine Utility Tools

A web application that provides various utility tools for Philippine users, including phone number validation, email phishing detection, and (planned) geolocation tracking.

## Features

### Current Features

1. **Philippine Phone Number Validation**
   - Validate if a number is a legitimate Philippine mobile number
   - Identify the provider (Globe, Smart, DITO, etc.)
   - Format the number correctly

2. **Email Phishing Detection**
   - Analyze email content for phishing indicators
   - Identify suspicious links and keywords
   - Provide a confidence score for phishing detection
   - Explain why an email might be suspicious

### Planned Features

1. **Geolocation Tracking**
   - Track the location of Philippine phone numbers
   - Provide map visualization
   - Offer historical location data
   - Support location-based alerts

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd philippine-utility-tools
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Download NLTK resources (for email phishing detection):
   ```python
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
   ```

5. Create a `.env` file in the project root with the following content:
   ```
   SECRET_KEY=your-secret-key
   ```

## Usage

1. Start the Flask development server:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://127.0.0.1:5000/
   ```

## Project Structure

```
philippine-utility-tools/
├── app.py                  # Main Flask application
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this file)
├── services/               # Service modules
│   ├── __init__.py
│   ├── phone_validator.py  # Phone number validation service
│   └── email_checker.py    # Email phishing detection service
├── static/                 # Static files
│   ├── css/
│   │   └── style.css       # Custom CSS styles
│   └── js/
│       └── main.js         # Custom JavaScript
└── templates/              # HTML templates
    ├── base.html           # Base template
    ├── index.html          # Home page
    └── about.html          # About page
```

## Technologies Used

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Libraries**: 
  - phonenumbers (for phone validation)
  - NLTK (for natural language processing)
  - BeautifulSoup (for HTML parsing)
  - scikit-learn (for machine learning components)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- [phonenumbers](https://github.com/daviddrysdale/python-phonenumbers) library for phone number validation
- [NLTK](https://www.nltk.org/) for natural language processing
- [Bootstrap](https://getbootstrap.com/) for frontend styling