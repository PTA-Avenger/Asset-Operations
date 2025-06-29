# AssetOpsAI

AssetOpsAI is an edge/cloud-enabled asset operations platform designed for industrial environments. It provides real-time equipment monitoring, anomaly detection, maintenance tracking, and secure user authentication, supporting both offline and online (cloud) modes.

## Features

- **User Authentication:**  
  Secure signup, login, and logout using employee number and password. Local authentication with automatic cloud sync (Firebase) when online.

- **Data Recording & Sync:**  
  All operational data is stored locally and automatically uploaded to Firebase when internet is available or at the end of each work week.

- **Dashboard:**  
  Real-time charts and maps for efficiency, anomalies, and maintenance, powered by live sensor data.

- **Edge/Cloud Hybrid:**  
  Designed to work seamlessly on edge devices with intermittent connectivity, syncing data to the cloud for centralized analytics.

## Getting Started

### Prerequisites

- Python 3.8+
- Node.js (for frontend assets)
- [Firebase Admin SDK JSON file](https://firebase.google.com/docs/admin/setup)
- (Optional) Virtual environment for Python

### Installation

1. **Clone the repository:**
   ```
   git clone https://github.com/yourorg/assetopsai.git
   cd assetopsai
   ```

2. **Install Python dependencies:**
   ```
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies (if modifying frontend):**
   ```
   cd app/static
   npm install
   ```

4. **Place your Firebase Admin SDK JSON file:**
   - Recommended: `c:\Hackarhons\assetopsai\firebase_admin.json`
   - Set the environment variable:
     ```
     set FIREBASE_CRED_PATH=c:\Hackarhons\assetopsai\firebase_admin.json
     ```

5. **Set up environment variables:**
   - `FIREBASE_CRED_PATH` (see above)
   - Any other required keys (see `.env.example` if available)

### Running the Application

1. **Start the Flask backend:**
   ```
   flask run
   ```
   or
   ```
   python app/main.py
   ```

2. **Access the dashboard:**
   Open your browser to [http://localhost:5000](http://localhost:5000)

### API Endpoints

#### Authentication

- `POST /auth/signup`  
  `{ "employee_number": "1234", "password": "yourpassword" }`

- `POST /auth/login`  
  `{ "employee_number": "1234", "password": "yourpassword" }`

- `POST /auth/logout`

#### Data

- Data is recorded locally and synced automatically; see `app/data/data_manager.py` for details.

### Project Structure
assetopsai/ │
├── app/ 
│ 
├── ai/ # AI and ML integrations (e.g., WatsonX client) 
│ 
├── auth/ # Authentication logic and Flask endpoints 
│ 
├── data/ # Local data storage and cloud sync logic 
│ 
├── static/ # Frontend JS, CSS, and assets 
│ 
├── templates/ # HTML templates for the web dashboard 
│ 
└── main.py # Flask app entry point 
│ 
├── firebase_admin.json # Firebase Admin SDK credentials (not committed) 
├── requirements.txt # Python dependencies 
├── README.md # Project documentation 
└── .env.example # Example environment variables (if present)

### Security Notes

- Passwords are securely hashed locally.
- Employee numbers are used as unique identifiers.
- All sensitive operations should be performed over HTTPS in production.

### Contributing

Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

### License

[MIT License](LICENSE)

---
