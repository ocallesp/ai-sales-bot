// src/app/shared/models/message.ts
export interface Message {
    id: string;
    text: string;
    sender: 'user' | 'bot';
    sentiment: string;
    timestamp: Date;
  }
