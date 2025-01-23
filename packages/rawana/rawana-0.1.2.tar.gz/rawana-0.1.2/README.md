# Rawana Python Package

The `rawana` Python package provides a comprehensive exploration of Rawana, the powerful demon king from the *Ramayana*, along with his legendary supernatural abilities. This package gives you an insightful look into Rawana's extraordinary powers and the key stories from his life. Perfect for mythology enthusiasts, scholars, and anyone interested in exploring one of Hinduism's most complex characters.

## Features
- **Powers:** Learn about Rawana's vast and diverse powers, ranging from immortality and strength to control over elements and time.
- **Stories:** Discover the key stories from Rawana's life, including his origin, penance, battle with gods, and ultimate downfall in the *Ramayana*.
- **Interactive Usage:** Easily access and explore Rawana's powers and stories through simple Python functions.

## Installation

You can install the `rawana` package using pip:

```bash
pip install rawana
```

## Usage

Once installed, you can start exploring Rawana's abilities and stories with ease. Here's how to use the package:

### Importing the Package

```python
from rawana import powers, stories
```

### Getting Rawana's Powers

To retrieve a list of Rawana's powers, you can call the `get_all_powers` function:

```python
# Get Rawana's powers
print(powers.get_all_powers())
```

This will return a dictionary of Rawana's supernatural powers with detailed descriptions for each ability.

Example output:

```python
{
    "immortality": "Blessed with immortality by Lord Brahma, Rawana cannot be killed by any divine being or force.",
    "strength": "Possesses the strength of a thousand elephants, able to perform feats of unimaginable power.",
    "flight": "Ability to fly through the skies at incredible speeds, making him almost unstoppable.",
    # and more...
}
```

### Getting a Specific Power Description

To get more details about a specific power, use the `get_power_description` function:

```python
# Get a specific power's description
print(powers.get_power_description("flight"))
```

Example output:

```python
"Ability to fly through the skies at incredible speeds, making him almost unstoppable."
```

### Exploring Rawana's Stories

You can explore Rawana's stories by calling the `get_story` function:

```python
# Read a story about Rawana
print(stories.get_story("origin"))
```

This will return the full description of the story associated with the specified key (e.g., "origin" or "abduction_of_sita").

Example output:

```python
"Long ago, Rawana was born to sage Vishrava and rakshasi Kaikesi..."
```

### Get All Available Stories

To get a list of all available stories about Rawana, use the `get_all_stories` function:

```python
# Get a list of all stories
print(stories.get_all_stories())
```

Example output:

```python
['origin', 'tapasya', 'battle_with_devas', 'abduction_of_sita', 'final_battle', 'rebirth_of_ravana', 'rawana_in_ramayana', 'lessons_from_ravana']
```

### Example: Full Script to Get Rawana's Powers and Stories

Here's a full example script that demonstrates how to use the package:

```python
from rawana import powers, stories

# Get and print all powers
print("Rawana's Powers:")
for power, description in powers.get_all_powers().items():
    print(f"{power.capitalize()}: {description}\n")

# Get and print a specific story
story_name = "abduction_of_sita"
print(f"Story: {story_name.capitalize()}")
print(stories.get_story(story_name))
```

### Example Output:
```bash
Rawana's Powers:
Immortality: Blessed with immortality by Lord Brahma, Rawana cannot be killed by any divine being or force.

Strength: Possesses the strength of a thousand elephants, able to perform feats of unimaginable power.

Flight: Ability to fly through the skies at incredible speeds, making him almost unstoppable.

...

Story: Abduction_of_sita
Rawana's most notorious act was the abduction of Sita, the wife of Lord Rama, an incarnation of the god Vishnu...
```

## Contributing

Contributions to the `rawana` package are welcome! Feel free to fork the repository, open issues, and submit pull requests.

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -am 'Add new feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License

The `rawana` package is open source and available under the MIT License.



**Repository Views** ![Views](https://profile-counter.glitch.me/rawana/count.svg)
