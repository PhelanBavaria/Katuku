from campaign.controllers.player import Player
from campaign.controllers.local_player import LocalPlayer
from campaign.controllers.ai import AI
from campaign.controllers.independent import Independent

types = {
    'local': LocalPlayer,
    'ai': AI,
    'independent': Independent
}
