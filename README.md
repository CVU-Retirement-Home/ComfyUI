# ComfyUI Setup Guide (Modified Fork)

This is a customized fork of [ComfyUI](https://github.com/comfyanonymous/ComfyUI), adapted for deepfake pipeline enhancements.

[View Original README](README_OG.md)

---

## 🔧 Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/CVU-Retirement-Home/ComfyUI-updated.git
cd ComfyUI-updated
```

### 2. Create and Activate Python 3.12 Virtual Environment
```bash
python3.12 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

install cuda from https://pytorch.org/get-started/locally/

### 4. Place Required Model Files
- Model checkpoints → `./models/checkpoints/`
- Lora models → `./models/loras/`
- Upscale models → `./models/upscale_models/`

### 5. Configuration
Edit the `deepfake.py` script to change the **output folder path** according to your setup.

### 6. Run the Application
```bash
python deepfake.py
```

---

## Links to models and what not
All models are downloaded from [huggingface](https://huggingface.co/models?other=deepfake) or [civitai](https://civitai.com/)

Sample Model used for deepfake generation

- [Stable diffusion 3 medium](https://civitai.com/models/497255?modelVersionId=552771)
- [Real-ESRGAN upscale model](https://huggingface.co/ai-forever/Real-ESRGAN)


---
## Automation of workflow
Repo to convert comfytUI json into python scripts https://github.com/pydn/ComfyUI-to-Python-Extension

 follow the git repo instructions to convert json worflows into python scripts then follow the format of existing [folders](workflows) in  for automation of deepefakes

## ⚠️ Notes

- Ensure all model folders exist before running.
- You must manually set the desired output directory,parameters and configs inside the script.
- The output directory will auto clear itself on run (use a different folder to save the outputs)

---

## 🔄 Changes from Original ComfyUI

**Replaced Files:**
- `nodes.py`
- `requirements.txt`

**Added Files and Directories:**
- `deepfake.py`
- `workflow_json`
    - the comfyUI json files for various workflows to test if output is valid
- `workflows`
    - folder that contains all the automation of the images using various workflows


---

