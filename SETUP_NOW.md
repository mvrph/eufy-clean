# Setup Instructions

## Step 1: Install Dependencies

Run this command in your terminal:

```bash
pip3 install aiohttp paho-mqtt protobuf python-dotenv
```

Or if you prefer using pip:
```bash
pip install aiohttp paho-mqtt protobuf python-dotenv
```

---

## Step 2: Create .env File

Create a file named `.env` in this directory with your credentials:

```bash
cat > .env << 'EOF'
EUFY_USERNAME=your-email@example.com
EUFY_PASSWORD=your-password
EOF
```

**Important**: Replace `your-email@example.com` and `your-password` with your actual Eufy account credentials!

Or manually create the file:
1. Create a new file named `.env` in this directory
2. Add these two lines (replace with your actual credentials):
   ```
   EUFY_USERNAME=your-email@example.com
   EUFY_PASSWORD=your-password
   ```

---

## Verify Setup

After completing steps 1 & 2, run:

```bash
python3 ready_to_use.py
```

This will verify everything is set up correctly.

---

## Then You're Ready!

Run the example:
```bash
python3 standalone_example.py
```
