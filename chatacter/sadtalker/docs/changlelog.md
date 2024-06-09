## changelogs

- **[2023.04.06]**: stable-diffiusion webui extension is release.

- **[2023.04.03]**: Enable TTS in huggingface and gradio local demo.

- **[2023.03.30]**: Launch beta version of the full body mode.

- **[2023.03.30]**: Launch new feature: through using reference videos, our algorithm can generate videos with more natural eye blinking and some eyebrow movement.

- **[2023.03.29]**: `resize mode` is online by `python infererence.py --preprocess resize`! Where we can produce a larger crop of the image as discussed in https://github.com/Winfredy/SadTalker/issues/35.

- **[2023.03.29]**: local gradio demo is online! `python app.py` to start the demo. New `requirments.txt` is used to avoid the bugs in `librosa`.

- **[2023.03.28]**: Online demo is launched in [![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/vinthony/SadTalker), thanks AK!

- **[2023.03.22]**: Launch new feature: generating the 3d face animation from a single image. New applications about it will be updated.

- **[2023.03.22]**: Launch new feature: `still mode`, where only a small head pose will be produced via `python inference.py --still`.

- **[2023.03.18]**: Support `expression intensity`, now you can change the intensity of the generated motion: `python inference.py --expression_scale 1.3 (some value > 1)`.

- **[2023.03.18]**: Reconfig the data folders, now you can download the checkpoint automatically using `bash scripts/download_models.sh`.
- **[2023.03.18]**: We have offically integrate the [GFPGAN](https://github.com/TencentARC/GFPGAN) for face enhancement, using `python inference.py --enhancer gfpgan` for better visualization performance.
- **[2023.03.14]**: Specify the version of package `joblib` to remove the errors in using `librosa`, [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Winfredy/SadTalker/blob/main/quick_demo.ipynb) is online!
- **[2023.03.06]**: Solve some bugs in code and errors in installation
- **[2023.03.03]**: Release the test code for audio-driven single image animation!
- **[2023.02.28]**: SadTalker has been accepted by CVPR 2023!
