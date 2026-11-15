def social_links(request):
    """
    Exposes official NABAS social media channels across all templates.
    """
    return {
        'NABAS_SOCIAL': {
            'instagram': 'https://www.instagram.com/p/DcLlAWijGEI/',
            'x': 'https://x.com/NabasNational',
            'facebook': 'https://web.facebook.com/NabasNational/',
            'whatsapp_group': 'https://whatsapp.com/Gqht6qffAWi6d2VB6X0m27?s=cl&p=i&mlu=4&ilr=4',
            'whatsapp_channel': 'https://whatsapp.com/channel/002VasQQCcA2pL2XinHox2m',
        }
    }
