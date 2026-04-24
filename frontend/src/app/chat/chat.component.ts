import { Component, OnInit } from '@angular/core';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrls: ['./chat.component.css'],
})
export class ChatComponent implements OnInit {
  currentUser: any = null;
  messages: any[] = [];
  loading = false;
  error = '';
  userMessage = '';

  constructor(private api: ApiService) {}

  ngOnInit() {
    const user = localStorage.getItem('currentUser');
    if (user) {
      this.currentUser = JSON.parse(user);
      this.loadChatHistory();
    }
  }

  loadChatHistory() {
    if (!this.currentUser?.token) {
      return;
    }
    this.api.getChatHistory(this.currentUser.token).subscribe(
      (messages) => {
        this.messages = messages || [];
      },
      () => {
        this.error = 'No se pudo cargar el historial de chat';
      },
    );
  }

  sendMessage() {
    if (!this.userMessage.trim()) {
      return;
    }

    if (!this.currentUser?.token) {
      this.error = 'Debes iniciar sesión para usar el chat';
      return;
    }

    this.loading = true;
    this.error = '';

    // Add user message to UI immediately
    this.messages.push({
      role: 'user',
      content: this.userMessage,
      created_at: new Date().toISOString(),
    });

    const message = this.userMessage;
    this.userMessage = '';

    this.api.sendChatMessage(message, this.currentUser.token).subscribe(
      (response) => {
        this.messages.push({
          role: response.role,
          content: response.message,
          created_at: new Date().toISOString(),
        });
        this.loading = false;
      },
      (err) => {
        this.error = err?.error?.detail || 'Error al enviar el mensaje';
        this.loading = false;
      },
    );
  }

  handleKeyPress(event: any) {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.sendMessage();
    }
  }
}
