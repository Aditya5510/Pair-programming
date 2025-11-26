from fastapi import APIRouter

from ..schemas.rooms import AutocompleteRequest, AutocompleteResponse

router = APIRouter(prefix="/autocomplete", tags=["autocomplete"])


@router.post("", response_model=AutocompleteResponse)
def get_autocomplete_suggestion(request: AutocompleteRequest):
    code = request.code
    cursor_pos = request.cursorPosition
    
    lines = code[:cursor_pos].split('\n')
    current_line = lines[-1] if lines else ""
    
    suggestion = ""
    
    if current_line.strip().endswith("def "):
        suggestion = "function_name():"
    elif current_line.strip().endswith("if "):
        suggestion = "condition:"
    elif current_line.strip().endswith("for "):
        suggestion = "item in items:"
    elif current_line.strip().endswith("import "):
        suggestion = "os"
    elif current_line.strip().endswith("class "):
        suggestion = "ClassName:"
    elif "print(" in current_line and not current_line.strip().endswith(")"):
        suggestion = "Hello, World!"
    else:
        suggestion = "# Add your code here"
    
    return AutocompleteResponse(suggestion=suggestion)

