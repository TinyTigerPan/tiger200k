import os
import sys
import time

import pandas as pd
from tqdm import tqdm

sys.path.append(os.path.join(os.path.dirname(__file__), "bilibili-downloader"))

import config
from models.category import Category
from models.video import Video
from strategy.bilibili_executor import BilibiliDownloader, BilibiliExecutor
from strategy.default import DefaultStrategy

config.TEMP_PATH = config.OUTPUT_PATH = "videos/source"
config.COOKIE = ""
assert config.COOKIE != "", "Please set your cookie for bilibili!"


class TigerStrategy(DefaultStrategy):
    def get(self, video: Video) -> Video:
        bs = self.get_video_page(video.url)
        title = self.get_video_title(bs)
        json = self.get_video_json(bs)

        payload = json["data"]["dash"]["video"]

        video_dict_by_quality = {x["id"]: x for x in payload}

        for quality_id in [120, 112, 80]:  # 4K, 1080P+, 1080P
            if quality_id in video_dict_by_quality:
                video.set_title(title)
                video.set_quality(quality_id)
                video.set_video_url(video_dict_by_quality[quality_id]["baseUrl"])
                video.set_audio_url(video_dict_by_quality[quality_id]["baseUrl"])

                return video

        raise ValueError(f"No available resolution for {video.url}")


class TigerDownloader(BilibiliDownloader):
    def download_video(self, video) -> None:
        print(f"[{video.bvid}] {video.title}")
        save_path = os.path.join(config.OUTPUT_PATH, video.bvid + ".mp4")
        self._download(video.video_url, save_path)


class TigerExecutor(BilibiliExecutor):
    def get(self, bvid: str) -> Video:
        url = f"https://www.bilibili.com/video/{bvid}/?spm_id_from=333.337.search-card.all.click"
        video = self.get_video(url)
        strategy = self._strategies[video.category]
        video = strategy.get(video)
        video.bvid = bvid

        return video


class BFacade:
    def __init__(self):
        self.downloader = TigerDownloader()
        self.crawler = TigerExecutor()
        self.crawler._strategies = {Category.default: TigerStrategy()}

    def download(self, bvid_list):
        os.makedirs(config.OUTPUT_PATH, exist_ok=True)
        for bvid in tqdm(bvid_list):
            save_path = os.path.join(config.OUTPUT_PATH, bvid + ".mp4")
            if not os.path.exists(save_path):
                video = self.crawler.get(bvid)
                self.downloader.download_video(video)


if __name__ == "__main__":
    start_time = time.time()

    df = pd.read_csv("../tiger200k_batch0.csv")
    BFacade().download(set(df["bvid"].tolist()))

    end_time = time.time()
    times = round(end_time - start_time)
    minutes = times // 60
    times %= 60
    seconds = times
    print(f"Time elapsed：{minutes} min {seconds} sec")
