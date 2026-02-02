// Node.js script to process pending Telegram messages
// This will be called by OpenClaw's system

const fs = require('fs');
const path = require('path');

function processPendingMessages() {
    const messageFile = path.join(__dirname, 'pending_telegram_message.txt');
    const typeFile = path.join(__dirname, 'message_type.txt');
    
    if (fs.existsSync(messageFile) && fs.existsSync(typeFile)) {
        try {
            const message = fs.readFileSync(messageFile, 'utf8').trim();
            const messageType = fs.readFileSync(typeFile, 'utf8').trim();
            
            // Log that we're processing the message
            console.log(`Processing ${messageType} message`);
            
            // The actual message sending would happen through OpenClaw's system
            // This is a placeholder for the actual implementation
            return {
                message: message,
                type: messageType,
                processed: true
            };
            
        } catch (error) {
            console.error('Error processing pending message:', error);
            return { error: error.message, processed: false };
        }
    }
    
    return { processed: false };
}

module.exports = { processPendingMessages };

if (require.main === module) {
    const result = processPendingMessages();
    console.log('Message processing result:', result);
}