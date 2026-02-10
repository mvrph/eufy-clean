"""Device controllers for Eufy vacuum communication.

This package contains the controller classes responsible for authentication,
MQTT connectivity, and device command handling.

- Base: Abstract base with DPS key mapping
- Login: Eufy cloud authentication and device discovery
- MqttConnect: MQTT transport layer (connect, subscribe, publish)
- SharedConnect: High-level device commands (clean, pause, go home, etc.)
"""
