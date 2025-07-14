# ComfyUI Setup Guide (Modified Fork)

This is a customized fork of [ComfyUI](https://github.com/comfyanonymous/ComfyUI), adapted for deepfake pipeline enhancements.

[View Original README](README_OG.md)

---

## 🔧 Setup Instructions

### 1. Download the portable version
[ComfyUI Portable](https://github.com/comfyanonymous/ComfyUI/releases/latest/download/ComfyUI_windows_portable_nvidia.7z)

```bash
cd .\ComfyUI_windows_portable
```
Delete the ComfyUI folder


### 2. Clone the Repository
```bash
git clone https://github.com/CVU-Retirement-Home/ComfyUI.git
cd ComfyUI
```

### 3. Create and Activate Python 3.12 Virtual Environment
Download UV if not installed yet
```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```
```bash
uv venv # to create the venv (python 3.12)
venv\scripts\activate
```

### 4. Install Dependencies
```bash
uv pip install -r requirements.txt --torch-backend=auto
```

### 5. Place Required Model Files
- Model checkpoints → `./models/checkpoints/`
- Lora models → `./models/loras/`
- Upscale models → `./models/upscale_models/`

### 6. Configuration
Edit the `deepfake.py` script to change the **output folder path** according to your setup.

### 7. Run the Application
```bash
uv run deepfake.py
```

---

## Links to models and what not
All models are downloaded from [huggingface](https://huggingface.co/models?other=deepfake) or [civitai](https://civitai.com/)

Sample Model used for deepfake generation

- [Stable diffusion 3 medium](https://civitai.com/models/497255?modelVersionId=552771)
- [Real-ESRGAN upscale model](https://huggingface.co/ai-forever/Real-ESRGAN)
- [realvisxlV40_v40Bakedvae checkpoint](https://huggingface.co/frankjoshua/realvisxlV40_v40Bakedvae/tree/main)


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

