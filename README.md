# DefendEye: A YOLO-NAS Based Threat Detection System

## Project Overview

DefendEye is an advanced weapon detection system designed to identify potential threats, such as firearms and knives, in real-time using the state-of-the-art YOLO-NAS architecture. This project aims to enhance public safety by providing real-time threat detection and alerting capabilities, which can be implemented in various security-sensitive environments such as airports, public spaces, and law enforcement.

## Features

- Real-time detection of weapons (knives, guns) and persons.
- High accuracy and speed using YOLO-NAS architecture.
- Integration with surveillance systems for live video feed analysis.
- Scalable for use in a wide range of environments and hardware setups.
- Provides real-time alerts for detected threats.
- Optimized for efficient use of resources with potential deployment on edge devices.

## Technologies Used
- **YOLO-NAS (You Only Look Once - Neural Architecture Search) :** Object detection architecture.
- **Deep Learning Frameworks :** PyTorch.
- **Web Framework :** Flask for creating the user interface and backend.
- **Frontend :** HTML, CSS, Bootstrap, JavaScript, jQuery.
-  ### Libraries:
     - **Image Processing :** OpenCV, Pillow.
     - **Data Handling :** NumPy, Pandas.
     - **Visualization :** Matplotlib.

## System Requirements
### Hardware Requirements
- **Running/Testing:**
  - **CPU:** Intel Core i5 or higher (2.5 GHz+).
  - **Memory:** Minimum 8GB RAM.
  - **Storage:** Minimum 3GB for libraries.
  - **Internet:** 40 Mbps or higher.
- **Training:**
  - **CPU:** Intel Core i5 or higher.
  - **GPU:** Nvidia RTX 3050 (4GB VRAM) or higher.
  - **Memory:** Minimum 16GB RAM.
  - **Storage:** 20GB for datasets and libraries.
## Software Requirements
- **Operating System:** Windows 10 or higher.
- **Programming Language:** Python 3.9.16.
- **Deep Learning Libraries:** PyTorch 2.0.1 or higher.
- **Web Framework:** Flask.
- **Development Environment:** Visual Studio Code, Jupyter Lab.
 

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/arjunvs903/Threat_Detection.git
   cd ThreatDetection
   ```

2. Create a virtual environment (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   > install PyTorch separately
   [PyTorch installing guide](https://pytorch.org/)
   ```
   pip install -r requirements.txt
   ```

1. Start the Flask application:
   it is located on **ThreatDetection** folder
   ```
   python app.py
   ```

2. Open a web browser and navigate to `http://localhost:5000`.

## Usage

**1. Running the Detection System:**

Upload an image,video clip  or provide a live video stream through the web    interface.
The system will process the input and provide real-time detection results,    highlighting any identified weapons or persons.

**2. Configuration Options:**

Customize threat detection classes and confidence thresholds via the settings page in the web interface.


## Model Training

To retrain the model or experiment with different configurations:

1. **Prepare the Dataset:** Organize images and annotations in the required format (YOLO-style).


2. **Train Model:**
 
   open train_model.ipynb from **training** folder on jupyter notebook or vs code 
   then run each cell one by one
3. **Evaluate the Model:**

   Use validation datasets to check the model's performance and adjust   hyperparameters as necessary.

## Evaluation Metrics
- **Precision@0.50:** 11.38% accuracy at detecting threats with a confidence threshold of 0.50.
- **Recall@0.50:** Perfect recall of 100% for identifying all weapons and persons.
- **mAP@0.50:** High mean Average Precision of 96.6%.
- **F1 Score:** Balanced performance between precision and recall, scoring 0.20.