# Backend Part of Chatacter

Back to [Chatacter](https://github.com/AlphaSphereDotAI/chatacter)

## Installation

```bash
git clone https://github.com/AlphaSphereDotAI/chatacter_backend.git
cd chatacter_backend
conda create -n chatacter python=3.10
conda activate chatacter
conda install ffmpeg pytorch=2.1.0 torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
conda install imageio=2.19.3 imageio-ffmpeg=0.4.7 librosa=0.9.2 pydub=0.25.1 kornia=0.6.8 yacs=0.1.8 scikit-image=0.19.3 facexlib=0.3.0 trimesh=3.9.20 fastapi pandas huggingface_hub langchain-groq opencv -c conda-forge
conda install face_alignment=1.3.5 -c 1adrianb
pip install basicsr==1.4.2 gfpgan wget cog
```
