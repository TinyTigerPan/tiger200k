<div align="center">
  <img src="assets/tiger.png"  height=100>
  <h1>Tiger200K Dataset</h1>
</div>

<div align="center">
  <a href="https://arxiv.org/abs/2504.15182"><img src="https://img.shields.io/static/v1?label=Tech%20Report&message=Arxiv&color=red"></a> &ensp;
  <a href="https://huggingface.co/datasets/tinytigerpan/tigerdataset"><img src="https://img.shields.io/static/v1?label=Dataset&message=HuggingFace&color=yellow"></a> &ensp;
  <a href="https://tinytigerpan.github.io/tiger200k"><img src="https://img.shields.io/static/v1?label=Tiger200K&message=Project%20Page&color=green"></a> &ensp;
</div>

## 🐯 Introduction
Tiger200K is a manually curated high visual quality video dataset sourced from User-Generated Content (UGC) platforms. By prioritizing visual fidelity and aesthetic quality, Tiger200K underscores the critical role of human expertise in data curation, and providing high-quality, temporally consistent video-text pairs for fine-tuning and optimizing video generation architectures through a simple but effective pipeline. The dataset will undergo ongoing expansion and be released as an open-source initiative to advance research and applications in video generative models.

🧐 For more information, you can refer to our paper and project page.

## 📣 Notice
⚠️ This dataset is for **non-commercial use only**. Please read carefully and follow the license on hugging face and README documents before use.

🎬 The information such as quality and resolution in the dataset refers to the highest quality that you can watch on the corresponding video platform. You need to handle issues such as obtaining the source video and copyright by yourself.


## 🔥 News
* Jul 7, 2025: 🚀 We expand tiger dataset to ~500k, and update better caption with Tarsier. [🤗](https://huggingface.co/datasets/tinytigerpan/tigerdataset)
* Apr 26, 2025: ✅ We release the tiger200k dataset and the scripts for data preparation.
* Apr 21, 2025: 👀 We release the paper and preview dataset.

## Data Preparation
```
├── meta_csv
│ └── tiger200k_batch0.csv
│
├── videos
│ ├── clips
│ │ ├── BV1134y1E7P5
│ │ │ ├── BV1134y1E7P5_secen1_cut1.mp4
│ │ │ ├── BV1134y1E7P5_secen1_cut2.mp4
│ │ │ └── ...
│ │ ├── BV114411z7v9
│ │ │ ├── BV1134y1E7P5_secen1_cut1.mp4
│ │ │ ├── BV1134y1E7P5_secen2_cut1.mp4
│ │ │ └── ...
│ │ └── ...
│ │
│ └──source
│   ├── BV1134y1E7P5.mp4
│   ├── BV114411z7v9.mp4
│   └── ...
```

### Download the Meta csv
Download the meta csv from [🤗hugging face](https://huggingface.co/collections/tinytigerpan/tiger200k-680b013101d997f97f29c030) to `meta_csv`.

### Source Video Download
We now release the script to download videos from Bilibili by bvid entries of tiger200k dataset. Thanks to [@MuteApo](https://github.com/MuteApo).

Downloaded videos will be placed in `videos/source` and named by bvid, such as `BV1134y1E7P5.mp4`.

HD/FHD streaming (720P and above) ​​requires **COOKIE** authentication​​ on Bilibili, while 4K resolution ​​mandates an active **premium subscription​​**.

Please refer to [bilibili-downloader](https://github.com/tyokyo320/bilibili-downloader/blob/master/docs/set-cookie.png) for instructions.


### Cut the video
Run `python cut_videos.py --meta-path meta_csv/tiger200k_batchxxx.csv` to cut source video to clips.

## Citation
```bibtex
@article{zhou2025tiger200k,
  title={Tiger200K: Manually Curated High Visual Quality Video Dataset from UGC Platform},
  author={Zhou, Xianpan},
  journal={arXiv preprint arXiv:2504.15182},
  year={2025}
}
```
