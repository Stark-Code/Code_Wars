import time
# Manacher Algorithm


def adjStrParity(s):
    oddStr = "#"
    for char in s:
        oddStr += char + "#"
    return oddStr


def longest_palindrome(s):
    s = adjStrParity(s)
    #     print(f"Adjusted String: {s}")
    c = 0
    r = 0
    lps = [0 for _ in range(len(s))]
    #     print(lps)

    for i in range(len(s)):
        iMirror = (2 * c) - i
        if r > i:
            lps[i] = min(r - i, lps[iMirror])
        try:
            while s[i + 1 + lps[i]] == s[i - 1 - lps[i]]:
                lps[i] += 1
        except:
            pass
        if i + lps[i] > r:
            c = i
            r = i + lps[i]

    #     print(f"LPS: {lps}")
    c, r = lps.index(max(lps)), max(lps)

    return s[c - r:c + r].replace("#", "")


tic = time.perf_counter()
# longest_palindrome('ttaaftffftfaafatf')  # , 'aaftffftfaa')
longest_palindrome('dde')
toc = time.perf_counter()

print(f"Time: {toc - tic:0.4f} seconds")









# Naive Approach
# def longest_palindrome(s):
#     palindrome = ""
#     strLen = len(s)
#     for idx in range(strLen):
#         frontPos, endPos, endRef = idx, strLen - 1, strLen - 1
#         palLen = len(palindrome)
#         if strLen - idx <= palLen:
#             break
#         while frontPos <= endPos:
# #             if strLen - idx <= palLen:
# #                 break
#             if s[frontPos] == s[endPos]:
#                 frontPos += 1
#                 endPos -= 1
#             else:
#                 frontPos, endPos = idx, endRef - 1
#                 endRef -= 1
#         if endRef+1 - idx > palLen:
#             palindrome = s[idx:endRef+1]
#             print(palindrome)
#     return palindrome
#
# tic = time.perf_counter()
# longest_palindrome('ttaaftffftfaafatf')  # , 'aaftffftfaa')
# toc = time.perf_counter()
#
# print(f"Time: {toc - tic:0.4f} seconds")


# Select start position
# Go to end of string, work backwards to find letter that matches start position.
# Once a match is found test for palindrome
# Store if found, else continue until you are back at start
# If a palindrome is found, stop looking, increment start and repeat.
# If distance from start to lastMatch is less than the length of current longest palindrome. Stop searching
# If distance from start to end of string is less than longest palindrome. Stop searching
