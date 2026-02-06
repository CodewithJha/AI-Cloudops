from tkinter import simpledialog, filedialog, messagebox
import boto3
from botocore.config import Config as BotoConfig
from .config import aws_config
import os


def _s3_client():
    session_kwargs = {}
    if aws_config.profile:
        session_kwargs["profile_name"] = aws_config.profile
    session = boto3.session.Session(**session_kwargs)
    return session.client(
        "s3",
        region_name=aws_config.region,
        config=BotoConfig(retries={"max_attempts": 10, "mode": "standard"}),
    )


def upload_fileobj(bucket: str, key: str, fileobj):
    s3 = _s3_client()
    s3.upload_fileobj(fileobj, bucket, key)
    return {"bucket": bucket, "key": key}


def delete_file(bucket: str, key: str):
    s3 = _s3_client()
    s3.delete_object(Bucket=bucket, Key=key)
    return {"bucket": bucket, "key": key}


def upload_file_interactive():
    filename = filedialog.askopenfilename(title="Select a file to upload")
    if not filename:
        return

    default_bucket = aws_config.default_s3_bucket
    bucket = (
        simpledialog.askstring("S3 Bucket", "Enter S3 bucket name:", initialvalue=default_bucket)
        or default_bucket
    )
    if not bucket:
        messagebox.showerror("Error", "Bucket name is required.")
        return

    key = os.path.basename(filename)
    try:
        s3 = _s3_client()
        s3.upload_file(filename, bucket, key)
        messagebox.showinfo("Success", f"Uploaded {key} to {bucket}")
    except Exception as exc:
        messagebox.showerror("Error", f"Failed to upload: {exc}")


def delete_file_interactive():
    default_bucket = aws_config.default_s3_bucket
    bucket = (
        simpledialog.askstring("S3 Bucket", "Enter S3 bucket name:", initialvalue=default_bucket)
        or default_bucket
    )
    if not bucket:
        messagebox.showerror("Error", "Bucket name is required.")
        return
    key = simpledialog.askstring("S3 Key", "Enter the filename/key to delete:")
    if not key:
        return
    try:
        delete_file(bucket, key)
        messagebox.showinfo("Success", f"Deleted {key} from {bucket}")
    except Exception as exc:
        messagebox.showerror("Error", f"Failed to delete: {exc}")

