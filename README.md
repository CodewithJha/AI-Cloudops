 import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import cv2
import smtplib
from geopy.geocoders import Nominatim
import boto3
import webbrowser

# Function to filter camera frames
def filter_camera():
    # Open default camera (usually 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Unable to open camera.")
        return
    
    filters = ["original", "grayscale", "invert"]
    current_filter_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame.")
            break

        # Apply the current filter
        current_filter = filters[current_filter_index]
        filtered_frame = apply_filter(frame, current_filter)

        # Display the filtered frame
        cv2.imshow('Filtered', filtered_frame)

        # Check for key press to switch filters
        key = cv2.waitKey(1)
        if key == ord('q'):  # Quit
            break
        elif key == ord('s'):  # Shuffle filter
            current_filter_index = (current_filter_index + 1) % len(filters)

    # Release the camera and close OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

# Function to apply filters to camera frames
def apply_filter(frame, filter_type):
    if filter_type == "grayscale":
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    elif filter_type == "invert":
        return cv2.bitwise_not(frame)
    else:
        return frame

# Function to get the location details
def get_location():
    # Ask user for location input
    location_input = simpledialog.askstring("Location Input", "Enter your location (address or city):")
    
    if location_input:
        # Initialize geolocator
        geolocator = Nominatim(user_agent="geoapiExercises")

        # Get the user's location details
        location = geolocator.geocode(location_input)

        if location:
            # Display latitude, longitude, and city name
            latitude = location.latitude
            longitude = location.longitude
            city = location.address.split(",")[-3]

            message = f"Latitude: {latitude}\nLongitude: {longitude}\nCity: {city}"
            messagebox.showinfo("Location Details", message)
        else:
            messagebox.showerror("Error", "Unable to retrieve location details.")
    else:
        messagebox.showerror("Error", "Location input is empty.")

# Function to send email
def send_email():
    # Get sender's email address and password
    sender_email = "kaatilladka18@gmail.com"
    sender_password = "zpenwbcqjwcxfsfn"

    # Set the SMTP server address
    smtp_server = "smtp.gmail.com"

    # Get the recipient's email address
    recipient_email = simpledialog.askstring("Recipient's Email", "Enter the recipient's email address:")

    # Get the email subject and body
    subject = simpledialog.askstring("Email Subject", "Enter the email subject:")
    body = simpledialog.askstring("Email Body", "Enter the email body:")

    # Create the email message
    message = f"Subject: {subject}\n\n{body}"

    # Connect to the SMTP server
    server = smtplib.SMTP(smtp_server, 587)
    server.starttls()
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, recipient_email, message)
    server.quit()

    print("Email sent!")

# Function to manage AWS EC2 instances
def manage_ec2():
    # Initialize EC2 client
    ec2 = boto3.client('ec2')

    def start_instance():
        instance_id = simpledialog.askstring("Start Instance", "Enter instance ID to start:")
        if instance_id:
            ec2.start_instances(InstanceIds=[instance_id])
            messagebox.showinfo("Success", f"Instance {instance_id} started successfully!")

    def stop_instance():
        instance_id = simpledialog.askstring("Stop Instance", "Enter instance ID to stop:")
        if instance_id:
            ec2.stop_instances(InstanceIds=[instance_id])
            messagebox.showinfo("Success", f"Instance {instance_id} stopped successfully!")

    def terminate_instance():
        instance_id = simpledialog.askstring("Terminate Instance", "Enter instance ID to terminate:")
        if instance_id:
            ec2.terminate_instances(InstanceIds=[instance_id])
            messagebox.showinfo("Success", f"Instance {instance_id} terminated successfully!")

    def exit_program():
        root.destroy()

    # Create tkinter window
    root = tk.Tk()
    root.title("AWS EC2 Management")

    # Create buttons
    start_button = tk.Button(root, text="Start Instance", command=start_instance, bg="#4CAF50", fg="white", width=20, height=2)
    start_button.pack(pady=5)

    stop_button = tk.Button(root, text="Stop Instance", command=stop_instance, bg="#008CBA", fg="white", width=20, height=2)
    stop_button.pack(pady=5)

    terminate_button = tk.Button(root, text="Terminate Instance", command=terminate_instance, bg="#f44336", fg="white", width=20, height=2)
    terminate_button.pack(pady=5)

    exit_button = tk.Button(root, text="Exit", command=exit_program, bg="#9b59b6", fg="white", width=20, height=2)
    exit_button.pack(pady=5)

    root.mainloop()

def s3_updl():
    class S3FileManager:
        def __init__(self, root):
            self.root = root
            self.root.title("S3 File Manager")

            # Initialize Boto3 client with AWS credentials
            self.s3 = boto3.client(
                's3',
                aws_access_key_id='AKIATCK7KNGBJOPYODZQ',
                aws_secret_access_key='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',
                region_name='ap-south-1'
            )

            # Create buttons
            self.upload_button = tk.Button(root, text="Upload File", command=self.upload_file, width=20, height=2)
            self.delete_button = tk.Button(root, text="Delete File", command=self.delete_file, width=20, height=2)

            # Layout
            self.upload_button.pack(pady=10)
            self.delete_button.pack(pady=10)

        def upload_file(self):
            filename = filedialog.askopenfilename(title="Select a file to upload")
            if filename:
                try:
                    # Get the filename from the path
                    key = filename.split("/")[-1]

                    # Upload file to S3 bucket
                    self.s3.upload_file(filename, 'myprojectbasket', key)

                    messagebox.showinfo("Success", "File uploaded successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to upload file: {e}")

        def delete_file(self):
            key = simpledialog.askstring("Delete File", "Enter the filename to delete:")
            if key:
                try:
                    # Delete file from S3 bucket
                    self.s3.delete_object(Bucket='myprojectbasket', Key=key)

                    messagebox.showinfo("Success", "File deleted successfully!")
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to delete file: {e}")

    root = tk.Tk()
    app = S3FileManager(root)
    root.mainloop()

def open_webpage():
    url = "http://3.110.30.49:10001/"
    webbrowser.open_new(url)

# Create main window
root = tk.Tk()
root.title("Button GUI")
root.geometry('500x300')
# Create buttons
btn_filter_camera = tk.Button(root, text="Filter Camera", command=filter_camera, bg="#2ecc71", fg="white", width=20, height=2)
btn_filter_camera.grid(row=0, column=0, padx=20, pady=20)

btn_get_location = tk.Button(root, text="Get Location", command=get_location, bg="#f39c12", fg="white", width=20, height=2)
btn_get_location.grid(row=0, column=1, padx=20, pady=20)

btn_send_email = tk.Button(root, text="Send Email", command=send_email, bg="#3498db", fg="white", width=20, height=2)
btn_send_email.grid(row=0, column=2, padx=20, pady=20)

btn_manage_ec2 = tk.Button(root, text="Manage EC2", command=manage_ec2, bg="#e74c3c", fg="white", width=20, height=2)
btn_manage_ec2.grid(row=1, column=0, padx=20, pady=20)

btn_s3_updl = tk.Button(root, text="s3 updl", command=s3_updl, bg="#e74c3c", fg="white", width=20, height=2)
btn_s3_updl.grid(row=1, column=1, padx=20, pady=20)

btn_open_webpage = tk.Button(root, text="Open Web Page", command=open_webpage, bg="#9b59b6", fg="white", width=20, height=2)
btn_open_webpage.grid(row=1, column=2, padx=20, pady=20)

# Run the Tkinter event loop
root.mainloop()
