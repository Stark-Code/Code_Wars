import logging
import re
import time
logging.basicConfig(level=logging.INFO, format='%(message)s')


def top_3_words(text):
    wordCount = {}
    if not re.search(r'[a-z\']+', text, flags=re.IGNORECASE):
        return []
    tList = re.findall(r'[a-z\']+', text, flags=re.IGNORECASE)
    print(tList)
    for word in tList:
        word = word.lower()
        if word in wordCount:
            wordCount[word] += 1
        else:
            wordCount[word] = 1
    sorted_dict = {}
    sorted_keys = sorted(wordCount, key=wordCount.get, reverse=True)  # [1, 3, 2]

    for w in sorted_keys:
        sorted_dict[w] = wordCount[w]
    for key in sorted_dict.items():
        print(key)
    result = list(sorted_dict)
    return result[:3]



t1 = """In a village of La Mancha, the name of which I have no desire to call to
mind, there lived not long since one of those gentlemen that keep a lance
in the lance-rack, an old buckler, a lean hack, and a greyhound for
coursing. An olla of rather more beef than mutton, a salad on most
nights, scraps on Saturdays, lentils on Fridays, and a pigeon or so extra
on Sundays, made away with three-quarters of his income."""

t2 = 'rNihDl.?../rNihDl,_/-RQrOUvxJNi,RQrOUvxJNi/RQrOUvxJNi/-:_RQrOUvxJNi?rNihDl?!!:-rNihDl_! ' \
     '-!RQrOUvxJNi;/RQrOUvxJNi/,_?_rNihDl-!!RQrOUvxJNi!// RQrOUvxJNi/RQrOUvxJNi:RQrOUvxJNi _,;/RQrOUvxJNi RQrOUvxJNi,' \
     '!-rNihDl;rNihDl -RQrOUvxJNi,:rNihDl_;_-rNihDl/!:,?RQrOUvxJNi...//rNihDl /?RQrOUvxJNi ;/,RQrOUvxJNi,' \
     'RQrOUvxJNi:RQrOUvxJNi,RQrOUvxJNi.:rNihDl RQrOUvxJNi_RQrOUvxJNi?-;RQrOUvxJNi_RQrOUvxJNi?_:?rNihDl,/ .,' \
     'RQrOUvxJNi,-?RQrOUvxJNi- rNihDl_;rNihDl?!RQrOUvxJNi!_.RQrOUvxJNi:.!?, '

