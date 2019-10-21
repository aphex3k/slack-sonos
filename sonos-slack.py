from __future__ import print_function
import os
from queue import Empty
import soco
import slack
from google_images_search import GoogleImagesSearch
from datetime import datetime, timedelta

slack_token = os.environ["SLACK_API_TOKEN"]
rtm_client = slack.RTMClient(token=slack_token)
speak_after = {}


@slack.RTMClient.run_on(event='message')
def say_hello(**payload):
    data = payload['data']
    global speak_after
    channel = data['channel']

    after_ts = datetime.min

    if channel in speak_after:
        after_ts = speak_after[channel]

    try:
        if datetime.today() < after_ts:
            raise Exception("The track last announced is still playing...")

        if 'song' in data['text'].lower() or 'sonos' in data['text'].lower() or 'music' in data['text'].lower():
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
                channel=channel,
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
            speak_after[channel] = datetime.today() + remaining_time
    except:
        buffer = datetime.today() + timedelta(0, 5)
        speak_after[channel] = speak_after[channel] if speak_after[channel] > buffer else buffer
        pass


rtm_client.start()
