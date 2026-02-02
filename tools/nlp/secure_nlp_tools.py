#!/usr/bin/env python3
"""
Secure NLP Tools for OpenClaw
Implements safe natural language processing with security validations
"""

import nltk
import spacy
from typing import Optional, List, Dict, Any
import re
from pathlib import Path

def initialize_nlp_models():
    """
    Initializes NLP models with security considerations
    """
    try:
        # Try to load spaCy English model
        try:
            nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("spaCy English model not found. Please install with: python -m spacy download en_core_web_sm")
            nlp = None
        
        # Download required NLTK data with security
        required_nltk_data = [
            'punkt',      # Tokenizer
            'stopwords',  # Stop words
            'wordnet',    # WordNet lexical database
            'averaged_perceptron_tagger',  # POS tagger
            'vader_lexicon'  # Sentiment analysis
        ]
        
        for item in required_nltk_data:
            try:
                nltk.data.find(f'tokenizers/{item}')
            except LookupError:
                print(f"NLTK data '{item}' not found. This may need to be downloaded separately.")
        
        return nlp
    except Exception as e:
        print(f"Error initializing NLP models: {str(e)}")
        return None

def validate_text_input(text: str, max_length: int = 100000) -> bool:
    """
    Validates text input for NLP processing
    """
    if not isinstance(text, str):
        return False
    
    if len(text) > max_length:
        print(f"Text too long: {len(text)} characters (max {max_length})")
        return False
    
    # Check for potential code injection patterns
    dangerous_patterns = [
        r'<script[^>]*>.*?</script>',  # Script tags
        r'javascript:',               # JavaScript URLs
        r'on\w+\s*=',                # Event handlers
    ]
    
    for pattern in dangerous_patterns:
        if re.search(pattern, text, re.IGNORECASE):
            print("Potential code injection detected in text")
            return False
    
    return True

def secure_tokenize(text: str, nlp_model=None) -> Optional[List[str]]:
    """
    Securely tokenizes text
    """
    if not validate_text_input(text):
        return None
    
    try:
        if nlp_model:
            doc = nlp_model(text)
            tokens = [token.text for token in doc if not token.is_space]
        else:
            # Fallback to NLTK if spaCy not available
            from nltk.tokenize import word_tokenize
            tokens = word_tokenize(text)
        
        return tokens
    except Exception as e:
        print(f"Error during tokenization: {str(e)}")
        return None

def secure_pos_tag(text: str, nlp_model=None) -> Optional[List[tuple]]:
    """
    Securely performs part-of-speech tagging
    """
    if not validate_text_input(text):
        return None
    
    try:
        if nlp_model:
            doc = nlp_model(text)
            pos_tags = [(token.text, token.pos_) for token in doc if not token.is_space]
        else:
            # Fallback to NLTK
            from nltk.tokenize import word_tokenize
            from nltk.tag import pos_tag
            tokens = word_tokenize(text)
            pos_tags = pos_tag(tokens)
        
        return pos_tags
    except Exception as e:
        print(f"Error during POS tagging: {str(e)}")
        return None

def secure_named_entity_recognition(text: str, nlp_model=None) -> Optional[List[Dict[str, Any]]]:
    """
    Securely performs named entity recognition
    """
    if not validate_text_input(text):
        return None
    
    try:
        if nlp_model:
            doc = nlp_model(text)
            entities = []
            for ent in doc.ents:
                entities.append({
                    'text': ent.text,
                    'label': ent.label_,
                    'description': spacy.explain(ent.label_),
                    'start': ent.start_char,
                    'end': ent.end_char
                })
            return entities
        else:
            print("NER requires spaCy model. Please install en_core_web_sm model.")
            return None
    except Exception as e:
        print(f"Error during NER: {str(e)}")
        return None

def secure_sentiment_analysis(text: str) -> Optional[Dict[str, float]]:
    """
    Securely performs sentiment analysis using VADER
    """
    if not validate_text_input(text, max_length=10000):
        return None
    
    try:
        from nltk.sentiment import SentimentIntensityAnalyzer
        
        sia = SentimentIntensityAnalyzer()
        scores = sia.polarity_scores(text)
        
        # Return normalized scores
        return {
            'neg': scores['neg'],
            'neu': scores['neu'],
            'pos': scores['pos'],
            'compound': scores['compound']
        }
    except Exception as e:
        print(f"Error during sentiment analysis: {str(e)}")
        return None

def secure_text_summarization(text: str, max_length: int = 1000, nlp_model=None) -> Optional[str]:
    """
    Securely summarizes text (basic implementation)
    """
    if not validate_text_input(text):
        return None
    
    try:
        # For now, implement a simple extractive summary
        # In the future, this could use more sophisticated methods
        
        if len(text) <= max_length:
            return text  # Already short enough
        
        # Split into sentences and take the first few
        if nlp_model:
            doc = nlp_model(text)
            sentences = [sent.text.strip() for sent in doc.sents]
        else:
            # Simple split by sentence endings
            import re
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
        
        # Build summary
        summary = ""
        for sentence in sentences:
            if len(summary) + len(sentence) > max_length:
                break
            summary += sentence + ". "
        
        return summary.strip()
    except Exception as e:
        print(f"Error during text summarization: {str(e)}")
        return None

