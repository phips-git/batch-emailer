# Basic usage

- Create a `.html` template and put it in the `templates` folder.
- Paste all relevant recipients to a `.txt` file and put it in the `addresses` folder. Make sure each email address has its own line.
- Copy `.env.example` to a new file called `.env`. Enter the credentials for your SMTP server and all relevant email data e.g. `MAIL_SENDER` or `MAIL_SUBJECT`.
- Make sure you have Python 3.9 installed and made available to your shell
- Open your preferred shell, move to the repository's directory and run `pipenv shell`, which will initialize a new virtual environment
- Then run `pipenv sync` to install the corresponding dependencies
- After that you will be able to run the script with `python mailer.py`.
