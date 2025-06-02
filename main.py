import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def parse_word_input(text_input):
    """Parse input like '55 "freedom", 16 "loyalty"' into a frequency dictionary"""
    # Pattern to match: number followed by quoted word
    pattern = r'(\d+)\s*"([^"]+)"'
    matches = re.findall(pattern, text_input)
    
    word_freq = {}
    for count, word in matches:
        word_freq[word.strip()] = int(count)
    
    return word_freq

def create_wordcloud(word_frequencies, output_filename="wordcloud.png"):
    """Create and save word cloud from frequency dictionary"""
    if not word_frequencies:
        print("No valid words found. Please check your input format.")
        return
    
    # Create WordCloud object
    wordcloud = WordCloud(
        width=800, 
        height=400, 
        background_color='white',
        max_words=100,
        relative_scaling=0.5,
        colormap='viridis'
    ).generate_from_frequencies(word_frequencies)
    
    # Display the word cloud
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title('Word Cloud Generated from Your Input')
    
    # Save the word cloud
    plt.savefig(output_filename, bbox_inches='tight', dpi=300)
    print(f"Word cloud saved as {output_filename}")
    
    # Show the plot
    plt.show()

def main():
    print("The word cloud will be created from the text you provide.")
    print('The text should be inside quotation marks and must be preceded by the number of references the word has.')
    print('Example: 55 "freedom", 16 "loyalty"')
    print()
    
    # Get user input
    user_input = input("Enter your words and counts: ")
    
    # Parse the input
    word_frequencies = parse_word_input(user_input)
    
    if word_frequencies:
        print(f"Found {len(word_frequencies)} words:")
        for word, count in word_frequencies.items():
            print(f"  {word}: {count}")
        print()
        
        # Create word cloud
        create_wordcloud(word_frequencies)
    else:
        print("No valid words found. Please check your input format.")
        print('Make sure to use the format: number "word", number "word"')

if __name__ == "__main__":
    main()