def secure_keyword_extraction(text: str, nlp_model=None, max_keywords: int = 10) -> Optional[List[str]]:
    """
    Securely extracts keywords from text
    """
    if not validate_text_input(text):
        return None
    
    try:
        if nlp_model:
            doc = nlp_model(text)
            # Extract noun phrases and important tokens
            keywords = []
            for token in doc:
                if (not token.is_stop and 
                    not token.is_punct and 
                    token.pos_ in ['NOUN', 'PROPN', 'ADJ'] and 
                    len(token.text) > 2):
                    keywords.append(token.text.lower())
            
            # Also include noun chunks
            for chunk in doc.noun_chunks:
                if len(chunk.text) > 2 and not chunk.text.isspace():
                    keywords.append(chunk.text.lower())
            
            # Remove duplicates while preserving order
            seen = set()
            unique_keywords = []
            for kw in keywords:
                if kw not in seen:
                    seen.add(kw)
                    unique_keywords.append(kw)
            
            return unique_keywords[:max_keywords]
        else:
            # Fallback using basic NLTK approach
            from nltk.tokenize import word_tokenize
            from nltk.corpus import stopwords
            from nltk.tag import pos_tag
            
            stop_words = set(stopwords.words('english'))
            tokens = word_tokenize(text.lower())
            pos_tags = pos_tag(tokens)
            
            keywords = [
                word for word, pos in pos_tags 
                if word not in stop_words and 
                pos.startswith(('NN', 'JJ')) and 
                len(word) > 2
            ]
            
            # Remove duplicates
            unique_keywords = list(dict.fromkeys(keywords))  # Preserves order
            return unique_keywords[:max_keywords]
    except Exception as e:
        print(f"Error during keyword extraction: {str(e)}")
        return None

def secure_text_similarity(text1: str, text2: str, nlp_model=None) -> Optional[float]:
    """
    Securely computes similarity between two texts
    """
    if not validate_text_input(text1) or not validate_text_input(text2):
        return None
    
    try:
        if nlp_model:
            doc1 = nlp_model(text1)
            doc2 = nlp_model(text2)
            similarity = doc1.similarity(doc2)
            return float(similarity)
        else:
            # Simple fallback similarity based on common words
            from nltk.tokenize import word_tokenize
            from collections import Counter
            
            tokens1 = set(word_tokenize(text1.lower()))
            tokens2 = set(word_tokenize(text2.lower()))
            
            intersection = tokens1.intersection(tokens2)
            union = tokens1.union(tokens2)
            
            if len(union) == 0:
                return 0.0
            
            return len(intersection) / len(union)
    except Exception as e:
        print(f"Error during text similarity calculation: {str(e)}")
        return None

def clean_text_for_nlp(text: str) -> str:
    """
    Cleans text for NLP processing, removing potential security issues
    """
    if not isinstance(text, str):
        return ""
    
    # Remove potential code injection patterns
    cleaned_text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'javascript:\s*\w+', '', cleaned_text, flags=re.IGNORECASE)
    cleaned_text = re.sub(r'vbscript:\s*\w+', '', cleaned_text, flags=re.IGNORECASE)
    
    # Remove other potentially dangerous patterns
    cleaned_text = re.sub(r'on\w+\s*=\s*["\'][^"\']*["\']', '', cleaned_text, flags=re.IGNORECASE)
    
    return cleaned_text

def analyze_text_security(text: str) -> Dict[str, Any]:
    """
    Analyzes text for potential security issues
    """
    analysis = {
        'length': len(text),
        'has_scripts': bool(re.search(r'<script[^>]*>.*?</script>', text, re.IGNORECASE)),
        'has_javascript_urls': bool(re.search(r'javascript:\s*\w+', text, re.IGNORECASE)),
        'has_event_handlers': bool(re.search(r'on\w+\s*=\s*["\'][^"\']*["\']', text, re.IGNORECASE)),
        'has_iframes': bool(re.search(r'<iframe[^>]*>.*?</iframe>', text, re.IGNORECASE)),
        'is_safe': True
    }
    
    # Determine if text is safe
    analysis['is_safe'] = not (
        analysis['has_scripts'] or 
        analysis['has_javascript_urls'] or 
        analysis['has_event_handlers'] or 
        analysis['has_iframes']
    )
    
    return analysis

def main():
    """
    Example usage of the secure NLP tools
    """
    print("Secure NLP Tools for OpenClaw")
    print("Provides safe natural language processing with security validations")
    
    # Initialize models
    nlp_model = initialize_nlp_models()
    
    if nlp_model:
        print("spaCy model loaded successfully")
    else:
        print("spaCy model not available - using NLTK fallbacks where possible")
    
    # Example usage (commented out since no specific text is provided)
    # text = "This is an example text for NLP processing."
    # tokens = secure_tokenize(text, nlp_model)
    # print(f"Tokens: {tokens}")

if __name__ == "__main__":
    main()