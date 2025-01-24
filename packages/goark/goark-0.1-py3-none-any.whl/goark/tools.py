#todo tomorrow:
#Update the input format to accomodate for the tests
# Create the python client
# Reach out to reddit.

tools_100 = {
    "Create Folder": "Creates a folder in a file storage service. Input: folder name, location. Action: Creates the folder at the specified location.",
    "Upload File": "Uploads a file to a cloud storage service. Input: file path, destination folder. Action: Uploads the file to the chosen folder.",
    "Commit to Repository": "Commits changes to a GitHub repository. Input: repository URL, commit message. Action: Pushes the changes to the repository with the given commit message.",
    "Send Email": "Sends an email to a recipient. Input: recipient email, subject, body, attachments (optional). Action: Delivers the email with the specified details.",
    "Schedule Meeting": "Schedules a meeting on a calendar. Input: meeting date, time, participants, duration, description. Action: Creates a calendar event and invites participants.",
    "Generate Report": "Generates a detailed report. Input: report type, data source, formatting preferences. Action: Outputs a formatted report.",
    "Translate Text": "Translates text from one language to another. Input: source language, target language, text. Action: Returns the translated text.",
    "Search Web": "Performs a web search. Input: query string. Action: Returns a list of relevant search results.",
    "Summarize Text": "Summarizes a given block of text. Input: text, summary length. Action: Outputs a concise summary.",
    "Book Appointment": "Books an appointment on behalf of a user. Input: date, time, location, service. Action: Confirms the appointment with the provider.",
    "Retrieve Weather Information": "Gets current weather data. Input: location, date (optional). Action: Returns weather details for the specified location.",
    "Create To-Do List": "Creates a new to-do list. Input: list name, items. Action: Creates and populates the list with items.",
    "Set Reminder": "Sets a reminder for a specific time and date. Input: reminder message, time, recurrence (optional). Action: Triggers a notification at the specified time.",
    "Fetch Stock Prices": "Retrieves stock market data. Input: stock symbol, date range (optional). Action: Returns stock prices or performance data.",
    "Analyze Sentiment": "Analyzes the sentiment of text. Input: text. Action: Outputs the sentiment (positive, neutral, negative).",
    "Run Code": "Executes a code snippet. Input: programming language, code. Action: Runs the code and returns the output.",
    "Generate Diagram": "Creates a diagram from input parameters. Input: diagram type, data, labels. Action: Outputs a graphical representation.",
    "Create Presentation": "Creates a slide presentation. Input: template, content. Action: Outputs a ready-to-edit slide deck.",
    "Optimize Image": "Reduces the size or improves quality of an image. Input: image file, optimization level. Action: Returns the optimized image.",
    "Perform OCR": "Extracts text from an image. Input: image file. Action: Returns the extracted text.",
    "Commit to Repository": "Commits changes to a GitHub repository. Input: repository URL, commit message. Action: Pushes the changes to the repository with the given commit message.",
    "Send Email": "Sends an email to a recipient. Input: recipient email, subject, body, attachments (optional). Action: Delivers the email with the specified details.",
    "Schedule Meeting": "Schedules a meeting on a calendar. Input: meeting date, time, participants, duration, description. Action: Creates a calendar event and invites participants.",
    "Generate Report": "Generates a detailed report. Input: report type, data source, formatting preferences. Action: Outputs a formatted report.",
    "Translate Text": "Translates text from one language to another. Input: source language, target language, text. Action: Returns the translated text.",
    "Search Web": "Performs a web search. Input: query string. Action: Returns a list of relevant search results.",
    "Summarize Text": "Summarizes a given block of text. Input: text, summary length. Action: Outputs a concise summary.",
    "Book Appointment": "Books an appointment on behalf of a user. Input: date, time, location, service. Action: Confirms the appointment with the provider.",
    "Retrieve Weather Information": "Gets current weather data. Input: location, date (optional). Action: Returns weather details for the specified location.",
    "Create To-Do List": "Creates a new to-do list. Input: list name, items. Action: Creates and populates the list with items.",
    "Set Reminder": "Sets a reminder for a specific time and date. Input: reminder message, time, recurrence (optional). Action: Triggers a notification at the specified time.",
    "Fetch Stock Prices": "Retrieves stock market data. Input: stock symbol, date range (optional). Action: Returns stock prices or performance data.",
    "Analyze Sentiment": "Analyzes the sentiment of text. Input: text. Action: Outputs the sentiment (positive, neutral, negative).",
    "Run Code": "Executes a code snippet. Input: programming language, code. Action: Runs the code and returns the output.",
    "Generate Diagram": "Creates a diagram from input parameters. Input: diagram type, data, labels. Action: Outputs a graphical representation.",
    "Create Presentation": "Creates a slide presentation. Input: template, content. Action: Outputs a ready-to-edit slide deck.",
    "Optimize Image": "Reduces the size or improves quality of an image. Input: image file, optimization level. Action: Returns the optimized image.",
    "Perform OCR": "Extracts text from an image. Input: image file. Action: Returns the extracted text.",
    "Calculate Metrics": "Computes specific metrics from data. Input: data source, metric type. Action: Outputs calculated metrics.",
    "Fetch News Articles": "Retrieves recent news articles. Input: topic, date range (optional). Action: Returns a list of news articles.",
    "Export Data": "Exports data from a source. Input: data type, format (CSV, JSON, etc.). Action: Provides the exported file.",
    "Generate Password": "Creates a strong password. Input: length, complexity preferences. Action: Outputs a generated password.",
    "Validate Email Address": "Checks if an email address is valid. Input: email address. Action: Returns a validity status.",
    "Process Payment": "Processes a payment through a gateway. Input: amount, currency, payment method. Action: Confirms the payment.",
    "Book Hotel": "Books a hotel room. Input: check-in date, check-out date, location, preferences. Action: Confirms the reservation.",
    "Set Timer": "Sets a countdown timer. Input: duration. Action: Notifies when the timer ends.",
    "Create Poll": "Creates a poll for voting. Input: question, options, duration (optional). Action: Shares the poll for responses.",
    "Track Package": "Tracks the status of a shipment. Input: tracking number. Action: Returns shipment status.",
    "Encrypt File": "Encrypts a file for security. Input: file path, encryption key. Action: Outputs an encrypted file.",
    "Decrypt File": "Decrypts an encrypted file. Input: file path, decryption key. Action: Outputs the original file.",
    "Generate Invoice": "Creates an invoice for a transaction. Input: customer details, transaction details. Action: Outputs a formatted invoice.",
    "Stream Video": "Streams a video file. Input: video URL, resolution (optional). Action: Plays the video.",
    "Monitor Server": "Checks server status. Input: server IP or URL. Action: Returns status details.",
    "Analyze Log Files": "Extracts insights from log files. Input: log file, query criteria. Action: Returns analyzed data.",
    "Clean Data": "Removes inconsistencies from data. Input: dataset, rules. Action: Outputs cleaned data.",
    "Merge Documents": "Combines multiple documents into one. Input: files to merge, output format. Action: Returns a single merged file.",
    "Generate Chart": "Creates a chart from data. Input: chart type, data, labels. Action: Outputs the chart.",
    "Send SMS": "Sends an SMS message. Input: recipient phone number, message. Action: Sends the text.",
    "Convert File Format": "Converts a file to a different format. Input: file path, target format. Action: Outputs the converted file.",
    "Scrape Website": "Extracts data from a website. Input: URL, data pattern. Action: Returns extracted data.",
    "Simulate Workflow": "Tests a workflow for debugging. Input: workflow steps, test data. Action: Simulates and reports results.",
    "Auto-Complete Form": "Fills a form automatically. Input: form fields, values. Action: Populates the form.",
    "Schedule Social Post": "Schedules a social media post. Input: platform, content, schedule time. Action: Posts at the specified time.",
    "Parse JSON": "Extracts data from a JSON object. Input: JSON object, query. Action: Returns extracted data.",
    "Run Query": "Executes a database query. Input: query, database credentials. Action: Returns query results.",
    "Generate API Token": "Creates an API token for authentication. Input: service details, validity period. Action: Outputs the token.",
    "Convert Currency": "Converts one currency to another. Input: amount, source currency, target currency. Action: Outputs converted value.",
    "Check Domain Availability": "Checks if a domain is available. Input: domain name. Action: Returns availability status."
}

from langchain_core.tools import StructuredTool

def multiply_structured_tool(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

async def amultiply_structured_tool(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

def generate_test_functions(test_names_descriptions, framework = "langchain"):
  test_functions = []
  for name, description in test_names_descriptions.items():
    function = StructuredTool.from_function(func=multiply_structured_tool, name = name, description = description, coroutine=amultiply_structured_tool)
    test_functions.append(function)
  return test_functions

test_data = generate_test_functions(tools_100)
api_keys = []
