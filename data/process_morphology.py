"""
Process quran-morphology.txt into a root-organized JSON structure for the Arabica app.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

def parse_morphology_line(line):
    """Parse a single line from quran-morphology.txt"""
    parts = line.strip().split('\t')
    if len(parts) < 3:
        return None

    location = parts[0]  # e.g., "1:1:3:2"
    arabic = parts[1]
    pos = parts[2]  # N, V, P

    # Parse the annotation field
    annotations = parts[3] if len(parts) > 3 else ""

    # Extract root
    root_match = re.search(r'ROOT:([^\|]+)', annotations)
    root = root_match.group(1) if root_match else None

    # Extract lemma
    lemma_match = re.search(r'LEM:([^\|]+)', annotations)
    lemma = lemma_match.group(1) if lemma_match else None

    # Extract verb form (VF:1 through VF:10)
    vf_match = re.search(r'VF:(\d+)', annotations)
    verb_form = int(vf_match.group(1)) if vf_match else None

    # Extract grammatical features
    features = {
        'gender': 'M' if '|M|' in annotations or annotations.startswith('M|') else ('F' if '|F|' in annotations else None),
        'number': None,
        'case': None,
        'is_verb': pos == 'V',
        'is_noun': pos == 'N',
        'is_particle': pos == 'P',
    }

    # Number
    if 'MP' in annotations or '|MP|' in annotations:
        features['number'] = 'plural_m'
    elif 'FP' in annotations or '|FP|' in annotations:
        features['number'] = 'plural_f'
    elif 'MD' in annotations or '|MD|' in annotations:
        features['number'] = 'dual_m'
    elif 'FD' in annotations or '|FD|' in annotations:
        features['number'] = 'dual_f'
    elif 'MS' in annotations or '|MS|' in annotations:
        features['number'] = 'singular_m'
    elif 'FS' in annotations or '|FS|' in annotations:
        features['number'] = 'singular_f'

    # Case
    if '|NOM' in annotations:
        features['case'] = 'nominative'
    elif '|ACC' in annotations:
        features['case'] = 'accusative'
    elif '|GEN' in annotations:
        features['case'] = 'genitive'

    # Verb tense
    if 'PERF' in annotations:
        features['tense'] = 'perfect'
    elif 'IMPF' in annotations:
        features['tense'] = 'imperfect'
    elif 'IMPV' in annotations:
        features['tense'] = 'imperative'

    # Participles
    if 'ACT_PCPL' in annotations:
        features['participle'] = 'active'
    elif 'PASS_PCPL' in annotations:
        features['participle'] = 'passive'

    # Parse location
    loc_parts = location.split(':')
    surah = int(loc_parts[0]) if loc_parts else None
    ayah = int(loc_parts[1]) if len(loc_parts) > 1 else None

    return {
        'location': location,
        'surah': surah,
        'ayah': ayah,
        'arabic': arabic,
        'pos': pos,
        'root': root,
        'lemma': lemma,
        'verb_form': verb_form,
        'features': features,
        'raw_annotations': annotations
    }

def build_root_index(morphology_file):
    """Build a root-organized index from the morphology data"""
    roots = defaultdict(lambda: {
        'root': None,
        'derivatives': defaultdict(lambda: {
            'lemma': None,
            'arabic_forms': set(),
            'pos': None,
            'verb_form': None,
            'frequency': 0,
            'example_locations': []
        })
    })

    # Also track lemma frequencies directly
    lemma_freq = defaultdict(int)

    with open(morphology_file, 'r', encoding='utf-8') as f:
        for line in f:
            parsed = parse_morphology_line(line)
            if not parsed or not parsed['root']:
                continue

            root = parsed['root']
            lemma = parsed['lemma'] or parsed['arabic']

            roots[root]['root'] = root

            deriv = roots[root]['derivatives'][lemma]
            deriv['lemma'] = lemma
            deriv['arabic_forms'].add(parsed['arabic'])
            deriv['frequency'] += 1
            deriv['pos'] = parsed['pos']
            if parsed['verb_form']:
                deriv['verb_form'] = parsed['verb_form']

            # Keep up to 3 example locations
            if len(deriv['example_locations']) < 3:
                loc = f"{parsed['surah']}:{parsed['ayah']}"
                if loc not in deriv['example_locations']:
                    deriv['example_locations'].append(loc)

            lemma_freq[lemma] += 1

    return roots, lemma_freq

def convert_to_serializable(roots, lemma_freq):
    """Convert the root index to a JSON-serializable format"""
    result = []

    for root_key in sorted(roots.keys()):
        root_data = roots[root_key]

        derivatives = []
        for lemma_key, deriv in root_data['derivatives'].items():
            derivatives.append({
                'lemma': deriv['lemma'],
                'arabic_forms': sorted(list(deriv['arabic_forms'])),
                'pos': deriv['pos'],
                'verb_form': deriv['verb_form'],
                'frequency': deriv['frequency'],
                'example_locations': deriv['example_locations']
            })

        # Sort derivatives by frequency (most common first)
        derivatives.sort(key=lambda x: -x['frequency'])

        # Calculate total frequency for this root
        total_freq = sum(d['frequency'] for d in derivatives)

        result.append({
            'root': root_key,
            'total_frequency': total_freq,
            'derivative_count': len(derivatives),
            'derivatives': derivatives
        })

    # Sort roots by total frequency
    result.sort(key=lambda x: -x['total_frequency'])

    # Add frequency rank
    for i, root in enumerate(result):
        root['frequency_rank'] = i + 1

    return result

def main():
    script_dir = Path(__file__).parent
    morphology_file = script_dir / 'quran-morphology.txt'
    output_file = script_dir / 'roots.json'

    print("Processing morphology data...")
    roots, lemma_freq = build_root_index(morphology_file)

    print(f"Found {len(roots)} unique roots")

    result = convert_to_serializable(roots, lemma_freq)

    # Calculate some stats
    total_derivatives = sum(r['derivative_count'] for r in result)
    total_occurrences = sum(r['total_frequency'] for r in result)

    print(f"Total derivatives: {total_derivatives}")
    print(f"Total word occurrences: {total_occurrences}")

    # Show top 10 roots (safe print for Windows console)
    print("\nTop 10 most frequent roots:")
    for i, root in enumerate(result[:10]):
        try:
            print(f"  {i+1}. {root['root']} - {root['total_frequency']} occurrences, {root['derivative_count']} derivatives")
        except UnicodeEncodeError:
            print(f"  {i+1}. [root] - {root['total_frequency']} occurrences, {root['derivative_count']} derivatives")

    # Save to JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\nSaved to {output_file}")

    # Also create a summary file
    summary = {
        'total_roots': len(result),
        'total_derivatives': total_derivatives,
        'total_occurrences': total_occurrences,
        'top_100_roots': [{'root': r['root'], 'frequency': r['total_frequency']} for r in result[:100]]
    }

    summary_file = script_dir / 'roots_summary.json'
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"Saved summary to {summary_file}")

if __name__ == '__main__':
    main()
