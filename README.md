# Daily Motivation Booster

Welcome to the game! This guide will help you set up the project on a fresh Ubuntu installation. Follow the steps below to get the application up and running.

---

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Backend Setup](#2-backend-setup)
  - [3. Frontend Setup](#3-frontend-setup)
- [Obtaining API Keys and Credentials](#obtaining-api-keys-and-credentials)
  - [Azure OpenAI API Key](#azure-openai-api-key)
  - [Azure Speech Service Key](#azure-speech-service-key)
  - [Microsoft App Registration](#microsoft-app-registration)
  - [Email SMTP Credentials](#email-smtp-credentials)
- [Configuring Environment Variables](#configuring-environment-variables)
  - [Backend `.env` Configuration](#backend-env-configuration)
  - [Frontend `.env` Configuration](#frontend-env-configuration)
- [Running the Application](#running-the-application)
  - [Starting the Backend Server](#starting-the-backend-server)
  - [Starting the Frontend Server](#starting-the-frontend-server)
- [Setting Up the Scheduler](#setting-up-the-scheduler)
- [Security Considerations](#security-considerations)
- [Logging and Monitoring](#logging-and-monitoring)
- [Additional Notes](#additional-notes)
- [License](#license)

---

## Introduction

This web app generates personalized motivational speeches using GPT-4 through Azure OpenAI API and converts them to audio using Azure Text-to-Speech services. Users can:

- Log in using their Microsoft account.
- Set preferences and schedule for receiving speeches.
- Choose from various personas and tones.
- Receive speeches via email.

---

## Prerequisites

Ensure you have the following installed on your Ubuntu system:

- **Python 3.8+**
- **Node.js 14+ and npm**
- **Git**
- **pip**
- **Virtualenv**

---

## Installation Steps

### 1. Clone the Repository

Open your terminal and run:

```bash
git clone https://github.com/tapania/daily-motivation-booster.git
cd daily-motivation-booster
```

---

### 2. Backend Setup

#### a. Navigate to the Backend Directory

```bash
cd backend
```

#### b. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

#### c. Upgrade pip and Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### d. Create the `.env` File

Copy the example `.env` file:

```bash
cp .env.example .env
```

You'll need to fill in the required environment variables in the `.env` file. See [Configuring Environment Variables](#configuring-environment-variables) for details.

---

### 3. Frontend Setup

#### a. Navigate to the Frontend Directory

Open a new terminal window/tab and navigate to the frontend directory:

```bash
cd frontend
```

#### b. Install Dependencies

```bash
npm install
```

#### c. Create the `.env` File

Copy the example `.env` file:

```bash
cp .env.example .env
```

Fill in the required environment variables in the `.env` file.

---

## Obtaining API Keys and Credentials

### Azure OpenAI API Key

1. **Create an Azure Account:**

   - Sign up at [Azure Portal](https://portal.azure.com/).

2. **Apply for Access to Azure OpenAI:**

   - Visit [Azure OpenAI Service](https://azure.microsoft.com/en-us/services/cognitive-services/openai-service/) and apply for access.

3. **Create an Azure OpenAI Resource:**

   - Once approved, create a new Azure OpenAI resource in your Azure portal.

4. **Get the API Key and Endpoint:**

   - Navigate to the resource.
   - Go to **Keys and Endpoint**.
   - Copy the **Key** and **Endpoint URL**.

### Azure Speech Service Key

1. **Create an Azure Speech Service Resource:**

   - In the Azure portal, create a new resource and select **Speech**.

2. **Get the API Key and Region:**

   - Navigate to the Speech resource.
   - Go to **Keys and Endpoint**.
   - Copy the **Key** and note the **Region**.

### Microsoft App Registration

1. **Register an Application in Azure AD:**

   - Go to [Azure Active Directory](https://portal.azure.com/#blade/Microsoft_AAD_IAM/ActiveDirectoryMenuBlade/Overview).
   - Select **App registrations** > **New registration**.

2. **Fill in the App Details:**

   - **Name:** Your app name.
   - **Supported account types:** Choose according to your needs.
   - **Redirect URI:** Use `http://localhost:8000/token` for development.

3. **Get the Client ID and Tenant ID:**

   - After registration, copy the **Application (client) ID** and **Directory (tenant) ID**.

4. **Create a Client Secret:**

   - Go to **Certificates & secrets**.
   - Click **New client secret** and copy the value.

### Email SMTP Credentials

You need SMTP credentials to send emails. You can use providers like SendGrid, Gmail, etc.

**Example with SendGrid:**

1. **Create a SendGrid Account:**

   - Sign up at [SendGrid](https://sendgrid.com/).

2. **Generate an API Key:**

   - Go to **Settings** > **API Keys**.
   - Create a new API Key with **Full Access**.

3. **SMTP Settings:**

   - **SMTP Host:** `smtp.sendgrid.net`
   - **SMTP Port:** `587`
   - **Username:** `apikey`
   - **Password:** Your SendGrid API Key.

---

## Configuring Environment Variables

### Backend `.env` Configuration

Edit the `backend/.env` file and fill in the following:

```env
# Azure AD Configuration
CLIENT_ID=your_microsoft_client_id
CLIENT_SECRET=your_microsoft_client_secret
REDIRECT_URI=http://localhost:8000/token
AUTHORITY=https://login.microsoftonline.com/common
SCOPE=User.Read

# Azure OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Azure Speech Service Configuration
SPEECH_KEY=your_speech_service_key
SPEECH_REGION=your_speech_service_region

# Email Configuration
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your_sendgrid_api_key

# Application Configuration
ALLOWED_ORIGINS=http://localhost:3000
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///./motivational_app.db
```

### Frontend `.env` Configuration

Edit the `frontend/.env` file and fill in:

```env
REACT_APP_CLIENT_ID=your_microsoft_client_id
REACT_APP_REDIRECT_URI=http://localhost:3000/
REACT_APP_BACKEND_URL=http://localhost:8000
```

---

## Running the Application

### Starting the Backend Server

1. **Activate the Virtual Environment:**

   ```bash
   cd backend
   source venv/bin/activate
   ```

2. **Run Database Migrations:**

   For initial setup:

   ```bash
   python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"
   ```

3. **Start the Server:**

   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The backend server should now be running at `http://localhost:8000`.

### Starting the Frontend Server

1. **Navigate to the Frontend Directory:**

   ```bash
   cd frontend
   ```

2. **Start the React App:**

   ```bash
   npm start
   ```

   The frontend should now be accessible at `http://localhost:3000`.

---

## Setting Up the Scheduler

The scheduler script (`scheduler.py`) needs to run hourly to generate and send speeches.

### Using Cron to Schedule the Script

1. **Ensure the Scheduler Script is Executable:**

   ```bash
   chmod +x backend/scheduler.py
   ```

2. **Edit the Crontab:**

   ```bash
   crontab -e
   ```

3. **Add the Cron Job:**

   Add the following line to run the scheduler every hour:

   ```cron
   0 * * * * cd /path/to/motivational-app/backend && /path/to/motivational-app/backend/venv/bin/python scheduler.py >> logs/cron.log 2>&1
   ```

   Replace `/path/to/motivational-app` with the actual path.

4. **Check Cron Logs:**

   Logs will be saved to `backend/logs/cron.log`.

---

## Security Considerations

- **Do not commit `.env` files or sensitive information to version control.**
- **Use HTTPS in production environments.**
- **Store secrets securely, preferably using environment variables or a secrets manager.**
- **Regularly update dependencies to patch security vulnerabilities.**
- **Implement proper error handling to prevent information leakage.**
- **Ensure your SMTP credentials are kept secure.**

---

## Logging and Monitoring

- **Backend Logging:**

  - Logs are stored in `backend/logs/app.log`.
  - Configure log rotation and retention as needed.

- **Monitoring:**

  - Integrate monitoring tools like Azure Monitor, Prometheus, or Grafana for real-time monitoring.
  - Set up alerts for critical issues.

---

## Additional Notes

- **Email Deliverability:**

  - Ensure your email provider is configured correctly to prevent emails from being marked as spam.
  - Consider setting up SPF, DKIM, and DMARC records for your domain.

- **Time Zones:**

  - Users should input their time zone correctly to receive speeches at the intended local time.
  - The application handles time zone conversions using Python's `pytz` library.

- **User Notifications:**

  - Users will receive speeches via email.
  - Ensure that users consent to receiving communications.

- **Error Handling:**

  - The application includes comprehensive error handling.
  - Errors are logged without exposing sensitive information to the user.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Congratulations! Your application should now be up and running. If you encounter any issues, please refer to the logs for more details or open an issue on the repository.

---

Feel free to contribute to the project by submitting pull requests or opening issues for any bugs or feature requests.

Happy coding!