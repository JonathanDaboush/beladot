def generate_email(to_email, subject, pagePath, context=None):
    """
    Generate and send an email using an HTML template and context.
    Args:
        to_email (str): Recipient email address.
        subject (str): Email subject.
        pagePath (str): Path to HTML template (relative to htmlPages/).
        context (dict, optional): Dict of template variables to replace in HTML.
    Returns:
        dict: API response from email send attempt.
    """
    html_content = _read_html(pagePath)
    if context:
        for k, v in context.items():
            html_content = html_content.replace(f'{{{{ {k} }}}}', str(v))
    return _send_email(to_email, subject, html_content)

# ------------------------------------------------------------------------------
# emailService.py
# ------------------------------------------------------------------------------
# Utility functions for generating and sending HTML emails using an external API.
# Reads HTML templates and sends emails via configured API endpoint.
# ------------------------------------------------------------------------------

import os
import requests

def _send_email(to_email, subject, html_content):
    api_url = os.environ.get('EMAIL_API_URL')
    api_key = os.environ.get('EMAIL_API_KEY')
    sender = os.environ.get('EMAIL_SENDER')

    if not all([api_url, api_key, sender]):
        raise Exception('Email API configuration missing in environment variables')

    data = {
        'from': sender,
        'to': [to_email],
        'subject': subject,
        'html': html_content
    }

    headers = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
    }

    try:
        response = requests.post(
            api_url,
            json=data,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(
            f"Email send failed: {e}"
        )


def _read_html(pagePath):
    """
    Read HTML content from a template file in the htmlPages directory.
    Args:
        pagePath (str): Relative path to the HTML file.
    Returns:
        str: HTML content as a string.
    """
    # Look for templates in backend/utilities/htmlPages
    base_dir = os.path.dirname(__file__)
    html_dir = os.path.join(base_dir, 'htmlPages')
    full_path = os.path.join(html_dir, pagePath)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Email template not found: {full_path}")
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()

