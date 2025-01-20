from barkr.connections.base import ConnectionMode
from barkr.connections.mastodon import MastodonConnection
from barkr.connections.bluesky import BlueskyConnection
from barkr.main import Barkr

h = Barkr(
    [
        # MastodonConnection(
        #     "Mastodon",
        #     modes=[ConnectionMode.READ],
        #     access_token="PGjHSnUb65x8FsHPQ3kxH0gBgbEHQnr77WmeYn0YB_c",
        #     instance_url="https://tech.lgbt",
        # ),
        BlueskyConnection(
            name="Bluesky",
            modes=[ConnectionMode.READ],
            handle="usbclima.bsky.social",
            password="M@ftHz56YK6N5VJ"
        )
    ]
)
h.start()
