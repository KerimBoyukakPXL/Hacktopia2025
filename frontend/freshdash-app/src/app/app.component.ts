import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {NavbarComponent} from "./core/navbar/navbar.component";
import { ChatbotOverlayComponent } from './core/chatbot/chatbot.component';
import { CommonModule } from '@angular/common';

@Component({
    selector: 'app-root',
    imports: [RouterOutlet, NavbarComponent, ChatbotOverlayComponent, CommonModule],
    templateUrl: './app.component.html',
    styleUrl: './app.component.css'

})
export class AppComponent {
  title = 'freshdash-app';
}
