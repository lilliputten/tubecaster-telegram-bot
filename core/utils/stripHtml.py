import re

removeStyles = re.compile(r'<style.*?</style>')
removeScripts = re.compile(r'<script.*?</script>')
removeTags = re.compile(r'<.*?>')
removeEolSpaces = re.compile(r'\s+$')
removeMultipleNewlines = re.compile(r'\n\s*\n')


def stripHtml(data):
    data = removeStyles.sub('', data)
    data = removeScripts.sub('', data)
    data = removeTags.sub('', data)
    data = removeEolSpaces.sub('', data)
    data = removeMultipleNewlines.sub('\n\n', data)
    return data.strip()
