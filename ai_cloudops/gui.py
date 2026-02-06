import tkinter as tk
from .config import app_config
from .camera import filter_camera
from .geolocation import prompt_and_show_location
from .emailer import send_email_interactive
from .aws_ec2 import (
    start_instance_interactive,
    stop_instance_interactive,
    terminate_instance_interactive,
)
from .aws_s3 import upload_file_interactive, delete_file_interactive
from .web import open_default_webpage


def build_and_run_gui():
    root = tk.Tk()
    root.title(app_config.app_title)
    root.geometry("650x260")

    # Row 0
    btn_filter_camera = tk.Button(
        root, text="Filter Camera", command=filter_camera, bg="#2ecc71", fg="white", width=20, height=2
    )
    btn_filter_camera.grid(row=0, column=0, padx=20, pady=20)

    btn_get_location = tk.Button(
        root,
        text="Get Location",
        command=prompt_and_show_location,
        bg="#f39c12",
        fg="white",
        width=20,
        height=2,
    )
    btn_get_location.grid(row=0, column=1, padx=20, pady=20)

    btn_send_email = tk.Button(
        root, text="Send Email", command=send_email_interactive, bg="#3498db", fg="white", width=20, height=2
    )
    btn_send_email.grid(row=0, column=2, padx=20, pady=20)

    # Row 1
    btn_start_ec2 = tk.Button(
        root, text="Start EC2", command=start_instance_interactive, bg="#27ae60", fg="white", width=20, height=2
    )
    btn_start_ec2.grid(row=1, column=0, padx=20, pady=20)

    btn_stop_ec2 = tk.Button(
        root, text="Stop EC2", command=stop_instance_interactive, bg="#e67e22", fg="white", width=20, height=2
    )
    btn_stop_ec2.grid(row=1, column=1, padx=20, pady=20)

    btn_terminate_ec2 = tk.Button(
        root,
        text="Terminate EC2",
        command=terminate_instance_interactive,
        bg="#e74c3c",
        fg="white",
        width=20,
        height=2,
    )
    btn_terminate_ec2.grid(row=1, column=2, padx=20, pady=20)

    # Row 2
    btn_s3_upload = tk.Button(
        root, text="S3 Upload", command=upload_file_interactive, bg="#8e44ad", fg="white", width=20, height=2
    )
    btn_s3_upload.grid(row=2, column=0, padx=20, pady=20)

    btn_s3_delete = tk.Button(
        root, text="S3 Delete", command=delete_file_interactive, bg="#9b59b6", fg="white", width=20, height=2
    )
    btn_s3_delete.grid(row=2, column=1, padx=20, pady=20)

    btn_open_webpage = tk.Button(
        root, text="Open Web Page", command=open_default_webpage, bg="#34495e", fg="white", width=20, height=2
    )
    btn_open_webpage.grid(row=2, column=2, padx=20, pady=20)

    root.mainloop()

