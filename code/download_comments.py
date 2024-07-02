import os
import glob
import json
import re

def download_comments_from_streams(stream_ids:[str] = []):
    """
    Call TwitchDownloaderCLI to download comments for each stream_id in the list
    """
    os.system("rm /app/code/comments/*.json")
    for stream_id in stream_ids:
        os.system(f"TwitchDownloaderCLI chatdownload --id {stream_id} --embed-images --bttv=true --ffz=false --stv=false -o /app/code/comments/chat_{stream_id}.json")

def parse_comments_events(comments_path:str = "comments"):
    files_to_load = glob.glob(f'{comments_path}/*.json')
    files_to_load.sort()

    commenter_subscribed = {}
    freeloaders = []
    founders_list = []
    subsribers_by_badge = {}

    for filename in files_to_load:
        with open(filename, "r") as f:
            data = json.loads(f.read())
        
        for comment in data["comments"]:
            for badge in comment["message"]["user_badges"]:
                if badge["_id"] == "founder":
                    founders_list.append(comment["commenter"]["display_name"])
            if "gifted" in str(comment):
                freeloader_names = re.findall(r" to (.*?)!", comment["message"]["body"])
                if freeloader_names:
                    freeloaders.append(freeloader_names[0])
                pass
            if "at Tier" in str(comment):
                # Subcribed event
                if comment["commenter"]["_id"] not in commenter_subscribed:
                    commenter_subscribed[comment["commenter"]["_id"]] = {
                        "created_at": comment["created_at"],
                        "display_name": comment["commenter"]["display_name"],
                        "game": data["video"]["game"]
                    }
                else:
                    print(f"repeated commenter: {comment['commenter']['display_name']}")

    for filename in files_to_load:
        with open(filename, "r") as f:
            data = json.loads(f.read())
        
        for comment in data["comments"]:
            for badge in comment["message"]["user_badges"]:
                if badge["_id"] == "subscriber":
                    if comment["commenter"]["_id"] not in subsribers_by_badge:
                        if comment["commenter"]["display_name"] not in freeloaders and comment["commenter"]["display_name"] not in founders_list and comment["commenter"]["_id"] not in commenter_subscribed:
                            subsribers_by_badge[comment["commenter"]["_id"]] = {
                                "created_at": comment["created_at"],
                                "display_name": comment["commenter"]["display_name"],
                                "game": data["video"]["game"]
                            }

    return {
        "founders" : list(set(founders_list)),
        "non_gifted_subscribers_first_comment": subsribers_by_badge
    }

if __name__ == "__main__":
    stream_ids = [
        "2164262428",
        "2165104316",
        "2165230777",
        "2168509794",
        "2169473950",
        "2170212699",
        "2171075428",
        "2172043667",
        "2173527824",
        "2174384734",
        "2175357482",
        "2176071193",
        "2176932438",
        "2177978469",
        "2179618516",
        "2180599868",
        "2180693622",
        "2181487698",
        "2182228140",
        "2184092647",
        "2184959671"
    ]
    
    download_comments_from_streams(stream_ids = stream_ids)

    print(json.dumps(parse_comments_events(comments_path="/app/code/comments"),indent=1))
