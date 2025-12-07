# Smart Blood Donation Management System with Donor Verification

A desktop application built with Python and Tkinter to streamline donor registration, blood request handling, and donor-recipient matching — with a simulated blockchain-based donor verification layer for integrity.

Key features
- Donor registration with real-time validation:
  - Name validation
  - Age validation (16–100)
  - Contact validation (10-digit phone number or Gmail)
- Blood request submission for hospitals/patients (blood type, location, urgency)
- Donor matching by compatible blood type and location, displayed in a clear table
- Simple, text-based blockchain simulation to verify donor registration records and preserve integrity
- CSV-based data storage for donors and requests

Technologies
- Python 3.x
- Tkinter (GUI)
- CSV (data persistence)
- re (regex for validation)
- Simple text-based blockchain simulation for verification

Quick start (local)
1. Prerequisites
   - Python 3.8+
   - pip (optional, if using virtualenv)

2. Clone the repository
   git clone https://github.com/Raji17-hub/Smart-Blood-Donation-Management-System-with-Donor-Verification.git
   cd Smart-Blood-Donation-Management-System-with-Donor-Verification

3. Install dependencies (if any)
   - This project uses only the Python standard library. If you add external packages, install them with:
     pip install -r requirements.txt

4. Run the application
   python main.py
   - Or run the appropriate launcher script in the project root (e.g., app.py) if present.

Usage overview
- Register a donor: fill the donor form with validated details (name, age 16–100, 10-digit phone or Gmail).
- Submit a blood request: enter patient/hospital details, blood type, location, and urgency.
- Match donors: use the matching tab to find compatible donors filtered by blood type and proximity.
- Verification: the app demonstrates a blockchain-like verification flow to show record integrity and tamper detection.

Data storage
- Donors and requests are stored as CSV files in the project folder (e.g., donors.csv, requests.csv).
- The blockchain simulation uses a simple text-based chain file (e.g., chain.txt) to append hashed records for verification.

Repository layout (typical)
- main.py or app.py — application entry point
- gui/ — Tkinter GUI components (tabs, forms)
- models/ — donor/request models, validation logic
- storage/ — CSV read/write helpers, chain simulator
- data/ — donors.csv, requests.csv, chain.txt
- README.md — this file

Validation rules
- Name: non-empty, reasonable characters
- Age: integer, between 16 and 100 inclusive
- Contact: either a 10-digit phone number or a Gmail address (regex enforced)

Blockchain-based verification (high level)
- Each registration or important action appends a record hash to a simple chain file.
- On verification, the app re-hashes records and compares chain hashes to detect tampering.
- This is a simulation intended to demonstrate integrity concepts (not a production blockchain).

Contributing
- Please open issues for bugs/feature requests.
- Fork, create a feature branch, and open a pull request with tests/explanations.
- Keep changes small and focused.

License
- Add an appropriate license file (e.g., MIT) to the repository to clarify reuse terms.

Contact
- Maintainer: Raji17-hub (update with email or GitHub profile link)

Notes and improvements ideas
- Add unit tests for validation, CSV storage, and blockchain simulation.
- Add packaging (pyinstaller) to build executables for Windows/macOS/Linux.
- Add mapping/location fuzzy-matching for donor proximity.
- Replace the simulated blockchain with a proper tamper-evident ledger if you need production-grade verification.
