## Backend Setup

Follow these steps to set up the Django backend:

### Step 0: Install Python 3.8 or Higher

Make sure you have Python 3.8 or a higher version installed on your system.

### Step 1: Install Django

Install Django using the following command:
```sh
sudo apt install python3-django
```

### Step 2: Install MongoDB

Ensure MongoDB is properly installed on your system.

### Step 3: Install Required Packages

Install the necessary Python packages by running the following command:
```sh
pip install -r requirements.txt
```

### Step 4: Setup SMTP Server

Configure an SMTP server by following this [video tutorial](https://www.youtube.com/watch?v=blYx6VQEPXY).

### Step 5: Configure Environment Variables

In the root directory of the project, create a `.env` file and set your OpenAI API key, MongoDB connection and configured SMTP email as environment variables:
```env
OPENAI_API_KEY="your_api_key_here"
MONGO_CONNECTION="your_mongodb_connection_uri_here"
SMTP_EMAIL="your_smtp_email_here"
```

### Step 6: Run the Server

Start the Django server with the following command:
```sh
python manage.py runserver
```

### Note

If you encounter any issues while installing required packages in Step 3, you can follow these additional steps:

1. Install `pipreqs` if not already installed:
   ```sh
   pip install pipreqs
   ```

2. Delete previous requirements.txt and Generate new `requirements.txt` file by running:
   ```sh
   pipreqs .
   ```

3. Install the packages from `requirements.txt`:
   ```sh
   pip install -r requirements.txt
   ```

If any packages are still missing when running the server, you may need to install those packages manually.

Now your Django backend should be set up and ready to go!