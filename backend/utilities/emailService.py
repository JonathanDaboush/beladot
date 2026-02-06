from typing import Any, Optional, Dict
import os
import requests
import re
import asyncio

try:
    from backend.config import settings
except Exception:
    settings = None


def generate_email(to_email: str, subject: str, pagePath: str, context: Optional[Dict[str, Any]] = None) -> Any:
    html_content = _read_html(pagePath)
    if context:
        for k, v in context.items():
            html_content = html_content.replace(f"{{{{ {k} }}}}", str(v))
    return _send_email(to_email, subject, html_content)


def _send_email(to_email: str, subject: str, html_content: str) -> Any:
    api_url = os.environ.get("EMAIL_API_URL") or (getattr(settings, "EMAIL_API_URL", None) if settings else None)
    api_key = os.environ.get("EMAIL_API_KEY") or (getattr(settings, "EMAIL_API_KEY", None) if settings else None)
    sender = os.environ.get("EMAIL_SENDER") or (getattr(settings, "EMAIL_SENDER", None) if settings else None)

    payload = {
        "to": to_email,
        "subject": subject,
        "html": html_content,
        "from": sender,
    }

    headers = {"Authorization": f"Bearer {api_key}" if api_key else "", "Content-Type": "application/json"}

    if not api_url:
        raise RuntimeError("No EMAIL_API_URL configured")

    response = requests.post(api_url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    try:
        return response.json()
    except Exception:
        return response.text


def _read_html(pagePath: str) -> str:
    base_dir = os.path.dirname(__file__)
    html_dir = os.path.join(base_dir, "htmlPages")
    full_path = os.path.join(html_dir, pagePath)
    if not os.path.exists(full_path):
        raise FileNotFoundError(f"Email template not found: {full_path}")
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()


def sanitize_template(html: str) -> str:
    html = re.sub(r"<(script|style)[^>]*>.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
    html = re.sub(r'on\w+="[^"]*"', "", html)
    return html


async def generate_email_async(to_email: str, subject: str, pagePath: str, context: Optional[Dict[str, Any]] = None, retries: int = 3) -> Any:
    html_content = _read_html(pagePath)
    if context:
        for k, v in context.items():
            html_content = html_content.replace(f"{{{{ {k} }}}}", str(v))
    html_content = sanitize_template(html_content)
    for attempt in range(retries):
        try:
            return _send_email(to_email, subject, html_content)
        except Exception:
            try:
                from backend.infrastructure.structured_logging import logger

                logger.exception("email.send_failed", to_email=to_email, subject=subject, attempt=attempt)
            except Exception:
                pass
            if attempt == retries - 1:
                with open("failed_emails.log", "a") as f:
                    f.write(f"{to_email}: {subject}\n")
                return None
            await asyncio.sleep(2 ** attempt)
