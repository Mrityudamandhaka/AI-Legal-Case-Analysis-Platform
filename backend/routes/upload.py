from fastapi import APIRouter, UploadFile, File, Depends
from services.auth_service import get_current_user
from io import BytesIO
from pypdf import PdfReader

router = APIRouter(prefix="/upload", tags=["upload"])

@router.post("/")
async def upload_file(file: UploadFile = File(...), current_user = Depends(get_current_user)):
    try:
        # Log the authenticated user
        print(f"User {current_user.username} uploading file: {file.filename}")
        
        # Read the file content
        content = await file.read()
        
        # Log the file information for debugging
        print(f"File name: {file.filename}")
        print(f"Content type: {file.content_type}")
        print(f"Content length: {len(content)}")
        
        # Check if it's a PDF file
        if file.content_type == "application/pdf":
            # Process PDF with pypdf
            pdf_file = BytesIO(content)
            pdf_reader = PdfReader(pdf_file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text()
            return {"message": "PDF processed successfully", "content": text[:4000]}
        else:
            # For text files, try to decode the content
            try:
                # Try UTF-8 first
                text = content.decode("utf-8")
                print(f"Decoded text: {text}")
                return {"message": "Text file processed successfully", "content": text[:4000]}
            except UnicodeDecodeError:
                try:
                    # Try with error handling
                    text = content.decode("utf-8", errors="ignore")
                    print(f"Decoded text (with errors ignored): {text}")
                    return {"message": "Text file processed successfully", "content": text[:4000]}
                except Exception as e:
                    print(f"Error decoding text: {e}")
                    return {"message": "Unsupported file type", "content": ""}
    except Exception as e:
        print(f"General error: {e}")
        return {"message": f"Error processing file: {str(e)}", "content": ""}