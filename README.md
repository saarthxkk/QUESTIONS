# ⚡ CodeArena — Personal DSA Practice Platform

Practice Data Structures & Algorithms with instant C++17 compilation, automated test case judging, and VS Code-style autocomplete.

## 🚀 How to Deploy on the Web (Vercel / Render / Railway)

You can deploy CodeArena to the web so you can practice from any browser on your laptop, phone, or tablet without running any local servers!

---

### Method A: Deploy on Vercel (Fastest & Free)

1. Push this folder to a new **GitHub repository**:
   ```bash
   cd ~/Desktop/COMPILER
   git init
   git add .
   git commit -m "Deploy CodeArena"
   git branch -M main
   git remote add origin https://github.com/<YOUR_USERNAME>/codearena.git
   git push -u origin main
   ```

2. Go to **[vercel.com](https://vercel.com)** and sign in with GitHub.
3. Click **"Add New..."** → **"Project"**.
4. Select your `codearena` repository and click **Deploy**.
5. Done! Vercel will give you a live link like `https://codearena.vercel.app`.

> **Note on C++ Compilation on Vercel:**  
> Since Vercel Serverless Functions do not have a local `g++` binary, CodeArena automatically switches to its high-speed **Cloud C++17 Compiler Engine** (Wandbox API) when running on Vercel, allowing you to compile and run any C++ code seamlessly on the web!

---

### Method B: Deploy on Render.com (Free Native C++ Container)

If you prefer having a dedicated Linux container with real `g++` compiled natively on the server:

1. Push your repo to GitHub.
2. Go to **[render.com](https://render.com)** and click **New +** → **Web Service**.
3. Connect your GitHub repository.
4. Select **Docker** environment (Render will automatically detect the included `Dockerfile`).
5. Choose the **Free** instance type and click **Create Web Service**.
6. Render gives you a public URL like `https://codearena.onrender.com`.

---

## 💻 Running Locally (Optional)

If you ever want to run it on your local machine:
```bash
python3 server.py
```
Or double-click `CodeArena.command` on your Desktop.
Open: [http://localhost:8080](http://localhost:8080)
