import re

#  error: Method "decode" overrides class "JSONDecoder" in an incompatible manner
#      Positional parameter count mismatch; base method has 3, but override has 3 (reportIncompatibleMethodOverride)
#  class SanityJson(json.JSONDecoder):
#      def decode(self, s, **kwargs):
#          regex_replacements = [
#              (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
#              (re.compile(r',(\s*])'), r'\1'),
#          ]
#          for regex, replacement in regex_replacements:
#              s = regex.sub(replacement, s)
#          return super().decode(s, **kwargs)


def sanityJson(s: str):
    regex_replacements = [
        (re.compile(r'([^\\])\\([^\\])'), r'\1\\\\\2'),
        (re.compile(r',(\s*])'), r'\1'),
    ]
    for regex, replacement in regex_replacements:
        s = regex.sub(replacement, s)
    return s
