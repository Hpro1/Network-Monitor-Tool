# Network-Monitor-Tool
Cross-platform application developed in Python, utilizing Tkinter for GUI. Allows users to monitor the network connectivity status of various IP addresses or hostnames. The tool is designed to be user-friendly, providing a dynamic interface where users can add or remove addresses and view real-time connectivity status.

## Features
- **Dynamic Interface**: Users can add and remove IP addresses or hostnames dynamically.
- **Real-Time Status**: The tool displays the connectivity status (green for active, red for inactive) in real-time.
- **Cross-Platform Compatibility**: Works on both Windows and macOS/Linux.
- **Responsive Design**: Utilizes threading to ensure responsive GUI during network operations.

## Technical Details
The tool leverages the system's native `ping` command to check connectivity, accommodating differences in command-line options between Windows and macOS:

- **Windows**: Uses `-n` (number of echo requests) and `-w` (timeout in milliseconds).
- **macOS**: Uses `-c` (number of packets to send) and `-W` (timeout in milliseconds).

This distinction is not too cruical, but as the syntax and behavior of the `ping` command vary between operating systems. For instance, the `-t` option in Windows is used for continuous pinging, whereas in macOS, it sets the Time To Live (TTL) for the packet.

## Implementation
- **Tkinter for GUI**: 
- **Threading**: 
- **Placeholder Management**: 
- **OS Detection**:

## Usage
1. **Add an IP or Hostname**: Click the '+' button to add a new row and enter an IP address or a hostname.
2. **View Status**: The color indicator next to each entry shows the current connectivity status.
3. **Edit or Remove**: Toggle the lock to edit entries or use the '-' button to remove them.

## Future Enhancements
- Error handling and logging for network operations.
- Thread management for large-scale usage.
- Configurable parameters through the GUI.
- Enhanced user feedback for network operation outcomes.
- Dynamically change the page amount
- Storage system of some sort
