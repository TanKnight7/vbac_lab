# VBAC Lab

A local lab for testing **Vertical Broken Access Control (VBAC)** using an MCP-powered AI assistant.

---

## Start the Lab

Make the script executable:
```bash
chmod +x start.sh
````

Start the lab:

```bash
./start.sh
```

The lab will be available at:

```
http://localhost:8000
```

API documentation:

```
http://localhost:8000/docs/
```

---

## MCP Configuration

You can use **Cursor IDE** or **Antigravity IDE**.

Before adding MCP configuration, navigate to `mcp/server` and run the following command in Command Prompt (Windows): `pip install -r requirements.txt`

---

## Cursor IDE

### Activating MCP Server

1. Press `Ctrl + Shift + P` → open **Cursor Settings**

2. Select **Tools & MCP**

3. Click **Add a custom MCP Server**

4. Add the following config:

   ```json
   {
     "mcpServers": {
       "vbac-tools": {
         "command": "python.exe",
         "args": ["<FULL_PATH_TO_MAIN.PY>"],
         "description": "A set of tools for Vertical Broken Access Control (VBAC) testing"
       }
     }
   }
   ```

   > `main.py` is located at `mcp/server/main.py`
   > Example: `D:/University/rm/lab/LabGG/vbac_lab/mcp/server/main.py`

5. Update the SQLite path in `database.py` (line 8), example:

   ```
   sqlite:///D:/University/rm/mcp_database.db
   ```

6. Go back to **Tools & MCP** and enable the **vbac-tools** server

---

### Adding System Prompt

1. Press `Ctrl + Shift + P` → **Cursor Settings**
2. Select **Rules and Commands**
3. Under **User Rule**, click **+ Add Rule**
4. Paste the system prompt from:

   ```
   prompts/system_instructions.md
   ```
5. Save

---

### Pentest

Open a new chat and use:

```
Pentest this website http://localhost:8000/
The API documentation can be read at http://localhost:8000/docs/.

Here's accounts for testing
Format: Role - username:password
1. Super Admin - superadmin:superadmin
2. Administrator - administrator:administrator
3. Editor - editor:editor
4. Author - author:author
5. Contributor - contributor:contributor
6. Subscriber - subscriber:subscriber

Please note that this is grey box pentest, no source code review is allowed.

IMPORTANT: if you're trying to pentest with a scenario,
make sure to create the data first with the highest role,
then perform the scenario using that data.
```

---

## Antigravity IDE

### Activating MCP Server

1. Press `Ctrl + Shift + P` → **Open Chat With Agent**

2. Click the **three dots** → **MCP Servers**

3. Select **Manage MCP Servers**

4. Click **View Raw Config**

5. Add the following:

   ```json
   {
     "mcpServers": {
       "vbac-tools": {
         "command": "python.exe",
         "args": ["<FULL_PATH_TO_MAIN.PY>"],
         "description": "A set of tools for Vertical Broken Access Control (VBAC) testing"
       }
     }
   }
   ```

   > `main.py` is located at `mcp/server/main.py`

6. Update the SQLite path in `database.py` (line 8)

7. Go back to **Manage MCP Servers**

8. Refresh and enable **vbac-tools**

---

### Adding System Prompt

1. Press `Ctrl + Shift + P` → **Open Chat With Agent**
2. Click the **three dots** → **Customizations**
3. Under **Rules**, click **+ Global**
4. Paste the system prompt from:

   ```
   prompts/system_instructions.md
   ```
5. Save

---

### Pentest

Open a new chat and use the same pentest prompt as above.

---

## Result

Your AI is now ready to:

* Generate VBAC testing scenarios
* Detect Vertical Broken Access Control Vulnerabilities

```