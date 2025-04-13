// src/app/customer/components/chat-view/chat-view.component.ts
import { Component, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { ChatBubbleComponent } from '../../../shared/components/chat-bubble/chat-bubble.component';
import { Message } from '../../../shared/models/message';
import { ApiService } from '../../../core/services/api.service';

@Component({
  selector: 'app-chat-view',
  standalone: true,
  imports: [
    CommonModule,
    ReactiveFormsModule,
    MatCardModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    ChatBubbleComponent
  ],
  templateUrl: './chat-view.component.html',
  styleUrls: ['./chat-view.component.scss']
})
export class ChatViewComponent implements AfterViewChecked {
  @ViewChild('messageContainer') private messageContainer!: ElementRef;

  chatForm = new FormGroup({
    text: new FormControl('', Validators.required)
  });

  messages: Message[] = [
    { id: '1', text: 'Welcome! Ask about our products.', sender: 'bot', sentiment: 'positive', timestamp: new Date() }
  ];

  constructor(private apiService: ApiService) {}

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  send() {
    if (this.chatForm.valid) {
      const text = this.chatForm.value.text!;
      this.messages.push({
        id: Date.now().toString(),
        text,
        sender: 'user',
        sentiment: '',
        timestamp: new Date()
      });
      this.apiService.sendMessage(text).subscribe({
        next: (response) => {
          this.messages[this.messages.length - 1].sentiment = response.user_sentiment;
          this.messages.push({
            id: (Date.now() + 1).toString(),
            text: response.reply,
            sender: 'bot',
            sentiment: response.bot_sentiment,
            timestamp: new Date()
          });
        },
        error: (err) => {
          console.error('Error sending message:', err);
          this.messages.push({
            id: (Date.now() + 1).toString(),
            text: `Error: ${err.message || 'Could not get a response.'}`,
            sender: 'bot',
            sentiment: 'negative',
            timestamp: new Date()
          });
        }
      });
      this.chatForm.reset();
    }
  }

  private scrollToBottom(): void {
    try {
      this.messageContainer.nativeElement.scrollTop = this.messageContainer.nativeElement.scrollHeight;
    } catch (err) {
      console.error('Scroll error:', err);
    }
  }
}
