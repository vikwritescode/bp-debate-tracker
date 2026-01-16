from urllib.parse import urlparse

def correct_url(url: str) -> str:
    """
    Docstring for correct_url
    
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
    elif not (output.startswith("https://")):
        # otherwise if our url doesn't start with https://
        output = "https://" + output
    
    # add .calicotab.com if there is no TLD
    if len(output.split(".")) < 2:
        output += ".calicotab.com"
        
    # parse URL
    parsed = urlparse(output)
    output = f"https://{parsed.netloc}"    
    return output