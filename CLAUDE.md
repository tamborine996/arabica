# Arabica - Quranic Arabic Vocabulary App

## Project Overview
A root-based flashcard learning app for Quranic Arabic vocabulary. Learn 1,651 roots covering the complete Quran.

## Deployment
- **Live URL**: https://tamborine996.github.io/arabica/
- **Repository**: https://github.com/tamborine996/arabica
- **Hosting**: GitHub Pages (master branch, root directory)

## Tech Stack
- Pure HTML/CSS/JavaScript (no build step)
- Amiri font for Arabic text
- localStorage for progress persistence

## Data Sources
- **Quranic Arabic Corpus** morphology data (GNU license)
- Processed via Python scripts in `data/`

## Key Files
- `index.html` - Main app structure
- `styles.css` - Warm educational theme
- `app.js` - Flashcard logic, progress tracking
- `data/app_data.json` - 1,651 roots with derivatives and meanings
- `data/add_derivative_meanings.py` - Script for adding individual word meanings
- `data/fix_remaining_meanings.py` - Script for fixing remaining meanings

## Features
- Frequency-based packs (Top 50/100/200/500/All)
- Switchable test direction (Arabic→English / English→Arabic)
- **Individual derivative meanings** with verb form labels (Form I-X)
- Tricky item review
- Keyboard shortcuts (Space, arrows)

## Data Coverage
- **Root meanings**: 427/1,651 roots have English meanings
- **Top 50 roots**: 100% coverage (both root and derivative meanings)
- **Derivative meanings**: 370+ individual word meanings for top 50 roots

## Future Enhancements
- [ ] Add English meanings for remaining 1,200+ roots
- [ ] Printable PDF reference sheet
- [ ] Audio pronunciation
- [ ] Spaced repetition algorithm
