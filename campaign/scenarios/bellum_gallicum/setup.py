

def setup(campaign):
    arverni = campaign.players[0]
    rome = campaign.players[1]

    provinces = {
        'gaul': campaign.provinces[(177, 201, 112, 255)],
        'cisalpina': campaign.provinces[(45, 201, 112, 255)],
        'narbonensis': campaign.provinces[(130, 48, 30, 255)]
    }

    campaign.events['change_owner'].trigger(provinces['gaul'], arverni)
    campaign.events['change_owner'].trigger(provinces['cisalpina'], rome)
    campaign.events['change_owner'].trigger(provinces['narbonensis'], rome)

    campaign.events['amass_units'].trigger(provinces['gaul'])
    campaign.events['amass_units'].trigger(provinces['cisalpina'])
    campaign.events['amass_units'].trigger(provinces['narbonensis'])
