import csv
import os
import subprocess
import argparse
import json

def get_video_dimensions(video_path):
    """ get video width and hight """
    cmd = [
        'ffprobe',
        '-v', 'error',
        '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height',
        '-of', 'json',
        video_path
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise ValueError(f"Error {result.stderr.decode()}")
    
    info = json.loads(result.stdout)
    return info['streams'][0]['width'], info['streams'][0]['height']


def process_csv(csv_path):
    with open(csv_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # read meta info
            bvid = row['bvid']
            scene_id = row['scene_id']
            cut_id = row['cut_id']
            start_time = row['cut_start_timecode']
            end_time = row['cut_end_timecode']
            crop_region = row['crop_region'].strip('[]"')
            
            # get video dimensions
            input_video = f"videos/source/{bvid}.mp4"
            if not os.path.exists(input_video):
                print(f"Video Not Found: {input_video}")
                continue

            try:
                video_width, video_height = get_video_dimensions(input_video)
            except Exception as e:
                print(f"Error [{input_video}]: {str(e)}")
                continue
            
            crop_values = list(map(float, crop_region.split(',')))
            ct, cb, cl, cr = (
            int(crop_values[0]*video_height)//2 * 2,
            int(crop_values[1]*video_height)//2 * 2,
            int(crop_values[2]*video_width)//2 * 2,
            int(crop_values[3]*video_width)//2 * 2
            )
            crop_str = f"crop={cr-cl}:{cb-ct}:{cl}:{ct}"

            # path for output
            output_dir = f"videos/clips/{bvid}"
            output_file = f"{bvid}_scene{scene_id}_cut{cut_id}.mp4"
            output_path = os.path.join(output_dir, output_file)
            os.makedirs(output_dir, exist_ok=True)
            
            # ffmpeg cut
            cmd = [
                'ffmpeg',
                '-i', input_video,
                '-ss', start_time,
                '-to', end_time,
                '-vf', crop_str,
                '-c:v', 'libx264',
                '-crf', '19',
                '-preset', 'fast',
                '-c:a', 'aac', 
                '-y', 
                output_path
            ]

            try:
                subprocess.run(cmd, check=True)
                print(f"sucess {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"fail {e}")
            except Exception as e:
                print(f"error {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Preprocess Tiger200K Dataset')
    parser.add_argument('--meta-path', 
                       type=str, 
                       required=True,
                       help='input the meta csv file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.meta_path):
        print(f"meta csv file not found [{args.meta_path}]")
        exit(1)
        
    process_csv(args.meta_path)