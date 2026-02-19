
def standardise_to_https(url: str) -> str:
    """
    turn http string into https
    
    :param url: The URL a user passes in
    :type url: str
    :return: A URL in an appropriate format. This does not mean it exists, just allows for common typings
    :rtype: str
    """
    output = url
    # add the http:// or https:// if it is missing
    if output.startswith("http://"):
        # if connection is insecure, upgrade because TLS is good
        output = "https://" + output[7:]
    return output