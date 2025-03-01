import { Component } from '@angular/core';

@Component({
  selector: 'app-chatbot-overlay',
  template: `
    <!-- Minimale knop rechtsonder met ✨ icoon -->
    <button
      class="fixed bottom-4 right-4 bg-blue-600 text-white px-3 py-2 rounded-full shadow-md flex items-center gap-1 hover:bg-blue-700"
      (click)="toggleChat()"
      NgIf="!isOpen"
    >
      ✨
    </button>

    <!-- Overlay voor de chatbot wanneer deze open is -->
    <div
      class="fixed bottom-4 right-4 w-80 h-96 bg-white border rounded-xl shadow-lg flex flex-col"
      NgIf="isOpen"
    >
      <!-- Header met sluit-knop -->
      <div class="flex justify-between items-center bg-blue-600 text-white p-2 rounded-t-xl">
        <span class="font-semibold">Chatbot</span>
        <button
          class="text-white hover:bg-blue-700 p-1 rounded"
          (click)="toggleChat()"
        >
          &times;
        </button>
      </div>

      <!-- iFrame om je Streamlit-app te tonen -->
      <iframe
        class="flex-1 w-full border-0"
        src="https://placeholder-url-naar-backend"
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
