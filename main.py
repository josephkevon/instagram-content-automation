import instagrapi
import os
import time

username = "" # enter your instagram username
password = "" # enter your instagram password
MIN_LIKES = 1000        # Minimum likes required
MIN_COMMENTS = 50       # Minimum comments required  
MIN_VIEWS = 10000       # Minimum views required
MAX_AGE_DAYS = 90       # Maximum age in days (optional)
target = ["financeunfolded", "casper.capital", "c3livetv"]  # username of the account you want to extract reels from



cl = instagrapi.Client()

def exrtact_videos():
    try:
        cl.login(username, password)
    except Exception as e:
        print(f"Login failed: {e}")
        exit(1)
    cl.request_timeout = 30  # Increase timeout to 30 seconds

    os.makedirs("reels", exist_ok=True)

    all_account_names = []
    all_captions = []
    all_user_ids = []


    for tar in target:
        user_id = cl.user_id_from_username(tar)

        reels = cl.user_clips(user_id, amount=100)  # get 10 reels

        for reel in reels:

            with open("reels.txt", "r") as f:
                lines = f.readlines()

            if reel.video_url in lines:
                print(f"Link already exists: {reel.video_url}")
                continue

            if reel.like_count < MIN_LIKES:
                print(f"Skipped {reel.pk}: Too few likes ({reel.like_count})")
                continue
                
            if reel.comment_count < MIN_COMMENTS:
                print(f"Skipped {reel.pk}: Too few comments ({reel.comment_count})")
                continue
                
            if reel.view_count < MIN_VIEWS:
                print(f"Skipped {reel.pk}: Too few views ({reel.view_count})")
                continue
            
            else:
                vids = cl.clip_download(reel.pk, "reels")
                print(f"reel id: {reel.pk}")
                print(f"username: {reel.user.username}")
                all_account_names.append(reel.user.username)
                all_captions.append(reel.caption_text)
                all_user_ids.append(reel.pk)
                with open("reels.txt", "a") as f:
                    f.write(f"{reel.video_url}\n")

    return all_account_names, vids, reel.pk, reels, reel.video_url, all_captions, all_user_ids



def post_video():
    cl.login(username, password)

    all_account_names, vids, pk, reels, video_url, all_captions, all_user_ids = exrtact_videos()


    for i in range(len(all_account_names)):
        video = f"reels/{all_account_names[i]}_{all_user_ids[i]}.mp4"
        media = cl.video_upload(video, f"{all_captions[i]} credit: @{all_account_names[i]}")

if __name__ == "__main__":
    while True:
        post_video()
        print("done")
        print("Sleeping for 24 hours...")
        min_in_day = 24 * 60

        time.sleep(min_in_day * 60)  # Sleep for 24 hours
