import sys
import regex
import os

def clean_file(filename):
    """
    Cleans a file in two reliable steps:
    1. Removes all emojis from the entire file using a truly comprehensive pattern.
    2. Re-formats all relevant markdown lines from '- **Text**:' to '- __Text__'.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f_read:
            content = f_read.read()

        original_content = content

        # Step 1: Remove ALL emojis from the entire file content first.
        # This pattern has been updated to include the U+2300 block for symbols like the pause button.
        UNIVERSAL_EMOJI_PATTERN = regex.compile(
            "["
            "\U0001F1E0-\U0001F1FF"  # Flags
            "\U0001F300-\U0001F5FF"  # Symbols & Pictographs
            "\U0001F600-\U0001F64F"  # Emoticons
            "\U0001F680-\U0001F6FF"  # Transport & Map
            "\U0001F900-\U0001F9FF"  # Supplemental Symbols
            "\U0001FA70-\U0001FAFF"  # Symbols Extended
            "\u2300-\u27BF"          # Miscellaneous Technical, Symbols, & Dingbats
            "\uFE0F"                # Variation Selector
            "]+"
        )
        content = UNIVERSAL_EMOJI_PATTERN.sub('', content)
        
        # Step 2: Now that emojis are gone, reliably reformat all matching lines.
        # This finds lines like '- ** Text  **:' and converts them to '- __Text__'.
        content = regex.sub(
            r'(^\s*-\s+)\*\*\s*(.*?)\s*\*\*:?',
            r'\1__\2__',
            content,
            flags=regex.MULTILINE
        )

        if original_content != content:
            with open(filename, 'w', encoding='utf-8') as f_write:
                f_write.write(content)
            print(f" Cleaned and reformatted: {filename}")
        else:
            print(f"ℹ No changes needed for: {filename}")

    except Exception as e:
        print(f"Error processing {filename}: {e}", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python3 master_cleaner.py <file1> <file2> ...")
    for path in sys.argv[1:]:
        if os.path.isfile(path):
            clean_file(path)
