from botCore.constants import emojies, limits


def getPlansInfoMessage(userId: int):
    """
    Returns usage plans description text.
    """
    guestPlanItems = [
        emojies.numbers[1]
        + f' GUEST PLAN allows to make {limits.guestCastRequests} download and {limits.guestInfoRequests} info requests.',
        'This mode is intended only for familiarization with the service in trial mode.',
    ]

    freePlanItems = [
        emojies.numbers[2]
        + f' FREE PLAN allows to make {limits.freeCastRequests} download and {limits.freeInfoRequests} info requests monthly.',
        'If you are still on the guest plan, you can try to request the free mode via /become_user command.',
    ]

    paidPlanItems = [
        emojies.numbers[3] + ' PAID PLAN allows you to make an unlimited number of downloads and info requests.',
        f'The monthly cost of the paid usage plan is {emojies.star} {limits.paidPlanPriceStars}.',
        'You can start it right now via the /get_full_access command.',
    ]

    # TODO: Add a link to the plans reference on the site

    contentItems = [
        'THERE ARE THREE USAGE PLANS AVAILABLE:',
        '\n\n'.join(list(filter(None, guestPlanItems))),
        '\n\n'.join(list(filter(None, freePlanItems))),
        '\n\n'.join(list(filter(None, paidPlanItems))),
    ]
    content = '\n\n'.join(list(filter(None, contentItems)))

    return content
