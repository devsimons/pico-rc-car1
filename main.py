from machine import Pin, PWM
import network
import socket
import time

###############################
#                             #
# S E T U P - H A R D W A R E #
#                             #
###############################
# Motor A (drive motor - forward/backward)
ain1 = Pin(0, Pin.OUT)
ain2 = Pin(1, Pin.OUT)
pwma = PWM(Pin(2))
pwma.freq(1000)

# Motor B (steering motor - left/right)
bin1 = Pin(3, Pin.OUT)
bin2 = Pin(4, Pin.OUT)
pwmb = PWM(Pin(5))
pwmb.freq(1000)

# Standby pin
stby = Pin(6, Pin.OUT)
stby.high()

# Speed settings
full_speed = 65535
half_speed = 32768

###############################
#                             #
# M O T O R - C O N T R O L   #
#                             #
###############################
def drive_motor(direction):
    if direction == "forward":
        ain1.high()
        ain2.low()
        pwma.duty_u16(full_speed)
    elif direction == "reverse":
        ain1.low()
        ain2.high()
        pwma.duty_u16(full_speed)
    elif direction == "stop":
        pwma.duty_u16(0)
        ain1.low()
        ain2.low()

def steering_motor(direction):
    if direction == "right":
        bin1.high()
        bin2.low()
        pwmb.duty_u16(full_speed)
    elif direction == "left":
        bin1.low()
        bin2.high()
        pwmb.duty_u16(full_speed)
    elif direction == "stop":
        pwmb.duty_u16(0)
        bin1.low()
        bin2.low()

def stop_all():
    drive_motor("stop")
    steering_motor("stop")

###############################
#                             #
# W I F I - S E T U P         #
#                             #
###############################
def create_wifi_ap():
    """Create WiFi Access Point"""
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='RC-Car', password='12345678')
    
    while not ap.active():
        time.sleep(0.1)
    
    print('WiFi AP Created!')
    print('SSID: RC-Car')
    print('Password: 12345678')
    print('IP Address:', ap.ifconfig()[0])
    return ap

###############################
#                             #
# W E B - S E R V E R         #
#                             #
###############################
def web_page():
    """Generate HTML control page"""
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>RC Car Control</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }
        h1 {
            color: white;
            margin-bottom: 30px;
            font-size: 28px;
        }
        .container {
            max-width: 400px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 5px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
        }
        .controls {
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 10px;
            margin: 20px 0;
        }
        button {
            padding: 25px;
            font-size: 18px;
            font-weight: bold;
            border: 2px solid #333;
            border-radius: 0;
            cursor: pointer;
            transition: all 0.3s;
            color: white;
        }
        button:active {
            transform: scale(0.95);
        }
        .forward { grid-column: 2; background: #10b981; }
        .left { grid-column: 1; grid-row: 2; background: #3b82f6; }
        .stop { grid-column: 2; grid-row: 2; background: #ef4444; }
        .right { grid-column: 3; grid-row: 2; background: #3b82f6; }
        .reverse { grid-column: 2; grid-row: 3; background: #f59e0b; }
        button:hover {
            opacity: 0.9;
            box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        }
        .status {
            margin-top: 20px;
            padding: 15px;
            background: #f3f4f6;
            border-radius: 0;
            color: #374151;
            border: 2px solid #333;
        }
    </style>
</head>
<body>
    <h1>RC Car Control</h1>
    <div class="container">
        <div class="controls">
            <button class="forward" ontouchstart="sendCommand('forward')" ontouchend="sendCommand('stop')" 
                    onmousedown="sendCommand('forward')" onmouseup="sendCommand('stop')">
                FORWARD
            </button>
            
            <button class="left" ontouchstart="sendCommand('left')" ontouchend="sendCommand('center')"
                    onmousedown="sendCommand('left')" onmouseup="sendCommand('center')">
                LEFT
            </button>
            
            <button class="stop" onclick="sendCommand('stop')">
                STOP
            </button>
            
            <button class="right" ontouchstart="sendCommand('right')" ontouchend="sendCommand('center')"
                    onmousedown="sendCommand('right')" onmouseup="sendCommand('center')">
                RIGHT
            </button>
            
            <button class="reverse" ontouchstart="sendCommand('reverse')" ontouchend="sendCommand('stop')"
                    onmousedown="sendCommand('reverse')" onmouseup="sendCommand('stop')">
                REVERSE
            </button>
        </div>
        <div class="status" id="status">Ready</div>
    </div>
    
    <script>
        function sendCommand(cmd) {
            fetch('/?command=' + cmd)
                .then(response => response.text())
                .then(data => {
                    document.getElementById('status').innerText = 'Command: ' + cmd.toUpperCase();
                })
                .catch(error => {
                    document.getElementById('status').innerText = 'Error!';
                });
        }
    </script>
</body>
</html>
"""
    return html

def handle_command(command):
    """Process control commands"""
    if command == 'forward':
        drive_motor('forward')
    elif command == 'reverse':
        drive_motor('reverse')
    elif command == 'left':
        steering_motor('left')
    elif command == 'right':
        steering_motor('right')
    elif command == 'center':
        steering_motor('stop')
    elif command == 'stop':
        stop_all()

def start_server():
    """Start web server"""
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(addr)
    s.listen(1)
    
    print('Web server running on port 80')
    print('Open your phone browser and connect to WiFi "RC-Car"')
    print('Then go to: http://192.168.4.1')
    
    while True:
        try:
            cl, addr = s.accept()
            request = cl.recv(1024).decode()
            
            # Parse command from URL
            if '/?command=' in request:
                command = request.split('/?command=')[1].split(' ')[0]
                handle_command(command)
                response = 'OK'
            else:
                response = web_page()
            
            cl.send('HTTP/1.1 200 OK\r\n')
            cl.send('Content-Type: text/html\r\n')
            cl.send('Connection: close\r\n\r\n')
            cl.sendall(response)
            cl.close()
            
        except Exception as e:
            print('Error:', e)
            cl.close()

###############################
#                             #
# M A I N                     #
#                             #
###############################
def main():
    print("Starting RC Car Web Controller...")
    stop_all()
    
    # Create WiFi access point
    create_wifi_ap()
    time.sleep(2)
    
    # Start web server
    start_server()

try:
    main()
except KeyboardInterrupt:
    print("\nProgram stopped by user")
    stop_all()
