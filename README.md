# WhatsApp Chat Analyzer

Live demo: https://whatsapp-chat-analyzer-2-4mu5.onrender.com

A simple tool to analyze WhatsApp chat exports (text files) and produce summary statistics and visualizations. This repository contains the code and resources to parse exported WhatsApp chat .txt files, compute metrics (message counts, active users, emojis, media, etc.), and show interactive charts.

Features
- Parse WhatsApp exported chat text files (both Android and iOS formats where possible)
- Compute per-user message counts, word counts, most active days/times
- Emoji and media usage summaries
- Basic visualizations and downloadable reports

Quick start
1. Clone the repository:
   git clone https://github.com/ayushmant908-web/whatsapp_chat_analyzer.git
2. Change into the project directory:
   cd whatsapp_chat_analyzer
3. Install dependencies (example for Python/Node — adjust based on project):
   - Python (if app uses Flask/FastAPI):
     pip install -r requirements.txt
   - Node (if app uses Node/React):
     npm install
4. Run the app locally (example):
   - Python: python app.py or flask run
   - Node: npm start
5. Open the live demo: https://whatsapp-chat-analyzer-2-4mu5.onrender.com

Usage
- Export your WhatsApp chat as a .txt file (without media) from the WhatsApp app.
- Upload the .txt file through the web UI (or provide the path if using a CLI tool).
- Review the generated statistics and visualizations.

Contributing
Contributions are welcome. Please open an issue to discuss changes or submit a pull request. Add tests and documentation for new features.

License
Specify your license here (e.g., MIT).

Contact
For questions or issues, open an issue on GitHub: https://github.com/ayushmant908-web/whatsapp_chat_analyzer/issues
