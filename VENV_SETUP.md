# Virtual Environment Setup

Your system requires a virtual environment for Python packages. Here's how to set it up:

## Quick Setup

Run this command:
```bash
./setup_venv.sh
```

This will:
1. Create a virtual environment in `venv/`
2. Install all required dependencies
3. Show you next steps

## Manual Setup

If you prefer to do it manually:

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate

# 3. Install dependencies
pip install aiohttp paho-mqtt protobuf python-dotenv
```

## Using the Virtual Environment

### Option 1: Activate manually
```bash
source venv/bin/activate
python3 standalone_example.py
```

### Option 2: Use the helper script
```bash
./run_with_venv.sh standalone_example.py
```

### Option 3: Use the ready check script
```bash
./run_with_venv.sh ready_to_use.py
```

## Important Notes

- **Always activate the virtual environment** before running Python scripts
- The virtual environment is in the `venv/` folder (gitignored)
- You only need to run `setup_venv.sh` once
- Activate it each time you open a new terminal: `source venv/bin/activate`

## After Setup

1. Create `.env` file with credentials:
   ```bash
   ./create_env.sh
   ```

2. Verify everything works:
   ```bash
   source venv/bin/activate
   python3 ready_to_use.py
   ```

3. Run the example:
   ```bash
   source venv/bin/activate
   python3 standalone_example.py
   ```
