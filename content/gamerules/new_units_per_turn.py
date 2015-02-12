

def max_connected_provinces(campaign, player):
    provinces = player.provinces[:]
    if not provinces:
        return 0
    groups = []
    def gather(neighbours):
        result = []
        for neighbour in neighbours:
            if neighbour in provinces:
                result.append(neighbour)
                provinces.remove(neighbour)
                neighbour = campaign.provinces[neighbour]
                result += gather(neighbour.neighbours)
        return result

    while provinces:
        province = provinces[0]
        provinces.pop(0)
        group = [province] + gather(campaign.provinces[province].neighbours)
        groups.append(group)
    return max([len(g) for g in groups])
