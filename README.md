This guide explains how to download the project ZIP, set it up, and run the Streamlit application on Windows or macOS.

1. 📥 Download the ZIP

Download the project ZIP provided by the workshop instructor.

Windows

Right-click the downloaded .zip file.

Select Extract All...

Extract the project to a convenient location.

Example:

Desktop/
└── agentic_ai_live_demo/

macOS

Double-click the downloaded .zip file.

macOS will automatically extract the folder.

Open the extracted project folder.

2. 🧑‍💻 Open the Project in VS Code

Open VS Code.

Go to:

File → Open Folder

Select the extracted project folder.

You should see files such as:

demo.py
requirements.txt
.env.example
README.md

Now open:

Terminal → New Terminal

🪟 WINDOWS

3. Check Python

Run:

py --version

Recommended:

Python 3.11

or

Python 3.12

If you have multiple Python versions:

py --list

Python 3.8 is not recommended for this project.

4. Create a Virtual Environment

For Python 3.12:

py -3.12 -m venv .venv

For Python 3.11:

py -3.11 -m venv .venv

5. Activate the Virtual Environment

Run:

.\.venv\Scripts\Activate.ps1

You should now see:

(.venv)

at the beginning of your terminal.

If PowerShell blocks activation

Run:

Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

Then:

.\.venv\Scripts\Activate.ps1

6. Install Dependencies

Run:

python -m pip install --upgrade pip

Then:

pip install -r requirements.txt

Wait until the installation finishes.

🍎 macOS

3. Check Python

Run:

python3 --version

Recommended:

Python 3.11

or

Python 3.12

4. Create a Virtual Environment

For Python 3.12:

python3.12 -m venv .venv

For Python 3.11:

python3.11 -m venv .venv

If python3 already points to Python 3.11/3.12:

python3 -m venv .venv

5. Activate the Virtual Environment

Run:

source .venv/bin/activate

You should see:

(.venv)

at the beginning of your terminal.

6. Install Dependencies

Run:

python -m pip install --upgrade pip

Then:

pip install -r requirements.txt

🔑 7. Add Your Groq API Key

The application uses a Groq API key.

In the project folder, create a copy of:

.env.example

and rename it:

.env

Open .env and add:

GROQ_API_KEY=your_groq_api_key_here

Replace the placeholder with your actual API key.

⚠️ IMPORTANT

Never share your API key and never upload .env to GitHub.

🚀 8. Run the Streamlit App

Make sure your virtual environment is activated.

You should see:

(.venv)

in the terminal.

Windows

python -m streamlit run demo.py

macOS

python -m streamlit run demo.py

Streamlit should display something similar to:

Local URL: http://localhost:8501

Open this address in your browser:

http://localhost:8501

You should now see the Agentic AI Crew application.

🛑 9. Stop the Application

To stop Streamlit:

Ctrl + C

in the terminal.

🔄 10. Run the App Again Later

You do not need to reinstall everything.

Windows

.\.venv\Scripts\Activate.ps1
python -m streamlit run demo.py

macOS

source .venv/bin/activate
python -m streamlit run demo.py

Then open:

http://localhost:8501

🐛 Troubleshooting

ModuleNotFoundError: No module named 'streamlit'

Make sure the virtual environment is activated.

Then run:

pip install -r requirements.txt

ModuleNotFoundError: No module named 'crewai'

Run:

pip install -r requirements.txt

Then verify:

python -c "import crewai; print('CrewAI installed successfully')"

ModuleNotFoundError: No module named 'dotenv'

Run:

pip install python-dotenv

Python version problem

Check:

Windows

py --list

macOS

python3 --version

Use Python 3.11 or 3.12.

If the virtual environment was created using the wrong Python version, delete .venv and create it again with Python 3.11/3.12.

Groq API Key Error

Check that:

.env

exists in the same folder as demo.py.

It should contain:

GROQ_API_KEY=your_actual_key

After changing .env, stop Streamlit with:

Ctrl + C

and start it again:

python -m streamlit run demo.py

Rate Limit / 429 Error

This means the Groq API has temporarily reached a usage limit.

Try:

Wait a little.

Run the task again.

Avoid repeatedly clicking Run Task.

Use your own Groq API key rather than sharing one key with the entire class.

Browser Does Not Open

If Streamlit is running but the browser does not open automatically, manually go to:

http://localhost:8501

Streamlit Command Not Found

Instead of:

streamlit run demo.py

use:

python -m streamlit run demo.py

This ensures Streamlit runs from the active Python environment.

✅ Quick Start

Once everything is installed:

Windows

.\.venv\Scripts\Activate.ps1
python -m streamlit run demo.py

macOS

source .venv/bin/activate
python -m streamlit run demo.py

Then open:

http://localhost:8501

🎉 You're ready to build your Agentic AI application!
