import {Component, OnInit} from '@angular/core';
import {NgForOf, NgIf} from "@angular/common";
import {BasketService} from "../../services/basket.service";

@Component({
  selector: 'app-basket',
  imports: [
    NgForOf,
    NgIf
  ],
  templateUrl: './basket.component.html',
  styleUrl: './basket.component.css'
})
export class BasketComponent implements OnInit {
  basket: any[] = [];
  successMessage: string = '';


  constructor(private basketService: BasketService) {}

  ngOnInit() {
    this.basket = this.basketService.getBasket();
  }

  clearBasket() {
    this.basketService.clearBasket();
    this.successMessage = '';
    this.basket = this.basketService.getBasket(); // Update the local basket array
  }
  checkout() {
    this.clearBasket();
    this.successMessage = 'Checkout successful!';
  }
}
