"""
Fill in missing meanings for top roots
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Additional meanings for roots that don't have them yet
ADDITIONAL_MEANINGS = {
    # Missing from top 200
    "أجر": "reward, wage",
    "شدد": "to be severe, strengthen",
    "دين": "religion, judgment day",
    "صحب": "companion, friend",
    "أخو": "brother",
    "ليل": "night",
    "شطن": "Satan, devil",
    "خلد": "eternal, to abide forever",
    "مول": "wealth, property",
    "أحد": "one, anyone",
    "كيف": "how",
    "زوج": "spouse, pair",
    "عقب": "to follow, consequence",
    "وجه": "face, direction",
    "قلل": "few, little",
    "ألم": "pain, suffering",
    "بيت": "house, home",
    "رجل": "man, foot",
    "يمن": "right hand, oath",
    "وكل": "to trust, rely on",
    "سور": "wall, surah",
    "حدث": "to speak, event",
    "جهنم": "hell",
    "فوق": "above, over",
    "خطأ": "sin, mistake",
    "صلو": "prayer, to pray",
    "تحت": "under, below",
    "زمن": "time",
    "حول": "around, to change",
    "عمر": "life, to live long",
    "نعم": "blessing, favor",
    "ثمر": "fruit",
    "حرر": "free, hot",
    "صغر": "small, young",
    "حسب": "to reckon, account",
    "فرق": "to divide, group",
    "حفظ": "to guard, memorize",
    "نكر": "to deny, unknown",
    "سفل": "low, beneath",
    "شرر": "evil, spark",
    "ميت": "dead",
    "أثم": "sin, crime",
    "عرب": "Arab, Arabic",
    "نهر": "river, day",
    "جبل": "mountain",
    "بحر": "sea, ocean",
    "صوم": "fasting",
    "حج": "pilgrimage",
    "زكو": "charity, purity",
    "ربو": "to grow, usury",
    "حلم": "dream, forbearance",
    "صبح": "morning",
    "مسو": "evening",
    "فجر": "dawn, to break forth",
    "ضحو": "forenoon",
    "عشو": "evening, dinner",
    "قمر": "moon",
    "شمس": "sun",
    "نجم": "star",
    "سحر": "magic, pre-dawn",
    "ملأ": "to fill, assembly",
    "فوز": "success, triumph",
    "خسر": "loss, to lose",
    "حزب": "party, group",
    "طعم": "food, taste",
    "شفع": "intercession",
    "ذنب": "sin, tail",
    "عفف": "chastity",
    "صفو": "pure, sincere",
    "وصف": "to describe",
    "حبس": "to imprison",
    "فتح": "to open, victory",
    "غلق": "to close",
    "بيع": "sale, to sell",
    "شهر": "month, famous",
    "سنن": "year, way",
    "أسبوع": "week",
    "طير": "bird",
    "حيوان": "animal",
    "سمك": "fish",
    "بقر": "cow",
    "غنم": "sheep",
    "جمل": "camel",
    "كلب": "dog",
    "خنزير": "pig",
    "فيل": "elephant",
    "نمل": "ant",
    "نحل": "bee",
    "عنكبوت": "spider",
    "حوت": "whale",
    "ذبب": "fly",
    "بعوض": "mosquito",
    "غراب": "crow",
    "هدهد": "hoopoe",
    "حمم": "dove",
    "تفح": "apple",
    "عنب": "grape",
    "تين": "fig",
    "زيتون": "olive",
    "نخل": "palm tree, date",
    "رمن": "pomegranate",
    "بصل": "onion",
    "ثوم": "garlic",
    "حنط": "wheat",
    "شعر": "barley, hair, poetry",
    "ماء": "water",
    "نار": "fire",
    "ريح": "wind",
    "ترب": "soil, dust",
    "حجر": "stone",
    "حديد": "iron",
    "ذهب": "gold, to go",
    "فضض": "silver",
    "نحس": "copper, unlucky",
    "لؤلؤ": "pearl",
    "مرجان": "coral",
    "ياقوت": "ruby",
    "كوكب": "planet, star",
    "سيء": "bad, evil",
    "طيب": "good, pleasant",
    "صعب": "difficult",
    "سهل": "easy",
    "ثقل": "heavy",
    "خفف": "light",
    "قرب": "near",
    "بعيد": "far",
    "سرع": "fast, quick",
    "بطء": "slow",
    "جديد": "new",
    "قدم": "old, foot",
    "حر": "hot, free",
    "برد": "cold",
    "يبس": "dry",
    "رطب": "wet, fresh dates",
    "صحح": "correct, healthy",
    "مرض": "sick, disease",
    "حلو": "sweet",
    "مرر": "bitter",
    "حمض": "sour",
    "ملح": "salt",
    "أبيض": "white",
    "أسود": "black",
    "أحمر": "red",
    "أخضر": "green",
    "أزرق": "blue",
    "أصفر": "yellow",
}

def main():
    script_dir = Path(__file__).parent

    # Load current app data
    with open(script_dir / 'app_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Update roots
    updated = 0
    for root in data['roots']:
        root_key = root['root']
        if not root['meaning'] and root_key in ADDITIONAL_MEANINGS:
            root['meaning'] = ADDITIONAL_MEANINGS[root_key]
            root['core_meaning'] = ADDITIONAL_MEANINGS[root_key].split(',')[0].strip()
            updated += 1

    # Count results
    with_meaning = sum(1 for r in data['roots'] if r['meaning'])
    without_meaning = sum(1 for r in data['roots'] if not r['meaning'])

    print(f"Updated {updated} roots with meanings")
    print(f"Total with meaning: {with_meaning}")
    print(f"Total without meaning: {without_meaning}")

    # Save
    with open(script_dir / 'app_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Saved updated app_data.json")

    # Show top 50 coverage
    print("\nTop 50 roots coverage:")
    top50 = data['roots'][:50]
    with_meaning_50 = sum(1 for r in top50 if r['meaning'])
    print(f"  {with_meaning_50}/50 have meanings")

    if with_meaning_50 < 50:
        print("  Missing meanings for:")
        for r in top50:
            if not r['meaning']:
                print(f"    rank {r['frequency_rank']}: {r['root']}")

if __name__ == '__main__':
    main()
