# 📸 EventLens – Find Yourself in Event Photos

EventLens is a **Streamlit-based web application** that helps users instantly find themselves in event photos using **facial recognition**.

With just a selfie, the app scans through event images and returns matching results in seconds.

---

## 🚀 Demo

👉 *Live App:* [EventLens](https://eventlens.streamlit.app/)

---

## 🧠 How It Works

1. User logs in (basic authentication)
2. Captures a selfie using the in-app camera
3. Image is converted to Base64 and sent to the backend API
4. AWS-powered backend processes the face match
5. Matching photos are returned and displayed in a grid
6. Optional: Download all matched images as a ZIP

---

## 🏗️ Tech Stack

### Frontend

* Streamlit
* Python
* Pillow (PIL)

### Backend (AWS)

* API Gateway
* AWS Lambda
* Amazon S3
* Amazon DynamoDB
* Amazon Rekognition *(optional for face matching)*

---

## 📂 Project Structure

```
EventLens/
│── app.py              # Main Streamlit application
│── requirements.txt    # Python dependencies
│── README.md           # Project documentation
│── .streamlit/
│    └── secrets.toml   # Secrets (API + credentials)
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```bash
git clone https://github.com/<your-username>/EventLens.git
cd EventLens
```

### 2️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Configure Secrets

Create `.streamlit/secrets.toml`:

```toml
API_URL = "your_api_endpoint_url"

APP_USERNAME = "your_username"
APP_PASSWORD = "your_password"
APP_PROFILE = "your_display_name"
```

### 4️⃣ Run locally

```bash
streamlit run app.py
```

---

## 🌐 Deployment (Streamlit Cloud)

1. Push code to GitHub (public repo)
2. Go to Streamlit Cloud
3. Click **New App**
4. Select your repo & branch
5. Set:

   * Main file → `app.py`
6. Add secrets in **App Settings → Secrets**
7. Deploy 🚀

---

## ✨ Features

* 🔐 Basic login authentication (session-based)
* 📷 Capture selfie directly from browser
* 🔍 One-click facial search
* 🖼️ Clean grid-based image results
* 📦 Download all matches as ZIP
* 🔄 Retake & re-search flow
* ⚡ Fast serverless backend

---

## 📡 API Contract

### Request

```json
POST /search
{
  "image": "<base64_encoded_image>"
}
```

### Response

```json
{
  "images": ["url1", "url2"],
  "zip_url": "https://download-link.com/file.zip"
}
```

---

## ⚠️ Notes

* ZIP link is typically valid for **limited time (e.g., 1 hour)**
* Ensure API is publicly accessible
* Store images in S3 with proper permissions
* Use HTTPS endpoints in production

---

## 📌 Future Improvements

* 🔑 Production-grade authentication (OAuth / JWT)
* 📤 Upload image option (not just camera)
* 🎯 Face confidence score display
* 📅 Event-based filtering
* 📊 API rate limiting / throttling
* 🎨 Improved UI/UX

---

## 👨‍💻 Author

**Tanmay Melanta**

---

## ⭐ Support

If you like this project:

* Give it a ⭐ on GitHub
* Share feedback
* Contribute improvements 🚀

---
