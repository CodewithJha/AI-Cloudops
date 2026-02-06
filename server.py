from fastapi import FastAPI, Response, UploadFile, File, Form, Body
from fastapi.responses import JSONResponse
from typing import Optional
from ai_cloudops.geolocation import geocode_location
from ai_cloudops.emailer import send_email
from ai_cloudops.aws_ec2 import start_instance, stop_instance, terminate_instance
from ai_cloudops.aws_s3 import upload_fileobj, delete_file
from ai_cloudops.config import aws_config, email_config

app = FastAPI(title="AI CloudOps Web")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/")
def home():
    # Premium black & white themed dashboard
    html = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>AI CloudOps | Premium Dashboard</title>
      <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
          background: #0a0a0a;
          color: #ffffff;
          min-height: 100vh;
          padding: 40px 20px;
          line-height: 1.6;
          position: relative;
        }
        .container { max-width: 1400px; margin: 0 auto; }
        .header {
          text-align: center;
          margin-bottom: 60px;
          padding-bottom: 40px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.1);
          position: relative;
        }
        .header::after {
          content: '';
          position: absolute;
          bottom: -1px;
          left: 50%;
          transform: translateX(-50%);
          width: 100px;
          height: 1px;
          background: #ffffff;
        }
        .header h1 {
          font-size: 3.5em;
          font-weight: 300;
          letter-spacing: 8px;
          color: #ffffff;
          margin-bottom: 15px;
          text-transform: uppercase;
          position: relative;
        }
        .header p {
          color: rgba(255, 255, 255, 0.5);
          font-size: 1.1em;
          font-weight: 300;
          letter-spacing: 2px;
        }
        .grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
          gap: 30px;
          margin-bottom: 40px;
        }
        .card {
          background: #111111;
          border: 1px solid rgba(255, 255, 255, 0.08);
          border-radius: 12px;
          padding: 35px;
          transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
          position: relative;
          overflow: hidden;
        }
        .card::before {
          content: '';
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 2px;
          background: #ffffff;
          transform: scaleX(0);
          transition: transform 0.4s ease;
        }
        .card:hover::before {
          transform: scaleX(1);
        }
        .card:hover {
          border-color: rgba(255, 255, 255, 0.2);
          box-shadow: 0 12px 32px rgba(0, 0, 0, 0.6);
          transform: translateY(-4px);
        }
        .card h2 {
          color: #ffffff;
          font-size: 1.4em;
          font-weight: 400;
          margin-bottom: 12px;
          letter-spacing: 1px;
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .card h2::before {
          content: '';
          width: 4px;
          height: 24px;
          background: #ffffff;
          display: inline-block;
          border-radius: 2px;
        }
        .card-icon {
          font-size: 1.2em;
          margin-right: 8px;
          opacity: 0.8;
        }
        .card p {
          color: rgba(255, 255, 255, 0.6);
          font-size: 0.95em;
          margin-bottom: 20px;
          line-height: 1.6;
        }
        input, textarea, select {
          width: 100%;
          padding: 14px 16px;
          margin: 10px 0;
          background: #1a1a1a;
          border: 1px solid rgba(255, 255, 255, 0.1);
          border-radius: 6px;
          color: #ffffff;
          font-size: 14px;
          font-family: inherit;
          transition: all 0.3s ease;
        }
        input:focus, textarea:focus, select:focus {
          outline: none;
          border-color: rgba(255, 255, 255, 0.4);
          background: #1f1f1f;
          box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.05);
        }
        input::placeholder, textarea::placeholder {
          color: rgba(255, 255, 255, 0.3);
        }
        button {
          padding: 12px 28px;
          margin: 6px 6px 6px 0;
          background: #ffffff;
          border: 1px solid #ffffff;
          border-radius: 6px;
          color: #000000;
          font-weight: 500;
          font-size: 13px;
          cursor: pointer;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          text-transform: uppercase;
          letter-spacing: 1.5px;
          font-family: inherit;
          position: relative;
          overflow: hidden;
        }
        button::before {
          content: '';
          position: absolute;
          top: 50%;
          left: 50%;
          width: 0;
          height: 0;
          border-radius: 50%;
          background: rgba(0, 0, 0, 0.1);
          transform: translate(-50%, -50%);
          transition: width 0.6s, height 0.6s;
        }
        button:hover::before {
          width: 300px;
          height: 300px;
        }
        button:hover {
          background: transparent;
          color: #ffffff;
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(255, 255, 255, 0.15);
        }
        button:active { transform: translateY(0); }
        button:disabled {
          opacity: 0.6;
          cursor: not-allowed;
          pointer-events: none;
        }
        .btn-danger {
          background: transparent;
          color: #ffffff;
          border-color: rgba(255, 255, 255, 0.3);
        }
        .btn-danger:hover {
          background: #ffffff;
          color: #000000;
          border-color: #ffffff;
        }
        .btn-success {
          background: #ffffff;
          color: #000000;
        }
        .btn-success:hover {
          background: transparent;
          color: #ffffff;
        }
        .spinner {
          display: inline-block;
          width: 14px;
          height: 14px;
          border: 2px solid rgba(0, 0, 0, 0.3);
          border-top-color: #000000;
          border-radius: 50%;
          animation: spin 0.6s linear infinite;
          margin-right: 8px;
          vertical-align: middle;
        }
        button.loading .spinner {
          border-color: rgba(255, 255, 255, 0.3);
          border-top-color: #ffffff;
        }
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
        video {
          width: 100%;
          max-width: 500px;
          border-radius: 8px;
          border: 1px solid rgba(255, 255, 255, 0.1);
          margin: 20px 0;
          background: #000000;
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.5);
        }
        pre {
          background: #0a0a0a;
          border: 1px solid rgba(255, 255, 255, 0.08);
          border-radius: 6px;
          padding: 18px;
          color: rgba(255, 255, 255, 0.8);
          font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
          font-size: 12px;
          overflow-x: auto;
          margin-top: 15px;
          min-height: 50px;
          white-space: pre-wrap;
          word-wrap: break-word;
          line-height: 1.6;
          transition: all 0.3s ease;
        }
        pre.success {
          border-color: rgba(255, 255, 255, 0.2);
          background: rgba(255, 255, 255, 0.02);
        }
        pre.error {
          border-color: rgba(255, 255, 255, 0.15);
        }
        .btn-group {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
          margin-top: 15px;
        }
        .status-badge {
          display: inline-block;
          padding: 4px 10px;
          background: rgba(255, 255, 255, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.2);
          border-radius: 12px;
          font-size: 11px;
          margin-left: 10px;
          font-weight: 500;
          letter-spacing: 0.5px;
          animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse {
          0%, 100% { opacity: 1; }
          50% { opacity: 0.6; }
        }
        .file-input-wrapper {
          position: relative;
          margin: 10px 0;
        }
        .file-input-wrapper input[type="file"] {
          padding: 12px;
          cursor: pointer;
        }
        select {
          cursor: pointer;
        }
        .toast-container {
          position: fixed;
          top: 20px;
          right: 20px;
          z-index: 10000;
          display: flex;
          flex-direction: column;
          gap: 10px;
        }
        .toast {
          background: #111111;
          border: 1px solid rgba(255, 255, 255, 0.2);
          border-radius: 8px;
          padding: 16px 20px;
          min-width: 300px;
          box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
          animation: slideIn 0.3s ease-out;
          display: flex;
          align-items: center;
          gap: 12px;
        }
        .toast.success {
          border-left: 3px solid #ffffff;
        }
        .toast.error {
          border-left: 3px solid rgba(255, 255, 255, 0.5);
        }
        .toast-icon {
          font-size: 20px;
        }
        .toast-message {
          flex: 1;
          font-size: 14px;
          color: rgba(255, 255, 255, 0.9);
        }
        .status-bar {
          display: flex;
          flex-wrap: wrap;
          gap: 16px;
          align-items: center;
          justify-content: center;
          margin-bottom: 24px;
          font-size: 12px;
          color: rgba(255, 255, 255, 0.7);
        }
        .status-item {
          border: 1px solid rgba(255, 255, 255, 0.15);
          border-radius: 999px;
          padding: 6px 16px;
          display: flex;
          align-items: center;
          gap: 6px;
        }
        .status-item span {
          font-weight: 500;
          color: #ffffff;
        }
        .command-row {
          margin-bottom: 32px;
          display: flex;
          justify-content: center;
        }
        .command-input {
          width: 100%;
          max-width: 600px;
          padding: 12px 16px;
          background: #101010;
          border-radius: 999px;
          border: 1px solid rgba(255, 255, 255, 0.15);
          color: #ffffff;
          font-size: 13px;
        }
        .command-input::placeholder {
          color: rgba(255, 255, 255, 0.35);
        }
        .activity-card {
          margin-top: 32px;
        }
        .activity-list {
          list-style: none;
          margin-top: 12px;
        }
        .activity-item {
          display: flex;
          gap: 10px;
          padding: 6px 0;
          border-bottom: 1px solid rgba(255, 255, 255, 0.06);
          font-size: 12px;
          color: rgba(255, 255, 255, 0.7);
        }
        .activity-time {
          font-family: 'SF Mono', 'Monaco', 'Courier New', monospace;
          color: rgba(255, 255, 255, 0.4);
          min-width: 64px;
        }
        .activity-text {
          flex: 1;
        }
        @keyframes slideIn {
          from {
            transform: translateX(400px);
            opacity: 0;
          }
          to {
            transform: translateX(0);
            opacity: 1;
          }
        }
        @media (max-width: 768px) {
          .header h1 { font-size: 2.5em; letter-spacing: 4px; }
          .grid { grid-template-columns: 1fr; }
          .card { padding: 25px; }
          .toast-container { right: 10px; left: 10px; }
          .toast { min-width: auto; }
        }
      </style>
    </head>
    <body>
      <div class="toast-container" id="toastContainer"></div>
      
      <div class="container">
        <div class="header">
          <h1>AI CloudOps</h1>
          <p>Premium Cloud Operations Dashboard</p>
        </div>

        <div class="status-bar">
          <div class="status-item">Environment<span>Local</span></div>
          <div class="status-item">Email<span id="emailStatus">Configured</span></div>
          <div class="status-item">AWS<span id="awsStatus">Not checked</span></div>
        </div>

        <div class="command-row">
          <input
            id="commandInput"
            class="command-input"
            placeholder="Type a command like 'start ec2 i-123...' – (visual demo only for now)"
          />
        </div>

        <div class="grid">
          <!-- Camera Card -->
          <div class="card">
            <h2><span class="card-icon">📹</span>Camera Filter <span class="status-badge">Live</span></h2>
            <p>Browser camera preview with real-time filters</p>
            <video id="cam" width="400" height="300" autoplay playsinline></video>
            <div class="btn-group">
              <button id="camBtn" onclick="startCam()">Start Camera</button>
              <select id="filter" onchange="applyFilter()" style="width: auto; min-width: 150px;">
                <option value="none">Original</option>
                <option value="grayscale(100%)">Grayscale</option>
                <option value="invert(100%)">Invert</option>
              </select>
            </div>
            <pre id="camout"></pre>
          </div>

          <!-- Geolocation Card -->
          <div class="card">
            <h2><span class="card-icon">📍</span>Geolocation</h2>
            <p>Lookup coordinates and location details</p>
            <input id="locq" type="text" placeholder="Enter city or address..." />
            <div class="btn-group">
              <button id="geoBtn" onclick="doGeocode()">Lookup</button>
              <button id="geoLiveBtn" onclick="useLiveLocation()" class="btn-danger">Use My Live Location</button>
            </div>
            <pre id="locout"></pre>
          </div>

          <!-- Email Card -->
          <div class="card">
            <h2><span class="card-icon">✉️</span>Email Service</h2>
            <p>Send emails via SMTP</p>
            <input id="to" type="email" placeholder="Recipient email" />
            <input id="subject" type="text" placeholder="Subject" />
            <textarea id="body" rows="4" placeholder="Message body..."></textarea>
            <button id="emailBtn" onclick="sendEmail()" class="btn-success">Send Email</button>
            <pre id="emailout"></pre>
          </div>

          <!-- EC2 Card -->
          <div class="card">
            <h2><span class="card-icon">☁️</span>AWS EC2</h2>
            <p>Manage EC2 instances</p>
            <input id="instanceId" type="text" placeholder="Instance ID (e.g., i-1234567890abcdef0)" />
            <div class="btn-group">
              <button id="ec2StartBtn" onclick="ec2('start')" class="btn-success">Start</button>
              <button id="ec2StopBtn" onclick="ec2('stop')">Stop</button>
              <button id="ec2TermBtn" onclick="ec2('terminate')" class="btn-danger">Terminate</button>
            </div>
            <pre id="ec2out"></pre>
          </div>

          <!-- S3 Card -->
          <div class="card">
            <h2><span class="card-icon">📦</span>AWS S3</h2>
            <p>Upload and manage S3 files</p>
            <input id="bucket" type="text" placeholder="Bucket name (optional)" />
            <input id="key" type="text" placeholder="File key/path (optional)" />
            <div class="file-input-wrapper">
              <input id="file" type="file" />
            </div>
            <div class="btn-group">
              <button id="s3UploadBtn" onclick="s3Upload()" class="btn-success">Upload</button>
              <button id="s3DeleteBtn" onclick="s3Delete()" class="btn-danger">Delete</button>
            </div>
            <pre id="s3out"></pre>
          </div>
        </div>

        <div class="activity-card card">
          <h2>Recent Activity</h2>
          <p>Live log of AI CloudOps actions in this session.</p>
          <ul id="activityList" class="activity-list"></ul>
        </div>
      </div>

      <script>
        function addActivity(text) {
          const list = document.getElementById('activityList');
          if (!list) return;
          const li = document.createElement('li');
          const now = new Date();
          const time = now.toLocaleTimeString();
          li.className = 'activity-item';
          li.innerHTML = `<span class="activity-time">${time}</span><span class="activity-text">${text}</span>`;
          list.prepend(li);
          const maxItems = 30;
          while (list.children.length > maxItems) {
            list.removeChild(list.lastChild);
          }
        }

        function showToast(message, type = 'success') {
          const container = document.getElementById('toastContainer');
          const toast = document.createElement('div');
          toast.className = `toast ${type}`;
          toast.innerHTML = `
            <span class="toast-icon">${type === 'success' ? '✓' : '✕'}</span>
            <span class="toast-message">${message}</span>
          `;
          container.appendChild(toast);
          setTimeout(() => {
            toast.style.animation = 'slideIn 0.3s ease-out reverse';
            setTimeout(() => toast.remove(), 300);
          }, 3000);
        }

        function setLoading(btnId, loading) {
          const btn = document.getElementById(btnId);
          if (!btn) return;
          if (loading) {
            btn.disabled = true;
            btn.classList.add('loading');
            btn.innerHTML = '<span class="spinner"></span>' + btn.textContent.trim();
          } else {
            btn.disabled = false;
            btn.classList.remove('loading');
            // Restore original text based on button
            const originalTexts = {
              'camBtn': 'Start Camera',
              'geoBtn': 'Lookup',
              'emailBtn': 'Send Email',
              'ec2StartBtn': 'Start',
              'ec2StopBtn': 'Stop',
              'ec2TermBtn': 'Terminate',
              's3UploadBtn': 'Upload',
              's3DeleteBtn': 'Delete'
            };
            btn.textContent = originalTexts[btnId] || btn.textContent;
          }
        }

        function setOutput(elementId, text, type = '') {
          const el = document.getElementById(elementId);
          el.textContent = text;
          el.className = type ? `pre ${type}` : 'pre';
        }

        async function startCam() {
          const v = document.getElementById('cam');
          const out = document.getElementById('camout');
          const btn = document.getElementById('camBtn');
          
          setLoading('camBtn', true);
          try {
            const stream = await navigator.mediaDevices.getUserMedia({ video: true });
            v.srcObject = stream;
            setOutput('camout', '[SUCCESS] Camera active', 'success');
            showToast('Camera activated successfully', 'success');
            addActivity('Camera started on local device');
          } catch (e) {
            setOutput('camout', '[ERROR] Camera error: ' + e.message, 'error');
            showToast('Camera error: ' + e.message, 'error');
          } finally {
            setLoading('camBtn', false);
          }
        }

        function applyFilter() {
          const v = document.getElementById('cam');
          const f = document.getElementById('filter').value;
          v.style.filter = f;
        }

        async function doGeocode() {
          const q = document.getElementById('locq').value;
          const out = document.getElementById('locout');
          if (!q) {
            setOutput('locout', '[WARNING] Please enter a location', 'error');
            return;
          }
          setLoading('geoBtn', true);
          setOutput('locout', '[PROCESSING] Searching...');
          try {
            const r = await fetch('/api/location', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({ query: q })
            });
            const data = await r.json();
            if (r.ok) {
              setOutput('locout', JSON.stringify(data, null, 2), 'success');
              showToast('Location found successfully', 'success');
              addActivity('Geolocation lookup: ' + (data.city || 'Unknown location'));
            } else {
              setOutput('locout', '[ERROR] ' + (data.error || 'Not found'), 'error');
              showToast('Location not found', 'error');
            }
          } catch (e) {
            setOutput('locout', '[ERROR] ' + e.message, 'error');
            showToast('Geolocation error', 'error');
          } finally {
            setLoading('geoBtn', false);
          }
        }

        async function useLiveLocation() {
          const out = document.getElementById('locout');
          if (!navigator.geolocation) {
            setOutput('locout', '[ERROR] Geolocation is not supported by this browser.', 'error');
            showToast('Geolocation not supported', 'error');
            return;
          }

          setLoading('geoLiveBtn', true);
          setOutput('locout', '[PROCESSING] Requesting device location permission...');

          navigator.geolocation.getCurrentPosition(
            async (pos) => {
              const latitude = pos.coords.latitude;
              const longitude = pos.coords.longitude;
              try {
                setOutput('locout', '[PROCESSING] Reverse geocoding coordinates...');
                const r = await fetch('/api/location/reverse', {
                  method: 'POST',
                  headers: {'Content-Type': 'application/json'},
                  body: JSON.stringify({ latitude, longitude })
                });
                const data = await r.json();
                if (r.ok) {
                  setOutput('locout', JSON.stringify(data, null, 2), 'success');
                  showToast('Live location retrieved', 'success');
                  addActivity('Live location: ' + (data.city || 'Unknown city'));
                } else {
                  setOutput('locout', '[ERROR] ' + (data.error || 'Reverse geocode failed'), 'error');
                  showToast('Reverse geocode failed', 'error');
                }
              } catch (e) {
                setOutput('locout', '[ERROR] ' + e.message, 'error');
                showToast('Live location error', 'error');
              } finally {
                setLoading('geoLiveBtn', false);
              }
            },
            (err) => {
              setOutput('locout', '[ERROR] Permission denied or unavailable: ' + err.message, 'error');
              showToast('Location permission denied', 'error');
              setLoading('geoLiveBtn', false);
            },
            { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
          );
        }

        async function sendEmail() {
          const to = document.getElementById('to').value;
          const subject = document.getElementById('subject').value;
          const body = document.getElementById('body').value;
          const out = document.getElementById('emailout');
          if (!to || !subject || !body) {
            setOutput('emailout', '[WARNING] Please fill all fields', 'error');
            return;
          }
          setLoading('emailBtn', true);
          setOutput('emailout', '[PROCESSING] Sending...');
          try {
            const r = await fetch('/api/email/send', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({ to, subject, body })
            });
            const data = await r.json();
            if (r.ok) {
              setOutput('emailout', '[SUCCESS] ' + JSON.stringify(data, null, 2), 'success');
              showToast('Email sent successfully', 'success');
              document.getElementById('to').value = '';
              document.getElementById('subject').value = '';
              document.getElementById('body').value = '';
              addActivity('Email sent to ' + to);
            } else {
              setOutput('emailout', '[ERROR] ' + (data.error || 'Failed to send'), 'error');
              showToast('Failed to send email', 'error');
            }
          } catch (e) {
            setOutput('emailout', '[ERROR] ' + e.message, 'error');
            showToast('Email error: ' + e.message, 'error');
          } finally {
            setLoading('emailBtn', false);
          }
        }

        async function ec2(action) {
          const instance_id = document.getElementById('instanceId').value;
          const out = document.getElementById('ec2out');
          if (!instance_id) {
            setOutput('ec2out', '[WARNING] Please enter an instance ID', 'error');
            return;
          }
          const btnId = action === 'start' ? 'ec2StartBtn' : action === 'stop' ? 'ec2StopBtn' : 'ec2TermBtn';
          setLoading(btnId, true);
          setOutput('ec2out', '[PROCESSING] Processing...');
          try {
            const r = await fetch('/api/ec2/' + action, {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({ instance_id })
            });
            const data = await r.json();
            if (r.ok) {
              setOutput('ec2out', '[SUCCESS] ' + JSON.stringify(data, null, 2), 'success');
              showToast(`Instance ${action}ed successfully`, 'success');
              addActivity(`EC2 ${action} requested for ${instance_id}`);
            } else {
              setOutput('ec2out', '[ERROR] ' + (data.error || 'Failed'), 'error');
              showToast(`Failed to ${action} instance`, 'error');
            }
          } catch (e) {
            setOutput('ec2out', '[ERROR] ' + e.message, 'error');
            showToast('EC2 error: ' + e.message, 'error');
          } finally {
            setLoading(btnId, false);
          }
        }

        async function s3Upload() {
          const bucket = document.getElementById('bucket').value;
          const key = document.getElementById('key').value;
          const file = document.getElementById('file').files[0];
          const out = document.getElementById('s3out');
          if (!file) {
            setOutput('s3out', '[WARNING] Please select a file', 'error');
            return;
          }
          setLoading('s3UploadBtn', true);
          setOutput('s3out', '[PROCESSING] Uploading...');
          try {
            const fd = new FormData();
            if (bucket) fd.append('bucket', bucket);
            if (key) fd.append('key', key);
            fd.append('file', file);
            const r = await fetch('/api/s3/upload', { method: 'POST', body: fd });
            const data = await r.json();
            if (r.ok) {
              setOutput('s3out', '[SUCCESS] ' + JSON.stringify(data, null, 2), 'success');
              showToast('File uploaded successfully', 'success');
              document.getElementById('file').value = '';
              addActivity('S3 upload: ' + (data.key || file.name));
            } else {
              setOutput('s3out', '[ERROR] ' + (data.error || 'Upload failed'), 'error');
              showToast('Upload failed', 'error');
            }
          } catch (e) {
            setOutput('s3out', '[ERROR] ' + e.message, 'error');
            showToast('Upload error: ' + e.message, 'error');
          } finally {
            setLoading('s3UploadBtn', false);
          }
        }

        async function s3Delete() {
          const bucket = document.getElementById('bucket').value;
          const key = document.getElementById('key').value;
          const out = document.getElementById('s3out');
          if (!key) {
            setOutput('s3out', '[WARNING] Please enter a file key to delete', 'error');
            return;
          }
          setLoading('s3DeleteBtn', true);
          setOutput('s3out', '[PROCESSING] Deleting...');
          try {
            const r = await fetch('/api/s3/delete', {
              method: 'POST',
              headers: {'Content-Type': 'application/json'},
              body: JSON.stringify({ bucket, key })
            });
            const data = await r.json();
            if (r.ok) {
              setOutput('s3out', '[SUCCESS] ' + JSON.stringify(data, null, 2), 'success');
              showToast('File deleted successfully', 'success');
              document.getElementById('key').value = '';
              addActivity('S3 delete: ' + key);
            } else {
              setOutput('s3out', '[ERROR] ' + (data.error || 'Delete failed'), 'error');
              showToast('Delete failed', 'error');
            }
          } catch (e) {
            setOutput('s3out', '[ERROR] ' + e.message, 'error');
            showToast('Delete error: ' + e.message, 'error');
          } finally {
            setLoading('s3DeleteBtn', false);
          }
        }
      </script>
    </body>
    </html>
    """
    return Response(content=html, media_type="text/html")


@app.post("/api/location")
def api_location(payload: dict = Body(...)):
    query = (payload or {}).get("query", "")
    if not query:
        return JSONResponse({"error": "query is required"}, status_code=400)
    data = geocode_location(query)
    if not data:
        return JSONResponse({"error": "not_found"}, status_code=404)
    return data


@app.post("/api/location/reverse")
def api_location_reverse(payload: dict = Body(...)):
    lat = (payload or {}).get("latitude")
    lon = (payload or {}).get("longitude")
    if lat is None or lon is None:
        return JSONResponse({"error": "latitude and longitude are required"}, status_code=400)
    try:
        lat_f = float(lat)
        lon_f = float(lon)
    except Exception:
        return JSONResponse({"error": "latitude/longitude must be numbers"}, status_code=400)

    # Reverse geocode using Nominatim (via geopy) for a friendly address
    from geopy.geocoders import Nominatim

    geolocator = Nominatim(user_agent="ai-cloudops-geo")
    location = geolocator.reverse((lat_f, lon_f), language="en")
    if not location:
        return JSONResponse({"error": "not_found"}, status_code=404)

    address = location.address
    parts = [p.strip() for p in address.split(",")] if address else []
    city = parts[-3] if len(parts) >= 3 else (parts[0] if parts else "")
    return {"latitude": str(lat_f), "longitude": str(lon_f), "city": city, "address": address}


@app.post("/api/email/send")
def api_email_send(payload: dict = Body(...)):
    to = (payload or {}).get("to", "")
    subject = (payload or {}).get("subject", "")
    body = (payload or {}).get("body", "")
    if not (email_config.username and email_config.password and email_config.from_address):
        return JSONResponse({"error": "smtp_not_configured"}, status_code=400)
    if not to:
        return JSONResponse({"error": "to is required"}, status_code=400)
    send_email(to, subject, body)
    return {"status": "sent"}


@app.post("/api/ec2/start")
def api_ec2_start(payload: dict = Body(...)):
    instance_id = (payload or {}).get("instance_id", "")
    if not instance_id:
        return JSONResponse({"error": "instance_id is required"}, status_code=400)
    start_instance(instance_id)
    return {"status": "starting", "instance_id": instance_id}


@app.post("/api/ec2/stop")
def api_ec2_stop(payload: dict = Body(...)):
    instance_id = (payload or {}).get("instance_id", "")
    if not instance_id:
        return JSONResponse({"error": "instance_id is required"}, status_code=400)
    stop_instance(instance_id)
    return {"status": "stopping", "instance_id": instance_id}


@app.post("/api/ec2/terminate")
def api_ec2_terminate(payload: dict = Body(...)):
    instance_id = (payload or {}).get("instance_id", "")
    if not instance_id:
        return JSONResponse({"error": "instance_id is required"}, status_code=400)
    terminate_instance(instance_id)
    return {"status": "terminating", "instance_id": instance_id}


@app.post("/api/s3/upload")
def api_s3_upload(
    file: UploadFile = File(...),
    bucket: Optional[str] = Form(None),
    key: Optional[str] = Form(None),
):
    use_bucket = bucket or aws_config.default_s3_bucket
    if not use_bucket:
        return JSONResponse({"error": "bucket is required (env or form)"}, status_code=400)
    use_key = key or file.filename
    upload_fileobj(use_bucket, use_key, file.file)
    return {"status": "uploaded", "bucket": use_bucket, "key": use_key}


@app.post("/api/s3/delete")
def api_s3_delete(payload: dict = Body(...)):
    bucket = (payload or {}).get("bucket") or aws_config.default_s3_bucket
    key = (payload or {}).get("key")
    if not bucket or not key:
        return JSONResponse({"error": "bucket and key are required"}, status_code=400)
    delete_file(bucket, key)
    return {"status": "deleted", "bucket": bucket, "key": key}
