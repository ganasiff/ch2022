def extractURL(tree):
    """#This will get the anchor tags <a href...> ending with csv format file"""

    refs = tree.xpath("//a")
    # Get the url from the ref
    links = [link.get('href', '') for link in refs]
    # Return a list that only ends with .com.br
    return [l for l in links if l.endswith('.csv')]
