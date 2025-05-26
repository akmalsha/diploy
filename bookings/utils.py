from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

def generate_invoice_pdf(template_src, context_dict):
    template = get_template(template_src)  # Load the HTML template
    html = template.render(context_dict)   # Render HTML with context
    result = BytesIO()                     # Create a buffer to hold PDF data
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)  # Convert HTML to PDF
    if not pdf.err:
        return result.getvalue()           # Return PDF binary if successful
    return None                            # Return None if failed


