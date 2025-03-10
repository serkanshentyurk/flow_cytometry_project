# Flow Cytometry Data Viewer

Welcome to the Flow Cytometry Data Viewer! This tool lets you view and analyse flow cytometry data using a simple graphical interface. Even if you have no coding experience, you can follow these step-by-step instructions to set up and run the program on your Windows or macOS computer.

---

## What Does This Tool Do?

- **Load Data Files:** Open tab-separated flow cytometry data files.
- **View Plots:** See plots of individual cell intensities or average intensity profiles.
- **Save Plots:** Save your plots as high-quality JPEG images.
- **User-Friendly Interface:** An easy-to-use window (GUI) built with Python and Tkinter.

---

## What You Need

1. **Python 3.6 or newer**
2. **Conda (Miniconda or Anaconda)**
3. **Some python packages** (specified in `requirements.txt`)

---

## Install Instructions

### Step 0: Check if Python Is Installed

Before you begin, check if Python is already installed on your computer.

- **On Windows:**
  1. Open the **Command Prompt**: Click on the Start menu, type `cmd`, and press Enter.
  2. Type the following command and press Enter:
     ```bash
     python --version
     ```
  3. If you see something like `Python 3.x.x`, Python is installed.  
     If not, download and install Python from [python.org/downloads/windows](https://www.python.org/downloads/windows/). Make sure to check **"Add Python to PATH"** during installation.

- **On macOS:**
  1. Open the **Terminal**: You can find it in Applications > Utilities.
  2. Type the following command and press Enter:
     ```bash
     python3 --version
     ```
  3. If you see a version number (e.g., `Python 3.x.x`), Python is installed.  
     If not, download and install Python from [python.org/downloads/macos](https://www.python.org/downloads/macos/).

---

### Step 1: Check if Conda Is Installed

Conda helps manage packages and environments without affecting your system-wide Python.

- **On Windows or macOS:**
  1. Open the **Command Prompt** (Windows) or **Terminal** (macOS).
  2. Type the following command and press Enter:
     ```bash
     conda --version
     ```
  3. If you see a version number (e.g., `conda 4.x.x`), Conda is installed.  
     If not, download and install **Miniconda** from [docs.conda.io/en/latest/miniconda.html](https://docs.conda.io/en/latest/miniconda.html). Follow the instructions for your operating system.

---

### Step 2: Download the Code

You have two options to download the project files:

#### **Option A: Using Git (If Git Is Installed)**

- **On Windows:**
  1. Open the **Command Prompt**.
  2. Navigate to the folder where you want to save the project (for example, your Desktop):
     ```bash
     cd Desktop
     ```
  3. Clone the repository (replace `<repository-url>` with the actual URL of the GitHub repo):
     ```bash
     git clone <repository-url>
     ```

- **On macOS:**
- Option 1:
  1. Open the **Terminal**.
  2. Navigate to the folder where you want to save the project:
     ```bash
     cd ~/Desktop
     ```
   3. Clone the repository:
     ```bash
     git clone <repository-url>
     ```
- Option 2:
  1. Double click to the folder where you want to save the project.
  2. Click `New Terminal at Folder`
  3. Clone the repository:
     ```bash
     git clone <repository-url>
     ```

#### **Option B: Downloading as a ZIP File (If Git Is Not Installed)**

1. Open your web browser and navigate to the GitHub page for this project.
2. Click the **"Code"** button near the top-right corner.
3. Select **"Download ZIP"**.
4. Save the ZIP file to your computer.
5. Extract the ZIP file by double-clicking it (this will create a folder with the project files).

---

### Step 3: Create a Conda Environment

Using Conda will help keep the required packages separate from other software.

1. **Open the Terminal/Command Prompt:**
   - **Windows:** Open the **Anaconda Prompt** from the Start menu.
   - **macOS:** Open the **Terminal** app.
   
2. **Navigate to the Project Folder:**  
   For example, if your project folder is on your Desktop and is named `FlowCytometryViewer`, type:
   ```bash
   cd Desktop/FlowCytometryViewer
   ```

   On macOS, you might need to adjust the path accordingly, e.g., 
   ```bash
   cd ~/Desktop/FlowCytometryViewer
   ```
   
   On macOS, you can also double click to the Project Folder and click `New Terminal at Folder`.

3. **Create a New Conda Environment:**
   Run the following command:
   ```
   conda create --name flowcytometry_viewer python=3.8
   ```
   - Feel free to replace 3.8 with a newer version if desired.
   - Feel free to replace `flowcytometry_viewer` with any other preferred name. However, you will be using that name again and again, choose wisely!

4. **Activate the Conda Environment:**
   ```
   conda activate flowcytometry_viewer
   ```
   or if you pick another name for the environment
   ```
   conda activate environment_name
   ```
---

### Step 4: Install the Required Python Packages

   Ensure you are in the project folder and that your Conda environment is active.
   Run the following command:
   ```
   pip install -r requirements.txt
   ```

---

## Running the Code

### Step 5: Launch the Application

#### **Ensure You Are in the Project Folder:**
Before running the application, make sure that you are inside the **project folder** where the script files are located.

1. **For Windows:**
   - Open the **Command Prompt** (type `cmd` in the start menu search and press Enter).
   - Type `dir` and press Enter. This will list the files and folders in your current directory.
   - If you see the files related to your project (e.g., `plot_flow_data.py`), you are in the correct folder.
   - If you do not see them, you need to navigate to the project folder.
   
   **To navigate to the project folder:**
   - Type the following command (replace `<path-to-your-folder>` with the actual path to your project folder):
     ```bash
     cd <path-to-your-folder>
     ```
     For example, if your project is on the Desktop, you would type:
     ```bash
     cd C:\Users\<your-username>\Desktop\FlowCytometryViewer
     ```

2. **For macOS:**
   - Open **Terminal** (you can find it in Applications > Utilities or by searching it via Spotlight).
   - Type `ls` and press Enter. This will list the files and folders in your current directory.
   - If you see the files related to your project (e.g., `plot_flow_data.py`), you are in the correct folder.
   - If you do not see them, you need to navigate to the project folder.
   
   **To navigate to the project folder:**
   - Type the following command (replace `<path-to-your-folder>` with the actual path to your project folder):
     ```bash
     cd <path-to-your-folder>
     ```
     For example, if your project is on the Desktop, you would type:
     ```bash
     cd ~/Desktop/FlowCytometryViewer
     ```
    - Or you can right click to the folder which contains the code and select **New Terminal at Folder**

### Launch!!!
#### **Activate the Conda Environment:**
Once you are inside the project folder, ensure that the Conda environment `flowcytometry_viewer` is activated. You can activate it by running:

```bash
conda activate flowcytometry_viewer
```
If the environment is activated correctly, you should see the environment name `(flowcytometry_viewer)` appear in your terminal/command prompt.

#### **Run the Application:**
Now that you are in the correct folder and the environment is active, you can run the application.

Simply type the following command:

```
python plot_flow_data.py
```
This will launch the graphical interface (GUI) of your application.

---

## What the GUI Does
1. **File Selection:**
- Use the GUI to select one or more flow cytometry data files (tab-separated format). You can add or remove files as needed.
Plotting Options:
- **Individual Cell Plot:** View the fluorescence intensity of a specific cell.
- **Average Intensity Plot:** See the average fluorescence intensity across all cells with variability indicators (such as standard deviation, standard error, or percentiles).
2. **Interactive Controls:**
- Adjust settings like figure size, colours, tick visibility, and log scale.
- Input labels for the axes and title for the plot.
- Save your plot as a high-resolution JPEG image.
3. **Navigation:**
- Easily switch between plotting individual cell data and the average intensity plot. You can go back to file selection if you want to load different data.

---

## Troubleshooting

- **Python/Conda Not Found:**
    Double-check the installation steps above and ensure that Python and Conda are properly installed and added to your system’s PATH.
- **GUI Issues:**
    If you encounter errors related to Tkinter, please verify that your Python installation includes Tkinter. On some systems, you may need to install an additional package (consult your operating system’s documentation).
- **Need More Help?**
    Feel free to open an issue on the GitHub repository or contact the project maintainer.

---

## License
MIT License

Copyright (c) 2025 Serkan Shentyurk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

## Contact

If you have any questions or need help, please open an issue on the GitHub repository or contact the maintainer.

Enjoy using the Flow Cytometry Data Viewer!