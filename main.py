import os
import shutil
import requests
from tqdm import tqdm

cwd = os.getcwd()

def downloadClip(link, i, path):
    r = requests.get(link, stream=True)
    with open(f'{cwd}/{path}/{i}.ts', 'wb') as f:
        f.write(r.content)

def joinClips(path: str):
    with open(path + '.ts', 'wb') as merged:
        
        dir = os.listdir(f'{cwd}/{path}')
        dir = [file for file in dir if file.endswith('.ts')]
        dir = sorted(dir, key = lambda x: int(x.split('.')[0]))

        print(path, ":", len(dir))

        for ts_file in dir:
            with open(f'{cwd}/{path}/{ts_file}', 'rb') as mergefile:
                shutil.copyfileobj(mergefile, merged)

if __name__ == '__main__':
    URL = input("Enter URL: ")
    CLIP_N = int(input("Enter number of clips: "))
    OUT_DIR = input("Enter output directory: ") or 'clips'

    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    print("Downloading clips...")
    for i in tqdm(range(1, CLIP_N+1)):
        downloadClip(URL + f'/seg-{i}-v1-a1.ts', i, OUT_DIR)

    print("Joining clips...")
    joinClips(OUT_DIR)

    print("Done! Check", cwd, "for the output file.")
