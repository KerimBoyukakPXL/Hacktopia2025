import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-chatbot-overlay',
  imports: [
    CommonModule // <-- voeg toe aan imports
  ],
  template: `
    <!-- Minimale knop rechtsonder met ✨ icoon -->
    <button
      class="fixed bottom-4 right-4 bg-green-600 text-white px-3 py-2 rounded-full shadow-md flex items-center gap-1 hover:bg-green-700"
      (click)="toggleChat()"
      NgIf="!isOpen"
    >
      ✨
    </button>

    <!-- Overlay voor de chatbot wanneer deze open is -->
    <div
      class="fixed bottom-4 right-4 w-80 h-96 bg-white border rounded-xl shadow-lg flex flex-col"
      *ngIf="isOpen"
    >
      <!-- Header met sluit-knop -->
      <div class="flex justify-between items-center bg-green-600 text-white p-2 rounded-t-xl">
        <span class="font-semibold">Chatbot</span>
        <button
          class="text-white hover:bg-green-700 p-1 rounded"
          (click)="toggleChat()"
        >
          &times;
        </button>
      </div>

      <!-- iFrame om je Streamlit-app te tonen -->
      <iframe
        class="flex-1 w-full border-0"
        src="http://18.234.131.104:8501/"
        title="Chatbot"
      ></iframe>
    </div>
  `,
  styles: []
})
export class ChatbotOverlayComponent {
  isOpen = false;

  toggleChat() {
    this.isOpen = !this.isOpen;
  }
}
