"""
Add individual English meanings to each derivative (not just root meanings).
Uses exact lemmas from the data file.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Individual derivative meanings - using exact lemmas from data
DERIVATIVE_MEANINGS = {
    # Root: أله (God, deity) - Rank 1
    "اللَّه": "Allah, God",
    "إِلٰه": "god, deity",
    "اللَّهُمَّ": "O Allah",

    # Root: ربب - additional
    "رَبّانِيِّن": "godly scholars",
    "رِبِّيّ": "devoted to God",

    # Root: علم - additional
    "عَلَّمَ": "he taught",
    "يَتَعَلَّمُ": "he learns",
    "مُعَلَّم": "taught, marked",

    # Root: قوم - additional
    "قَيِّم": "upright, valuable",
    "قَيُّوم": "Self-Subsisting (Allah)",
    "قَيِّمَة": "upright (f.)",

    # Root: كفر - additional
    "كَفَّرَ": "he atoned for",

    # Root: بين - additional forms
    "بَيِّنَة": "clear proof",
    "بَيَّنُ": "he explained",
    "تَبَيَّنَ": "it became clear",
    "مُبَيِّنَة": "clarifying (f.)",
    "تَسْتَبِينَ": "it becomes clear",
    "تِبْيان": "clear exposition",
    "بَيِّن": "clear, evident",
    "مُسْتَبِين": "clearly shown",
    "يُبِينُ": "he clarifies",

    # Root: شيأ - additional
    "شَىْء": "thing",

    # Root: رسل - additional
    "مُرْسِل": "sender",
    "مُرْسِلَة": "sent (f.)",
    "مُرْسَلَة": "sent ones (f.)",

    # Root: سمو - additional
    "مُسَمًّى": "appointed, named",
    "سَمَّى": "he named",
    "تَسْمِيَة": "naming",

    # Root: كلل - additional
    "كُلَّما": "whenever",
    "كَلالَة": "without direct heirs",
    "كَلّ": "burden",

    # Root: عذب (to punish) - NEW
    "عَذاب": "punishment, torment",
    "عَذَّبَ": "he punished",
    "مُعَذِّب": "punisher",
    "مُعَذَّب": "punished one",
    "عَذْب": "fresh (water)",

    # Root: عمل - additional
    "عامِلَة": "working (f.)",

    # Root: رحم (mercy) - NEW
    "رَحِيم": "Most Merciful",
    "رَحْمَة": "mercy",
    "رَحْمٰن": "Most Gracious",
    "رَحِمَ": "he had mercy",
    "أَرْحام": "wombs, kinship",
    "راحِم": "merciful one",
    "أَرْحَم": "most merciful",
    "رُحْم": "mercy",
    "مَرْحَمَة": "mercy",

    # Root: أنس - additional
    "آنَسَ": "he perceived",
    "تَسْتَأْنِسُ": "you seek permission",
    "مُسْتَأْنِس": "one seeking permission",

    # Root: رأي - additional
    "أَرَيْ": "I showed",
    "رِئاء": "showing off",
    "رَأْى": "vision",
    "يُراءُ": "he shows off",
    "تَراءَتِ": "they saw each other",
    "رِءْي": "appearance",

    # Root: كتب (to write) - NEW
    "كِتاب": "book, scripture",
    "كَتَبَ": "he wrote",
    "كاتِب": "writer, scribe",
    "مَكْتُوب": "written",
    "كاتِبُ": "writer",
    "اكْتَتَبَ": "he had it written",
    "كِتابِي": "my record",

    # Root: هدي - additional
    "مُهْتَدي": "rightly guided",
    "أَهْدَى": "more guided",
    "هاد": "guide",
    "مُهْتَد": "guided one",
    "هَدِيَّة": "gift",

    # Root: ظلم - additional
    "ظُلُمَة": "darkness",
    "أَظْلَم": "more wrongful",
    "ظَلّام": "greatly unjust",
    "ظالِمَة": "wrongdoing (f.)",
    "ظالِمِي": "wrongdoers",
    "مُظْلِم": "dark",
    "ظَلُوم": "very unjust",
    "أَظْلَمَ": "it became dark",

    # Root: نفس - additional
    "تَنَفَّسَ": "it breathed/dawned",
    "يَتَنافَسِ": "they compete",
    "مُتَنافِس": "competitor",

    # Root: قبل - additional
    "تَقَبَّلَ": "he accepted",
    "يَقْبَلُ": "he accepts",
    "مُتَقابِل": "facing each other",
    "قَبِيل": "group, type",
    "قَبُول": "acceptance",
    "قابِل": "acceptor",
    "مُسْتَقْبِل": "one facing",
    "قَبائِل": "tribes",

    # Root: نزل - additional
    "نَزَّلَ": "he sent down",
    "تَنَزَّلَتْ": "they descended",
    "مُنزِل": "sender down",
    "مَنازِل": "stations, phases",
    "مُنَزِّل": "revealer",
    "مُنَزَّل": "revealed",
    "نَزْلَة": "descent",

    # Root: ذكر (to remember) - NEW
    "تَذَكَّرَ": "he remembered",
    "ذِكْرَى": "reminder",
    "ذُكِّرَ": "he was reminded",
    "ذَكَر": "male",
    "مُدَّكِر": "one who takes heed",
    "ذاكِر": "one who remembers",
    "تَذْكِير": "reminding",
    "ادَّكَرَ": "he remembered",
    "ذاكِرَة": "remembering (f.)",
    "مَذْكُور": "mentioned",
    "مُذَكِّر": "reminder, warner",
    "ذِكْر": "remembrance, mention",
    "ذَكَرَ": "he remembered",

    # Root: حقق - additional
    "حَقَّ": "it was true/due",
    "يُحِقَّ": "he establishes truth",
    "حاقَّة": "the Reality",
    "اسْتَحَقَّ": "he deserved",

    # Root: كذب - additional
    "كَذَّبَ": "he denied",
    "مُكَذِّب": "denier",
    "كَذَبَ": "he lied",
    "كَذّاب": "great liar",
    "كِذّاب": "great liar",
    "مَكْذُوب": "lied against",
    "تَكْذِيب": "denial",

    # Root: عبد - additional
    "عِبادَت": "acts of worship",
    "عَبَّد": "he enslaved",
    "عابِدَة": "worshipping (f.)",

    # Root: أخذ - additional
    "اتَّخَذَ": "he took, adopted",
    "يُؤاخِذُ": "he punishes",
    "آخِذ": "taker",
    "مُتَّخِذ": "one who takes",
    "اتِّخاذ": "taking, adopting",

    # Root: خلق - additional
    "خَلاق": "portion, character",
    "مُخَلَّقَة": "formed",
    "اخْتِلاق": "fabrication",

    # Root: وقي - additional
    "اتَّقَى": "he feared God",
    "مُتَّقي": "God-fearing",
    "وَقَى": "he protected",
    "تَقِيّ": "pious",
    "واق": "protector",
    "أَتْقَى": "most pious",
    "تُقاة": "precaution",

    # Root: أخر - additional
    "أَخَّرَ": "he delayed",
    "يَسْتَأْخِرُ": "he seeks delay",
    "تَأَخَّرَ": "he was delayed",

    # Root: أمر (to command) - NEW
    "أَمْر": "command, affair",
    "أَمَرَ": "he commanded",
    "يَأْتَمِرُ": "he conspires",
    "آمِر": "commander",
    "أَمّارَة": "constantly urging",
    "إِمْر": "grievous thing",

    # Root: بعد - additional
    "بَعُدَتْ": "it became far",
    "مُبْعَد": "kept far away",
    "باعِدْ": "keep far!",

    # Root: غفر (to forgive) - NEW
    "غَفُور": "Most Forgiving",
    "غَفَرَ": "he forgave",
    "اسْتَغْفَرَ": "he sought forgiveness",
    "مَغْفِرَة": "forgiveness",
    "غَفّار": "Oft-Forgiving",
    "غافِر": "forgiver",
    "غُفْران": "forgiveness",
    "مُسْتَغْفِر": "one seeking forgiveness",
    "اسْتِغْفار": "seeking forgiveness",

    # Root: ولي (guardian) - NEW
    "وَلِيّ": "guardian, protector",
    "تَوَلَّى": "he turned away",
    "وَلَّى": "he turned",
    "مَوْلَى": "master, protector",
    "أَوْلَى": "more entitled",
    "مَوالِي": "protectors",
    "وَلايَت": "guardianship",
    "مُوَلِّي": "one who turns",
    "أَوْلَيان": "more appropriate",
    "يَلُ": "he turns",
    "وال": "friend, protector",

    # Root: دعو - additional
    "دَعْوَى": "claim, lawsuit",
    "داع": "caller",
    "يَدَّعُ": "he claims",

    # Root: حكم (to judge) - NEW
    "حَكِيم": "All-Wise",
    "حَكَمَ": "he judged",
    "حُكْم": "judgment, ruling",
    "حِكْمَة": "wisdom",
    "حاكِم": "judge, ruler",
    "حَكَم": "arbiter",
    "مُحْكَمَة": "precise, clear",
    "يُحَكِّمُ": "he appoints as judge",
    "أُحْكِمَتْ": "made precise",
    "أَحْكَم": "most wise",
    "حُكّام": "rulers",
    "يَتَحاكَمُ": "they seek judgment",

    # Root: ملك (to possess) - NEW
    "مَلَك": "angel",
    "مُلْك": "kingdom, sovereignty",
    "مَلَكَتْ": "she possessed",
    "مَلِك": "king",
    "مالِك": "owner, master",
    "مَلَكُوت": "dominion",
    "مَمْلُوك": "owned, slave",
    "مَلْك": "property",
    "مَلِيك": "sovereign",

    # Root: جنن (garden, jinn) - NEW
    "جَنَّة": "garden, paradise",
    "جِنّ": "jinn",
    "مَجْنُون": "possessed, mad",
    "جِنَّة": "madness, jinn",
    "جانّ": "serpent, jinn",
    "جُنَّة": "shield, cover",
    "جَنَّ": "it became dark",
    "أَجِنَّة": "embryos",

    # Root: عند - additional
    "عَنِيد": "stubborn",

    # Root: خير - additional
    "خَيْرَة": "best",
    "اخْتارَ": "he chose",
    "خِيَرَة": "choice",
    "يَتَخَيَّرُ": "he selects",

    # Root: حسن (good, beautiful) - NEW
    "مُحْسِن": "doer of good",
    "أَحْسَن": "best, most beautiful",
    "حَسَنَة": "good deed",
    "أَحْسَنَ": "he did good",
    "حَسَن": "good, beautiful",
    "حُسْنَى": "best (f.)",
    "حُسْن": "beauty, goodness",
    "إِحْسان": "excellence, kindness",
    "حَسُنَ": "it was good",
    "حُسْنَيَيْن": "two best things",
    "مُحْسِنَة": "doer of good (f.)",

    # Root: قول (to say, speak) - Rank 2
    "قالَ": "he said",
    "قَوْل": "speech, word",
    "قائِل": "speaker, one who says",
    "قِيل": "it was said",
    "تَقَوَّلَ": "to fabricate (a saying)",
    "أَقاوِيل": "false sayings",

    # Root: كون (to be, exist) - Rank 3
    "كانَ": "he was, to be",
    "مَكان": "place, location",
    "مَكانَت": "position, status",

    # Root: ربب (lord, master) - Rank 4
    "رَبّ": "lord, master",
    "رَبّانِيِّن": "godly scholars",
    "رِبِّيّ": "devoted to God",
    "رَبائِب": "stepdaughters",

    # Root: أمن (to believe, be safe) - Rank 5
    "آمَنَ": "he believed",
    "مُؤْمِن": "believer",
    "إِيمان": "faith, belief",
    "مُؤْمِنَة": "believing woman",
    "أَمِنَ": "he was safe",
    "آمِن": "safe, secure",
    "أَمِين": "trustworthy",
    "أَمْن": "safety, security",
    "أَمانَة": "trust, trustworthiness",
    "أَمانَت": "trusts",
    "أَمَنَة": "security",
    "اؤْتُمِنَ": "he was entrusted",
    "مَأْمَن": "place of safety",
    "آمِنَة": "safe (f.)",
    "مَأْمُون": "trusted one",

    # Root: علم (to know) - Rank 6
    "عَلِمَ": "he knew",
    "عَلِيم": "All-Knowing",
    "عِلْم": "knowledge",
    "عالَم": "world, universe",
    "أَعْلَم": "more knowing",
    "عَلَّمَ": "he taught",
    "عالِم": "scholar, knower",
    "مَعْلُوم": "known",
    "عَلّام": "All-Knowing",
    "يَتَعَلَّمُ": "he learns",
    "مَعْلُومَة": "known (f.)",
    "أَعْلام": "banners, signs",
    "عَلامَة": "sign, mark",
    "مُعَلَّم": "taught, marked",

    # Root: قوم (to stand, establish) - Rank 7
    "قَوْم": "people, nation",
    "قِيامَة": "resurrection",
    "أَقامَ": "he established",
    "مُسْتَقِيم": "straight",
    "قامَ": "he stood",
    "قائِم": "standing, upright",
    "مَقام": "station, place",
    "مُقِيم": "resident, established",
    "اسْتَقامُ": "they were steadfast",
    "قائِمَة": "standing (f.)",
    "قَيِّم": "upright, valuable",
    "أَقْوَم": "more upright",
    "قَيُّوم": "Self-Subsisting",
    "قَوّام": "maintainers",
    "مُقام": "place of standing",
    "إِقام": "establishing",
    "قَيِّمَة": "upright (f.)",
    "قِيَم": "values",
    "إِقامَت": "establishing",
    "قَوام": "sustenance",
    "مُقامَة": "residence",
    "تَقْوِيم": "form, creation",

    # Root: أيي (sign, verse) - Rank 8
    "آيَة": "sign, verse",
    "أَيّ": "which, any",

    # Root: أتي (to come, bring) - Rank 9
    "آتَى": "he gave, brought",
    "أَتَى": "he came",
    "آتِي": "coming, one who brings",
    "إِيتاء": "giving",
    "مُؤْتي": "giver",
    "مَأْتِيّ": "coming (to be reached)",

    # Root: كفر (to disbelieve) - Rank 10
    "كَفَرَ": "he disbelieved",
    "كافِر": "disbeliever",
    "كُفْر": "disbelief",
    "كَفَّرَ": "he atoned",
    "كَفُور": "very ungrateful",
    "كَفّار": "persistent disbeliever",
    "كَفّارَة": "expiation",
    "كُفُور": "disbelief",
    "كافِرَة": "disbelieving (f.)",
    "كُفْران": "ingratitude",
    "كَوافِر": "disbelievers (f. pl.)",
    "كافُور": "camphor",
    "أَكْفَرَ": "more disbelieving",

    # Root: جعل (to make, place) - Rank 11
    "جَعَلَ": "he made, placed",
    "يَجْعَل": "he makes",
    "جاعِل": "maker",

    # Root: بين (between, clear) - Rank 12
    "بَيْن": "between",
    "بَيَّنَ": "he made clear",
    "مُبِين": "clear, manifest",
    "بَيِّنَة": "clear proof",
    "بَيِّن": "clear, evident",
    "تَبَيَّنَ": "it became clear",
    "بَيان": "explanation",

    # Root: جيأ (to come) - Rank 13
    "جاءَ": "he came",
    "مَجِيء": "coming, arrival",

    # Root: عمل (to do, work) - Rank 14
    "عَمِلَ": "he did, worked",
    "عَمَل": "deed, work",
    "عامِل": "worker, doer",

    # Root: شيأ (thing, to will) - Rank 15
    "شَيْء": "thing",
    "شاءَ": "he willed",
    "مَشِيئَة": "will",

    # Root: رأي (to see) - Rank 16
    "رَأَى": "he saw",
    "رَءا": "he saw",
    "أَرَى": "he showed",
    "رَأْي": "opinion, view",
    "رُءْيا": "vision, dream",
    "تَرَى": "you see",
    "يَرَى": "he sees",

    # Root: خلق (to create) - Rank 17
    "خَلَقَ": "he created",
    "خَلْق": "creation",
    "خالِق": "creator",
    "خَلّاق": "Supreme Creator",
    "خُلُق": "character",

    # Root: نزل (to send down) - Rank 18
    "نَزَّلَ": "he sent down",
    "أَنزَلَ": "he sent down",
    "نُزُل": "lodging, provision",
    "مُنَزَّل": "sent down",
    "تَنزِيل": "revelation",
    "نازِل": "descending",
    "مُنزَل": "sent down",

    # Root: دعو (to call, pray) - Rank 19
    "دَعا": "he called, prayed",
    "دُعاء": "supplication",
    "داعِي": "caller",
    "دَعْوَة": "call, invitation",
    "ادَّعَى": "he claimed",

    # Root: قبل (before, to accept) - Rank 20
    "قَبْل": "before",
    "قَبِلَ": "he accepted",
    "أَقْبَلَ": "he approached",
    "قِبَل": "from, direction",
    "مُقْبِل": "approaching",
    "قِبْلَة": "prayer direction",
    "اسْتَقْبَلَ": "he faced",
    "قُبُل": "front",

    # Root: يوم (day) - Rank 21
    "يَوْم": "day",

    # Root: ذلك (that) - Rank 22
    "ذٰلِكَ": "that",

    # Root: هدي (to guide) - Rank 23
    "هَدَى": "he guided",
    "هُدًى": "guidance",
    "هادِي": "guide",
    "مُهْتَدِي": "rightly guided",
    "اهْتَدَى": "he was guided",
    "هَدِيَّة": "gift",
    "هَدْي": "sacrifice",

    # Root: كذب (to deny, lie) - Rank 24
    "كَذَّبَ": "he denied",
    "كَذِب": "lie",
    "كاذِب": "liar",
    "مُكَذِّب": "denier",
    "كِذَّاب": "great liar",
    "أَكْذَبَ": "he proved a liar",

    # Root: وقي (to fear God) - Rank 25
    "اتَّقَى": "he feared God",
    "تَقْوَى": "piety",
    "مُتَّقِي": "God-fearing",
    "وِقايَة": "protection",

    # Root: أرض (earth, land) - Rank 26
    "أَرْض": "earth, land",

    # Root: سمو (sky, heaven, name) - Rank 27
    "سَماء": "sky, heaven",
    "سَمّى": "he named",
    "اسْم": "name",
    "مُسَمًّى": "appointed, named",
    "سَمِيّ": "namesake",

    # Root: رود (to want) - Rank 28
    "أَرادَ": "he wanted",
    "يُرِيد": "he wants",
    "إِرادَة": "will, intention",
    "مُراد": "intended",
    "راوَدَ": "he tried to seduce",

    # Root: نفس (soul, self) - Rank 29
    "نَفْس": "soul, self",
    "أَنفُس": "souls",
    "تَنَفَّسَ": "he breathed",

    # Root: كلل (all, every) - Rank 30
    "كُلّ": "all, every",

    # Root: تبع (to follow) - Rank 31
    "اتَّبَعَ": "he followed",
    "تَبِعَ": "he followed",
    "تابِع": "follower",
    "تَبَع": "followers",
    "اتَّبِع": "follow!",

    # Root: أنس (human) - Rank 32
    "إِنسان": "human being",
    "ناس": "people, mankind",
    "إِنس": "humans",
    "أُناس": "people",
    "إِنسِيّ": "human",

    # Root: حقق (truth, right) - Rank 33
    "حَقّ": "truth, right",
    "حَقِيق": "worthy",
    "حَقَّ": "it was due",
    "أَحَقّ": "more deserving",
    "حاقَّ": "he argued",

    # Root: رسل (messenger) - Rank 34
    "رَسُول": "messenger",
    "أَرْسَلَ": "he sent",
    "رِسالَة": "message",
    "مُرْسَل": "sent one",

    # Root: أخذ (to take) - Rank 35
    "أَخَذَ": "he took",
    "اتَّخَذَ": "he took, adopted",
    "أَخْذ": "taking",
    "يَأْخُذ": "he takes",
    "مُؤاخَذَة": "punishment",

    # Root: عبد (to worship) - Rank 36
    "عَبَدَ": "he worshipped",
    "عَبْد": "servant, slave",
    "عِبادَة": "worship",
    "عابِد": "worshipper",
    "مَعْبُود": "one worshipped",

    # Root: أخر (other, last) - Rank 37
    "آخَر": "other",
    "أُخْرَى": "other (f.)",
    "آخِرَة": "hereafter",
    "آخِر": "last",
    "أَخَّرَ": "he delayed",
    "تَأَخَّرَ": "he was delayed",
    "مُؤَخَّر": "postponed",
    "مُسْتَأْخِر": "seeking delay",

    # Root: ظلم (to wrong) - Rank 38
    "ظَلَمَ": "he wronged",
    "ظُلْم": "injustice",
    "ظالِم": "wrongdoer",
    "مَظْلُوم": "oppressed",
    "ظُلُمات": "darkness",
    "ظَلام": "darkness",

    # Root: بعد (after) - Rank 39
    "بَعْد": "after",
    "بَعِيد": "far",
    "أَبْعَد": "farther",
    "بُعْد": "distance",

    # Root: سأل (to ask) - Rank 40
    "سَأَلَ": "he asked",
    "سُؤال": "question",
    "سائِل": "questioner",
    "مَسْئُول": "responsible",

    # Root: وجد (to find) - Rank 41
    "وَجَدَ": "he found",
    "يَجِد": "he finds",
    "وُجُود": "existence",
    "واجِد": "finder",
    "مَوْجُود": "found, existing",

    # Root: عند (at, with) - Rank 42
    "عِنْدَ": "at, with",

    # Root: خرج (to go out) - Rank 43
    "خَرَجَ": "he went out",
    "أَخْرَجَ": "he brought out",
    "خُرُوج": "exit",
    "مُخْرَج": "exit, output",
    "إِخْراج": "expulsion",
    "خارِج": "outside",

    # Root: خير (good) - Rank 44
    "خَيْر": "good, better",
    "خَيْرات": "good things",
    "اخْتَرْنا": "we chose",

    # Root: أكل (to eat) - Rank 45
    "أَكَلَ": "he ate",
    "أَكْل": "eating",
    "آكِل": "eater",
    "أُكُل": "fruit",
    "مَأْكُول": "eaten",

    # Root: ليس (not to be) - Rank 46
    "لَيْسَ": "is not",

    # Root: نور (light) - Rank 47
    "نُور": "light",
    "نار": "fire",
    "أَنار": "he illuminated",
    "مُنِير": "illuminating",

    # Root: فعل (to do) - Rank 48
    "فَعَلَ": "he did",
    "فِعْل": "action",
    "فاعِل": "doer",
    "مَفْعُول": "done to",
    "يَفْعَل": "he does",

    # Root: سبل (way) - Rank 49
    "سَبِيل": "way, path",
    "سُبُل": "ways",

    # Root: نظر (to look) - Rank 50
    "نَظَرَ": "he looked",
    "نَظَر": "look, sight",
    "ناظِر": "observer",
    "مَنظَر": "view",
    "انتَظَرَ": "he waited",
    "ناظِرَة": "looking at",
}

def main():
    script_dir = Path(__file__).parent

    # Load current app data
    with open(script_dir / 'app_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Update derivatives with individual meanings
    updated_derivatives = 0
    updated_roots = 0

    for root in data['roots']:
        root_updated = False
        for deriv in root['derivatives']:
            lemma = deriv['lemma']
            if lemma in DERIVATIVE_MEANINGS:
                deriv['meaning'] = DERIVATIVE_MEANINGS[lemma]
                updated_derivatives += 1
                root_updated = True
        if root_updated:
            updated_roots += 1

    print(f"Updated {updated_derivatives} derivatives across {updated_roots} roots")

    # Save updated data
    with open(script_dir / 'app_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Saved updated app_data.json")

    # Show sample
    print("\nSample output (first 5 roots):")
    for root in data['roots'][:5]:
        print(f"\n=== {root['root']} ({root['meaning']}) ===")
        for d in root['derivatives'][:5]:
            meaning = d.get('meaning', '—')
            vf = f"Form {d['verb_form']}" if d.get('verb_form') else d['pos']
            print(f"  {d['lemma']}: {meaning} [{vf}]")

if __name__ == '__main__':
    main()
