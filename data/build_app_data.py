"""
Build the final app data by merging roots.json with meanings.
Creates the flashcard-ready data structure.
"""
import json
from pathlib import Path

def main():
    script_dir = Path(__file__).parent

    # Load roots data
    with open(script_dir / 'roots.json', 'r', encoding='utf-8') as f:
        roots = json.load(f)

    # Load meanings
    with open(script_dir / 'root_meanings.json', 'r', encoding='utf-8') as f:
        meanings = json.load(f)

    # Build flashcard data
    flashcards = []
    roots_with_meanings = 0

    for root in roots:
        root_key = root['root']
        meaning_data = meanings.get(root_key, {})

        if meaning_data:
            roots_with_meanings += 1

        root_entry = {
            'root': root_key,
            'meaning': meaning_data.get('meaning', ''),
            'core_meaning': meaning_data.get('core', ''),
            'total_frequency': root['total_frequency'],
            'frequency_rank': root['frequency_rank'],
            'derivatives': []
        }

        for deriv in root['derivatives']:
            deriv_entry = {
                'lemma': deriv['lemma'],
                'arabic_forms': deriv['arabic_forms'][:5],  # Limit forms shown
                'pos': deriv['pos'],
                'verb_form': deriv['verb_form'],
                'frequency': deriv['frequency'],
                'examples': deriv['example_locations']
            }
            root_entry['derivatives'].append(deriv_entry)

        flashcards.append(root_entry)

    print(f"Processed {len(flashcards)} roots")
    print(f"Roots with meanings: {roots_with_meanings}")

    # Create frequency-based packs
    packs = {
        'top_50': [],
        'top_100': [],
        'top_200': [],
        'top_500': [],
        'all': []
    }

    for root in flashcards:
        rank = root['frequency_rank']
        packs['all'].append(root)
        if rank <= 500:
            packs['top_500'].append(root)
        if rank <= 200:
            packs['top_200'].append(root)
        if rank <= 100:
            packs['top_100'].append(root)
        if rank <= 50:
            packs['top_50'].append(root)

    # Also create derivative-level flashcards (individual words)
    word_cards = []
    for root in flashcards:
        for deriv in root['derivatives']:
            word_cards.append({
                'root': root['root'],
                'root_meaning': root['meaning'],
                'lemma': deriv['lemma'],
                'pos': 'verb' if deriv['pos'] == 'V' else ('noun' if deriv['pos'] == 'N' else 'particle'),
                'verb_form': deriv['verb_form'],
                'frequency': deriv['frequency'],
                'examples': deriv['examples'],
                'root_rank': root['frequency_rank']
            })

    # Sort word cards by frequency
    word_cards.sort(key=lambda x: -x['frequency'])

    # Add word rank
    for i, card in enumerate(word_cards):
        card['word_rank'] = i + 1

    # Save outputs
    output = {
        'roots': flashcards,
        'packs': {
            'top_50': {'name': 'Top 50 Roots', 'description': 'Most frequent roots - covers ~40% of Quran', 'count': len(packs['top_50'])},
            'top_100': {'name': 'Top 100 Roots', 'description': 'Covers ~55% of Quran', 'count': len(packs['top_100'])},
            'top_200': {'name': 'Top 200 Roots', 'description': 'Covers ~70% of Quran', 'count': len(packs['top_200'])},
            'top_500': {'name': 'Top 500 Roots', 'description': 'Covers ~85% of Quran', 'count': len(packs['top_500'])},
            'all': {'name': 'All Roots', 'description': f'Complete vocabulary - {len(packs["all"])} roots', 'count': len(packs['all'])}
        },
        'stats': {
            'total_roots': len(flashcards),
            'total_derivatives': sum(len(r['derivatives']) for r in flashcards),
            'roots_with_meanings': roots_with_meanings
        }
    }

    with open(script_dir / 'app_data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Saved app_data.json")

    # Save word cards separately (larger file)
    with open(script_dir / 'word_cards.json', 'w', encoding='utf-8') as f:
        json.dump({'words': word_cards[:1000], 'total': len(word_cards)}, f, ensure_ascii=False, indent=2)

    print(f"Saved word_cards.json (top 1000 of {len(word_cards)} words)")

    # Print pack stats
    print("\nPack statistics:")
    for pack_id, pack_info in output['packs'].items():
        print(f"  {pack_info['name']}: {pack_info['count']} roots")

if __name__ == '__main__':
    main()
