"""
Fix remaining derivative meanings by directly modifying data.
"""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

def main():
    script_dir = Path(__file__).parent

    # Load current app data
    with open(script_dir / 'app_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Directly assign meanings based on root and derivative index
    # This ensures exact matching
    meaning_assignments = {
        # (root, derivative_lemma): meaning
        # We'll build this from the data
    }

    # Process each root in top 50 and assign meanings
    updated = 0
    for root in data['roots'][:50]:
        root_str = root['root']
        for d in root['derivatives']:
            if d.get('meaning'):
                continue

            lemma = d['lemma']

            # Assign based on root and patterns
            meaning = None

            if root_str == 'أله':
                if lemma == root['derivatives'][0]['lemma']:  # First = Allah
                    meaning = "Allah, God"
                elif 'م' in lemma:  # O Allah
                    meaning = "O Allah"

            elif root_str == 'قول':
                if d.get('verb_form') == 5:  # Form V
                    meaning = "to fabricate (a saying)"

            elif root_str == 'ربب':
                if 'ان' in lemma:
                    meaning = "godly scholars"
                elif 'ربّي' in lemma.lower() or 'رِب' in lemma:
                    meaning = "devoted to God"

            elif root_str == 'علم':
                if d.get('verb_form') == 2:
                    meaning = "he taught"
                elif d.get('verb_form') == 5:
                    meaning = "he learns"
                elif 'مُع' in lemma:
                    meaning = "taught, marked"

            elif root_str == 'قوم':
                if d['pos'] == 'N' and 'قَيّ' in lemma or 'قَيِّ' in lemma:
                    if 'وم' in lemma:
                        meaning = "Self-Subsisting (Allah)"
                    elif lemma.endswith('ة'):
                        meaning = "upright (f.)"
                    else:
                        meaning = "upright, valuable"

            elif root_str == 'كفر':
                if d.get('verb_form') == 2:
                    meaning = "he atoned for"

            elif root_str == 'بين':
                if d['pos'] == 'N':
                    if lemma.endswith('ة'):
                        meaning = "clear proof"
                    else:
                        meaning = "clear, evident"
                elif d.get('verb_form') == 2:
                    meaning = "he made clear"
                elif d.get('verb_form') == 5:
                    meaning = "it became clear"
                elif d.get('verb_form') == 4:
                    meaning = "clarifying"

            elif root_str == 'سمو':
                if d['pos'] == 'N' and 'مُس' in lemma:
                    meaning = "appointed, named"
                elif d.get('verb_form') == 2:
                    meaning = "he named"

            elif root_str == 'كلل':
                if 'ما' in lemma:
                    meaning = "whenever"

            elif root_str == 'عذب':
                if d.get('verb_form') == 2:
                    meaning = "he punished"
                elif d['pos'] == 'N' and 'مُعَ' in lemma:
                    if 'ذِّب' in lemma:
                        meaning = "punisher"
                    else:
                        meaning = "punished one"

            elif root_str == 'هدي':
                if 'يَّة' in lemma:
                    meaning = "gift"

            elif root_str == 'نفس':
                if d.get('verb_form') == 5:
                    meaning = "it breathed/dawned"

            elif root_str == 'قبل':
                if d.get('verb_form') == 5:
                    meaning = "he accepted"

            elif root_str == 'نزل':
                if d.get('verb_form') == 2:
                    if d['pos'] == 'V':
                        meaning = "he sent down"
                    elif 'مُنَزِّ' in lemma:
                        meaning = "revealer"
                    else:
                        meaning = "revealed"
                elif d.get('verb_form') == 5:
                    meaning = "they descended"

            elif root_str == 'ذكر':
                if d.get('verb_form') == 5:
                    meaning = "he remembered"
                elif d.get('verb_form') == 2:
                    if d['pos'] == 'V':
                        meaning = "he was reminded"
                    else:
                        meaning = "reminder, warner"
                elif d.get('verb_form') == 8:
                    meaning = "he remembered"
                elif 'مُدّ' in lemma:
                    meaning = "one who takes heed"

            elif root_str == 'حقق':
                if d['pos'] == 'V' and d.get('verb_form') == 1:
                    meaning = "it was true/due"
                elif d.get('verb_form') == 4:
                    meaning = "he establishes truth"
                elif d.get('verb_form') == 10:
                    meaning = "he deserved"
                elif 'حاقَّ' in lemma:
                    meaning = "the Reality"

            elif root_str == 'كذب':
                if d.get('verb_form') == 2:
                    if d['pos'] == 'V':
                        meaning = "he denied"
                    else:
                        meaning = "denier"

            elif root_str == 'عبد':
                if d.get('verb_form') == 2:
                    meaning = "he enslaved"

            elif root_str == 'أخذ':
                if d.get('verb_form') == 8:
                    if d['pos'] == 'V':
                        meaning = "he took, adopted"
                    elif 'مُتّ' in lemma:
                        meaning = "one who takes"
                    else:
                        meaning = "taking, adopting"

            elif root_str == 'خلق':
                if 'مُخَ' in lemma and 'لَّق' in lemma:
                    meaning = "formed"

            elif root_str == 'وقي':
                if d.get('verb_form') == 8:
                    if d['pos'] == 'V':
                        meaning = "he feared God"
                    else:
                        meaning = "God-fearing"

            elif root_str == 'أخر':
                if d.get('verb_form') == 2:
                    meaning = "he delayed"
                elif d.get('verb_form') == 5:
                    meaning = "he was delayed"

            elif root_str == 'ولي':
                if d.get('verb_form') == 5:
                    meaning = "he turned away"
                elif d.get('verb_form') == 2:
                    if d['pos'] == 'V':
                        meaning = "he turned"
                    else:
                        meaning = "one who turns"

            elif root_str == 'دعو':
                if d.get('verb_form') == 8:
                    meaning = "he claims"

            elif root_str == 'حكم':
                if d.get('verb_form') == 2:
                    meaning = "he appoints as judge"

            elif root_str == 'جنن':
                if d['pos'] == 'N':
                    if 'جَنَّة' in lemma:
                        meaning = "garden, paradise"
                    elif 'جِنَّة' in lemma:
                        meaning = "madness, jinn"
                    elif 'جُنَّة' in lemma:
                        meaning = "shield, cover"
                    elif 'أَجِ' in lemma:
                        meaning = "embryos"
                elif d['pos'] == 'V':
                    meaning = "it became dark"

            elif root_str == 'خير':
                if d.get('verb_form') == 5:
                    meaning = "he selects"

            if meaning:
                d['meaning'] = meaning
                updated += 1

    print(f"Updated {updated} derivatives")

    # Count coverage
    with_meaning = 0
    without_meaning = 0
    for root in data['roots'][:50]:
        for d in root['derivatives']:
            if d.get('meaning'):
                with_meaning += 1
            else:
                without_meaning += 1

    print(f"Top 50 roots: {with_meaning} with meaning, {without_meaning} without")

    # Save
    with open(script_dir / 'app_data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print("Saved updated app_data.json")

    # Show remaining
    if without_meaning > 0:
        print("\nRemaining without meanings:")
        for root in data['roots'][:50]:
            for d in root['derivatives']:
                if not d.get('meaning'):
                    print(f"  {root['root']}: {d['lemma']} [VF={d.get('verb_form')}, POS={d['pos']}]")

if __name__ == '__main__':
    main()
