import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from app.core.config import settings

def send_order_confirmation_email(to_email: str, order_details: Dict[str, Any]):
    """
    Send an order confirmation email to the customer.
    
    Args:
        to_email: Customer's email address.
        order_details: Dictionary containing order information.
    """
    if not settings.smtp_username or not settings.smtp_password:
        print("⚠️ SMTP credentials not set. Skipping email sending.")
        return

    subject = f"Order Confirmation - Order #{order_details.get('id', 'N/A')}"
    
    # Construct email body
    items_html = ""
    for item in order_details.get('items', []):
        items_html += f"<li>{item['product_name']} x {item['quantity']} - ${item['price']:.2f}</li>"
        
    html_content = f"""
    <html>
        <body>
            <h2>Thank you for your order, {order_details.get('customer_name')}!</h2>
            <p>We have received your order and it is being processed.</p>
            
            <h3>Order Summary (Order #{order_details.get('id')})</h3>
            <ul>
                {items_html}
            </ul>
            
            <p><strong>Total Amount: ${order_details.get('total_amount', 0):.2f}</strong></p>
            
            <p>We will notify you when your order is ready.</p>
            <br>
            <p>Best regards,<br>Dough-Re-Me Bakery</p>
        </body>
    </html>
    """

    msg = MIMEMultipart()
    msg["From"] = settings.sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(html_content, "html"))

    try:
        server = smtplib.SMTP(settings.smtp_server, settings.smtp_port)
        server.starttls()
        server.login(settings.smtp_username, settings.smtp_password)
        server.sendmail(settings.sender_email, to_email, msg.as_string())
        server.quit()
        print(f"✅ Order confirmation email sent to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
