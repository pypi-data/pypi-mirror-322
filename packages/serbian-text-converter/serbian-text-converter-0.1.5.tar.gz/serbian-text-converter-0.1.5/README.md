# Serbian Text Converter

A Python utility for converting Serbian text between Cyrillic and Latin scripts, and generating URL-friendly slugs.

## Installation

```bash
pip install serbian-text-converter
```

## Usage

from serbian_text_converter import SerbianTextConverter

### Convert to Latin
print(SerbianTextConverter.to_latin("Љубав"))  # Output: Ljubav

### Convert to Cyrillic
print(SerbianTextConverter.to_cyrillic("Ljubav"))  # Output: Љубав

### Normalize for URLs
print(SerbianTextConverter.normalize("Љубав и Живот"))  # Output: ljubav-i-zivot