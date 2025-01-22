import base64
import datetime
import json
import os
import re
import threading
import traceback
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from typing import Optional, Union, Dict, Tuple

import requests
from flask import session
from smtpymailer import SmtpMailer
from werkzeug.exceptions import default_exceptions

from arched_emailer.encryption import obfuscate_sensitive_info, generate_random_string

__version__ = "0.3.5"

BASE_URL = "https://arched.dev"


class ArchedEmailer:
    """
    A class for sending emails.
    ARCHED.DEV
    """
    error_log: dict
    app_name: str = "ArchedErrors"
    app_author: str = "Arched"
    error_sender: str = "errors@arched.dev"
    error_sender_name: str = "Arched Errors"
    success_sender: str = "success@arched.dev"
    success_sender_name: str = "Arched Notifications"
    errors_name_time: dict = dict()
    connection_details: str
    arched_api_key: str
    temp_app: Optional[str] = None
    time_start: Optional[datetime.datetime] = None
    app: Optional[str] = None
    flask_app: Optional["Flask"] = None
    mailer: Optional[SmtpMailer] = None
    success_mailer: Optional[SmtpMailer] = None
    task_id: Optional[int] = None
    current_user = None
    arched_api_key = None
    _lock = threading.Lock()

    def __init__(self, app: str, api_key: Optional[str] = None, mail_connection_string: Optional[str] = None,
                 task_id: Optional[int] = None, flask: Optional[bool] = False):

        self.app = app
        self.task_id = task_id
        self.errors_name_time = self._load_error_log()  # Load existing error log

        if not flask:
            self.setup(api_key, mail_connection_string)

        self._cleanup_error_log()

    def setup(self, api_key: Optional[str] = None, mail_connection_string: Optional[str] = None):
        """
        Set up the ArchedEmailer instance.

        Args:
            app (str): The name of the application.
            api_key (str): The API key for the Arched API.
            mail_connection_string (str): The connection string for the mail server.

        Returns:
            None
        """

        self.arched_api_key = os.getenv("ARCHED_API_KEY") or api_key
        self.connection_details = os.getenv("MAIL_CONNECTION_STRING") or mail_connection_string

        self._get_set_user_details()
        self._load_env()

        self.mailer = SmtpMailer(self.error_sender, self.error_sender_name)
        self.success_mailer = SmtpMailer(self.success_sender, self.success_sender_name)

    def init_app(self, app, intercept_errors: Optional[bool] = True, add_current_user: bool = True, ignore_url_patterns=None, **kwargs):
        """
        Initialize the application with the ArchedEmailer instance.
        Args:
            app: The Flask application instance.
            intercept_errors: A boolean value indicating whether to intercept errors and send emails. Default is True.
            add_current_user (bool): Whether to use the current user for the error details. Default is True.
            ignore_url_patterns: A list of regular expressions to ignore when sending error emails.
        Returns:
            None
        """
        from flask import request, session

        app.extensions["arched_emailer"] = self
        self.flask_app = app

        if intercept_errors:

            if ignore_url_patterns:
                self.ignore_url_patterns = ignore_url_patterns

            def format_dict_for_email(data):
                """
                Format a dictionary for use in an email.

                Args:
                    data (dict): The dictionary to be formatted.

                Returns:
                    str: The formatted dictionary.
                """
                return json.dumps(data, indent=4).replace(" ", "&nbsp;").replace("\n", "<br>")

            def update_visited_urls():
                # Initialize the visited URLs list in the session if not present
                if 'visited_urls' not in session:
                    session['visited_urls'] = []

                # Get the current URL
                current_url = request.url
                if "static" not in current_url and ".js" not in current_url and ".css" not in current_url:
                    # Update the session with the current URL, keeping only the last 5 URLs
                    visited_urls = session['visited_urls']
                    visited_urls.append(current_url)
                    session['visited_urls'] = visited_urls[-5:]  # Keep only the last 5 URLs

            @app.before_request
            def before_request():
                """
                A function to run before each request.
                It logs the visited URLs.
                """
                update_visited_urls()

            # Register a custom error handler for HTTP exceptions
            def handle_http_exception(error):
                # This is to stop errors that I'm getting from bots trying to access the server
                from arched_emailer.utils import is_bot
                if is_bot():
                    return
                if hasattr(self, "ignore_url_patterns"):
                    for pattern in self.ignore_url_patterns:
                        if re.match(pattern, request.url):
                            return
                self._process_error(error, add_current_user, request)
                # Re-raise the exception to let Flask handle it further
                raise error

            # Register handlers for all HTTP exceptions
            for code in default_exceptions.keys():
                app.register_error_handler(code, handle_http_exception)

            # Register a handler for non-HTTP exceptions (to catch 500 errors)
            app.register_error_handler(Exception, handle_http_exception)

        self.setup(kwargs.get("api_key"), kwargs.get("mail_connection_string"))

    def _process_error(self, error, add_current_user, request):
        """
        Process the error by sending an error email.

        Args:
            error: The exception object.
            add_current_user (bool): Whether to include current user details.
            request: The Flask request context.

        Returns:
            None
        """
        def format_dict_for_email(data):
            """
            Format a dictionary for use in an email.

            Args:
                data (dict): The dictionary to be formatted.

            Returns:
                str: The formatted dictionary.

            """
            return json.dumps(data, indent=4).replace(" ", "&nbsp;").replace("\n", "<br>")

        try:

            ip = request.headers.get('X-Forwarded-For', request.remote_addr)
            user_agent = request.headers.get('User-Agent', 'Unknown')
            referer = request.headers.get('Referer', 'Unknown')
            requested_url = request.url
            requested_path = request.path

            error_text = (
                f"<br><strong style='font-size:larger'>404 Error Occurred</strong><br>"
                f"<strong>IP Address:</strong> {ip}<br>"
                f"<strong>User Agent:</strong> {user_agent}<br>"
                f"<strong>Referer:</strong> {referer}<br>"
                f"<strong>Request URL:</strong> {requested_url}<br>"
                f"<strong>Requested Path:</strong> {requested_path}<br>"
                f"<strong>Method:</strong> {request.method}<br>"
            )

            # Include the last visited URLs
            visited_urls = session.get('visited_urls', [])
            if visited_urls:
                visited_urls.reverse()
                error_text += (
                    f"<br><strong style='font-size:larger'>Last Visited URLs:</strong><br>"
                    f"{'<br>'.join(visited_urls)}<br>"
                )

            if add_current_user:
                from flask_login import current_user
                email = getattr(current_user, "email", None)
                name = getattr(current_user, "name", None)
                user_id = getattr(current_user, "id", None)
                error_text += (
                    f"<br><strong style='font-size:larger'>User Details:</strong><br>"
                    f"{f'Email: {email} - ' if email else ''}"
                    f"{f'Name: {name} - ' if name else ''}"
                    f"{f'ID: {user_id}' if user_id else ''}<br>"
                )

            if (request.content_type in ["application/xml", "text/xml"]) and request.method.lower() == "post":
                error_text += f"<br><strong style='font-size:larger'>Request XML:</strong><br>{request.data.decode()}<br>"
            elif request.method.lower() == "post" and request.is_json:
                error_text += f"<br><strong style='font-size:larger'>Request JSON:</strong><br>{format_dict_for_email(request.get_json())}<br>"
            elif request.method.lower() == "post" and request.form:
                error_text += f"<br><strong style='font-size:larger'>Request Form:</strong><br>{format_dict_for_email(request.form.to_dict())}<br>"

            self.send_error_email(
                ["lewis@arched.dev"],
                error_text=error_text,
                exception=error,
                allowed_minutes=60
            )
        except Exception as e:
            # Log the exception in a safe way; avoid recursive error handling
            pass

    def _get_error_log_path(self):
        """
        Returns the path to the error log JSON file.
        """
        data_dir = self._get_create_data_dir()
        return os.path.join(data_dir, "error_log.json")

    def _load_error_log(self) -> Dict[str, str]:
        """
        Loads the error log from a JSON file.

        Returns:
            dict: A dictionary mapping error messages to their last sent timestamp.
        """
        with self._lock:
            error_log_path = self._get_error_log_path()
            if os.path.exists(error_log_path):
                try:
                    with open(error_log_path, 'r') as f:
                        data = json.load(f)
                        # Convert timestamp strings back to datetime objects
                        return {k: datetime.datetime.fromisoformat(v) for k, v in data.items()}
                except Exception as e:
                    print(f"Failed to load error log: {e}")
            return {}

    def _save_error_log(self):
        """
        Saves the current error log to a JSON file.
        """
        with self._lock:
            error_log_path = self._get_error_log_path()
            try:
                with open(error_log_path, 'w') as f:
                    # Convert datetime objects to ISO format strings for JSON serialization
                    data = {k: v.isoformat() for k, v in self.errors_name_time.items()}
                    json.dump(data, f, indent=4)
            except Exception as e:
                print(f"Failed to save error log: {e}")

    def _cleanup_error_log(self, max_age_minutes: int = 2880):  # 1 day
        current_time = datetime.datetime.now()
        keys_to_delete = [k for k, v in self.errors_name_time.items() if
                          (current_time - v).total_seconds() / 60 > max_age_minutes]
        for k in keys_to_delete:
            del self.errors_name_time[k]
        self._save_error_log()

    def _get_set_user_details(self):
        """
        Fetches the user details from the API and saves them locally. If the server is down or the data fetch fails,
        it attempts to load the user details from a local file.

        Returns:
            None
        """
        if self.connection_details:
            return

        try:
            data = self._make_request(f"{BASE_URL}/email/user")

            if data[2] == 200 and data[1]:
                # Server responded successfully, update details
                self.customer_id = data[1]["id"]
                if not self.connection_details:
                    self.connection_details = data[1]["connection_string"]

                # Save these details locally as a fallback
                self._save_user_details_locally(data[1])
            else:
                raise ValueError(
                    "Server did not respond with user details, either API_KEY is invalid or server is down.")
        except Exception as e:
            # Attempt to load from local file if server is down or data fetch failed
            self._load_user_details_from_local()

    def _save_user_details_locally(self, user_details):
        """
        Saves the user details to a local file.
        Args:
            user_details (dict): The user details to be saved.

        Returns:
            None
        """
        data_dir = self._get_create_data_dir()
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        file_path = os.path.join(data_dir, "user_details.json")
        with open(file_path, 'w') as file:
            json.dump(user_details, file)

    def _load_user_details_from_local(self):
        """
        Loads the user details from a local file.
        Returns:
            None
        """
        data_dir = self._get_create_data_dir()
        file_path = os.path.join(data_dir, "user_details.json")
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                user_details = json.load(file)
                self.customer_id = user_details.get("id", None)
                if not self.connection_details:
                    self.connection_details = user_details.get("connection_string", self.connection_details)

    def _make_request(self, url: str, method: Optional[str] = "GET", body: Optional[dict] = None) -> Tuple[
        str, Union[Dict, str], int]:
        """
        A method for making API calls.
        Args:
            url: 
            method: 
            body: 

        Returns:

        """
        headers = {"Authorization": f"Bearer {self.arched_api_key}"}

        # Choosing the appropriate requests method based on `method` parameter.
        method = method.lower()
        if method == 'get':
            response = requests.get(url, headers=headers)
        elif method == 'post':
            response = requests.post(url, json=body, headers=headers)
        elif method == 'put':
            response = requests.put(url, json=body, headers=headers)
        elif method == 'delete':
            response = requests.delete(url, headers=headers)
        else:
            return "Error", "Unsupported method", 500

        # Checking and returning the response appropriately.
        if response.status_code == 200:
            try:
                return "Success:", response.json(), 200
            except ValueError:
                return "Success:", response.text, 200
        else:
            try:
                return "Error:", response.json(), response.status_code
            except ValueError:
                return "Error:", response.text, response.status_code

    def _load_env(self):
        """
        Load environment variables from encoded connection details.

        This method decodes the given connection details, splits it into key-value pairs,
        and sets the corresponding environment variables.

        Returns:
            None
        """
        if self.connection_details:
            decoded_bytes = base64.b64decode(self.connection_details)
            decoded_string = decoded_bytes.decode("utf-8")
            for val in decoded_string.split(";"):
                if "=" in val:
                    key, value = val.split("=")
                    os.environ[key] = value

    def _get_create_data_dir(self):
        """
        Gets or creates a directory for storing data specific to the application.

        Returns:
            str: The path to the data directory.

        """

        import appdirs
        app_data_dir = Path(appdirs.user_data_dir(self.app_name, self.app_author))
        app_data_dir.mkdir(parents=True, exist_ok=True)
        return str(app_data_dir)

    def _get_email_path(self, typ="error", task_id: Optional[int] = None):
        """
        Fetches the success email template from the API and saves it to a local file.

        Returns:
            str: The path to the saved email template file.

        Raises:
            None.


        Example usage:
            email_path = _get_error_email_path()
        """

        data_dir = self._get_create_data_dir()
        email_path = os.path.join(data_dir, f"{typ}.html")

        resp_text = self._make_request(f"{BASE_URL}/email/{typ}" + ("?task=" + str(task_id) if task_id else ""))
        if resp_text[2] == 200:
            with open(email_path, "w") as f:
                f.write(resp_text[1])

        return email_path

    def log_message(self, log_level: str, text: str, task_id: int = None):
        """
        Logs a message to the specified logging endpoint.

        Args:
            task_id (int): The task ID associated with the log.
            log_level (str): The level of the log (e.g., "INFO", "ERROR", "DEBUG").
            text (str): The log message to be sent.

        Returns:
            Tuple[str, Union[Dict, str], int]: The response status, response data, and HTTP status code.
        """

        task_id = task_id or self.task_id

        url = f"{BASE_URL}/logger/{task_id}"
        log_data = {"log_level": log_level, "text": text}

        return self._make_request(url, method="POST", body=log_data)

    def send_email(self, sender_email: str, sender_name: str, recipients: Union[str, list], subject: str,
                   cc_recipients: Optional[Union[str, list]] = None, bcc_recipients: Optional[Union[str, list]] = None,
                   dkim_selector: Optional[str] = "default", template: Optional[str] = None, **kwargs):
        """
        Args:
            sender_email: The email address of the sender.
            sender_name: The name of the sender.
            recipients: The email address(es) of the recipient(s). Can be a string or a list of strings.
            subject: The subject of the email.
            cc_recipients: Optional. The email address(es) of the CC recipient(s). Can be a string or a list of strings.
            bcc_recipients: Optional. The email address(es) of the BCC recipient(s). Can be a string or a list of strings.
            dkim_selector: Optional. The DKIM selector. Default is "default".
            template: Optional. The template for the email.
            **kwargs: Additional keyword arguments for the `send_email` method.

        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """

        try:
            os.environ["MAIL_DKIM_SELECTOR"] = dkim_selector
            self.mailer = SmtpMailer(sender_email, sender_name)
            return self.mailer.send_email(recipients, cc_recipients=cc_recipients, bcc_recipients=bcc_recipients,
                                          subject=subject, template=template, **kwargs)
        except:
            return False

    def _allowed_to_send(self, exception: Union[str, Exception], allowed_minutes: int = 60) -> bool:
        """
        Checks if the exception is allowed to send based on the allowed_minutes.

        Args:
            exception (Union[str, Exception]): The exception or error message to be checked.
            allowed_minutes (int): The number of minutes within which the exception is allowed to be sent again.

        Returns:
            bool: True if allowed to send, False otherwise.
        """
        exception_text = str(exception)
        current_time = datetime.datetime.now()

        last_sent = self.errors_name_time.get(exception_text)
        if last_sent:
            elapsed = (current_time - last_sent).total_seconds() / 60  # minutes
            if elapsed < allowed_minutes:
                return False

        # Update the timestamp and save
        self.errors_name_time[exception_text] = current_time
        self._save_error_log()
        return True

    def _send_to_db(self, success=True, **kwargs: dict):
        """
        Send the email attempt to the database.
        Args:
            kwargs (dict): The keyword arguments for the email attempt.

        Returns:
            None
        """
        if kwargs.get("task_id"):
            data = {"sent_to": kwargs.get("recipients"), "sent_from": kwargs.get("sender"), "success": success,
                    "html_response": kwargs.get("html"), "task_id": kwargs.get("task_id")}
            self._make_request(f"{BASE_URL}/email/tasks/taskrun", method="POST", body=data)

    def _get_html_content(self, message: MIMEMultipart):
        """
        Get the HTML content of the email.
        Args:
            message (MIMEMultipart): The MIMEMultipart object.
        Returns:
            str: The HTML content of the email.
        """
        html_content = ""
        for part in message.walk():
            # Check if the content type is HTML
            if part.get_content_type() == 'text/html':
                # Get the HTML content and stop looping
                return part.get_payload(decode=True).decode(part.get_content_charset())

        return html_content

    def send_success_email(self, recipients: Union[str, list], dump_time_taken: Optional[bool] = True,
                           dkim_selector: str = "default", sender: Optional[str] = None,
                           sender_name: Optional[str] = None, app: Optional[str] = None, task_id: Optional[int] = None,
                           update_db_only: Optional[bool] = False, **kwargs):
        """
        Sends an error email.

        Args:
            recipients: The recipients of the error email. Can be a string or a list of strings.
            dump_time_taken: A boolean value indicating whether to include the time taken in the email. Default is True.
            dkim_selector: The DKIM selector to use for sending emails from the server. Default is "default".
            sender: The email address of the sender. If provided, it will be used as the sender of the email.
            sender_name: The name of the sender. Used only if sender is provided.
            app: The name of the application. If provided, it will be used as the application name in the email.
            task_id: The ID of the report. If provided, it will be used as the report ID in the email.
            update_db_only: A boolean value indicating whether to only update the database with the email attempt. Default is False.
            **kwargs: Additional keyword arguments for the `send_email` method.
        """
        try:
            if sender:
                self.success_mailer = SmtpMailer(sender, sender_name)

            # gets and creates the email template
            email_path = self._get_email_path(typ="success", task_id=task_id if task_id else self.task_id)

            # sets the DKIM selector, needed for sending emails from the server
            os.environ["MAIL_DKIM_SELECTOR"] = dkim_selector
            date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

            time_taken = datetime.datetime.now() - self.time_start if self.time_start else None
            if dump_time_taken and self.time_start:
                # add the time taken to the kwargs
                kwargs["time_taken"] = str(time_taken).split(".")[0]
                # reset the time taken
                self._log_timer(True)

            app_name = app if app else self.app
            if not update_db_only:
                self.success_mailer.send_email(recipients, subject=f"Success: {app_name} - {generate_random_string()}",
                                               template=email_path, date=date, app=app_name, **kwargs)

                html_content = self._get_html_content(self.success_mailer.message)
            else:
                html_content = None

            self._send_to_db(success=True, recipients=recipients, sender=self.success_mailer.sender.email,
                             html=html_content, task_id=task_id if task_id else self.task_id, **kwargs)

        except Exception as e:
            print(e)

    def send_error_email(self, recipients: Union[str, list], error_text: Optional[str] = None,
                         exception: Optional[Exception] = None, include_tb: bool = True, dump_enviro: bool = True,
                         dump_globals: bool = True, dump_locals: bool = True, dkim_selector: str = "default",
                         sender: Optional[str] = None, sender_name: Optional[str] = None,
                         allowed_minutes: Optional[int] = 60, task_id: Optional[int] = None, app: Optional[str] = None,
                         send_to_db: Optional[bool] = True):
        """
        Sends an error email.

        Args:
            recipients: The recipients of the error email. Can be a string or a list of strings.
            error_text: The error message to be included in the email.
            exception: The exception object associated with the error.
            include_tb: A boolean value indicating whether to include the traceback in the email. Default is True.
            dump_enviro: A boolean value indicating whether to include the environment variables in the email. Default is True.
            dump_globals: A boolean value indicating whether to include the global variables in the email. Default is True.
            dump_locals: A boolean value indicating whether to include the local variables in the email. Default is True.
            dkim_selector: The DKIM selector to use for sending emails from the server. Default is "default".
            sender: The email address of the sender. If provided, it will be used as the sender of the email.
            sender_name: The name of the sender. Used only if sender is provided.
            allowed_minutes: The number of minutes to wait before sending another email of the same exception.
                             Default is 60. 0 means no limit.
            task_id: The ID of the report. If provided, it will be used as the report ID in the email.
            app: The name of the application. If provided, it will be used as the application name in the email.
            send_to_db: A boolean value indicating whether to send the email attempt to the database. Default is True.
        """
        try:
            if sender:
                self.mailer = SmtpMailer(sender, sender_name)

            # gets and creates the email template
            email_path = self._get_email_path(typ="error", task_id=task_id if task_id else self.task_id)

            # sets the DKIM selector, needed for sending emails from the server
            os.environ["MAIL_DKIM_SELECTOR"] = dkim_selector
            date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
            error_id = generate_random_string()

            template_data = {}
            if include_tb:
                template_data["traceback"] = traceback.format_exc()
            if dump_enviro:
                template_data["enviro"] = obfuscate_sensitive_info(dict(os.environ))
            for dump_ok, dump_type, dump_ob in [[dump_globals, "globals", globals], [dump_locals, "locals", locals]]:
                if dump_ok:
                    dump_dict = {}
                    for k in dump_ob().keys():
                        if k not in ["request", "session"]:
                            val = str(dump_ob().get(k))
                            dump_dict.update(obfuscate_sensitive_info({str(k): val}))

                    template_data[str(dump_type)] = dump_dict

            issue = error_text or str(exception) or str(traceback.format_exc())
            if issue:
                if self._allowed_to_send(issue, allowed_minutes=allowed_minutes):
                    app_name = app if app else self.app
                    self.mailer.send_email(recipients, subject=f"Error: {app_name} - {error_id}", template=email_path,
                                           date=date, app=app_name, error_id=error_id, exception=exception,
                                           error_text=error_text, **template_data)

                    html = None
                    if hasattr(self.mailer, "message"):
                        html = self._get_html_content(self.mailer.message)
                    if send_to_db:
                        self._send_to_db(success=False, recipients=recipients, sender=self.mailer.sender.email,
                                         html=html, task_id=task_id if task_id else self.task_id)
        except Exception as e:
            print(e)

    def try_log_function(self, error_recipients: Union[str, list], send_success: Optional[bool] = False,
                         success_recipients: Optional[Union[str, list]] = None, allowed_minutes: Optional[int] = 60,
                         send_to_db: Optional[bool] = True, task_id: Optional[int] = None, *args, **kwargs):
        """
        A decorator for logging the start time of a function and sending an error email if the function raises an
        exception.
        Optionally, it can also send a success email if the function completes successfully.

        Args:
            error_recipients (Union[str, list]): The recipients of the error email. Can be a string or a list of
                strings.
            send_success (bool): A boolean value indicating whether to send a success email if the function completes
            success_recipients (Union[str, list]): The recipients of the success email. Can be a string or a list of
                strings.
            allowed_minutes (int): The number of minutes to wait before sending another email of the same exception.
                                   Default is 60. 0 means no limit.
            send_to_db (bool): A boolean value indicating whether to send the email attempt to the database.
                Default is True.
            *args: Additional positional arguments for the jinja email template.
            **kwargs (dict): Additional keyword arguments for the jinja email template.

        Returns:
            None

        """

        def decorator(func):
            def wrapper(*func_args, **func_kwargs):
                result = None

                self._log_timer()
                try:
                    result = func(*func_args, **func_kwargs)
                    success_text = f"<strong style='font-size:larger'>Function Result: </strong>: <br> "
                    if result is not None:
                        if type(result) == dict:
                            success_text += json.dumps(result, indent=4).replace(" ", "&nbsp;").replace("\n", "<br>")
                        if type(result) in (str, int, float):
                            success_text += str(result)
                        else:
                            success_text += f"TYPE: {type(result)}"

                    if send_success and success_recipients:
                        self.send_success_email(success_recipients, success_text=success_text, task_id=task_id,
                                                **kwargs)
                    if not send_success and send_to_db:
                        self.send_success_email(success_recipients, success_text=success_text, task_id=task_id,
                                                update_db_only=True, **kwargs)
                except Exception as e:
                    self.send_error_email(error_recipients, exception=e, allowed_minutes=allowed_minutes,
                                          task_id=task_id, **kwargs)
                finally:
                    self._log_timer(True)
                    return result

            return wrapper

        return decorator

    def _log_timer(self, reset=False):
        """
        Log the start time of the application.
        """
        if reset:
            self.time_start = None
            return
        self.time_start = datetime.datetime.now()
