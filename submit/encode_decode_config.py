
# Encoder / Decoder configuration - determines the Unicode character ranges to be used in encoding and decoding.

# Maximum character code of input
maxCharacterCodeOfInput = 255

# Number of character codes allocated to the task of replacing substrings
allocationForReplacingSubstrings = 1792

# The last two numbers added together
# Corresponds to the upper limit of characters used for original document content and replaced substrings
maxCodeofInputAndSubstrings = maxCharacterCodeOfInput + allocationForReplacingSubstrings