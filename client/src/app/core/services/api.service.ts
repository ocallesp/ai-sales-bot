// src/app/core/services/api.service.ts
import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = 'http://localhost:8000/api';
  private adminCredentials = { username: 'admin', password: 'password123' };

  constructor(private http: HttpClient) {}

  private getAuthHeaders(): HttpHeaders {
    const auth = btoa(`${this.adminCredentials.username}:${this.adminCredentials.password}`);
    return new HttpHeaders({
      'Authorization': `Basic ${auth}`
    });
  }

  sendMessage(text: string): Observable<{ reply: string; user_sentiment: string; bot_sentiment: string }> {
    return this.http.post<{ reply: string; user_sentiment: string; bot_sentiment: string }>(`${this.apiUrl}/chat`, { text });
  }

  getMonthlySentiment(): Observable<{ month: string; positive: number; neutral: number; negative: number }[]> {
    return this.http.get<{ month: string; positive: number; neutral: number; negative: number }[]>(`${this.apiUrl}/sentiment/monthly`, {
      headers: this.getAuthHeaders()
    });
  }

  clearChatHistory(): Observable<void> {
    return this.http.delete<void>(`${this.apiUrl}/chat/history`, {
      headers: this.getAuthHeaders()
    });
  }

  getMessages(): Observable<{ timestamp: string; sender: string; text: string; sentiment: string }[]> {
    return this.http.get<{ timestamp: string; sender: string; text: string; sentiment: string }[]>(`${this.apiUrl}/messages`, {
      headers: this.getAuthHeaders()
    });
  }

  getProducts(): Observable<{ id: string; name: string; price: number; stock: number; discount: string }[]> {
    return this.http.get<{ id: string; name: string; price: number; stock: number; discount: string }[]>(`${this.apiUrl}/products`);
  }

  addProduct(product: { name: string; price: number; stock: number; discount: string }): Observable<void> {
    return this.http.post<void>(`${this.apiUrl}/products`, product, {
      headers: this.getAuthHeaders()
    });
  }
}
