# AlgorithmSpeaks

Welcome to AlgorithmSpeaks! This guide will help you set up and run the project on a fresh Ubuntu installation. Follow the steps below to get the application up and running.

---

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Backend Setup](#2-backend-setup)
  - [3. Frontend Setup](#3-frontend-setup)
- [Obtaining API Keys and Credentials](#obtaining-api-keys-and-credentials)
  - [Azure Active Directory Application Registration](#azure-active-directory-application-registration)
  - [Azure OpenAI Service](#azure-openai-service)
  - [Azure Cognitive Services (Speech)](#azure-cognitive-services-speech)
  - [Azure Blob Storage](#azure-blob-storage)
  - [Azure Communication Services (Email)](#azure-communication-services-email)
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

AlgorithmSpeaks is a web application that generates personalized motivational speeches using GPT-4 through Azure OpenAI API and converts them to audio using Azure Text-to-Speech services. Users can:

- Log in using their Microsoft account via Azure AD.
- Set preferences and schedule for receiving speeches.
- Choose from various personas and tones.
- Receive speeches via email.
- Generate and view public motivational speeches.

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

To run AlgorithmSpeaks, you'll need to set up various Azure services and obtain the necessary API keys and credentials.

### Azure Active Directory Application Registration

AlgorithmSpeaks uses Azure Active Directory (Azure AD) for user authentication via Microsoft accounts.

1. **Register an Application in Azure AD:**

   - Sign in to the [Azure Portal](https://portal.azure.com/).
   - Navigate to **Azure Active Directory** > **App registrations**.
   - Click on **New registration**.

2. **Fill in the App Details:**

   - **Name:** Enter a name for your app, e.g., `AlgorithmSpeaks`.
   - **Supported account types:** Select **Accounts in any organizational directory and personal Microsoft accounts**.
   - **Redirect URI:** Enter `http://localhost:8000/callback`.

3. **Register the Application:**

   - Click **Register**.
   - After registration, you'll be redirected to the application's overview page.

4. **Get the Client ID and Tenant ID:**

   - Copy the **Application (client) ID** and **Directory (tenant) ID**; you'll need these for your backend `.env` file.

5. **Create a Client Secret:**

   - Navigate to **Certificates & secrets**.
   - Click **New client secret**.
   - Add a description and choose an expiration period.
   - Click **Add** and copy the **Value** (client secret); you'll need this for your backend `.env` file.

6. **Configure API Permissions:**

   - Navigate to **API Permissions**.
   - Ensure that the application has **Microsoft Graph API** permissions for `User.Read`.

### Azure OpenAI Service

AlgorithmSpeaks uses Azure OpenAI for generating speech text.

1. **Apply for Access to Azure OpenAI Service:**

   - Visit the [Azure OpenAI Service](https://azure.microsoft.com/en-us/services/cognitive-services/openai-service/) page and apply for access.

2. **Create an Azure OpenAI Resource:**

   - Once approved, create a new Azure OpenAI resource in your Azure portal.

3. **Get the API Key and Endpoint:**

   - Navigate to the Azure OpenAI resource.
   - Go to **Keys and Endpoint**.
   - Copy the **Key** and **Endpoint URL**; you'll need these for your backend `.env` file.

4. **Deploy a Model:**

   - Navigate to **Model deployments**.
   - Deploy the desired model (e.g., `gpt-4` or `gpt-35-turbo`).
   - Note the **Deployment Name**; you'll need this for your backend `.env` file.

### Azure Cognitive Services (Speech)

AlgorithmSpeaks uses Azure Cognitive Services for text-to-speech conversion.

1. **Create an Azure Speech Service Resource:**

   - In the Azure portal, create a new resource and select **Speech**.

2. **Get the API Key and Region:**

   - Navigate to the Speech resource.
   - Go to **Keys and Endpoint**.
   - Copy the **Key** and note the **Region**; you'll need these for your backend `.env` file.

### Azure Blob Storage

AlgorithmSpeaks uses Azure Blob Storage to store and serve audio files.

1. **Create a Storage Account:**

   - In the Azure portal, create a new **Storage Account**.

2. **Create a Container:**

   - Navigate to your Storage Account.
   - Go to **Blob Service** > **Containers**.
   - Create a new container (e.g., `speeches`).

3. **Generate a SAS Token:**

   - Navigate to the container.
   - Click on **Generate SAS**.
   - Configure the SAS token with appropriate permissions (e.g., Read, Write).
   - Set an appropriate expiration date.
   - Generate the SAS token and copy the **Container SAS URL**; you'll need this for your backend `.env` file.

### Azure Communication Services (Email)

AlgorithmSpeaks uses Azure Communication Services to send emails.

1. **Create an Azure Communication Services Resource:**

   - In the Azure portal, create a new **Communication Services** resource.

2. **Get the Connection String:**

   - Navigate to the Communication Services resource.
   - Go to **Keys**.
   - Copy the **Connection String**; you'll need this for your backend `.env` file.

3. **Set Up a Verified Sender Email Address:**

   - Navigate to **Email** > **Senders**.
   - Add and verify a sender email address.
   - You'll need this email address for your backend `.env` file.

---

## Configuring Environment Variables

### Backend `.env` Configuration

Create a `.env` file in the `backend` directory and fill in the following variables:

```env
# Azure AD Configuration
CLIENT_ID=your_microsoft_client_id
CLIENT_SECRET=your_microsoft_client_secret
REDIRECT_URI=http://localhost:8000/callback
AUTHORITY=https://login.microsoftonline.com/common
SCOPE=User.Read

# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_azure_openai_api_key
AZURE_OPENAI_ENDPOINT=your_azure_openai_endpoint
AZURE_OPENAI_DEPLOYMENT=your_azure_openai_deployment_name

# Azure Speech Service Configuration
AZURE_SPEECH_SUBSCRIPTION_KEY=your_azure_speech_service_key
AZURE_SPEECH_REGION=your_azure_speech_service_region

# Azure Blob Storage Configuration
AZURE_CONTAINER_SAS_URL=your_azure_container_sas_url

# Azure Communication Services Configuration
AZURE_COMMUNICATION_CONNECTION_STRING=your_communication_services_connection_string
SENDER_EMAIL_ADDRESS=your_verified_sender_email_address

# Application Configuration
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///./app.db
FRONTEND_URL=http://localhost:3000
ALLOWED_ORIGINS=http://localhost:3000
COOKIE_SECURE=False
```

### Frontend `.env` Configuration

Create a `.env` file in the `frontend` directory and fill in the following variables:

```env
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

The scheduler script (`scheduler.py`) needs to run hourly to generate and send speeches based on user schedules.

### Using Cron to Schedule the Script

1. **Ensure the Scheduler Script is Executable:**

   ```bash
   chmod +x scheduler.py
   ```

2. **Edit the Crontab:**

   ```bash
   crontab -e
   ```

3. **Add the Cron Job:**

   Add the following line to run the scheduler every hour:

   ```cron
   0 * * * * cd /path/to/daily-motivation-booster/backend && /usr/bin/env bash -c 'source venv/bin/activate && python scheduler.py' >> logs/cron.log 2>&1
   ```

   Replace `/path/to/daily-motivation-booster` with the actual path to your project directory.

4. **Check Cron Logs:**

   Logs will be saved to `backend/logs/cron.log`.

---

## Security Considerations

- **Do not commit `.env` files or sensitive information to version control.**
- **Use HTTPS in production environments.**
- **Store secrets securely, preferably using environment variables or a secrets manager.**
- **Regularly update dependencies to patch security vulnerabilities.**
- **Implement proper error handling to prevent information leakage.**
- **Ensure your Azure keys and connection strings are kept secure.**

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

  - Ensure your email provider (Azure Communication Services) is configured correctly to prevent emails from being marked as spam.
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

- **CORS Configuration:**

  - The backend uses CORS middleware to allow requests from the frontend.
  - Update `ALLOWED_ORIGINS` in the backend `.env` file if you change the frontend URL.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

Congratulations! Your application should now be up and running. If you encounter any issues, please refer to the logs for more details or open an issue on the repository.

---

Feel free to contribute to the project by submitting pull requests or opening issues for any bugs or feature requests.

Happy coding!