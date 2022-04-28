import vlc.vlc as v
import requests
import json
import time

def get_cid(bvid):
    head = "https://api.bilibili.com/x/player/pagelist"
    url = head + "?bvid=" + bvid
    response = requests.get(url)
    raw = json.loads(response.text)
    return raw["data"][0]["cid"]

def get_mp3(bvid):
    head = "https://api.bilibili.com/x/player/playurl"
    bv = "?bvid=" + bvid
    cid = "&cid=" + str(get_cid(bvid))
    fnval = "&fnval=16"
    url = head + bv + cid + fnval
    response = requests.get(url)
    raw = json.loads(response.text)
    return raw["data"]["dash"]["audio"][len(raw["data"]["dash"]["audio"]) - 1]["baseUrl"]

def download(bvid):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
        "Referer": "https://www.bilibili.com/video/bv" + bvid
    }
    sess = requests.Session()
    url = get_mp3(bvid)
    r = sess.options(url, headers=header)
    r = sess.get(url, headers=header)
    with open("temp/temp.m4s", "wb") as f:
        f.write(r.content)
    return 0
   
def play(bvid):
    download(bvid)
    # play temp/temp.m4s using instance of vlc
    vlc = v.Instance()
    vlc.log_unset()
    player = vlc.media_player_new()
    media = vlc.media_new("temp/temp.m4s")
    player.set_media(media)
    player.play()
    # Show progress
    while player.get_state() != v.State.Playing:
        print("\rLoading...")
        time.sleep(0.1)
    control(player)
    return 0

def control(player):
    while True:
        print("\rPress 'p' to pause/resume, 'q' to quit")
        order = input()
        if order == "p":
            if player.get_state() == v.State.Playing:
                player.pause()
            else:
                player.play()
        elif order == "q":
            player.stop()
            return 0