// src/app/shared/shared.module.ts
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ChatBubbleComponent } from './components/chat-bubble/chat-bubble.component';

@NgModule({
  imports: [
    CommonModule,
    ChatBubbleComponent
  ],
  exports: [
    ChatBubbleComponent
  ]
})
export class SharedModule { }
