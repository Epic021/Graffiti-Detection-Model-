# Graffiti Detection System

A real-time computer vision system designed to detect and monitor graffiti or unauthorized markings in a specific region of interest (ROI) using a camera feed.

## Features

- Real-time video monitoring with configurable Region of Interest (ROI)
- Motion detection using Mean Squared Error (MSE) analysis
- Automatic event logging with timestamps
- Email notifications with captured images
- SMS notifications (optional)
- Configurable detection parameters
- Motion blur reduction for better detection

## Prerequisites

- Python 
- OpenCV (cv2)
- NumPy
- SMTP library for email functionality
- Requests library for SMS functionality

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd Graffiti-Detection-Model-
```

2. Install required packages:
```bash
pip install opencv-python numpy requests
```

## Configuration

Edit `project_config.py` to configure the following settings:

### Email Settings
- `EXTDEF_ENABLE_EMAIL`: Enable/disable email notifications
- `EXTDEF_EMAIL_TOADDR`: Recipient email address
- `EXTDEF_EMAIL_FROMADDR`: Sender email address
- `EXTDEF_EMAIL_GMAIL_KEY`: Gmail app password
- `EXTDEF_EMAIL_SUBJECT`: Email subject
- `EXTDEF_EMAIL_BODY`: Email body

### SMS Settings
- `EXTDEF_ENABLE_SMS`: Enable/disable SMS notifications
- `EXTDEF_SMS_APIKEY`: Fast2SMS API key
- `EXTDEF_SMS_TONUMBER`: Recipient phone number
- `EXTDEF_SMS_BODY`: SMS message body

### Detection Settings
- `EXTDEF_UPDATE_IMAGE_FLAG`: Enable/disable reference image updates
- `EXTDEF_EVENT_CHECK_FRAMES`: Number of frames to check for changes
- `EXTDEF_SUSTAINED_EVENT_VERIFICATION_RUNS`: Number of sustained detections required
- `EXTDEF_NOTIFICATION_GAP_IN_SECONDS`: Time gap between notifications

## Usage

1. Configure the settings in `project_config.py`
2. Run the main script:
```bash
python main.py
```

3. The system will:
   - Initialize the camera feed
   - Display the video feed with ROI
   - Monitor for changes in the ROI
   - Send notifications when changes are detected
   - Log events to `eventlog.txt`

## Camera Configuration

The system uses the following default camera settings:
- Device ID: 0
- Resolution: 320x240
- ROI Position: (80, 20)
- ROI Size: 120x120 pixels

## Event Detection

The system uses the following detection process:
1. Captures initial reference frame
2. Continuously compares new frames with reference
3. Triggers event when sustained changes are detected
4. Sends notifications and logs events
5. Updates reference image if configured

## File Structure

- `main.py`: Core detection and monitoring logic
- `project_config.py`: Configuration settings
- `send_sms.py`: SMS notification functionality
- `imageTransfer.py`: Email notification functionality
- `eventlog.txt`: Event logging file

## Security Notes

- Keep your email and SMS credentials secure
- Do not commit sensitive information to version control
- Use environment variables for sensitive data in production
