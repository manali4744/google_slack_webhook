# Google Drive and Gmail Webhook Setup

  Acquire the client secret file from the 'Google Developer Console'.

  Establish two directories in the directory where 'main.py' is located: one named 'drive_download' and the other        named 'webhookdata'.

  ## Create a virtual environment and install all necessary dependencies using the 'requirements.txt' file.

  ```bash
  $ python -m venv env
  ```

  ```bash
  $ python install -r requirements.txt
  ```

  ## Register the Google Drive webhook by running the provided code.

  ```bash
  $ python drive_webhook_register.py
  ```

  ## For Gmail, insert your Ngrok URL in the Pub/Sub('Publish/Subscribe') section within the Developer Console.
  ## Run the 'main.py' file by using the following command:
  ```bash
  uvicorn main:app --reload
  ```

# Slack Webhook Setup

Navigate to the URL(https://api.slack.com/apps/<app-info>/event-subscriptions?) and modify the event subscription URL as needed.

Within your Slack workspace, there exists an app known as "Webhook." Customize this app by including the channel name in which you desire to establish a connection with the webhook.

      
