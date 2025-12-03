# Email Setup Guide

## SMTP Configuration for Order Confirmations

The chatbot can send order confirmation emails via SMTP. To enable this feature:

### 1. Get Gmail App Password (Recommended)

If using Gmail:
1. Go to your Google Account settings
2. Enable 2-Step Verification
3. Go to Security → App Passwords
4. Generate an app password for "Mail"
5. Copy the 16-character password

### 2. Update .env File

Add these lines to your `.env` file:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-16-char-app-password
SENDER_EMAIL=your-email@gmail.com
```

### 3. Test the Feature

1. Start the app: `python -m app.main`
2. Open the chat widget
3. Say: "I want to order Blueberry Crumble Cake"
4. Provide your details when asked: "My name is John, email john@example.com, phone 1234567890"
5. Check your email for the order confirmation

## Alternative SMTP Providers

### Outlook/Hotmail
```env
SMTP_SERVER=smtp-mail.outlook.com
SMTP_PORT=587
```

### Yahoo
```env
SMTP_SERVER=smtp.mail.yahoo.com
SMTP_PORT=587
```

## Troubleshooting

- **No email received**: Check spam folder
- **Authentication error**: Verify app password is correct
- **Connection refused**: Check firewall/antivirus settings
- **Email not sent**: Check terminal logs for error messages

## Chatbot Features

### Show All Items
- "Show all items"
- "List all desserts"
- "What do you have?"

### Place Order via Chat
1. "I want to order [item name]"
2. Assistant will ask for your details
3. Provide: Name, Email, Phone
4. Order is created and confirmation email sent

### Get Recommendations
- "Recommend something sweet"
- "Suggest a dessert"
