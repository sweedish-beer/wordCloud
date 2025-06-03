import re
import os
from datetime import datetime
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# ANSI color codes for terminal styling
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    PURPLE = '\033[35m'
    ORANGE = '\033[33m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def generate_filename(base_name="wordcloud"):
    """Generate unique filename with timestamp if file exists"""
    extension = ".png"
    filename = f"{base_name}{extension}"
    
    if not os.path.exists(filename):
        return filename
    
    # Add timestamp if file exists
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    return f"{base_name}_{timestamp}{extension}"

def print_colorful_separator():
    """Print a colorful separator for visual clarity"""
    separator = "=" * 60
    print(f"\n{Colors.CYAN}{Colors.BOLD}{separator}{Colors.END}")
    print(f"{Colors.YELLOW}{Colors.BOLD}🎨 WORD CLOUD GENERATOR 🎨{Colors.END}")
    print(f"{Colors.CYAN}{Colors.BOLD}{separator}{Colors.END}\n")

def display_color_schemes():
    """Display available color schemes in their representative colors"""
    schemes = {
        '1': {'name': 'plasma', 'color': Colors.PURPLE},
        '2': {'name': 'viridis', 'color': Colors.GREEN}, 
        '3': {'name': 'magma', 'color': Colors.RED},
        '4': {'name': 'inferno', 'color': Colors.ORANGE},
        '5': {'name': 'cool', 'color': Colors.CYAN},
        '6': {'name': 'hot', 'color': Colors.YELLOW},
        '7': {'name': 'rainbow', 'color': Colors.HEADER}
    }
    
    print(f"{Colors.BOLD}Choose a color scheme:{Colors.END}")
    for key, scheme in schemes.items():
        color_name = f"{scheme['color']}{Colors.BOLD}{scheme['name']}{Colors.END}"
        print(f"  {Colors.BOLD}{key}.{Colors.END} {color_name}")
    
    return schemes

def get_color_scheme_choice():
    """Get user's color scheme choice"""
    schemes = display_color_schemes()
    
    while True:
        choice = input(f"\n{Colors.BOLD}Enter your choice (1-7): {Colors.END}").strip()
        if choice in schemes:
            selected_scheme = schemes[choice]['name']
            color = schemes[choice]['color']
            print(f"{Colors.GREEN}✓ Selected: {color}{Colors.BOLD}{selected_scheme}{Colors.END}")
            return selected_scheme
        else:
            print(f"{Colors.RED}Invalid choice! Please select a number from 1 to 7.{Colors.END}")

def parse_word_input(text_input):
    """Parse input like '55 "freedom", 16 "loyalty"' into a frequency dictionary"""
    # Debug: show what we received
    print(f"{Colors.BLUE}Debug - Input received: {repr(text_input)}{Colors.END}")
    
    # Pattern to match: number followed by quoted word
    pattern = r'(\d+)\s*"([^"]+)"'
    matches = re.findall(pattern, text_input)
    
    # Debug: show what matches we found
    print(f"{Colors.BLUE}Debug - Matches found: {matches}{Colors.END}")
    
    word_freq = {}
    for count, word in matches:
        word_freq[word.strip()] = int(count)
    
    return word_freq  # This was missing!

def create_wordcloud(word_frequencies, colormap='plasma', output_filename=None):
    """Create and save word cloud from frequency dictionary"""
    if not word_frequencies:
        print(f"{Colors.RED}No valid words found. Please check your input format.{Colors.END}")
        return
    
    if output_filename is None:
        output_filename = generate_filename()
    
    # Create WordCloud object with enhanced styling
    wordcloud = WordCloud(
        width=1200, 
        height=600, 
        background_color='black',
        max_words=100,
        relative_scaling=0.6,
        colormap=colormap,
        font_path=None,  # Use default font
        max_font_size=120,
        min_font_size=10,
        random_state=42,  # For consistent layout
        collocations=False,
        prefer_horizontal=0.7
    ).generate_from_frequencies(word_frequencies)
    
    # Generate figure and axis
    plt.figure(figsize=(12, 6), facecolor='black')
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    
    # Save the generated image
    plt.savefig(output_filename, bbox_inches='tight', dpi=300, 
                facecolor='black', edgecolor='none')
    print(f"{Colors.GREEN}{Colors.BOLD}✓ Word cloud saved as {output_filename}{Colors.END}")
    
    # Show the plot
    plt.show()

def main():
    print_colorful_separator()
    
    print(f"{Colors.BOLD}The word cloud will be created from the text you provide.{Colors.END}")
    print(f"The text should be inside {Colors.YELLOW}quotation marks{Colors.END} and must be preceded by the {Colors.CYAN}number of references{Colors.END} the word has.")
    print(f"{Colors.GREEN}Example:{Colors.END} {Colors.BOLD}55 \"freedom\", 16 \"loyalty\"{Colors.END}")
    print()
    
    # Get user input
    user_input = input(f"{Colors.BOLD}Enter your words and counts: {Colors.END}")
    
    # Parse the input
    word_frequencies = parse_word_input(user_input)
    
    if word_frequencies:
        print(f"\n{Colors.GREEN}{Colors.BOLD}✓ Found {len(word_frequencies)} words:{Colors.END}")
        for word, count in word_frequencies.items():
            print(f"  {Colors.CYAN}{word}{Colors.END}: {Colors.YELLOW}{count}{Colors.END}")
        print()
        
        # Get color scheme choice
        colormap = get_color_scheme_choice()
        print()
        
        # Create word cloud
        print(f"{Colors.BLUE}Generating word cloud...{Colors.END}")
        create_wordcloud(word_frequencies, colormap)
    else:
        print(f"{Colors.RED}No valid words found. Please check your input format.{Colors.END}")
        print(f'Make sure to use the format: {Colors.BOLD}number "word", number "word"{Colors.END}')

if __name__ == "__main__":
    main()