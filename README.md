⚙️ Installation  

### 1️⃣ Clone the repository  
```bash
git clone https://github.com/your-username/ai-web-doc-scraper.git
cd ai-web-doc-scraper
```
Create a virtual environment
python -m venv ai

3️⃣ Activate the virtual environment

Windows (PowerShell)

.\ai\Scripts\activate


Mac/Linux

source ai/bin/activate

4️⃣ Install dependencies
pip install -r requirements.txt

📦 Requirements

Your requirements.txt should include:

streamlit
pandas
matplotlib
seaborn
PyPDF2
python-docx
lxml
ollama

▶️ Running the App

Once everything is installed, run:

streamlit run main.py


This will launch the app in your browser at:
👉 http://localhost:8501

🧑‍💻 Project Structure
ai-web-doc-scraper/
│── main.py             # Streamlit app entry point  
│── scraper.py          # Web scraping logic  
│── parse.py            # Document parsing logic  
│── visualizer.py       # Graph and chart rendering  
│── ollama_handler.py   # AI question-answering handler  
│── requirements.txt    # Dependencies  
│── README.md           # Project documentation 
