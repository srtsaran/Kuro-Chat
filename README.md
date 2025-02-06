# Local AI Chat Web App with Flask and ngrok

This guide walks you through setting up a simple web interface to interact with a locally hosted LLM using Flask and ngrok. You can access the chat interface from your phone or any external device.

---

## **1. Prerequisites**

- **macOS** (M1/M2 or Intel)
- **Python 3 installed**
- **Homebrew installed**
- **ngrok account (free)**

---

## **2. Install Dependencies**

### **Install Flask and Required Libraries**
```bash
pip install flask flask-cors requests
```

### **Install ngrok via Homebrew**
```bash
brew install ngrok
```

### **Add ngrok Auth Token**
1. Sign up at [ngrok.com](https://ngrok.com/)
2. Find your **auth token** in the dashboard.
3. Run the following command:
   ```bash
   ngrok config add-authtoken <your-token>
   ```

---

## **3. Set Up Flask Server**

### **Create `server.py`**
```python
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests

app = Flask(__name__, static_folder="static")  # Serve static files from 'static' folder
CORS(app)

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

@app.route('/')
def serve_index():
    return send_from_directory('static', 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get("message", "")

    payload = {
        "model": "meta-llama-3-8b-instruct",
        "messages": [{"role": "user", "content": user_message}],
        "temperature": 0.7,
        "max_tokens": 200
    }

    response = requests.post(LM_STUDIO_URL, json=payload)
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
```

---

## **4. Create the Web Interface**

### **Move `index.html` to a `static` folder**
```bash
mkdir static
mv index.html static/
```

### **Create `index.html` in `static/` Folder**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Local AI Chat</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 20px; }
        textarea { width: 80%; height: 100px; }
        button { padding: 10px; margin-top: 10px; }
        #response { margin-top: 20px; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h2>Local AI Chat</h2>
    <textarea id="userInput" placeholder="Type a message..."></textarea><br>
    <button onclick="sendMessage()">Send</button>
    <div id="response"></div>

    <script>
        async function sendMessage() {
            const userMessage = document.getElementById("userInput").value;
            const responseDiv = document.getElementById("response");
            
            const response = await fetch("https://YOUR_NGROK_URL/chat", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ message: userMessage })
            });
            
            const data = await response.json();
            responseDiv.innerText = data.choices[0].message.content;
        }
    </script>
</body>
</html>
```

**Replace `YOUR_NGROK_URL` with your actual ngrok forwarding URL.**

---

## **5. Run the Flask Server**
```bash
python server.py
```

---

## **6. Expose Flask Server to the Internet with ngrok**
Run:
```bash
ngrok http 5050
```
You will see output similar to:
```
Forwarding                    https://randomstring.ngrok-free.app -> http://localhost:5050
```
Copy the **ngrok URL** and update `index.html` to use this URL instead of localhost.

---

## **7. Access Your Web App**
Open the ngrok URL in a browser (desktop or phone) to use the AI chat interface.

---

## **8. Troubleshooting**
- If `Failed to Fetch` errors occur, ensure Flask is running and ngrok is correctly configured.
- If `Mixed Content` errors appear, ensure you're using the HTTPS ngrok URL.
- If `/favicon.ico` 404 errors appear, ignore them—they don’t affect functionality.

---

## **🎉 Success!**
Your web-based AI chatbot is now accessible from anywhere! 🚀
