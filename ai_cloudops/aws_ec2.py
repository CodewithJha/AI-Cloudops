from tkinter import simpledialog, messagebox
import boto3
from botocore.config import Config as BotoConfig
from .config import aws_config


def _ec2_client():
    session_kwargs = {}
    if aws_config.profile:
        session_kwargs["profile_name"] = aws_config.profile
    session = boto3.session.Session(**session_kwargs)
    return session.client(
        "ec2",
        region_name=aws_config.region,
        config=BotoConfig(retries={"max_attempts": 10, "mode": "standard"}),
    )


def start_instance(instance_id: str):
    ec2 = _ec2_client()
    return ec2.start_instances(InstanceIds=[instance_id])


def stop_instance(instance_id: str):
    ec2 = _ec2_client()
    return ec2.stop_instances(InstanceIds=[instance_id])


def terminate_instance(instance_id: str):
    ec2 = _ec2_client()
    return ec2.terminate_instances(InstanceIds=[instance_id])


def start_instance_interactive():
    instance_id = simpledialog.askstring("Start Instance", "Enter instance ID to start:")
    if not instance_id:
        return
    start_instance(instance_id)
    messagebox.showinfo("Success", f"Instance {instance_id} started successfully!")


def stop_instance_interactive():
    instance_id = simpledialog.askstring("Stop Instance", "Enter instance ID to stop:")
    if not instance_id:
        return
    stop_instance(instance_id)
    messagebox.showinfo("Success", f"Instance {instance_id} stopped successfully!")


def terminate_instance_interactive():
    instance_id = simpledialog.askstring(
        "Terminate Instance", "Enter instance ID to terminate:"
    )
    if not instance_id:
        return
    terminate_instance(instance_id)
    messagebox.showinfo("Success", f"Instance {instance_id} terminated successfully!")

