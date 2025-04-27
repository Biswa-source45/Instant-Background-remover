
# 🎨 Instant Background Remover 🖼️

Effortlessly remove image backgrounds with just one click! Built with 🐍  using Streamlit and rembg.

## ✨ Features

- 📸 **Image Upload**: Supports JPG, JPEG, and PNG formats.
- ⚡ **One-Click Background Removal**: Powered by the rembg library for fast and accurate results.
- 🎛️ **Customizable Output**:
  - Transparent or white background fill.
  - Resize output image (10% ➡️ 100%).
  - Adjust output quality for optimal file size and clarity.
  - Set custom filenames for your downloads.
- 📱 **Responsive Design**: Works beautifully across desktops, tablets, and phones.
- 🚀 **Performance Optimization**:
  - Auto-resizing large images to prevent memory overload.
  - Progress bar and memory checks for smooth processing.
  - Timeout & cancellation support for user flexibility.
- 🎯 **User Feedback**: Clear success/error messages to guide your experience.
- 📥 **Downloadable Results**: Save your background-free images easily as PNG.

## 🛠️ Technologies Used

- 🐍 **Python 3.10+**
- 🌐 **Streamlit** – for building the interactive web app
- 🎨 **rembg** – for AI-based background removal
- 🖌️ **Pillow (PIL)** – image manipulation
- 🧠 **psutil** – system monitoring
- 💻 **HTML/CSS** – for stylish custom interfaces

## 🚀 Installation and Local Setup

### 📋 Prerequisites

- Python 3.10 or higher
- Git installed
- (Recommended) Virtual environment for dependencies

### 🧩 Steps to Run Locally

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/Biswa-source45/Instant-Background-remover.git
   cd instant-background-remover
   ```

2. **Create a Virtual Environment**:

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   ```

3. **Install Required Packages**:

   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Application**:

   ```bash
   streamlit run app.py
   ```

5. **Open the App**:

   Visit `http://localhost:8501` in your web browser 🚀

## 🌎 Deployment on Streamlit Community Cloud

### Steps to Deploy:

1. **Push your project to GitHub**:

   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Log in to Streamlit Cloud**.

3. **Select your GitHub repo** and set `app.py` as the entry point.

4. 🚀 **Deploy** and get a public URL for your app!

🔗 **Need help?** [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-community-cloud/get-started)

## 🎯 How to Use

1. 📤 **Upload**: Pick your JPG, JPEG, or PNG image.
2. 🖱️ **Remove**: Click "Remove Background" and wait for magic ✨.
3. 🎛️ **Customize**:
   - **Background**: Transparent or white
   - **Resize**: Adjust scaling
   - **Quality**: Balance clarity and file size
   - **Filename**: Name your masterpiece
4. 💾 **Download**: Click to save your processed image!

### 💡 Pro Tips:

- Use images smaller than 1000px for faster results.
- Ensure enough system memory for large files.

## 🗂️ Project Structure

```bash
instant-background-remover/
├── .gitignore
├── app.py          # 🚀 Main application
├── requirements.txt # 📦 Project dependencies
└── README.md        # 📖 Documentation
```

## 📜 License

This project is under the MIT License.  
See [LICENSE](LICENSE) for details.

## 👏 Credits

- 👨‍💻 **Developed by**: Biswabhusan Sahoo
- 🛠️ **Powered by**: Streamlit + rembg
- 🌟 **Inspiration**: Making image editing easy for everyone!

## 📬 Contact

Got questions or ideas? Let's connect!

- **LinkedIn**: [https://www.linkedin.com/in/biswabhusan-sahoo-22b704292/]
- **Email**: [biswapvt506@gmail.com]

© 2025 Instant Background Remover,biswabhusan Sahoo.All rights reserved.
