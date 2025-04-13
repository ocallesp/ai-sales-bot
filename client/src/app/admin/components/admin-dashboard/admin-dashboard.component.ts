// src/app/admin/components/admin-dashboard/admin-dashboard.component.ts
import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormControl, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';
import { ApiService } from '../../../core/services/api.service';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatTableModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    ReactiveFormsModule
  ],
  templateUrl: './admin-dashboard.component.html',
  styleUrls: ['./admin-dashboard.component.scss']
})
export class AdminDashboardComponent implements OnInit {
  displayedColumns: string[] = ['month', 'positive', 'neutral', 'negative'];
  monthlyData: { month: string; positive: number; neutral: number; negative: number }[] = [];
  messageColumns: string[] = ['timestamp', 'sender', 'text', 'sentiment'];
  messages: { timestamp: string; sender: string; text: string; sentiment: string }[] = [];
  productColumns: string[] = ['id', 'name', 'price', 'stock', 'discount'];
  products: { id: string; name: string; price: number; stock: number; discount: string }[] = [];
  productForm = new FormGroup({
    name: new FormControl<string>('', [Validators.required]),
    price: new FormControl<number | null>(null, [Validators.required]),
    stock: new FormControl<number | null>(null, [Validators.required]),
    discount: new FormControl<string>('', [Validators.required])
  });

  constructor(private apiService: ApiService) {}

  ngOnInit(): void {
    this.fetchMonthlySentiment();
    this.fetchMessages();
    this.fetchProducts();
  }

  fetchMonthlySentiment(): void {
    this.apiService.getMonthlySentiment().subscribe({
      next: (data) => {
        this.monthlyData = data;
      },
      error: (err) => {
        console.error('Error fetching monthly sentiment:', err);
      }
    });
  }

  fetchMessages(): void {
    this.apiService.getMessages().subscribe({
      next: (data) => {
        this.messages = data;
      },
      error: (err) => {
        console.error('Error fetching messages:', err);
      }
    });
  }

  fetchProducts(): void {
    this.apiService.getProducts().subscribe({
      next: (data) => {
        this.products = data;
      },
      error: (err) => {
        console.error('Error fetching products:', err);
      }
    });
  }

  clearChatHistory(): void {
    this.apiService.clearChatHistory().subscribe({
      next: () => {
        alert('Chat history cleared successfully.');
        this.fetchMonthlySentiment();
        this.fetchMessages();
      },
      error: (err) => {
        console.error('Error clearing chat history:', err);
        alert('Failed to clear chat history.');
      }
    });
  }

  addProduct(): void {
    if (this.productForm.valid) {
      const formValue = this.productForm.getRawValue();
      const product = {
        name: formValue.name!,
        price: Number(formValue.price!),
        stock: Number(formValue.stock!),
        discount: formValue.discount!
      };
      this.apiService.addProduct(product).subscribe({
        next: () => {
          alert('Product added successfully.');
          this.productForm.reset();
          this.fetchProducts(); // Refresh the products list
        },
        error: (err) => {
          console.error('Error adding product:', err);
          alert('Failed to add product.');
        }
      });
    }
  }
}
