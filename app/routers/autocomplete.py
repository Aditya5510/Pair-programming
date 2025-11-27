from fastapi import APIRouter, HTTPException

from ..schemas.rooms import AutocompleteRequest, AutocompleteResponse
from ..config import settings

router = APIRouter(prefix="/autocomplete", tags=["autocomplete"])


def get_gemini_suggestion(code: str, cursor_pos: int, language: str) -> str:
    """Get autocomplete suggestion from Gemini API."""
    try:
        import google.genai as genai
        
        client = genai.Client(api_key=settings.gemini_api_key)
        
        lines = code[:cursor_pos].split('\n')
        current_line = lines[-1] if lines else ""
        context_lines = lines[-10:] if len(lines) > 10 else lines
        
        prompt = f"""You are a code autocomplete assistant. Given the following {language} code context, suggest ONLY the next few tokens to complete the current line.

Code context:
{chr(10).join(context_lines)}

Current line (incomplete): {current_line}

IMPORTANT: Provide ONLY the completion text that should come after the cursor position. 
- Do NOT include the existing code
- Do NOT provide explanations
- Do NOT provide multiple examples
- Keep it VERY concise (1-5 tokens maximum)
- If the line is complete, return an empty string
- Return ONLY the completion text, nothing else

Completion:"""
        
        try:
            # Try newer models first
            response = client.models.generate_content(
                model="models/gemini-2.5-flash",
                contents=prompt
            )
        except Exception as e1:
            try:
                # Fallback to gemini-pro-latest
                response = client.models.generate_content(
                    model="models/gemini-pro-latest",
                    contents=prompt
                )
            except Exception as e2:
                print(f"Gemini API model error (flash): {e1}")
                print(f"Gemini API model error (pro-latest): {e2}")
                return ""
        
        suggestion = ""
        if hasattr(response, 'text'):
            suggestion = response.text.strip()
        elif hasattr(response, 'candidates') and response.candidates:
            if hasattr(response.candidates[0], 'content'):
                if hasattr(response.candidates[0].content, 'parts'):
                    suggestion = response.candidates[0].content.parts[0].text.strip()
                elif hasattr(response.candidates[0].content, 'text'):
                    suggestion = response.candidates[0].content.text.strip()
        elif hasattr(response, 'content'):
            if hasattr(response.content, 'parts'):
                suggestion = response.content.parts[0].text.strip()
            elif hasattr(response.content, 'text'):
                suggestion = response.content.text.strip()
        
        # Clean up the suggestion - take only the first line and limit length
        if suggestion:
            # Remove any code blocks or markdown formatting
            suggestion = suggestion.replace('```', '').strip()
            # Take only the first line
            suggestion = suggestion.split('\n')[0].strip()
            # Remove any leading/trailing quotes or parentheses that might be explanations
            suggestion = suggestion.strip('"\'`()[]{}')
            # Limit to reasonable length for autocomplete
            if len(suggestion) > 50:
                # Try to find a natural break point
                words = suggestion.split()
                suggestion = ' '.join(words[:10])  # Max 10 words
        
        return suggestion
    except Exception as e:
        print(f"Gemini API error: {e}")
        import traceback
        traceback.print_exc()
        return ""


def get_mocked_suggestion(code: str, cursor_pos: int) -> str:
    """Fallback mocked suggestions."""
    lines = code[:cursor_pos].split('\n')
    current_line = lines[-1] if lines else ""
    current_line_stripped = current_line.strip()
    
    if current_line.endswith("def ") or current_line_stripped == "def":
        return "function_name():"
    elif current_line.endswith("if ") or current_line_stripped == "if":
        return "condition:"
    elif current_line.endswith("for ") or current_line_stripped == "for":
        return "item in items:"
    elif current_line.endswith("import ") or current_line_stripped == "import":
        return "os"
    elif current_line.endswith("class ") or current_line_stripped == "class":
        return "ClassName:"
    elif "print(" in current_line and not current_line.strip().endswith(")"):
        return "Hello, World!"
    else:
        return ""


@router.post("", response_model=AutocompleteResponse)
def get_autocomplete_suggestion(request: AutocompleteRequest):
    code = request.code
    cursor_pos = request.cursorPosition
    language = request.language
    
    suggestion = ""
    
    if settings.gemini_api_key:
        suggestion = get_gemini_suggestion(code, cursor_pos, language)
    
    if not suggestion:
        suggestion = get_mocked_suggestion(code, cursor_pos)
    
    return AutocompleteResponse(suggestion=suggestion)

