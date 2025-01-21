import os
import re
import time
import traceback
from datetime import datetime
import smtplib
from email.header import Header
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Callable, Union, List, Dict, Optional
import schedule


class ManagerScheduler:
    @staticmethod
    def pocwatch(
        job: Callable,
        schedule_time: Union[int, float, str, List[str], Dict[Union[int, str], Union[int, float, str, List[str]]]],
        sender: Optional[str] = None,
        password: Optional[str] = None,
        recipients: Optional[List[str]] = None,
        smtp_server: Optional[str] = None,
        smtp_port: Optional[int] = None,
        smtp_ssl: bool = True,
        success_subject: str = "",
        success_body: str = "",
        success_file_path: Optional[str] = None,
        success_img_path: Optional[str] = None,
        failure_subject: str = "",
        failure_body: str = "",
        failure_file_path: Optional[str] = None,
        failure_img_path: Optional[str] = None,
        notify_success: bool = False,
        notify_failure: bool = False
    ) -> None:
        """

        from etool import pocwatch

        def your_task():
            print("任务执行中...")


        pocwatch(
            job=your_task, 
            schedule_time="08:00",
            sender=None,  # 缺省则不发送
            password=None,  # 缺省则不发送
            recipients=[],  # 缺省则不发送
            smtp_server='smtp.exmail.qq.com',  # 缺省值则自动选择
            smtp_port=465,  # 缺省值则自动选择
            smtp_ssl=True,  # 缺省值则自动选择

            success_subject="success",  # 缺省默认值 subject和body只填一个则会subject和body相同
            success_body="success",  # 缺省默认值

            failure_subject="failure",  # 缺省默认值 subject和body只填一个则会subject和body相同
            failure_body="task failure: error_message",  # 缺省默认值
        )

        Run the task scheduler.

        :param job: The task function to schedule
        :param schedule_time: The schedule time, can be a number (seconds), a string ("HH:MM"), a list, or a dictionary
        :param sender: Sender's email address
        :param password: Sender's email password
        :param recipients: List of recipient email addresses
        :param smtp_server: SMTP server address
        :param smtp_port: SMTP server port
        :param smtp_ssl: Use SSL or not
        :param success_subject: Email subject for success notifications
        :param success_body: Email body for success notifications
        :param failure_subject: Email subject for failure notifications
        :param failure_body: Email body for failure notifications, the error message will replace `error_message`
        :param notify_success: Whether to send notification on success
        :param notify_failure: Whether to send notification on failure

        - `schedule_time`: 执行时间

        如果是数字则默认单位是秒，每间隔`schedule_time`秒执行一次，例如`120`，则每2分钟执行一次。

        如果是字符串则默认是时间点，请遵从`HH:MM`的格式，例如`08:00`，每天在这个时间点执行一次。

        如果是列表，则默认是多个时间点，例如`["08:00", "12:00", "16:00"]`，每天在这些时间点执行一次。

        如果传入的是字典，则解析字典的键：

        如果字典的键为数字，则默认是日期，对应字典的值遵从上方数字、字符串、列表的判断。

        如果字典的键为字符串，则默认是星期几（以周一为例，支持的写法包括：`1`、`monday`、`Monday`、`MONDAY`、`mon`、`mon.`、`m`，以此类推），对应字典的值遵从上方数字、字符串、列表的判断。

        例如下面是1号的8点、2号的8点、12点、16点、3号每隔一个小时执行一次、每周一的8点执行一次。

        schedule_time = {
            1: "08:00",
            2: ["08:00", "12:00", "16:00"],
            3: 216000,
            "1": "08:00",
        }


        - `sender`: 发件人邮箱，如果不想发送邮件，则可以不配置。
        - `password`: 发件人邮箱密码，如果不想发送邮件，则可以不配置。
        - `recipients`: 收件人邮箱列表，如果不想发送邮件，则可以不配置。
        - `smtp_server`: SMTP服务器地址，缺省值则自动选择。
        - `smtp_port`: SMTP服务器端口，缺省值则自动选择。
        - `smtp_ssl`: 是否使用SSL，缺省值则自动选择。
        - `success_subject`: 任务成功时的邮件主题，subject和body只填一个则会subject和body相同
        - `success_body`: 任务成功时的邮件内容，subject和body只填一个则会subject和body相同
        - `failure_subject`: 任务失败时的邮件主题，subject和body只填一个则会subject和body相同
        - `failure_body`: 任务失败时的邮件内容，subject和body只填一个则会subject和body相同
        """
        if bool(success_subject) != bool(success_body):
            if not bool(success_subject):
                success_subject = success_body
            else:
                success_body = success_subject

        if bool(failure_subject) != bool(failure_body):
            if not bool(failure_subject):
                failure_subject = failure_body
            else:
                failure_body = failure_subject

        notify_success = bool(success_subject) or bool(success_body)
        notify_failure = bool(failure_subject) or bool(failure_body)

        # When notifications are enabled, sender, password, and recipients must be provided
        if (notify_success or notify_failure) and (
            not sender or not password or not recipients
        ):
            raise ValueError(
                "When notifications are enabled, sender, password, and recipients must be provided."
            )
       
        def wrapper():
            try:
                job()
                if notify_success:
                    ManagerScheduler.send_email(
                        sender,
                        password,
                        recipients,
                        smtp_server,
                        smtp_port,
                        smtp_ssl,
                        success_subject,
                        success_body,
                        success_file_path,
                        success_img_path,
                    )
            except Exception as e:
                if notify_failure:
                    error_msg = traceback.format_exc()
                    formatted_failure_body = failure_body.replace(
                        "error_message", error_msg
                    )
                    ManagerScheduler.send_email(
                        sender,
                        password,
                        recipients,
                        smtp_server,
                        smtp_port,
                        smtp_ssl,
                        failure_subject,
                        formatted_failure_body,
                        failure_file_path,
                        failure_img_path,
                    )
                raise e

        ManagerScheduler.setup_schedule(wrapper, schedule_time)

        while True:
            schedule.run_pending()
            time.sleep(1)


    @staticmethod
    def setup_schedule(job_wrapper, schedule_time):
        """
        Set up scheduling tasks.

        :param job_wrapper: The wrapped task function
        :param schedule_time: The schedule time
        """
        if isinstance(schedule_time, (int, float)):
            # Execute every specified number of seconds
            schedule.every(schedule_time).seconds.do(job_wrapper)
        elif isinstance(schedule_time, str):
            # Execute once at a specific time each day
            schedule.every().day.at(schedule_time).do(job_wrapper)
        elif isinstance(schedule_time, list):
            # Execute at multiple specific times each day
            for time_point in schedule_time:
                schedule.every().day.at(time_point).do(job_wrapper)
        elif isinstance(schedule_time, dict):
            # Perform complex scheduling based on dictionary key-value pairs
            for key, value in schedule_time.items():
                if isinstance(key, int):
                    # Schedule by date
                    ManagerScheduler.setup_date_schedule(job_wrapper, key, value)
                elif isinstance(key, str):
                    # Schedule by day of the week
                    ManagerScheduler.setup_week_schedule(job_wrapper, key, value)
                else:
                    raise ValueError(f"Invalid schedule key type: {type(key)}")
        else:
            raise ValueError("Invalid schedule_time type.")


    @staticmethod
    def setup_date_schedule(job_wrapper, day, value):
        """
        Schedule tasks by date.

        :param job_wrapper: The wrapped task function
        :param day: Date (1-31)
        :param value: Schedule time, can be a number (seconds), a string ("HH:MM"), a list, or other
        """
        if isinstance(value, (int, float)):
            # On the specified date, execute the task every certain seconds
            def date_wrapper():
                today = datetime.now().day
                if today == day:
                    try:
                        job_wrapper()
                    except Exception as e:
                        # Task failure handling is already in the main scheduler
                        pass

            schedule.every().day.at("00:00").do(date_wrapper).tag(str(day))
        elif isinstance(value, str):
            # Execute once at a specific time on the specified date
            def date_time_wrapper():
                today = datetime.now().day
                if today == day:
                    job_wrapper()

            schedule.every().day.at(value).do(date_time_wrapper).tag(str(day))
        elif isinstance(value, list):
            # Execute at multiple specific times on the specified date
            for time_point in value:

                def date_time_list_wrapper(tp=time_point):
                    today = datetime.now().day
                    if today == day:
                        job_wrapper()

                schedule.every().day.at(time_point).do(date_time_list_wrapper).tag(str(day))
        else:
            raise ValueError(f"Invalid schedule value type: {type(value)}")


    @staticmethod
    def setup_week_schedule(job_wrapper, day_str, value):
        """
        Schedule tasks by day of the week.

        :param job_wrapper: The wrapped task function
        :param day_str: Day of the week string (e.g., "mon", "Monday")
        :param value: Schedule time, can be a number (seconds), a string ("HH:MM"), a list, or other
        """
        day = ManagerScheduler.parse_weekday(day_str)
        if not day:
            raise ValueError(f"Invalid day of week: {day_str}")

        if isinstance(value, (int, float)):
            # Execute every specified number of seconds
            schedule.every().week.do(ManagerScheduler.run_weekly_job, job_wrapper, value).day_of_week = day
        elif isinstance(value, str):
            # Execute once at a specific time each week
            getattr(schedule.every(), day).at(value).do(job_wrapper)
        elif isinstance(value, list):
            # Execute at multiple specific times each week
            for time_point in value:
                getattr(schedule.every(), day).at(time_point).do(job_wrapper)
        else:
            raise ValueError(f"Invalid schedule value type: {type(value)}")


    @staticmethod
    def run_weekly_job(job_wrapper, interval_seconds):
        """
        Execute job_wrapper every interval_seconds during the week.

        :param job_wrapper: The wrapped task function
        :param interval_seconds: Execution interval in seconds
        """
        next_run = time.time()
        while True:
            current_time = time.time()
            if current_time >= next_run:
                try:
                    job_wrapper()
                except Exception as e:
                    pass  # Error handling is already in the main scheduler
                next_run = current_time + interval_seconds
            time.sleep(1)
            if datetime.now().weekday() != ManagerScheduler.schedule_weekday():
                break


    @staticmethod
    def parse_weekday(day_str):
        """
        Parse the day of week string.

        :param day_str: Day of week string
        :return: schedule library supported day of week method name (e.g., 'monday') or None
        """
        day_str = day_str.strip().lower()
        days = {
            "1": "monday",
            "mon": "monday",
            "monday": "monday",
            "星期一": "monday",
            "周一": "monday",
            "礼拜一": "monday",
            "2": "tuesday",
            "tue": "tuesday",
            "tuesday": "tuesday",
            "星期二": "tuesday",
            "周二": "tuesday",
            "礼拜二": "tuesday",
            "3": "wednesday",
            "wed": "wednesday",
            "wednesday": "wednesday",
            "星期三": "wednesday",
            "周三": "wednesday",
            "礼拜三": "wednesday",
            "4": "thursday",
            "thu": "thursday",
            "thursday": "thursday",
            "星期四": "thursday",
            "周四": "thursday",
            "礼拜四": "thursday",
            "5": "friday",
            "fri": "friday",
            "friday": "friday",
            "星期五": "friday",
            "周五": "friday",
            "礼拜五": "friday",
            "6": "saturday",
            "sat": "saturday",
            "saturday": "saturday",
            "星期六": "saturday",
            "周六": "saturday",
            "礼拜六": "saturday",
            "7": "sunday",
            "sun": "sunday",
            "sunday": "sunday",
            "星期日": "sunday",
            "星期天": "sunday",
            "周日": "sunday",
            "周天": "sunday",
            "礼拜日": "sunday",
            "礼拜天": "sunday",
        }
        return days.get(day_str[:3], None)


    @staticmethod
    def schedule_weekday():
        """
        Get the current weekday (0-6, 0 is Monday).
        """
        return datetime.now().weekday()


    @staticmethod
    def get_smtp_settings(email):
        email_providers = {
            "qq.com": ("smtp.qq.com", 465),
            "exmail.qq.com": ("smtp.exmail.qq.com", 465),
            "163.com": ("smtp.163.com", 465),
            "126.com": ("smtp.126.com", 465),
            "yeah.net": ("smtp.yeah.net", 465),
            "sina.com": ("smtp.sina.com", 465),
            "sina.cn": ("smtp.sina.cn", 465),
            "sohu.com": ("smtp.sohu.com", 465),
            "outlook.com": ("smtp.office365.com", 587),
            "hotmail.com": ("smtp.office365.com", 587),
            "live.com": ("smtp.office365.com", 587),
            "gmail.com": ("smtp.gmail.com", 587),
            "yahoo.com": ("smtp.mail.yahoo.com", 465),
            "yahoo.com.cn": ("smtp.mail.yahoo.com.cn", 465),
            "aliyun.com": ("smtp.aliyun.com", 465),
            "139.com": ("smtp.139.com", 465),
            "189.cn": ("smtp.189.cn", 465),
            "21cn.com": ("smtp.21cn.com", 465),
        }

        domain = email.split("@")[-1].lower()
        return email_providers.get(domain, ("smtp.exmail.qq.com", 465))


    @staticmethod
    def send_email(sender, password, recipients, smtp_server=None, smtp_port=None, smtp_ssl=True,
                subject=None, body=None, file_paths=None, img_paths=None):
        msg = MIMEMultipart()
        msg.attach(MIMEText(body or '', 'html', 'utf-8'))
        msg['Subject'] = Header(subject or '', 'utf-8')
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)

        if smtp_server is None or smtp_port is None:
            default_smtp_server, default_smtp_port = ManagerScheduler.get_smtp_settings(sender)
            smtp_server = smtp_server or default_smtp_server
            smtp_port = smtp_port or default_smtp_port

        # 处理文件附件
        if file_paths:
            if isinstance(file_paths, str):
                file_paths = [file_paths]
            for file_path in file_paths:
                att = MIMEText(open(file_path, 'rb').read(), 'base64', 'utf-8')
                att['Content-Type'] = 'application/octet-stream'
                file_name = os.path.basename(file_path)
                if re.search(r'[\u4e00-\u9fff]', file_name):
                    att.add_header('Content-Disposition', 'attachment', filename=('utf-8', '', file_name))
                else:
                    att['Content-Disposition'] = f'attachment; filename="{file_name}"'
                msg.attach(att)

        # 处理图片
        if img_paths:
            if isinstance(img_paths, str):
                img_paths = [img_paths]
            mime_images = ''
            for i, img_path in enumerate(img_paths, start=1):
                mime_images += f'<p><img src="cid:imageid{i}" alt="imageid{i}"></p>'
                with open(img_path, 'rb') as img_file:
                    mime_img = MIMEImage(img_file.read(), _subtype='octet-stream')
                    mime_img.add_header('Content-ID', f'<imageid{i}>')
                    msg.attach(mime_img)
            
            mime_html = MIMEText(f'<html><body><p>{body or ""}</p>{mime_images}</body></html>', 'html', 'utf-8')
            msg.attach(mime_html)

        try:
            if smtp_ssl:
                server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            else:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
            server.login(sender, password)
            server.sendmail(sender, recipients, msg.as_string())
            server.quit()
        except Exception as e:
            print(f"Failed to send email: {str(e)}")