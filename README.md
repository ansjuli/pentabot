# Pentabot 🛡️

Pentabot is an offline-first, cybersecurity-focused voice assistant built in Python.

It is designed to automate security tasks, analyze systems, and provide a unified control layer for cybersecurity tools.

---

## 🚀 Features (v0.1)

* 🎧 Voice input using Vosk (offline speech recognition)
* 🧠 Intent-based command routing
* ⚙️ System command execution
* 🔁 Continuous listening loop
* 🛡️ Basic system reconnaissance (network info, processes)

---

## 🧠 Architecture

Pentabot follows a modular layered design:

Voice → Brain → Security Core → Execution

* **voice/** → handles speech recognition
* **brain/** → parses and routes intents
* **security_core/** → cybersecurity tools (scans, analysis)
* **tools/** → execution layer

---

## ⚙️ Setup

```bash
conda create -n pentabot_env python=3.10
conda activate pentabot_env
pip install vosk sounddevice
```

Download a Vosk model and place it inside:

```
/models/vosk-model-small-en-us-0.15
```

---

## ▶️ Run

```bash
python main.py
```

---

## 🎯 Example Commands

* "scan network"
* "check process"
* "exit"

---

## ⚠️ Note

Pentabot is under active development and currently in early-stage prototype (v0.1).

---

## 👤 Author

Juli
