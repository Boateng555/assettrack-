#!/usr/bin/env python
"""
Script to convert the Azure AD Integration Guide to Word document format.
This script will help you create a properly formatted Word document.
"""

import os
import sys

def create_word_document():
    print("📄 Azure AD Integration Guide - Word Document Conversion")
    print("=" * 60)
    
    print("\n📋 Instructions to create Word document:")
    print("-" * 40)
    
    print("\n1. 📖 Copy the content from 'Azure_AD_Integration_Guide.md'")
    print("2. 📝 Open Microsoft Word")
    print("3. 📋 Paste the content into Word")
    print("4. 🎨 Apply formatting:")
    
    print("\n   📝 Text Formatting:")
    print("   - Use Heading 1 for main sections (##)")
    print("   - Use Heading 2 for subsections (###)")
    print("   - Use Heading 3 for sub-subsections (####)")
    print("   - Use Code formatting for commands and code blocks")
    print("   - Use Bold for important terms and steps")
    
    print("\n   🎨 Visual Elements:")
    print("   - Add page numbers")
    print("   - Create a table of contents")
    print("   - Add headers and footers")
    print("   - Use consistent fonts (Arial or Calibri)")
    print("   - Add page breaks between major sections")
    
    print("\n   📊 Tables and Lists:")
    print("   - Convert markdown tables to Word tables")
    print("   - Use bullet points for lists")
    print("   - Use numbered lists for step-by-step instructions")
    
    print("\n5. 💾 Save as 'Azure_AD_Integration_Guide.docx'")
    
    print("\n📁 File locations:")
    print(f"   Markdown file: {os.path.abspath('Azure_AD_Integration_Guide.md')}")
    print("   Word document: Create in your preferred location")
    
    print("\n🎯 Recommended Word Document Structure:")
    print("-" * 40)
    
    sections = [
        "Title Page",
        "Table of Contents",
        "Executive Summary",
        "Prerequisites",
        "Step 1: Azure AD App Registration",
        "Step 2: Configure Azure AD Permissions", 
        "Step 3: Create Client Secret",
        "Step 4: Django Application Setup",
        "Step 5: Environment Configuration",
        "Step 6: Testing the Integration",
        "Troubleshooting",
        "Maintenance",
        "Support and Resources",
        "Appendices"
    ]
    
    for i, section in enumerate(sections, 1):
        print(f"   {i:2d}. {section}")
    
    print("\n✅ Conversion Tips:")
    print("-" * 20)
    print("• Use Word's 'Styles' feature for consistent formatting")
    print("• Add screenshots of Azure Portal steps")
    print("• Include your actual Azure AD configuration details")
    print("• Add company branding and logos")
    print("• Include version control information")
    print("• Add review and approval signatures")

def show_markdown_content():
    """Show the first few lines of the markdown file"""
    try:
        with open('Azure_AD_Integration_Guide.md', 'r', encoding='utf-8') as f:
            content = f.read()
            print("\n📄 First 500 characters of the markdown file:")
            print("-" * 50)
            print(content[:500] + "...")
            print("\n📄 Total file size:", len(content), "characters")
    except FileNotFoundError:
        print("❌ Azure_AD_Integration_Guide.md not found!")
        print("Please ensure the file exists in the current directory.")

if __name__ == "__main__":
    create_word_document()
    show_markdown_content()
    
    print("\n🚀 Ready to create your Word document!")
    print("Open 'Azure_AD_Integration_Guide.md' and copy the content to Word.")
