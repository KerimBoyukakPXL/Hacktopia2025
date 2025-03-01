import { Component } from '@angular/core';
import { Router } from '@angular/router';
import {FormsModule} from "@angular/forms";

@Component({
    selector: 'app-home',
    imports: [
        FormsModule
    ],
    templateUrl: './home.component.html',
    styleUrls: ['./home.component.css']
})
export class HomeComponent {
  location: string = '';

  constructor(private router: Router) {}

  search() {
    this.router.navigate(['/location-detail'], { queryParams: { location: this.location } });
  }
}
