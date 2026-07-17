# Personal Finance Calcuator & Budgeter

This application was made so you can easily and freely input your income and adjust different setting to figure out where you should allocate your funds for certain pay periods. I made this specifically because I've been recently getting very into saving and getting into good spending habits.
On top of that it solved my problem with having to manually do every calculation on my phone after each paycheck and also allowed me to learn Python and SQL with it.

### Pre-Requisites:
  Python 3.10 - 3.13
  Google AI Studio developer API key (If you want to use integrated AI chatbot)

### Installations & Dependicies:
  git clone http://github.com/Jackson-Link/personal-finance-dashboard.git
  cd personal-finance-dashboard
  pip install streamlit google-genai python-dotenv httpx

### Integrated AI Chatbot:
  touch .env #Creates a .env file
  Add GEMINI_API_KEY=your_api_key to .env

### To Run Application:
  python -m streamlit run dashboard.py

Developer Note: The integrated Chatbot AI wont work unless your time zone is up to date, if your getting handshake errors sync your computers time.
