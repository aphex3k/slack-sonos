from __future__ import print_function
import os
from queue import Empty
import soco
import slack
from google_images_search import GoogleImagesSearch
from datetime import datetime

slack_token = os.environ["SLACK_API_TOKEN"]
rtmclient = slack.RTMClient(token=slack_token)
speak_after = datetime.min

@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    global speak_after
    try:
        if datetime.today() < speak_after:
            raise Exception("The track last announced is still playing...")

        if 'song' in data['text'].lower() or 'sonos' in data['text'].lower() or 'music' in data['text'].lower():
            channel_id = data['channel']
            thread_ts = data['ts']
            # user = data['user']

            text="I couldn't find anything playing currently."

            coordinator = Empty

            for zone in soco.discover():
                if zone.is_coordinator and zone.get_current_transport_info()['current_transport_state'] == "PLAYING" \
                        and len(zone.get_current_track_info()['title']) > 0:
                    coordinator = zone
                    break

            track = coordinator.get_current_track_info()
            attachment = []

            if len(track['title']) > 0:
                text = zone.player_name.strip() + " is playing " + track['artist'].strip() + " with " + track['title'].strip() + " from the album " + track['album'].strip()

                gis = GoogleImagesSearch(os.environ["GOOGLE_API_TOKEN"], os.environ["GOOGLE_CX_TOKEN"])

                _search_params = {
                    'q': "album cover " + track['artist'].strip() + " " + track['album'].strip(),
                    'num': 1
                }

                gis.search(search_params=_search_params, cache_discovery=False)
                image_url = gis.results().pop().url
                attachment.append({
                    "image_url": image_url,
                    "fallback": track['artist'].strip() + " - " + track['title'].strip(),
                    "title": track['artist'].strip() + " - " + track['title'].strip(),
                    "text": track['album'].strip(),
                    "color": "#212121"
                })

            webclient = payload['web_client']
            webclient.chat_postMessage(
                channel=channel_id,
                text=text,
                thread_ts=thread_ts,
                as_user=False,
                icon_url="https://images-na.ssl-images-amazon.com/images/I/41838a7kfqL.png",
                username="Sonos",
                attachments=attachment
            )

            duration = datetime.strptime(track['duration'], '%H:%M:%S')
            position = datetime.strptime(track['position'], '%H:%M:%S')
            remaining_time = duration - position
            speak_after = datetime.today() + remaining_time
    except:
        speak_after = datetime.today() + datetime.timedelta(0, 5)
        pass

rtmclient.start()