t3 = "KK'-bfaFvo-QVLZI,_;uOsjpZaXN_- _xaWLNMyfNK?-;,zfXxUn.-.PTuQXs:!bXaOHW/ ;/;bfaFvo ::.ghJ' PTuQXs;," \
     "! llbsUdRv!iJV!zfXxUn/;QVLZI:,!llbsUdRv?-;:iJV.PTuQXs,./bfaFvo:-_dWxPC''ia;,.ghJ' ?:bfaFvo_-iJV QVLZI? ?/ " \
     "PTuQXs.?/ ,zfXxUn?aTMcju.:./.bXaOHW!!:_;ghJ'; PTuQXs//QVLZI?;uOsjpZaXN/QVLZI!!?_!iJV_?/?QVLZI,;;aTMcju?bfaFvo.," \
     "/?!KK',.QVLZI!iJV,,?_iJV-bfaFvo_-xaWLNMyfNK- ?zfXxUn??;;-PTuQXs-/;?KK'.:-!uOsjpZaXN?_/aTMcju;!QVLZI.! " \
     ";PTuQXs?.bXaOHW! /bfaFvo.,;dWxPC''ia,!bfaFvo. /zfXxUn?_.//lGb!?_iJV,_xaWLNMyfNK-!:PTuQXs;GatGOgh'  bfaFvo," \
     "llbsUdRv/dWxPC''ia?PTuQXs?!llbsUdRv::.?-PTuQXs_zfXxUn/llbsUdRv;;!!;lGb::;/!ghJ'!;iJV?:-QVLZI;,iJV,:ghJ'.ghJ'," \
     "/iJV.?/;llbsUdRv.?/KK'_.! xaWLNMyfNK!.bXaOHW,._?;KK'- :iJV/:: KK':? !QVLZI_?KK';_?.,zfXxUn:KK' " \
     "_QVLZI?GatGOgh'//,;;ghJ',?? xaWLNMyfNK !/ KK'.,KK'; ?_ KK' -bXaOHW./--iJV_/ :iJV,_/PTuQXs;  _!uOsjpZaXN!_KK' " \
     ".:/;KK'-uOsjpZaXN_/zfXxUn.-  /aTMcju:!bfaFvo!_ghJ'? /:xaWLNMyfNK, ;._uOsjpZaXN!ghJ';_,,/bfaFvo," \
     "-_llbsUdRv!bfaFvo: !:,KK'!;!_/uOsjpZaXN.:!PTuQXs-,-QVLZI!QVLZI,-; ?iJV,_llbsUdRv?.;;aTMcju!GatGOgh';," \
     "zfXxUn_;?!!zfXxUn-_,ghJ'_:-zfXxUn-iJV;PTuQXs;!;/.PTuQXs?," \
     ":xaWLNMyfNK?_-bfaFvo!;._?lGb.:QVLZI?;/xaWLNMyfNK?!::GatGOgh'-KK'?,,PTuQXs!.;ghJ'-/ " \
     ";KK'-;/;-iJV;.QVLZI_..llbsUdRv; ghJ'_ghJ'.PTuQXs! ?- xaWLNMyfNK: ?xaWLNMyfNK,_QVLZI zfXxUn:.iJV, __uOsjpZaXN: " \
     "!//zfXxUn?iJV.: KK':;-; PTuQXs-QVLZI/;,ghJ'--/KK'-.QVLZI:bfaFvo:;_bfaFvo/!. zfXxUn!bfaFvo.!xaWLNMyfNK-llbsUdRv! " \
     "ghJ'://xaWLNMyfNK!//.;xaWLNMyfNK/?xaWLNMyfNK: PTuQXs;;:QVLZI," \
     "bfaFvo_?bXaOHW!/;?;PTuQXs:.uOsjpZaXN?-_ghJ'?:llbsUdRv,!-_?KK'!,,;;KK':/,;:iJV ?QVLZI_/KK'  bfaFvo,/zfXxUn;.KK'," \
     "zfXxUn/uOsjpZaXN:/-,PTuQXs_;;;/iJV;:bXaOHW?_//zfXxUn??,/dWxPC''ia/??bXaOHW.!/bfaFvo,;?GatGOgh'.;. " \
     ";xaWLNMyfNK?:bXaOHW?:_, PTuQXs_?GatGOgh'_;ghJ'.! KK'?? ?_KK'-PTuQXs/ /:PTuQXs!llbsUdRv;/;?dWxPC''ia; " \
     "uOsjpZaXN/:;_:xaWLNMyfNK-.:-?ghJ'/.!iJV   PTuQXs-; llbsUdRv,?!;QVLZI_ " \
     ";KK'_;?!zfXxUn?_?!dWxPC''ia;;?xaWLNMyfNK--_KK'-/,-ghJ'.;;_QVLZI KK'?-PTuQXs?:KK'!! " \
     ":xaWLNMyfNK;-uOsjpZaXN.;_xaWLNMyfNK_bfaFvo -.-GatGOgh'.__;zfXxUn-xaWLNMyfNK/:!bfaFvo/. ghJ'!_lGb;, " \
     "_!QVLZI.;ghJ';_:-:PTuQXs.KK':- -!ghJ'?;iJV., :-ghJ':_;-ghJ'_- ! bfaFvo !:uOsjpZaXN,,KK'-PTuQXs," \
     "; !;iJV?!aTMcju_?!_!iJV "
# Should be at least 21 ghj the problem is with _
tic = time.perf_counter()
r = top_3_words(t3)
print(r)
toc = time.perf_counter()
print(f"Time: {toc - tic:0.4f} seconds")



