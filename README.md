# HERE IS A QUICK DEMO HOW MY PROJECT LOOK LIKES:-
https://github.com/user-attachments/assets/213056a6-748c-40d0-a9e8-79c6aef7a2b4

# RealTimeWhiteboard_using_python
Description:
SyncSketch is a real-time collaborative whiteboard application that allows multiple clients to connect and interact on the same canvas using a peer-to-peer (P2P) network architecture. Built with Python and leveraging the socket programming library, this project facilitates seamless sharing and drawing among users in real-time.

Key Features:
. P2P Networking: Utilizes a socket-based architecture to establish direct connections between clients, enabling efficient data transfer and reducing latency.
. Real-Time Collaboration: Multiple users can simultaneously draw, erase, and interact on a shared whiteboard, with all actions instantly reflected across all connected clients.
. Dynamic Canvas Updates: Each client's drawing actions are transmitted in real-time, ensuring all participants see the latest changes as they happen.
. User-Friendly Interface: The whiteboard interface allows for easy navigation, drawing, and collaboration, making it accessible for users of all skill levels.
. Multi-Client Support: Designed to handle multiple connections on the same port, allowing various users to join the session without complications.
  Technologies Used:

- Python: The core language for implementing the application logic and socket communication.
- Socket Programming: Facilitates the creation of a server-client model for real-time data exchange.
- Threading: Ensures smooth performance by handling multiple client connections concurrently.


How It Works:
- server Setup: A central server listens for incoming client connections on a specified port.
- Client Connection: When a new client connects, it establishes a P2P link with the existing clients, allowing for direct data exchange.
- Drawing Data Transmission: As users draw on the canvas, their actions (e.g., strokes, colors, and positions) are serialized and sent to all connected peers in real-time.
- Canvas Rendering: Each client receives drawing data and updates their local canvas, ensuring all users see the same content.

